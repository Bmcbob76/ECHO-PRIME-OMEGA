"""
🚀 MASTER MODULAR LAUNCHER ENHANCED V3 - ECHO_XV4
Authority Level 11.0 - Commander Bobby Don McWilliams II
Full MCP Integration | Auto-Discovery | Hot Reload | Docker Support

Features:
- Automatic server discovery in E:\ECHO_XV4\MLS\servers
- Dynamic port assignment and management
- Health monitoring with auto-healing
- Live web dashboard
- MCP integration for Claude Desktop
- Docker container support
- Hot reload on file changes
"""

import sys
import os
import asyncio
import time
import logging
import json
import yaml
import subprocess
import threading
import psutil
import socket
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, jsonify, render_template_string
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from colorama import Fore, Back, Style, init
import setproctitle

# Initialize colorama for Windows
init(autoreset=True)

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except (ImportError, TypeError) as e:
    MCP_AVAILABLE = False
    print(f"⚠️ MCP not available (dependency issue): {str(e)}")

# GS343 Foundation Integration
GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

class ServerFileWatcher(FileSystemEventHandler):
    """Watch servers directory for changes"""

    def __init__(self, launcher):
        self.launcher = launcher
        self.last_event_time = {}

    def on_created(self, event):
        if not event.is_directory:
            self.launcher.logger.info(f"📁 New server detected: {event.src_path}")
            self.launcher.discover_servers()

    def on_deleted(self, event):
        if not event.is_directory:
            self.launcher.logger.info(f"📁 Server removed: {event.src_path}")
            self.launcher.discover_servers()

    def on_modified(self, event):
        if not event.is_directory:
            # Debounce events
            current_time = time.time()
            if event.src_path in self.last_event_time:
                if current_time - self.last_event_time[event.src_path] < 1:
                    return
            self.last_event_time[event.src_path] = current_time

            self.launcher.logger.info(f"📁 Server modified: {event.src_path}")
            self.launcher.handle_server_modification(event.src_path)

