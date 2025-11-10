import os
import sys
import subprocess
import socket
import logging
import threading
import time
from plugin import Plugin
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
from health import check_http_health, check_custom_health

def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

class ServerProcess:
    def __init__(self, plugin, args, idx, docker_support):
        self.plugin = plugin
        self.args = args
        self.idx = idx
        self.port = find_free_port()
        self.process = None
        self.docker_support = docker_support
        self.restart_count = 0
        self.start()

    def start(self):
        if self.plugin.is_docker() and self.docker_support:
            image_name = os.path.basename(self.plugin.path).lower()
            cmd = ["docker", "build", "-t", image_name, self.plugin.path]
            subprocess.run(cmd, check=True)
            cmd = ["docker", "run", "--rm", "-p", f"{self.port}:{self.port}", image_name] + self.args
            self.process = subprocess.Popen(cmd)
            logging.info(f"Started Docker {image_name}#{self.idx} on port {self.port} (PID={self.process.pid})")
        elif self.plugin.is_python_script():
            cmd = [sys.executable, self.plugin.path, str(self.port)] + self.args
            self.process = subprocess.Popen(cmd)
            logging.info(f"Started {self.plugin.path}#{self.idx} on port {self.port} (PID={self.process.pid})")
        elif self.plugin.is_executable():
            cmd = [self.plugin.path, str(self.port)] + self.args
            self.process = subprocess.Popen(cmd)
            logging.info(f"Started Executable {self.plugin.path}#{self.idx} on port {self.port} (PID={self.process.pid})")
        else:
            raise Exception("Unknown plugin type")

    def is_alive(self):
        return self.process.poll() is None

    def check_health(self):
        # Prefer HTTP health if possible
        if self.plugin.is_python_script():
            return check_http_health(self.port)
        elif self.plugin.is_executable():
            return check_custom_health(self.plugin.path, self.port)
        elif self.plugin.is_docker():
            return check_http_health(self.port)
        return False

    def restart(self, backoff=2):
        self.restart_count += 1
        logging.warning(f"Restarting {self.plugin.path}#{self.idx} (was on port {self.port})")
        time.sleep(backoff)
        self.start()

    def stop(self):
        if self.is_alive():
            self.process.terminate()
            logging.info(f"Terminated {self.plugin.path}#{self.idx}")
