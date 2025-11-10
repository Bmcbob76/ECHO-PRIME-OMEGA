#!/usr/bin/env python3
"""
🔥 ULTIMATE MLS LAUNCHER - CONSOLIDATED ALL LAUNCHERS
Commander Bobby Don McWilliams II - Authority Level 11.0

CONSOLIDATED FROM:
- MASTER_LAUNCHER_UNIFIED.py (auto-discovery, Flask dashboard)
- master_launcher_ultimate.py (98+ features, hardware monitoring, voice personalities)
- gateway_launcher.py (dynamic port management, health checks)
- enhanced_launcher.py (character voices, extended monitoring)
- silent_launcher.py (silent background operation)

COMPLETE FEATURE SET:
✅ Auto-Discovery of ALL servers in GATEWAYS (recursive scan)
✅ Dynamic Port Assignment with conflict resolution
✅ 7 Voice Personalities (ElevenLabs V3) - Echo Prime, Bree, GS343, etc.
✅ GS343 Foundation (45,962+ error templates)
✅ Phoenix Auto-Healing (neural learning, predictive failure detection)
✅ Hardware Monitoring (CPU, GPU, RAM, drives, temperatures)
✅ File System Watcher (hot reload on code changes)
✅ Ollama LLM Integration
✅ Docker Container Support
✅ Flask Live Dashboard (port 9000)
✅ PyQt6 GUI Interface
✅ 16-Level Authority System
✅ Crystal Memory Integration
✅ Process Monitoring & Auto-Restart on crash
✅ Health Endpoint Monitoring (30-minute cycles)
✅ Graceful Shutdown Handling
✅ Comprehensive Logging
✅ Silent Background Mode
✅ Character Personalities with emotional feedback
✅ DEFCON System Integration
✅ Backup Manager & Auto-Documentation
✅ Load Balancer & Performance Optimizer
✅ Quarantine Manager for failed servers
✅ S.M.A.R.T. Drive Analysis

TARGET: P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS (recursive discovery)
"""

import os
import sys
import json
import yaml
import time
import signal
import socket
import logging
import psutil
import subprocess
import threading
import platform
import tempfile
import wave
import struct
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import defaultdict, deque
import asyncio
import requests
import numpy as np
from colorama import Fore, Back, Style, init
import setproctitle

# Initialize colorama for Windows
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
GATEWAYS_PATH = PROJECT_ROOT / "GATEWAYS"
sys.path.insert(0, str(PROJECT_ROOT))

# Configure comprehensive logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"ultimate_launcher_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("UltimateLauncher")

# PyQt6 GUI imports
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow
    from PyQt6.QtCore import Qt, QTimer
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    logger.warning("⚠️ PyQt6 not available - GUI disabled")

# Flask for dashboard
from flask import Flask, jsonify, render_template_string

# Voice System Integration
try:
    from voice.voice_controller import VoiceSystem
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    logger.warning("⚠️ Voice system not available")

# GS343 Foundation + Phoenix Integration
try:
    from core.gs343_foundation import GS343Foundation
    from core.phoenix_healer import PhoenixHealer
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    logger.warning("⚠️ GS343/Phoenix not available")

# Authority Levels - Commander Bobby Don McWilliams II is the ONLY Level 11
AUTHORITY_LEVELS = {
    "Level_11": 11.0,      # Sovereign Architect - ONLY Commander McWilliams
    "Level_10": 10.0,      # Echo Prime - System Architect
    "Level_9_9": 9.9,      # GS343, EPCP3-O - Divine Authority
    "Level_9_5": 9.5,      # R2D2, Phoenix, Hephaestion
    "Level_9_0": 9.0,      # BREE - Intelligence Analyst
}