class MasterModularLauncherV3:
    """Enhanced Master Launcher with Auto-Discovery and MCP Integration"""

    def __init__(self, config_path: str = "E:/ECHO_XV4/MLS/config.yaml"):
        self.authority_level = 11.0
        self.commander = "Bobby Don McWilliams II"
        self.base_path = Path("E:/ECHO_XV4/MLS")
        self.servers_path = self.base_path / "servers"
        self.logs_path = self.base_path / "logs"
        self.static_path = self.base_path / "static"

        # Create directories
        self.servers_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)
        self.static_path.mkdir(parents=True, exist_ok=True)

        # Load configuration
        self.config = self._load_config(config_path)

        # Server registry - dynamically discovered
        self.servers = {}
        self.next_port = self.config.get('base_port', 8000)

        # MCP Server
        self.mcp_server = Server("master-launcher-v3") if MCP_AVAILABLE else None

        # GS343 Integration
        if GS343_AVAILABLE:
            self.gs343 = GS343UniversalFoundation("MasterLauncherV3", authority_level=11.0)
            self.phoenix = PhoenixAutoHeal("MasterLauncherV3", authority_level=11.0)
            self.phoenix.start_monitoring()
        else:
            self.gs343 = None
            self.phoenix = None

        # Setup logging
        self.logger = self._setup_logging()

        # Performance metrics
        self.metrics = {
            'servers_discovered': 0,
            'servers_launched': 0,
            'servers_failed': 0,
            'health_checks': 0,
            'auto_heals': 0,
            'start_time': datetime.now()
        }

        # Threading
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.process_pool = ProcessPoolExecutor(max_workers=10)

        # File watcher
        self.file_observer = None

        # Flask dashboard
        self.dashboard_app = self._create_dashboard()

        # Register MCP tools
        if MCP_AVAILABLE:
            self._register_mcp_tools()

        self.logger.info(f"🚀 Master Modular Launcher V3 initialized")
        self.logger.info(f"🚀 Authority Level: {self.authority_level}")
        self.logger.info(f"🚀 Auto-discovery enabled for: {self.servers_path}")

    def print_colored(self, message: str, status: str = 'info'):
        """Print colored status messages"""
        colors = {
            'good': Fore.GREEN,      # Server running perfectly
            'running': Fore.CYAN,    # Server running with minor issues
            'warning': Fore.YELLOW,  # Server crashed/restarting
            'error': Fore.RED,       # Server failed to launch
            'info': Fore.WHITE,      # Normal info
            'success': Fore.GREEN + Style.BRIGHT,
            'critical': Fore.RED + Style.BRIGHT
        }
        color = colors.get(status, Fore.WHITE)
        print(f"{color}{message}{Style.RESET_ALL}")

    def check_ollama_running(self) -> bool:
        """Check if Ollama server is running on port 11434"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 11434))
            sock.close()
            return result == 0
        except:
            return False

    def start_ollama(self):
        """Start Ollama server if not running"""
        if self.check_ollama_running():
            self.print_colored("✅ Ollama server already running on port 11434", 'good')
            return True

        self.print_colored("🚀 Starting Ollama server...", 'info')
        ollama_path = r"C:\Users\bobmc\AppData\Local\Programs\Ollama\ollama.exe"

        if not Path(ollama_path).exists():
            self.print_colored("❌ Ollama not found at expected path", 'error')
            return False

        try:
            # Start Ollama in background
            subprocess.Popen(
                [ollama_path, "serve"],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Wait for it to start
            for i in range(10):
                time.sleep(1)
                if self.check_ollama_running():
                    self.print_colored("✅ Ollama server started successfully!", 'success')
                    return True

            self.print_colored("⚠️ Ollama started but port not responding", 'warning')
            return False

        except Exception as e:
            self.print_colored(f"❌ Failed to start Ollama: {e}", 'error')
            return False

    def _load_config(self, config_path: str) -> dict:
        """Load or create default configuration"""
        config_file = Path(config_path)

        default_config = {
            'servers_dir': str(self.servers_path),
            'log_file': str(self.logs_path / 'master.log'),
            'log_level': 'INFO',
            'base_port': 8000,
            'num_instances_per_server': 1,
            'dashboard_port': 9000,
            'health_check_interval': 30,
            'health_check_timeout': 5,
            'docker_support': True,
            'metrics_enabled': True,
            'restart_backoff': 5,
            'max_restart_attempts': 3,
            'auto_discovery': True,
            'hot_reload': True,
            'mcp_enabled': True,
            'resource_limits': {
                'memory_mb': 512,
                'cpu_percent': 80
            },
            'notification_hooks': {
                'on_restart': '',
                'on_crash': ''
            }
        }

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    if loaded_config:
                        default_config.update(loaded_config)
            except Exception as e:
                print(f"⚠️ Failed to load config: {e}, using defaults")
        else:
            # Save default config
            with open(config_file, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)

        return default_config

    def _setup_logging(self):
        """Setup comprehensive logging"""
        log_file = Path(self.config['log_file'])

        logger = logging.getLogger("MasterLauncherV3")
        logger.setLevel(getattr(logging, self.config['log_level']))
        logger.handlers.clear()

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def discover_servers(self):
        """Auto-discover all servers in the servers directory"""
        self.logger.info(f"🔍 Discovering servers in {self.servers_path}")

        discovered = []

        # Scan for Python scripts
        for py_file in self.servers_path.glob("*.py"):
            server_id = py_file.stem
            if server_id not in self.servers:
                self.servers[server_id] = self._create_server_config(
                    server_id, py_file, 'python'
                )
                discovered.append(server_id)

        # Scan for executables
        for exe_file in self.servers_path.glob("*.exe"):
            server_id = exe_file.stem
            if server_id not in self.servers:
                self.servers[server_id] = self._create_server_config(
                    server_id, exe_file, 'executable'
                )
                discovered.append(server_id)

        # Scan for Docker directories
        if self.config['docker_support']:
            for item in self.servers_path.iterdir():
                if item.is_dir() and (item / "Dockerfile").exists():
                    server_id = item.name
                    if server_id not in self.servers:
                        self.servers[server_id] = self._create_server_config(
                            server_id, item, 'docker'
                        )
                        discovered.append(server_id)

        # Remove servers that no longer exist
        removed = []
        for server_id in list(self.servers.keys()):
            if not self.servers[server_id]['path'].exists():
                if self.servers[server_id]['process']:
                    self.stop_server(server_id)
                del self.servers[server_id]
                removed.append(server_id)

        self.metrics['servers_discovered'] = len(self.servers)

        if discovered:
            self.logger.info(f"✅ Discovered {len(discovered)} new servers: {discovered}")

        if removed:
            self.logger.info(f"🗑️ Removed {len(removed)} servers: {removed}")

        return discovered

    def _create_server_config(self, server_id: str, path: Path, server_type: str) -> dict:
        """Create server configuration"""
        port = self._get_free_port()

        return {
            'id': server_id,
            'name': server_id.replace('_', ' ').title(),
            'path': path,
            'type': server_type,
            'port': port,
            'instances': [],  # List of process objects
            'status': 'discovered',
            'health_url': f'http://localhost:{port}/health',
            'restart_count': 0,
            'last_health_check': None,
            'auto_restart': True,
            'mcp_enabled': 'mcp' in server_id.lower(),
            'created_at': datetime.now().isoformat()
        }

    def _get_free_port(self) -> int:
        """Get next available port"""
        while self._is_port_in_use(self.next_port):
            self.next_port += 1

        port = self.next_port
        self.next_port += 1
        return port

    def _is_port_in_use(self, port: int) -> bool:
        """Check if port is in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return False
            except:
                return True

    def launch_server(self, server_id: str, instance_num: int = 0) -> bool:
        """Launch a specific server instance"""
        if server_id not in self.servers:
            self.print_colored(f"❌ Unknown server: {server_id}", 'error')
            self.logger.error(f"Unknown server: {server_id}")
            return False

        server = self.servers[server_id]

        self.print_colored(f"🚀 Launching {server['name']}...", 'info')

        try:
            # Build launch command based on server type
            if server['type'] == 'python':
                cmd = [sys.executable, str(server['path']), str(server['port'])]

            elif server['type'] == 'executable':
                cmd = [str(server['path']), str(server['port'])]

            elif server['type'] == 'docker':
                # Build Docker image
                docker_dir = server['path']
                image_name = f"mls_{server_id}:latest"

                build_cmd = ['docker', 'build', '-t', image_name, str(docker_dir)]
                subprocess.run(build_cmd, check=True)

                # Run container
                cmd = [
                    'docker', 'run', '-d',
                    '-p', f"{server['port']}:{server['port']}",
                    '--name', f"mls_{server_id}_{instance_num}",
                    image_name
                ]

            else:
                self.logger.error(f"Unknown server type: {server['type']}")
                return False

            # Set environment variables
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['SERVER_PORT'] = str(server['port'])
            env['ECHO_DEBUG'] = '1'
            env['MCP_ENABLED'] = '1' if server['mcp_enabled'] else '0'
            env['SERVER_NAME'] = f"ECHO_XV4: {server['name']} - Port {server['port'] + instance_num}"
            env['SERVER_ID'] = server_id

            # Launch process
            process = subprocess.Popen(
                cmd,
                cwd=str(self.servers_path),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Add to instances list
            if instance_num >= len(server['instances']):
                server['instances'].append(None)

            server['instances'][instance_num] = {
                'process': process,
                'pid': process.pid,
                'port': server['port'] + instance_num,  # Offset port for multiple instances
                'started_at': datetime.now().isoformat(),
                'status': 'starting'
            }

            # Monitor output
            self.executor.submit(self._monitor_server_output, server_id, instance_num, process)

            # Give it time to start
            time.sleep(2)

            # Check if still running
            if process.poll() is None:
                server['status'] = 'running'
                server['instances'][instance_num]['status'] = 'running'
                self.metrics['servers_launched'] += 1
                self.print_colored(f"✅ {server['name']} RUNNING on port {server['port'] + instance_num} (PID: {process.pid})", 'good')
                self.logger.info(f"✅ Launched {server['name']} instance {instance_num} on port {server['port'] + instance_num} (PID: {process.pid})")
                return True
            else:
                server['status'] = 'failed'
                server['instances'][instance_num]['status'] = 'failed'
                self.metrics['servers_failed'] += 1
                self.print_colored(f"❌ {server['name']} FAILED TO START", 'error')
                self.logger.error(f"❌ Failed to launch {server['name']}")
                return False

        except Exception as e:
            self.print_colored(f"❌ {server['name']} ERROR: {e}", 'error')
            self.logger.error(f"Error launching {server_id}: {e}")
            self.metrics['servers_failed'] += 1
            return False

    def stop_server(self, server_id: str, instance_num: Optional[int] = None) -> bool:
        """Stop a server or specific instance"""
        if server_id not in self.servers:
            return False

        server = self.servers[server_id]

        if instance_num is not None:
            # Stop specific instance
            if instance_num < len(server['instances']) and server['instances'][instance_num]:
                instance = server['instances'][instance_num]
                if instance['process']:
                    try:
                        instance['process'].terminate()
                        instance['process'].wait(timeout=10)
                    except:
                        instance['process'].kill()
                    instance['status'] = 'stopped'
                    self.logger.info(f"✅ Stopped {server['name']} instance {instance_num}")
                return True
        else:
            # Stop all instances
            for i, instance in enumerate(server['instances']):
                if instance and instance['process']:
                    try:
                        instance['process'].terminate()
                        instance['process'].wait(timeout=10)
                    except:
                        instance['process'].kill()
                    instance['status'] = 'stopped'
            server['status'] = 'stopped'
            self.logger.info(f"✅ Stopped all instances of {server['name']}")
            return True

        return False

    def restart_server(self, server_id: str) -> bool:
        """Restart a server"""
        self.stop_server(server_id)
        time.sleep(self.config['restart_backoff'])

        # Launch configured number of instances
        success = True
        for i in range(self.config['num_instances_per_server']):
            if not self.launch_server(server_id, i):
                success = False

        if success:
            self.servers[server_id]['restart_count'] += 1

        return success

    def check_server_health(self, server_id: str) -> dict:
        """Check health of a server"""
        if server_id not in self.servers:
            return {'healthy': False, 'error': 'Unknown server'}

        server = self.servers[server_id]
        health_results = []

        for i, instance in enumerate(server['instances']):
            if not instance or not instance['process']:
                health_results.append({'instance': i, 'healthy': False, 'status': 'no_process'})
                continue

            # Check if process is alive
            if instance['process'].poll() is not None:
                instance['status'] = 'dead'
                health_results.append({'instance': i, 'healthy': False, 'status': 'dead'})
                continue

            # Try HTTP health check
            try:
                response = requests.get(
                    f"http://localhost:{instance['port']}/health",
                    timeout=self.config['health_check_timeout']
                )
                if response.status_code == 200:
                    instance['status'] = 'healthy'
                    health_results.append({'instance': i, 'healthy': True, 'status': 'healthy'})
                else:
                    instance['status'] = 'unhealthy'
                    health_results.append({'instance': i, 'healthy': False, 'status': 'unhealthy'})
            except:
                # Assume healthy if no health endpoint
                instance['status'] = 'running'
                health_results.append({'instance': i, 'healthy': True, 'status': 'running'})

        server['last_health_check'] = datetime.now().isoformat()
        self.metrics['health_checks'] += 1

        return {
            'server': server_id,
            'overall_healthy': all(r['healthy'] for r in health_results),
            'instances': health_results
        }

    def perform_health_sweep(self):
        """Check health of all servers and auto-heal if needed"""
        unhealthy_servers = []

        for server_id in self.servers:
            health = self.check_server_health(server_id)
            server = self.servers[server_id]

            if not health['overall_healthy']:
                unhealthy_servers.append(server_id)
                self.print_colored(f"⚠️ {server['name']} UNHEALTHY - attempting restart", 'warning')

                # Auto-heal if configured
                if server['auto_restart']:
                    if server['restart_count'] < self.config['max_restart_attempts']:
                        self.logger.warning(f"🔧 Auto-healing {server_id}")
                        self.restart_server(server_id)
                        self.metrics['auto_heals'] += 1
                    else:
                        self.print_colored(f"❌ {server['name']} MAX RESTARTS EXCEEDED", 'critical')
                        self.logger.error(f"❌ Max restart attempts reached for {server_id}")
            else:
                # Check status for coloring
                if server['status'] == 'healthy':
                    status_color = 'good'
                elif server['status'] == 'running':
                    status_color = 'running'
                else:
                    status_color = 'warning'

        return unhealthy_servers

    def handle_server_modification(self, file_path: str):
        """Handle when a server file is modified"""
        file_path = Path(file_path)

        # Find which server this belongs to
        for server_id, server in self.servers.items():
            if server['path'] == file_path or (server['path'].is_dir() and file_path.parent == server['path']):
                self.logger.info(f"🔄 Reloading modified server: {server_id}")
                self.restart_server(server_id)
                break

    def _monitor_server_output(self, server_id: str, instance_num: int, process: subprocess.Popen):
        """Monitor server output for debugging"""
        log_file = self.logs_path / f"{server_id}_{instance_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        try:
            with open(log_file, 'w') as f:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        f.write(line)
                        f.flush()

                        # Check for important messages
                        if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed']):
                            self.logger.warning(f"⚠️ {server_id}[{instance_num}]: {line.strip()}")
                        elif 'mcp' in line.lower() and 'initialized' in line.lower():
                            self.logger.info(f"🔌 {server_id}[{instance_num}]: MCP initialized")
        except Exception as e:
            self.logger.error(f"Output monitor error for {server_id}[{instance_num}]: {e}")

    def _create_dashboard(self):
        """Create Flask dashboard app"""
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template_string(self._get_dashboard_html())

        @app.route('/api/status')
        def api_status():
            return jsonify(self.get_status())

        @app.route('/api/servers')
        def api_servers():
            return jsonify(self.servers)

        @app.route('/api/metrics')
        def api_metrics():
            return jsonify(self.metrics)

        @app.route('/api/launch/<server_id>')
        def api_launch(server_id):
            success = self.launch_server(server_id, 0)
            return jsonify({'success': success})

        @app.route('/api/stop/<server_id>')
        def api_stop(server_id):
            success = self.stop_server(server_id)
            return jsonify({'success': success})

        @app.route('/api/restart/<server_id>')
        def api_restart(server_id):
            success = self.restart_server(server_id)
            return jsonify({'success': success})

        return app

    def _get_dashboard_html(self):
        """Get dashboard HTML template"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>MLS Dashboard - ECHO_XV4</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }

                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                    color: #00ff41;
                    padding: 20px;
                    min-height: 100vh;
                }

                .header {
                    text-align: center;
                    padding: 30px;
                    background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
                    border-radius: 15px;
                    box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
                    margin-bottom: 30px;
                    border: 2px solid #00ff41;
                }

                .header h1 {
                    font-size: 3em;
                    text-shadow: 0 0 20px #00ff41;
                    animation: glow 2s ease-in-out infinite alternate;
                }

                @keyframes glow {
                    from { text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41; }
                    to { text-shadow: 0 0 20px #00ff41, 0 0 30px #00ff41, 0 0 40px #00ff41; }
                }

                .header .subtitle {
                    color: #00ccff;
                    font-size: 1.2em;
                    margin-top: 10px;
                    text-shadow: 0 0 10px #00ccff;
                }

                .container { max-width: 1600px; margin: 0 auto; }

                .metrics {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 25px;
                    margin-bottom: 40px;
                }

                .metric {
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    padding: 30px;
                    border-radius: 15px;
                    border: 2px solid #00ff41;
                    box-shadow: 0 0 25px rgba(0, 255, 65, 0.2);
                    transition: all 0.3s ease;
                    text-align: center;
                }

                .metric:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 5px 35px rgba(0, 255, 65, 0.4);
                }

                .metric h3 {
                    color: #00ff41;
                    font-size: 1.2em;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }

                .metric .value {
                    font-size: 3em;
                    font-weight: bold;
                    text-shadow: 0 0 15px #00ff41;
                    color: #00ff41;
                }

                .servers-section {
                    margin-top: 40px;
                }

                .servers-section h2 {
                    font-size: 2em;
                    margin-bottom: 25px;
                    text-shadow: 0 0 15px #00ff41;
                    padding-left: 10px;
                    border-left: 5px solid #00ff41;
                }

                .servers {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                    gap: 25px;
                }

                .server {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    padding: 25px;
                    border-radius: 15px;
                    border: 2px solid #444;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
                    transition: all 0.3s ease;
                }

                .server:hover {
                    transform: scale(1.02);
                }

                .server.running {
                    border-color: #00ff41;
                    box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
                }

                .server.failed {
                    border-color: #ff4141;
                    box-shadow: 0 0 30px rgba(255, 65, 65, 0.3);
                }

                .server.starting {
                    border-color: #ffff41;
                    box-shadow: 0 0 30px rgba(255, 255, 65, 0.3);
                }

                .server h3 {
                    font-size: 1.5em;
                    margin-bottom: 15px;
                    color: #00ccff;
                    text-shadow: 0 0 10px #00ccff;
                }

                .server-info {
                    color: #aaa;
                    margin: 10px 0;
                    font-size: 0.95em;
                }

                .status {
                    display: inline-block;
                    padding: 6px 14px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    font-weight: bold;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin: 10px 0;
                }

                .status.running {
                    background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
                    color: #000;
                    box-shadow: 0 0 15px #00ff41;
                }

                .status.stopped {
                    background: #666;
                    color: #fff;
                }

                .status.failed {
                    background: linear-gradient(135deg, #ff4141 0%, #cc0000 100%);
                    color: #fff;
                    box-shadow: 0 0 15px #ff4141;
                }

                .status.starting {
                    background: linear-gradient(135deg, #ffff41 0%, #ffcc00 100%);
                    color: #000;
                    box-shadow: 0 0 15px #ffff41;
                }

                .controls {
                    margin-top: 15px;
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }

                button {
                    background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
                    color: #000;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    box-shadow: 0 4px 15px rgba(0, 255, 65, 0.3);
                }

                button:hover {
                    background: linear-gradient(135deg, #00cc33 0%, #00ff41 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0, 255, 65, 0.5);
                }

                button:active {
                    transform: translateY(0);
                }

                button.stop {
                    background: linear-gradient(135deg, #ff4141 0%, #cc0000 100%);
                    box-shadow: 0 4px 15px rgba(255, 65, 65, 0.3);
                }

                button.stop:hover {
                    background: linear-gradient(135deg, #cc0000 0%, #ff4141 100%);
                    box-shadow: 0 6px 20px rgba(255, 65, 65, 0.5);
                }

                .instances {
                    margin-top: 15px;
                    padding-top: 15px;
                    border-top: 1px solid #333;
                }

                .instance {
                    background: rgba(0, 255, 65, 0.1);
                    padding: 10px;
                    margin: 8px 0;
                    border-radius: 8px;
                    border-left: 3px solid #00ff41;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                }

                .refresh-section {
                    text-align: center;
                    margin-top: 40px;
                    padding: 30px;
                    background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
                    border-radius: 15px;
                    border: 2px solid #00ff41;
                }

                .refresh-section button {
                    font-size: 1.2em;
                    padding: 15px 40px;
                }

                .timestamp {
                    color: #666;
                    font-size: 0.9em;
                    margin-top: 15px;
                }

                .loading {
                    text-align: center;
                    padding: 60px;
                    font-size: 1.5em;
                    color: #00ff41;
                }

                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }

                .loading {
                    animation: pulse 1.5s ease-in-out infinite;
                }
            </style>
            <script>
                async function loadStatus() {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.json();
                        updateDashboard(data);
                        document.getElementById('timestamp').textContent = new Date().toLocaleString();
                    } catch (error) {
                        console.error('Failed to load status:', error);
                    }
                }

                function updateDashboard(data) {
                    // Update metrics
                    document.getElementById('total-servers').textContent = data.total_servers;
                    document.getElementById('running-servers').textContent = data.running_servers;
                    document.getElementById('health-checks').textContent = data.metrics.health_checks;
                    document.getElementById('auto-heals').textContent = data.metrics.auto_heals;

                    // Update server list
                    const serversDiv = document.getElementById('servers');
                    serversDiv.innerHTML = '';

                    for (const [id, server] of Object.entries(data.servers)) {
                        const serverDiv = document.createElement('div');
                        serverDiv.className = `server ${server.status}`;
                        serverDiv.innerHTML = `
                            <h3>🖥️ ${server.name}</h3>
                            <div class="server-info">
                                <strong>Type:</strong> ${server.type.toUpperCase()} |
                                <strong>Port:</strong> ${server.port}
                            </div>
                            <div class="server-info">
                                <span class="status ${server.status}">${server.status.toUpperCase()}</span>
                            </div>
                            <div class="server-info">
                                <strong>Restarts:</strong> ${server.restart_count} |
                                <strong>MCP:</strong> ${server.mcp_enabled ? '✅' : '❌'}
                            </div>
                            <div class="controls">
                                <button onclick="controlServer('launch', '${id}')">🚀 Launch</button>
                                <button class="stop" onclick="controlServer('stop', '${id}')">🛑 Stop</button>
                                <button onclick="controlServer('restart', '${id}')">🔄 Restart</button>
                            </div>
                            <div class="instances">
                                ${server.instances.map((inst, i) => inst ? `
                                    <div class="instance">
                                        ⚙️ Instance ${i}: PID ${inst.pid} - <strong>${inst.status.toUpperCase()}</strong> - Port ${inst.port}
                                    </div>
                                ` : '').join('')}
                            </div>
                        `;
                        serversDiv.appendChild(serverDiv);
                    }
                }

                async function controlServer(action, serverId) {
                    try {
                        await fetch(`/api/${action}/${serverId}`);
                        setTimeout(loadStatus, 1000);
                    } catch (error) {
                        console.error('Control action failed:', error);
                    }
                }

                // Auto-refresh every 3 seconds
                setInterval(loadStatus, 3000);

                // Initial load
                window.onload = () => {
                    loadStatus();
                };
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 MASTER LAUNCHER DASHBOARD</h1>
                    <div class="subtitle">ECHO_XV4 - Authority Level 11.0</div>
                    <div class="subtitle">Commander Bobby Don McWilliams II</div>
                </div>

                <div class="metrics">
                    <div class="metric">
                        <h3>📊 Total Servers</h3>
                        <div class="value" id="total-servers">-</div>
                    </div>
                    <div class="metric">
                        <h3>✅ Running</h3>
                        <div class="value" id="running-servers">-</div>
                    </div>
                    <div class="metric">
                        <h3>🏥 Health Checks</h3>
                        <div class="value" id="health-checks">-</div>
                    </div>
                    <div class="metric">
                        <h3>🔧 Auto Heals</h3>
                        <div class="value" id="auto-heals">-</div>
                    </div>
                </div>

                <div class="servers-section">
                    <h2>🖥️ Server Status</h2>
                    <div class="servers" id="servers">
                        <div class="loading">⚡ Loading servers...</div>
                    </div>
                </div>

                <div class="refresh-section">
                    <button onclick="loadStatus()">🔄 Refresh Now</button>
                    <div class="timestamp">Last updated: <span id="timestamp">-</span></div>
                </div>
            </div>
        </body>
        </html>
        '''

    def _register_mcp_tools(self):
        """Register MCP tools for Claude integration"""
        if not self.mcp_server:
            return

        @self.mcp_server.list_tools()
        async def list_tools() -> List[Tool]:
            tools = [
                Tool(
                    name="discover_servers",
                    description="Discover all servers in the servers directory",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="launch_server",
                    description="Launch a specific server",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "server_id": {"type": "string", "description": "Server ID to launch"}
                        },
                        "required": ["server_id"]
                    }
                ),
                Tool(
                    name="stop_server",
                    description="Stop a specific server",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "server_id": {"type": "string", "description": "Server ID to stop"}
                        },
                        "required": ["server_id"]
                    }
                ),
                Tool(
                    name="get_status",
                    description="Get comprehensive status of all servers",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="health_check",
                    description="Perform health check on all servers",
                    inputSchema={"type": "object", "properties": {}}
                )
            ]
            return tools

        @self.mcp_server.call_tool()
        async def call_tool(name: str, arguments: dict) -> List[TextContent]:
            try:
                if name == "discover_servers":
                    result = self.discover_servers()
                elif name == "launch_server":
                    result = self.launch_server(arguments['server_id'], 0)
                elif name == "stop_server":
                    result = self.stop_server(arguments['server_id'])
                elif name == "get_status":
                    result = self.get_status()
                elif name == "health_check":
                    result = self.perform_health_sweep()
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

    def get_status(self) -> dict:
        """Get comprehensive status"""
        running_servers = sum(1 for s in self.servers.values() if s['status'] == 'running')

        return {
            'authority_level': self.authority_level,
            'commander': self.commander,
            'total_servers': len(self.servers),
            'running_servers': running_servers,
            'servers': self.servers,
            'metrics': self.metrics,
            'config': self.config,
            'timestamp': datetime.now().isoformat()
        }

    def start_file_watcher(self):
        """Start watching servers directory for changes"""
        if not self.config['hot_reload']:
            return

        event_handler = ServerFileWatcher(self)
        self.file_observer = Observer()
        self.file_observer.schedule(event_handler, str(self.servers_path), recursive=True)
        self.file_observer.start()
        self.logger.info(f"👁️ File watcher started for {self.servers_path}")

    def start_dashboard(self):
        """Start web dashboard in background"""
        def run_dashboard():
            self.dashboard_app.run(
                host='0.0.0.0',
                port=self.config['dashboard_port'],
                debug=False,
                use_reloader=False
            )

        dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        self.logger.info(f"📊 Dashboard started on http://localhost:{self.config['dashboard_port']}")

    async def run(self):
        """Main run loop"""
        self.print_colored("=" * 60, 'info')
        self.print_colored("🚀 MASTER MODULAR LAUNCHER V3 - ECHO_XV4", 'success')
        self.print_colored("=" * 60, 'info')

        self.logger.info("🚀 Starting Master Modular Launcher V3")

        # Start Ollama first
        self.start_ollama()

        # Initial server discovery
        self.print_colored("\n🔍 Discovering servers...", 'info')
        self.discover_servers()
        self.print_colored(f"✅ Found {len(self.servers)} servers\n", 'good')

        # Launch all servers
        for server_id in self.servers:
            for i in range(self.config['num_instances_per_server']):
                self.launch_server(server_id, i)

        # Start file watcher
        self.start_file_watcher()

        # Start dashboard
        self.print_colored("\n📊 Starting Dashboard...", 'info')
        self.start_dashboard()
        self.print_colored(f"✅ Dashboard: http://localhost:{self.config['dashboard_port']}", 'success')

        # Show summary
        self.print_colored("\n" + "=" * 60, 'info')
        self.print_colored(f"✅ SYSTEM READY - {self.metrics['servers_launched']} servers running", 'success')
        self.print_colored("=" * 60 + "\n", 'info')

        # Start MCP server if available
        if MCP_AVAILABLE and self.mcp_server:
            mcp_task = asyncio.create_task(self.run_mcp_server())

        # Main monitoring loop
        try:
            while True:
                # Perform health sweep
                unhealthy = self.perform_health_sweep()
                if unhealthy:
                    self.print_colored(f"⚠️ Unhealthy servers detected: {len(unhealthy)}", 'warning')
                    self.logger.warning(f"⚠️ Unhealthy servers: {unhealthy}")

                # Check for new servers periodically
                if self.config['auto_discovery']:
                    new_servers = self.discover_servers()
                    for server_id in new_servers:
                        for i in range(self.config['num_instances_per_server']):
                            self.launch_server(server_id, i)

                await asyncio.sleep(self.config['health_check_interval'])

        except KeyboardInterrupt:
            self.print_colored("\n🛑 Shutting down...", 'warning')
            self.logger.info("🛑 Shutting down...")
        finally:
            await self.shutdown()

    async def run_mcp_server(self):
        """Run MCP server for Claude integration"""
        self.logger.info("🔌 Starting MCP Server for Claude Desktop")
        async with stdio_server() as (read_stream, write_stream):
            await self.mcp_server.run(
                read_stream,
                write_stream,
                self.mcp_server.create_initialization_options()
            )

    async def shutdown(self):
        """Graceful shutdown"""
        self.logger.info("🛑 Shutting down Master Launcher")

        # Stop all servers
        for server_id in self.servers:
            self.stop_server(server_id)

        # Stop file watcher
        if self.file_observer:
            self.file_observer.stop()
            self.file_observer.join()

        # Stop Phoenix monitoring
        if self.phoenix:
            self.phoenix.stop_monitoring()

        # Shutdown executors
        self.executor.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)

        self.logger.info("✅ Shutdown complete")

async def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     MASTER MODULAR LAUNCHER V3 - ECHO_XV4                 ║
    ╠════════════════════════════════════════════════════════════╣
    ║  Authority Level: 11.0                                    ║
    ║  Commander: Bobby Don McWilliams II                       ║
    ║  Features: Auto-Discovery | Hot Reload | MCP | Docker     ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    launcher = MasterModularLauncherV3()
    await launcher.run()

if __name__ == "__main__":
    os.chdir("E:/ECHO_XV4/MLS")
    asyncio.run(main())
