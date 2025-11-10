import os
import sys
import yaml
import logging
import time
import threading
from watchdog.observers import Observer
from pathlib import Path
import sys

# GS343 Foundation Integration - MANDATORY
GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    print("?? WARNING: GS343 Foundation not loaded - Limited functionality")
from watchdog.events import FileSystemEventHandler
from plugin import Plugin
from server_manager import ServerProcess
from dashboard import start_dashboard_thread, server_status, metrics

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_logging(log_file, log_level):
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def scan_plugins(servers_dir):
    plugins = []
    for entry in os.scandir(servers_dir):
        if entry.is_file() and entry.name.endswith('.py'):
            plugins.append(Plugin(entry.path))
        elif entry.is_dir():
            if os.path.exists(os.path.join(entry.path, 'Dockerfile')):
                plugins.append(Plugin(entry.path))
    return plugins

class HotReloadHandler(FileSystemEventHandler):
    def __init__(self, servers_dir, server_procs, config, docker_support):
        self.servers_dir = servers_dir
        self.server_procs = server_procs
        self.config = config
        self.docker_support = docker_support

    def on_any_event(self, event):
        logging.info('Detected change in servers directory, rescanning plugins...')
        new_plugins = scan_plugins(self.servers_dir)
        # TODO: Add logic to add/remove ServerProcess instances as needed

def monitor_servers(server_procs, config):
    while True:
        server_status.clear()
        for sp in server_procs:
            status = {
                'name': os.path.basename(sp.plugin.path),
                'port': sp.port,
                'status': 'running' if sp.is_alive() else 'dead',
                'restarts': sp.restart_count
            }
            if config['metrics_enabled']:
                metrics[sp.port] = status
            server_status.append(status)
            health_ok = sp.check_health()
            if not sp.is_alive() or not health_ok:
                logging.error(f"{sp.plugin.path}#{sp.idx} dead/unhealthy, restarting...")
                sp.restart(config.get('restart_backoff', 2))
        time.sleep(config['health_check_interval'])

def main():
    config = load_config('config.yaml')
    setup_logging(config['log_file'], config['log_level'])
    servers_dir = config['servers_dir']
    num_instances = config.get('num_instances_per_server', 1)
    extra_args = config.get('extra_args', [])
    docker_support = config.get('docker_support', True)

    plugins = scan_plugins(servers_dir)
    if not plugins:
        logging.error(f"No server scripts found in {servers_dir}")
        return

    server_procs = []
    for plugin in plugins:
        for idx in range(num_instances):
            sp = ServerProcess(plugin, extra_args, idx, docker_support)
            server_procs.append(sp)

    threading.Thread(target=monitor_servers, args=(server_procs, config), daemon=True).start()
    start_dashboard_thread(config['dashboard_port'])

    observer = Observer()
    event_handler = HotReloadHandler(servers_dir, server_procs, config, docker_support)
    observer.schedule(event_handler, servers_dir, recursive=True)
    observer.start()

    input("Press Enter to terminate master...\n")
    observer.stop()
    observer.join()
    for sp in server_procs:
        sp.stop()

if __name__ == '__main__':
    main()