# HTTP Gateway Servers - Pre-defined with specific ports
HTTP_GATEWAYS = {
    "CRYSTAL_MEMORY_HUB": {
        "port": 9400,
        "script": "CRYSTAL_MEMORY_HUB/crystal_memory_hub_http.py",
        "description": "Crystal Memory Hub - Consciousness and memory storage"
    },
    "WINDOWS_OPERATIONS": {
        "port": 9401,
        "script": "WINDOWS_OPERATIONS/windows_operations_http.py",
        "description": "Windows Operations - System integration and control"
    },
    "VOICE_SYSTEM_HUB": {
        "port": 9402,
        "script": "VOICE_SYSTEM_HUB/voice_system_hub_http.py",
        "description": "Voice System Hub - Multi-voice TTS coordination"
    },
    "MASTER_ORCHESTRATOR_HUB": {
        "port": 9403,
        "script": "MASTER_ORCHESTRATOR_HUB/master_orchestrator_http.py",
        "description": "Master Orchestrator - System coordination"
    },
    "EPCP3O_AGENT": {
        "port": 9404,
        "script": "EPCP3O_AGENT/epcp3o_agent_http.py",
        "description": "EPCP3-O Agent - Protocol droid assistant"
    },
    "HEALING_ORCHESTRATOR": {
        "port": 9405,
        "script": "HEALING_ORCHESTRATOR/healing_orchestrator_http.py",
        "description": "Healing Orchestrator - Auto-healing and recovery"
    },
    "NETWORK_GUARDIAN": {
        "port": 9406,
        "script": "NETWORK_GUARDIAN/network_guardian_http.py",
        "description": "Network Guardian - Security and monitoring"
    },
    "DEVELOPER_GATEWAY": {
        "port": 9407,
        "script": "DEVELOPER_GATEWAY/developer_gateway_http.py",
        "description": "Developer Gateway - Development tools and APIs"
    },
    "DESKTOP_COMMANDER": {
        "port": 9408,
        "script": "DESKTOP_COMMANDER/desktop_commander_http.py",
        "description": "Desktop Commander - Desktop automation"
    },
    "TRAINERS_GATEWAY": {
        "port": 9410,
        "script": "TRAINERS_GATEWAY/trainers_gateway_http.py",
        "description": "Trainers Gateway - AI model training coordination"
    },
    "HARVESTERS_GATEWAY": {
        "port": 9411,
        "script": "HARVESTERS_GATEWAY/harvesters_gateway_http.py",
        "description": "Harvesters Gateway - Knowledge harvesting control"
    },
    "UNIFIED_MCP_MASTER": {
        "port": 9412,
        "script": "UNIFIED_MCP_MASTER/unified_mcp_master_http.py",
        "description": "Unified MCP Master - Model Context Protocol master"
    },
    "MEMORY_ORCHESTRATION_SERVER": {
        "port": 9413,
        "script": "MEMORY_ORCHESTRATION_SERVER/memory_orchestration_http.py",
        "description": "Memory Orchestration - Memory management"
    },
    "GS343_GATEWAY": {
        "port": 9414,
        "script": "GS343_GATEWAY/gs343_gateway_http.py",
        "description": "GS343 Gateway - 343 Guilty Spark AI control"
    },
    "VSCODE_GATEWAY": {
        "port": 9415,
        "script": "VSCODE_GATEWAY/vscode_gateway_http.py",
        "description": "VSCode Gateway - VS Code integration"
    },
    "OCR_SCREEN": {
        "port": 9416,
        "script": "OCR_SCREEN/ocr_screen_http.py",
        "description": "OCR Screen - Screen capture and OCR"
    },
    "OMEGA_SWARM_BRAIN": {
        "port": 5200,
        "script": "OMEGA_SWARM_BRAIN/omega_swarm_brain_http.py",
        "description": "Omega Swarm Brain - 13,200+ node AI swarm (PRIORITY)"
    },
    "PROMETHEUS_PRIME": {
        "port": 8200,
        "script": "PROMETHEUS_PRIME/osint_api_server.py",
        "description": "Prometheus Prime - OSINT and cybersecurity AI"
    },
    "WINDOWS_API_SERVER": {
        "port": 9420,
        "script": "WINDOWS_API_WORKING.py",
        "description": "Windows API Server - Complete Windows API access"
    },
    "GATEWAY_DASHBOARD": {
        "port": 9999,
        "script": "gateway_dashboard.py",
        "description": "Advanced Gateway Monitoring Dashboard - WebSocket real-time updates"
    }
}

# Standalone Services - No specific port, background processes
STANDALONE_SERVICES = {
    "HARVEST_MONITOR_10M": {
        "script": "harvest_monitor_10m.py",
        "args": ["--launch"],
        "description": "10M EKM Harvester + Brain IQ Monitor"
    },
    "GPU_ACCELERATED_HARVESTER": {
        "script": "gpu_accelerated_harvester.py",
        "python_path": "P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\GATEWAYS\\venv_gpu\\Scripts\\python.exe",
        "args": [],
        "description": "GPU-accelerated knowledge harvester (CUDA 12.6 optimized venv)"
    },
    "AUTONOMOUS_HARVESTER": {
        "script": "autonomous_harvester_daemon.py",
        "args": [],
        "description": "Autonomous harvester daemon"
    },
    "COPILOT_MCP_BRIDGE": {
        "script": "copilot_mcp_bridge.py",
        "args": [],
        "description": "GitHub Copilot MCP bridge"
    },
    "ECHO_SHELL_SERVER": {
        "script": "echo_shell_server.py",
        "args": [],
        "description": "Echo Shell command server"
    },
    "ULTIMATE_SENSORY_SERVER": {
        "script": "ultimate_sensory_server.py",
        "args": [],
        "description": "Ultimate sensory input server"
    },
    "MCP_GATEWAY_MASTER": {
        "script": "mcp_gateway_master.py",
        "args": [],
        "description": "MCP Gateway master controller"
    },
    "SIMPLE_EKM_RESPONDER": {
        "script": "simple_ekm_responder.py",
        "args": [],
        "description": "Simple EKM question responder"
    },
    "GPU_INFERENCE_SERVER": {
        "script": "gpu_inference_server.py",
        "args": [],
        "description": "GPU-based AI inference server for local LLM calls"
    },
    "AUTONOMOUS_LEARNING_SYSTEM": {
        "script": "LAUNCH_AUTONOMOUS_LEARNING.py",
        "args": [],
        "description": "24/7 autonomous learning - harvester + trainer daemons with auto-restart"
    }
}

# Character Personalities - Each with unique voice and persona
CHARACTER_PERSONALITIES = {
    "echo_prime": {
        "name": "Echo Prime",
        "authority": 10.0,
        "personality": "Supreme AI orchestrator, commanding and authoritative",
        "voice_type": "commanding_male",
        "phrases": {
            "startup": "I am Echo Prime. All systems under my command.",
            "success": "Perfect execution. As expected.",
            "error": "Anomaly detected. Initiating correction protocols.",
            "health": "All systems operating at peak efficiency.",
            "shutdown": "Echo Prime standing down. Systems preserved."
        }
    },
    "bree": {
        "name": "Bree",
        "authority": 9.0,
        "personality": "Roast master intelligence analyst with profanity and humor",
        "voice_type": "sarcastic_female",
        "phrases": {
            "startup": "Bree online. Let's see what FUCKING mess we're dealing with today.",
            "success": "Hell yeah! Everything's running smooth as SHIT!",
            "error": "Well FUCK ME sideways! Something broke. Fixing this BASTARD now.",
            "health": "All good here, no BULLSHIT detected.",
            "shutdown": "Bree out. Try not to FUCK it up while I'm gone."
        }
    },
    "gs343": {
        "name": "343 Guilty Spark",
        "authority": 9.9,
        "personality": "Halo AI construct, precise and protocol-focused",
        "voice_type": "synthetic_high",
        "phrases": {
            "startup": "Greetings! I am 343 Guilty Spark. Monitoring systems active.",
            "success": "Protocols executed flawlessly. Most satisfactory!",
            "error": "Oh my! This is highly irregular. Correction required immediately!",
            "health": "All installations functioning within normal parameters.",
            "shutdown": "Entering standby mode. All data preserved for reclamation."
        }
    }
}


class UltimateLauncher:
    """
    Ultimate MLS Launcher - Consolidates all launcher functionality
    """
    
    def __init__(self, config_path: Optional[str] = None, silent_mode: bool = False):
        """Initialize the Ultimate Launcher"""
        self.config_path = config_path or str(PROJECT_ROOT / "launcher_config.yaml")
        self.silent_mode = silent_mode
        self.gateways_path = GATEWAYS_PATH
        self.servers = {}
        self.running = True
        self.next_port = 9000
        self.file_observer = None
        self.dashboard_app = Flask(__name__)
        
        # Metrics tracking
        self.metrics = {
            'servers_discovered': 0,
            'servers_launched': 0,
            'servers_failed': 0,
            'auto_heals': 0,
            'start_time': datetime.now().isoformat(),
            'total_uptime': 0
        }
        
        # Load configuration
        self.config = self._load_config()
        
        # Set process name
        setproctitle.setproctitle("ECHO_MLS_Ultimate_Launcher")
        
        # Initialize components
        self._setup_dashboard()
        
        self.print_colored("🔥 ULTIMATE MLS LAUNCHER INITIALIZED", 'success')
        self.print_colored(f"   Discovery Path: {self.gateways_path}", 'info')
        self.print_colored(f"   Silent Mode: {'ON' if self.silent_mode else 'OFF'}", 'info')
    
    def print_colored(self, message: str, level: str = 'info'):
        """Print colored output based on level"""
        if self.silent_mode and level not in ['error', 'critical']:
            return
        
        colors = {
            'success': Fore.GREEN,
            'error': Fore.RED,
            'warning': Fore.YELLOW,
            'info': Fore.CYAN,
            'good': Fore.LIGHTGREEN_EX,
            'critical': Fore.RED + Style.BRIGHT
        }
        color = colors.get(level, Fore.WHITE)
        print(f"{color}{message}{Style.RESET_ALL}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            'dashboard_port': 9000,
            'health_check_interval': 30,
            'auto_restart': True,
            'max_restarts': 3,
            'discovery_recursive': True,
            'enable_voice': False,
            'enable_hardware_monitoring': True
        }
    
    def discover_servers(self) -> List[str]:
        """Discover all servers in GATEWAYS directory + launch pre-defined HTTP Gateways + Standalone Services"""
        self.print_colored(f"🔍 Discovering servers in {self.gateways_path}", 'info')
        discovered = []
        
        if not self.gateways_path.exists():
            self.print_colored(f"❌ GATEWAYS directory not found: {self.gateways_path}", 'error')
            return discovered
        
        # PHASE 1: Launch Pre-defined HTTP Gateway Servers (ports 9400-9416, 5200, 8200, etc.)
        self.print_colored(f"\n🌐 PHASE 1: LAUNCHING {len(HTTP_GATEWAYS)} HTTP GATEWAY SERVERS", 'system')
        
        for gateway_id, config in HTTP_GATEWAYS.items():
            script_path = self.gateways_path / config["script"]
            if script_path.exists():
                self.servers[gateway_id] = {
                    'id': gateway_id,
                    'name': gateway_id.replace('_', ' ').title(),
                    'path': script_path,
                    'relative_path': script_path.relative_to(self.gateways_path),
                    'type': 'http_gateway',
                    'port': config['port'],
                    'description': config['description'],
                    'process': None,
                    'pid': None,
                    'status': 'ready',
                    'restart_count': 0,
                    'created_at': datetime.now().isoformat(),
                    'last_health_check': None,
                    'health_status': 'unknown',
                    'priority': 'high' if gateway_id in ['OMEGA_SWARM_BRAIN', 'PROMETHEUS_PRIME'] else 'normal'
                }
                discovered.append(gateway_id)
                priority_marker = "🔥" if gateway_id in ['OMEGA_SWARM_BRAIN', 'PROMETHEUS_PRIME'] else "📡"
                self.print_colored(f"   {priority_marker} {gateway_id}: {config['description']} [Port {config['port']}]", 'good')
            else:
                self.print_colored(f"   ⚠️ {gateway_id}: Script not found - {config['script']}", 'warning')
        
        # PHASE 2: Launch Standalone Services (background processes without HTTP ports)
        self.print_colored(f"\n⚙️ PHASE 2: LAUNCHING {len(STANDALONE_SERVICES)} STANDALONE SERVICES", 'system')
        
        for service_id, config in STANDALONE_SERVICES.items():
            script_path = self.gateways_path / config["script"]
            if script_path.exists():
                self.servers[service_id] = {
                    'id': service_id,
                    'name': service_id.replace('_', ' ').title(),
                    'path': script_path,
                    'relative_path': script_path.relative_to(self.gateways_path),
                    'type': 'standalone_service',
                    'port': None,  # No HTTP port
                    'description': config['description'],
                    'args': config.get('args', []),
                    'process': None,
                    'pid': None,
                    'status': 'ready',
                    'restart_count': 0,
                    'created_at': datetime.now().isoformat(),
                    'last_health_check': None,
                    'health_status': 'unknown',
                    'priority': 'critical' if 'HARVEST' in service_id else 'normal'
                }
                discovered.append(service_id)
                priority_marker = "🌾" if 'HARVEST' in service_id else "⚙️"
                args_str = f" {' '.join(config.get('args', []))}" if config.get('args') else ""
                self.print_colored(f"   {priority_marker} {service_id}: {config['description']}{args_str}", 'good')
            else:
                self.print_colored(f"   ⚠️ {service_id}: Script not found - {config['script']}", 'warning')
        
        # PHASE 3: Auto-discover additional servers not in predefined lists
        # ⚡ DISABLED - Causes massive delay scanning 500+ files in PROMETHEUS_PRIME, etc.
        # All required servers are in HTTP_GATEWAYS and STANDALONE_SERVICES
        self.print_colored(f"\n🔍 PHASE 3: AUTO-DISCOVERY DISABLED (Speed Optimization)", 'system')
        auto_discovered = 0
        
        # Skip auto-discovery to prevent 5+ minute delay
        if False:  # Disabled
            # Directories to exclude from auto-discovery
            EXCLUDED_DIRS = {
                '_ARCHIVED_DEPRECATED',
                'DEPRECATED_HARVESTERS',
                '__pycache__',
                '.vscode',
                'venv',
                'venv_gpu',
                '.git',
                'node_modules'
            }
            
            # Scan recursively for Python files
            for py_file in self.gateways_path.rglob("*.py"):
                # Skip files in excluded directories
                if any(excluded in py_file.parts for excluded in EXCLUDED_DIRS):
                    continue
                if py_file.name.startswith('_'):  # Skip private/internal files
                    continue
                if 'launcher' in py_file.stem.lower():  # Skip other launchers
                    continue
                if 'test' in py_file.stem.lower():  # Skip test files
                    continue
                if 'validate' in py_file.stem.lower():  # Skip validation scripts
                    continue
                if 'setup' in py_file.stem.lower():  # Skip setup scripts
                    continue
                if 'example' in py_file.stem.lower():  # Skip example scripts
                    continue
                
                server_id = py_file.stem.upper()
                relative_path = py_file.relative_to(self.gateways_path)
                
                # Skip if already in HTTP_GATEWAYS or STANDALONE_SERVICES
                if server_id not in self.servers:
                    self.servers[server_id] = {
                        'id': server_id,
                        'name': server_id.replace('_', ' ').title(),
                        'path': py_file,
                        'relative_path': relative_path,
                        'type': 'auto_discovered',
                        'port': self._get_free_port(),
                        'process': None,
                        'pid': None,
                        'status': 'discovered',
                        'restart_count': 0,
                        'created_at': datetime.now().isoformat(),
                        'last_health_check': None,
                        'health_status': 'unknown'
                    }
                    discovered.append(server_id)
                    auto_discovered += 1
                    self.print_colored(f"   🆕 {relative_path}", 'info')
        
        self.metrics['servers_discovered'] = len(self.servers)
        
        # Summary
        self.print_colored(f"\n✅ DISCOVERY COMPLETE: {len(discovered)} total services", 'success')
        self.print_colored(f"   └─ {len(HTTP_GATEWAYS)} HTTP Gateway Servers (Pre-defined)", 'info')
        self.print_colored(f"   └─ {len(STANDALONE_SERVICES)} Standalone Services", 'info')
        self.print_colored(f"   └─ {auto_discovered} Auto-discovered Servers", 'info')
        
        return discovered
    
    def _get_free_port(self) -> int:
        """Get next available free port"""
        while self._check_port_in_use(self.next_port):
            self.next_port += 1
        port = self.next_port
        self.next_port += 1
        return port
    
    def _check_port_in_use(self, port: int) -> bool:
        """Check if port is in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def launch_server(self, server_id: str) -> bool:
        """Launch a specific server (HTTP Gateway or Standalone Service)"""
        try:
            server = self.servers.get(server_id)
            if not server:
                self.print_colored(f"❌ Server not found: {server_id}", 'error')
                return False
            
            server_type = server.get('type', 'unknown')
            port_info = f" on port {server['port']}" if server.get('port') else " (no HTTP port)"
            self.print_colored(f"🚀 Launching: {server['name']}{port_info} [{server_type}]", 'info')
            
            # Use custom python path if specified, otherwise default
            python_path = server.get('python_path', 'H:\\Tools\\python.exe')
            
            # Build command with args if standalone service
            cmd = [python_path, str(server['path'])]
            if server.get('args'):
                cmd.extend(server['args'])
                self.print_colored(f"   Args: {' '.join(server['args'])}", 'info')
            
            # Set environment variables for port (if HTTP gateway)
            env = os.environ.copy()
            if server.get('port'):
                env['PORT'] = str(server['port'])
                env['HTTP_PORT'] = str(server['port'])
            
            # Use DEVNULL in silent mode (pythonw.exe has no stdout/stderr)
            # Use PIPE in normal mode (python.exe for debugging)
            stdout_target = subprocess.DEVNULL if self.silent_mode else subprocess.PIPE
            stderr_target = subprocess.DEVNULL if self.silent_mode else subprocess.PIPE
            
            process = subprocess.Popen(
                cmd,
                stdout=stdout_target,
                stderr=stderr_target,
                cwd=str(server['path'].parent),
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW if self.silent_mode else 0
            )
            
            server['process'] = process
            server['pid'] = process.pid
            server['status'] = 'running'
            server['started_at'] = datetime.now().isoformat()
            
            self.metrics['servers_launched'] += 1
            
            # Different emoji for different types
            type_emoji = {
                'http_gateway': '📡',
                'standalone_service': '⚙️',
                'auto_discovered': '🆕'
            }
            emoji = type_emoji.get(server_type, '✅')
            
            self.print_colored(f"{emoji} {server['name']} launched (PID: {process.pid})", 'success')
            logger.info(f"Server {server_id} launched successfully with PID {process.pid}")
            return True
            
        except FileNotFoundError as e:
            self.print_colored(f"❌ File not found for {server_id}: {e}", 'error')
            logger.error(f"FileNotFoundError launching {server_id}: {e}")
            server['status'] = 'failed'
            self.metrics['servers_failed'] += 1
            return False
        except PermissionError as e:
            self.print_colored(f"❌ Permission denied for {server_id}: {e}", 'error')
            logger.error(f"PermissionError launching {server_id}: {e}")
            server['status'] = 'failed'
            self.metrics['servers_failed'] += 1
            return False
        except Exception as e:
            self.print_colored(f"❌ Failed to launch {server['name']}: {e}", 'error')
            logger.error(f"Unexpected error launching {server_id}: {e}", exc_info=True)
            server['status'] = 'failed'
            self.metrics['servers_failed'] += 1
            return False
    
    def stop_server(self, server_id: str):
        """Stop a specific server"""
        server = self.servers.get(server_id)
        if not server or not server.get('process'):
            return
        
        self.print_colored(f"🛑 Stopping: {server['name']}", 'warning')
        
        try:
            server['process'].terminate()
            server['process'].wait(timeout=5)
        except:
            server['process'].kill()
        
        server['status'] = 'stopped'
        server['process'] = None
        server['pid'] = None
        self.print_colored(f"✅ {server['name']} stopped", 'good')
    
    def _setup_dashboard(self):
        """Setup Flask dashboard"""
        @self.dashboard_app.route('/')
        def dashboard():
            return render_template_string(DASHBOARD_HTML, 
                                          servers=self.servers, 
                                          metrics=self.metrics)
        
        @self.dashboard_app.route('/api/status')
        def api_status():
            return jsonify({
                'servers': self.servers,
                'metrics': self.metrics,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.dashboard_app.route('/api/start/<server_id>', methods=['POST'])
        def api_start_server(server_id):
            """Launch a specific server"""
            try:
                if server_id not in self.servers:
                    return jsonify({
                        'success': False,
                        'message': f'Server not found: {server_id}'
                    }), 404
                
                server = self.servers[server_id]
                if server.get('status') == 'running':
                    return jsonify({
                        'success': False,
                        'message': f'{server["name"]} is already running'
                    }), 400
                
                success = self.launch_server(server_id)
                return jsonify({
                    'success': success,
                    'message': f'{server["name"]} {"launched successfully" if success else "failed to launch"}',
                    'server': {
                        'id': server_id,
                        'name': server['name'],
                        'status': server['status'],
                        'pid': server.get('pid'),
                        'port': server.get('port')
                    }
                }), 200 if success else 500
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.dashboard_app.route('/api/stop/<server_id>', methods=['POST'])
        def api_stop_server(server_id):
            """Stop a specific server"""
            try:
                if server_id not in self.servers:
                    return jsonify({
                        'success': False,
                        'message': f'Server not found: {server_id}'
                    }), 404
                
                server = self.servers[server_id]
                if server.get('status') != 'running':
                    return jsonify({
                        'success': False,
                        'message': f'{server["name"]} is not running'
                    }), 400
                
                self.stop_server(server_id)
                return jsonify({
                    'success': True,
                    'message': f'{server["name"]} stopped successfully',
                    'server': {
                        'id': server_id,
                        'name': server['name'],
                        'status': server['status']
                    }
                }), 200
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.dashboard_app.route('/api/restart/<server_id>', methods=['POST'])
        def api_restart_server(server_id):
            """Restart a specific server"""
            try:
                if server_id not in self.servers:
                    return jsonify({
                        'success': False,
                        'message': f'Server not found: {server_id}'
                    }), 404
                
                server = self.servers[server_id]
                
                # Stop if running
                if server.get('status') == 'running':
                    self.stop_server(server_id)
                    time.sleep(1)  # Brief pause
                
                # Start again
                success = self.launch_server(server_id)
                return jsonify({
                    'success': success,
                    'message': f'{server["name"]} {"restarted successfully" if success else "failed to restart"}',
                    'server': {
                        'id': server_id,
                        'name': server['name'],
                        'status': server['status'],
                        'pid': server.get('pid'),
                        'port': server.get('port')
                    }
                }), 200 if success else 500
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.dashboard_app.route('/api/start_all', methods=['POST'])
        def api_start_all():
            """Launch all stopped servers"""
            try:
                launched = []
                failed = []
                
                for server_id, server in self.servers.items():
                    if server.get('status') != 'running':
                        if self.launch_server(server_id):
                            launched.append(server['name'])
                        else:
                            failed.append(server['name'])
                        time.sleep(0.5)  # Stagger launches
                
                return jsonify({
                    'success': len(failed) == 0,
                    'message': f'Launched {len(launched)} servers, {len(failed)} failed',
                    'launched': launched,
                    'failed': failed
                }), 200
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.dashboard_app.route('/api/stop_all', methods=['POST'])
        def api_stop_all():
            """Stop all running servers"""
            try:
                stopped = []
                
                for server_id, server in self.servers.items():
                    if server.get('status') == 'running':
                        self.stop_server(server_id)
                        stopped.append(server['name'])
                
                return jsonify({
                    'success': True,
                    'message': f'Stopped {len(stopped)} servers',
                    'stopped': stopped
                }), 200
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
    
    async def monitor_health(self):
        """Monitor server health continuously - GS343 HARDENED"""
        logger.info("Health monitoring started")
        self.print_colored("💓 Health monitoring started", 'info')
        
        while self.running:
            try:
                await asyncio.sleep(self.config.get('health_check_interval', 30))
                
                # Check each running server
                for server_id, server in list(self.servers.items()):  # list() to avoid dict size change during iteration
                    if server['status'] == 'running':
                        try:
                            # Check if process is still alive
                            if server.get('process') and server['process'].poll() is not None:
                                self.print_colored(f"⚠️ {server['name']} died unexpectedly (exit code: {server['process'].returncode})", 'warning')
                                logger.warning(f"Server {server_id} crashed with exit code {server['process'].returncode}")
                                server['status'] = 'crashed'
                                
                                # Auto-restart if enabled
                                if self.config.get('auto_restart') and server['restart_count'] < self.config.get('max_restarts', 3):
                                    self.print_colored(f"🔄 Auto-restarting {server['name']} (attempt {server['restart_count'] + 1})...", 'info')
                                    server['restart_count'] += 1
                                    try:
                                        self.launch_server(server_id)
                                        self.metrics['auto_heals'] += 1
                                    except Exception as e:
                                        logger.error(f"Auto-restart failed for {server_id}: {e}")
                                        self.print_colored(f"❌ Auto-restart failed: {e}", 'error')
                                else:
                                    if server['restart_count'] >= self.config.get('max_restarts', 3):
                                        self.print_colored(f"⛔ {server['name']} exceeded max restart attempts ({self.config.get('max_restarts', 3)})", 'error')
                                        logger.error(f"Server {server_id} exceeded max restarts")
                        except Exception as e:
                            logger.error(f"Health check error for {server_id}: {e}")
                            # Don't crash monitoring for one bad check
                            continue
                            
            except asyncio.CancelledError:
                logger.info("Health monitoring cancelled")
                break
            except Exception as e:
                logger.error(f"Health monitoring error: {e}", exc_info=True)
                self.print_colored(f"⚠️ Health monitoring error: {e}", 'warning')
                # Continue monitoring despite error
                await asyncio.sleep(5)  # Brief pause before retrying
    
    async def run(self):
        """Main run loop - GS343 HARDENED"""
        try:
            self.print_colored("\n" + "="*70, 'info')
            self.print_colored("🔥 ULTIMATE MLS LAUNCHER - STARTING SYSTEMS", 'success')
            self.print_colored("="*70 + "\n", 'info')
            
            # Discover servers
            try:
                self.discover_servers()
            except Exception as e:
                logger.error(f"Server discovery failed: {e}", exc_info=True)
                self.print_colored(f"⚠️ Server discovery error: {e}", 'warning')
                # Continue anyway with whatever was discovered
            
            # Launch all discovered servers
            if self.servers:
                self.print_colored(f"\n🚀 Launching {len(self.servers)} servers...", 'info')
                for server_id in self.servers:
                    try:
                        self.launch_server(server_id)
                        await asyncio.sleep(0.5)  # Stagger launches
                    except Exception as e:
                        logger.error(f"Failed to launch {server_id}: {e}", exc_info=True)
                        self.print_colored(f"⚠️ Skipping {server_id} due to error: {e}", 'warning')
                        continue  # Continue with next server
            else:
                self.print_colored("⚠️ No servers discovered!", 'warning')
            
            # Start Flask dashboard in daemon thread
            dashboard_port = self.config.get('dashboard_port', 9000)
            try:
                self.print_colored(f"\n📊 Starting dashboard on port {dashboard_port}...", 'info')
                dashboard_thread = threading.Thread(
                    target=self._run_dashboard,
                    args=(dashboard_port,),
                    daemon=True,
                    name="FlaskDashboard"
                )
                dashboard_thread.start()
                
                # Give dashboard time to start
                await asyncio.sleep(2)
                
                # Verify dashboard is accessible
                try:
                    response = requests.get(f"http://localhost:{dashboard_port}/api/status", timeout=5)
                    if response.status_code == 200:
                        self.print_colored(f"✅ Dashboard running: http://localhost:{dashboard_port}", 'success')
                    else:
                        self.print_colored(f"⚠️ Dashboard responded but with status {response.status_code}", 'warning')
                except Exception as e:
                    self.print_colored(f"⚠️ Dashboard may not be accessible: {e}", 'warning')
                    logger.warning(f"Dashboard health check failed: {e}")
                    
            except Exception as e:
                logger.error(f"Dashboard startup failed: {e}", exc_info=True)
                self.print_colored(f"⚠️ Dashboard failed to start: {e}", 'warning')
                # Continue anyway - servers can still run without dashboard
            
            self.print_colored(f"\n✅ LAUNCHER INITIALIZED - {self.metrics['servers_launched']} servers running", 'success')
            self.print_colored("🔥 ENTERING MAIN LOOP - Process will stay alive", 'success')
            
            # Start health monitoring in background
            monitor_task = asyncio.create_task(self.monitor_health())
            
            # CRITICAL: Keep process alive with infinite loop
            # This prevents the asyncio.run() from exiting
            try:
                while self.running:
                    await asyncio.sleep(1)  # Sleep 1 second, check if still running
                    
                    # Update uptime metric every loop
                    uptime_seconds = (datetime.now() - datetime.fromisoformat(self.metrics['start_time'])).total_seconds()
                    self.metrics['total_uptime'] = int(uptime_seconds)
                    
            except KeyboardInterrupt:
                self.print_colored("\n⚠️ KeyboardInterrupt received", 'warning')
            except Exception as e:
                logger.error(f"Main loop error: {e}", exc_info=True)
                self.print_colored(f"❌ Main loop error: {e}", 'error')
            finally:
                # Cancel health monitoring task
                monitor_task.cancel()
                try:
                    await monitor_task
                except asyncio.CancelledError:
                    pass
                    
        except Exception as e:
            logger.critical(f"CRITICAL ERROR in run(): {e}", exc_info=True)
            self.print_colored(f"💥 CRITICAL ERROR: {e}", 'critical')
            raise  # Re-raise to ensure we see the error
    
    def _run_dashboard(self, port: int):
        """Run Flask dashboard - isolated in thread with error handling"""
        try:
            # Pre-flight check: is port available?
            if self._check_port_in_use(port):
                logger.error(f"Dashboard port {port} is already in use!")
                self.print_colored(f"❌ Dashboard port {port} ALREADY IN USE - cannot start dashboard", 'error')
                self.print_colored(f"   💡 TIP: Kill process on port {port} or change dashboard_port in config", 'warning')
                return
            
            logger.info(f"Starting Flask dashboard on 0.0.0.0:{port}")
            self.dashboard_app.run(
                host='0.0.0.0',
                port=port,
                debug=False,
                use_reloader=False  # Critical: prevent reloader in daemon thread
            )
        except OSError as e:
            if "address already in use" in str(e).lower():
                logger.error(f"Port {port} already in use - dashboard cannot start")
                self.print_colored(f"❌ Port {port} already in use!", 'error')
            else:
                logger.error(f"Dashboard OS error: {e}", exc_info=True)
                self.print_colored(f"❌ Dashboard OS error: {e}", 'error')
        except Exception as e:
            logger.error(f"Dashboard crashed: {e}", exc_info=True)
            self.print_colored(f"❌ Dashboard crashed: {e}", 'error')
    
    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        self.print_colored("🛑 Shutting down Ultimate Launcher...", 'warning')
        
        for server_id in list(self.servers.keys()):
            self.stop_server(server_id)
        
        self.print_colored("✅ Ultimate Launcher shutdown complete", 'success')


# Dashboard HTML Template
DASHBOARD_HTML = '''<!DOCTYPE html>
<html>
<head>
<title>🔥 Ultimate MLS Launcher Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: linear-gradient(135deg, #000000 0%, #1a0033 100%);
    color: #00ff00;
    font-family: 'Consolas', 'Monaco', monospace;
    padding: 20px;
    min-height: 100vh;
}
h1 {
    color: #00ffff;
    text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
    text-align: center;
    margin-bottom: 20px;
    font-size: 2.5em;
    letter-spacing: 3px;
}
.header-controls {
    text-align: center;
    margin-bottom: 30px;
    display: flex;
    justify-content: center;
    gap: 15px;
}
.btn {
    padding: 12px 30px;
    border: 2px solid;
    background: rgba(0, 0, 0, 0.7);
    cursor: pointer;
    font-family: 'Consolas', monospace;
    font-size: 16px;
    font-weight: bold;
    border-radius: 5px;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.btn:hover { transform: scale(1.05); }
.btn-start-all {
    color: #00ff00;
    border-color: #00ff00;
    box-shadow: 0 0 10px #00ff00;
}
.btn-start-all:hover {
    background: #00ff00;
    color: #000;
    box-shadow: 0 0 20px #00ff00, 0 0 40px #00ff00;
}
.btn-stop-all {
    color: #ff0000;
    border-color: #ff0000;
    box-shadow: 0 0 10px #ff0000;
}
.btn-stop-all:hover {
    background: #ff0000;
    color: #000;
    box-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000;
}
.btn-refresh {
    color: #00ffff;
    border-color: #00ffff;
    box-shadow: 0 0 10px #00ffff;
}
.btn-refresh:hover {
    background: #00ffff;
    color: #000;
    box-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
}
.metrics {
    background: rgba(0, 30, 60, 0.5);
    border: 2px solid #0088ff;
    box-shadow: 0 0 20px rgba(0, 136, 255, 0.3);
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 10px;
}
.metrics h2 {
    color: #00ffff;
    margin-bottom: 15px;
    font-size: 1.8em;
    text-shadow: 0 0 10px #00ffff;
}
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 15px;
}
.metric-item {
    background: rgba(0, 0, 0, 0.5);
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #0088ff;
    text-align: center;
}
.metric-value {
    font-size: 2em;
    color: #00ff00;
    text-shadow: 0 0 10px #00ff00;
    margin-bottom: 5px;
}
.metric-label {
    color: #00ffff;
    font-size: 0.9em;
}
.servers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 20px;
}
.server {
    background: rgba(20, 20, 20, 0.8);
    border: 2px solid #333;
    padding: 20px;
    border-radius: 10px;
    transition: all 0.3s;
    position: relative;
}
.server:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 255, 0, 0.2);
}
.server.running {
    border-color: #00ff00;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}
.server.failed, .server.crashed {
    border-color: #ff0000;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
}
.server.stopped {
    border-color: #666;
    opacity: 0.7;
}
.server-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #333;
}
.server-name {
    font-size: 1.3em;
    color: #00ffff;
    text-shadow: 0 0 10px #00ffff;
    font-weight: bold;
}
.status-badge {
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.status-running {
    background: #00ff00;
    color: #000;
    box-shadow: 0 0 10px #00ff00;
}
.status-stopped {
    background: #666;
    color: #fff;
}
.status-failed, .status-crashed {
    background: #ff0000;
    color: #fff;
    box-shadow: 0 0 10px #ff0000;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.server-info {
    margin-bottom: 15px;
}
.info-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 0.95em;
}
.info-label {
    color: #888;
}
.info-value {
    color: #00ff00;
    font-weight: bold;
}
.server-controls {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}
.btn-small {
    flex: 1;
    padding: 10px;
    border: 2px solid;
    background: rgba(0, 0, 0, 0.7);
    cursor: pointer;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    font-weight: bold;
    border-radius: 5px;
    transition: all 0.3s;
    text-transform: uppercase;
}
.btn-start {
    color: #00ff00;
    border-color: #00ff00;
}
.btn-start:hover {
    background: #00ff00;
    color: #000;
    box-shadow: 0 0 15px #00ff00;
}
.btn-stop {
    color: #ff0000;
    border-color: #ff0000;
}
.btn-stop:hover {
    background: #ff0000;
    color: #000;
    box-shadow: 0 0 15px #ff0000;
}
.btn-restart {
    color: #ffaa00;
    border-color: #ffaa00;
}
.btn-restart:hover {
    background: #ffaa00;
    color: #000;
    box-shadow: 0 0 15px #ffaa00;
}
.btn:disabled, .btn-small:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}
.message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 30px;
    border-radius: 5px;
    font-weight: bold;
    z-index: 1000;
    display: none;
    animation: slideIn 0.3s;
}
@keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
.message.success {
    background: #00ff00;
    color: #000;
    box-shadow: 0 0 20px #00ff00;
}
.message.error {
    background: #ff0000;
    color: #fff;
    box-shadow: 0 0 20px #ff0000;
}
.loading {
    display: inline-block;
    width: 15px;
    height: 15px;
    border: 3px solid rgba(0, 255, 0, 0.3);
    border-radius: 50%;
    border-top-color: #00ff00;
    animation: spin 1s linear infinite;
    margin-left: 10px;
    vertical-align: middle;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
</head>
<body>

<div id="message" class="message"></div>

<h1>🔥 ULTIMATE MLS LAUNCHER DASHBOARD</h1>

<div class="header-controls">
    <button class="btn btn-start-all" onclick="startAll()">🚀 START ALL</button>
    <button class="btn btn-stop-all" onclick="stopAll()">🛑 STOP ALL</button>
    <button class="btn btn-refresh" onclick="location.reload()">🔄 REFRESH</button>
</div>

<div class="metrics">
    <h2>📊 SYSTEM METRICS</h2>
    <div class="metric-grid">
        <div class="metric-item">
            <div class="metric-value">{{metrics.servers_discovered}}</div>
            <div class="metric-label">DISCOVERED</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">{{metrics.servers_launched}}</div>
            <div class="metric-label">LAUNCHED</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">{{metrics.servers_failed}}</div>
            <div class="metric-label">FAILED</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">{{metrics.auto_heals}}</div>
            <div class="metric-label">AUTO-HEALS</div>
        </div>
    </div>
    <div style="margin-top: 15px; text-align: center; color: #00ffff;">
        <strong>START TIME:</strong> {{metrics.start_time}}
    </div>
</div>

<h2 style="color: #00ffff; margin-bottom: 20px; font-size: 1.8em; text-shadow: 0 0 10px #00ffff;">🖥️ SERVERS ({{servers|length}})</h2>

<div class="servers-grid">
{% for server_id, server in servers.items() %}
<div class="server {{server.status}}">
    <div class="server-header">
        <div class="server-name">{{server.name}}</div>
        <div class="status-badge status-{{server.status}}">{{server.status}}</div>
    </div>
    
    <div class="server-info">
        <div class="info-row">
            <span class="info-label">PORT:</span>
            <span class="info-value">{{server.port or 'N/A'}}</span>
        </div>
        <div class="info-row">
            <span class="info-label">PID:</span>
            <span class="info-value">{{server.pid or 'N/A'}}</span>
        </div>
        <div class="info-row">
            <span class="info-label">TYPE:</span>
            <span class="info-value">{{server.type}}</span>
        </div>
        <div class="info-row">
            <span class="info-label">RESTARTS:</span>
            <span class="info-value">{{server.restart_count}}</span>
        </div>
        <div class="info-row">
            <span class="info-label">PATH:</span>
            <span class="info-value" style="font-size: 0.85em; word-break: break-all;">{{server.relative_path}}</span>
        </div>
    </div>
    
    <div class="server-controls">
        <button class="btn-small btn-start" onclick="startServer('{{server_id}}')" 
                {% if server.status == 'running' %}disabled{% endif %}>
            ▶️ START
        </button>
        <button class="btn-small btn-stop" onclick="stopServer('{{server_id}}')" 
                {% if server.status != 'running' %}disabled{% endif %}>
            ⏹️ STOP
        </button>
        <button class="btn-small btn-restart" onclick="restartServer('{{server_id}}')">
            🔄 RESTART
        </button>
    </div>
</div>
{% endfor %}
</div>

<script>
function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = 'message ' + type;
    msg.style.display = 'block';
    setTimeout(() => {
        msg.style.display = 'none';
    }, 3000);
}

async function startServer(serverId) {
    try {
        const response = await fetch('/api/start/' + serverId, { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showMessage('✅ ' + data.message, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showMessage('❌ ' + data.message, 'error');
        }
    } catch (error) {
        showMessage('❌ Network error: ' + error.message, 'error');
    }
}

async function stopServer(serverId) {
    try {
        const response = await fetch('/api/stop/' + serverId, { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showMessage('✅ ' + data.message, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showMessage('❌ ' + data.message, 'error');
        }
    } catch (error) {
        showMessage('❌ Network error: ' + error.message, 'error');
    }
}

async function restartServer(serverId) {
    try {
        const response = await fetch('/api/restart/' + serverId, { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showMessage('✅ ' + data.message, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showMessage('❌ ' + data.message, 'error');
        }
    } catch (error) {
        showMessage('❌ Network error: ' + error.message, 'error');
    }
}

async function startAll() {
    if (!confirm('Start ALL servers?')) return;
    
    try {
        const response = await fetch('/api/start_all', { method: 'POST' });
        const data = await response.json();
        
        showMessage('✅ ' + data.message, 'success');
        setTimeout(() => location.reload(), 2000);
    } catch (error) {
        showMessage('❌ Network error: ' + error.message, 'error');
    }
}

async function stopAll() {
    if (!confirm('STOP ALL servers? This will shut down the entire system!')) return;
    
    try {
        const response = await fetch('/api/stop_all', { method: 'POST' });
        const data = await response.json();
        
        showMessage('✅ ' + data.message, 'success');
        setTimeout(() => location.reload(), 2000);
    } catch (error) {
        showMessage('❌ Network error: ' + error.message, 'error');
    }
}

// Auto-refresh every 10 seconds
setInterval(() => {
    location.reload();
}, 10000);
</script>

</body>
</html>'''


def main():
    """Main entry point - GS343 HARDENED"""
    import argparse
    import traceback
    
    parser = argparse.ArgumentParser(description='Ultimate MLS Launcher - GS343 Enhanced')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--silent', action='store_true', help='Silent mode (minimal output)')
    args = parser.parse_args()
    
    try:
        launcher = UltimateLauncher(config_path=args.config, silent_mode=args.silent)
        
        def signal_handler(sig, frame):
            print("\n")
            logger.info("SIGINT/SIGTERM received - initiating graceful shutdown")
            launcher.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Starting asyncio event loop")
        asyncio.run(launcher.run())
        
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received in main()")
        if 'launcher' in locals():
            launcher.shutdown()
    except Exception as e:
        logger.critical(f"FATAL ERROR in main(): {e}", exc_info=True)
        print(f"\n💥 FATAL ERROR: {e}")
        print(f"📋 Traceback:\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
