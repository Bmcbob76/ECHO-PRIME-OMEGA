"""
🚀 MASTER MODULAR LAUNCHER V3 - VISUAL EDITION
Real-time display with server details and status
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
import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
import colorama

# Initialize colorama for Windows
colorama.init()

class VisualMasterLauncher:
    """Master Launcher with Visual Display"""
    
    def __init__(self):
        self.console = Console()
        self.base_path = Path("E:/ECHO_XV4/MLS")
        self.servers_path = self.base_path / "servers"
        self.logs_path = self.base_path / "logs"
        self.logs_path.mkdir(exist_ok=True)
        
        # Server registry
        self.servers = {}
        self.next_port = 8000
        self.launch_results = []
        
        # Display components
        self.status_table = None
        self.live_display = None
        
        # Load config
        self.config = self._load_config()
        
        # Setup logging
        self.logger = self._setup_logging()
        
    def _load_config(self):
        """Load configuration"""
        config_file = self.base_path / "config.yaml"
        default_config = {
            'base_port': 8000,
            'health_check_interval': 30,
            'dashboard_port': 9000,
            'max_restart_attempts': 3,
            'restart_backoff': 5
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    loaded = yaml.safe_load(f)
                    if loaded:
                        default_config.update(loaded)
            except:
                pass
        
        return default_config
    
    def _setup_logging(self):
        """Setup logging"""
        log_file = self.logs_path / f"visual_launcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger("VisualLauncher")
    
    def discover_servers(self):
        """Discover all servers in the servers directory"""
        self.console.print("\n[cyan]🔍 Discovering servers...[/cyan]")
        
        discovered = []
        
        # Scan for Python scripts
        for py_file in self.servers_path.glob("*.py"):
            server_id = py_file.stem
            if server_id not in self.servers:
                port = self._get_free_port()
                self.servers[server_id] = {
                    'id': server_id,
                    'name': server_id.replace('_', ' ').title(),
                    'path': py_file,
                    'port': port,
                    'process': None,
                    'status': 'discovered',
                    'pid': None,
                    'start_time': None,
                    'health_checks': 0,
                    'restarts': 0
                }
                discovered.append(server_id)
        
        self.console.print(f"[green]✅ Discovered {len(self.servers)} servers[/green]")
        
        if discovered:
            for sid in discovered[:5]:  # Show first 5
                self.console.print(f"  • {self.servers[sid]['name']}")
            if len(discovered) > 5:
                self.console.print(f"  • ... and {len(discovered) - 5} more")
        
        return discovered
    
    def _get_free_port(self):
        """Get next available port"""
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('localhost', self.next_port))
                sock.close()
                port = self.next_port
                self.next_port += 1
                return port
            except:
                self.next_port += 1
    
    def create_status_table(self):
        """Create status table"""
        table = Table(title="🚀 ECHO_XV4 Server Status", show_header=True, header_style="bold magenta")
        table.add_column("Server", style="cyan", no_wrap=True)
        table.add_column("Port", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("PID", style="blue")
        table.add_column("Health", style="magenta")
        table.add_column("Restarts", style="red")
        
        for server_id, server in self.servers.items():
            status_color = "green" if server['status'] == 'running' else "red" if server['status'] == 'failed' else "yellow"
            status_text = Text(server['status'].upper(), style=status_color)
            
            table.add_row(
                server['name'][:30],
                str(server['port']),
                status_text,
                str(server['pid']) if server['pid'] else "-",
                str(server['health_checks']),
                str(server['restarts'])
            )
        
        return table
    
    def launch_server(self, server_id: str) -> bool:
        """Launch a specific server"""
        if server_id not in self.servers:
            return False
        
        server = self.servers[server_id]
        
        try:
            # Build command
            cmd = [sys.executable, str(server['path']), str(server['port'])]
            
            # Set environment
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['SERVER_PORT'] = str(server['port'])
            
            # Launch process
            process = subprocess.Popen(
                cmd,
                cwd=str(self.servers_path),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            server['process'] = process
            server['pid'] = process.pid
            server['status'] = 'starting'
            server['start_time'] = datetime.now()
            
            # Give it time to start
            time.sleep(1)
            
            # Check if still running
            if process.poll() is None:
                server['status'] = 'running'
                self.launch_results.append(f"[green]✅ {server['name']} on port {server['port']}[/green]")
                return True
            else:
                server['status'] = 'failed'
                self.launch_results.append(f"[red]❌ {server['name']} failed to start[/red]")
                return False
                
        except Exception as e:
            server['status'] = 'error'
            self.launch_results.append(f"[red]❌ {server['name']}: {str(e)}[/red]")
            return False
    
    def check_server_health(self, server_id: str) -> bool:
        """Check if server is healthy"""
        server = self.servers.get(server_id)
        if not server:
            return False
        
        # Check process
        if server['process'] and server['process'].poll() is None:
            # Try health endpoint
            try:
                response = requests.get(f"http://localhost:{server['port']}/health", timeout=2)
                if response.status_code == 200:
                    server['health_checks'] += 1
                    return True
            except:
                # Process running but no health endpoint - still consider healthy
                return True
        
        return False
    
    def monitor_servers(self):
        """Monitor server health in background"""
        while True:
            time.sleep(10)  # Check every 10 seconds
            for server_id, server in self.servers.items():
                if server['status'] == 'running':
                    if not self.check_server_health(server_id):
                        server['status'] = 'unhealthy'
                        # Auto-restart
                        if server['restarts'] < self.config['max_restart_attempts']:
                            self.console.print(f"[yellow]🔄 Restarting {server['name']}...[/yellow]")
                            if server['process']:
                                server['process'].terminate()
                            time.sleep(2)
                            self.launch_server(server_id)
                            server['restarts'] += 1
    
    async def run(self):
        """Main run method with visual display"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print header
        self.console.print(Panel.fit(
            "[bold cyan]MASTER MODULAR LAUNCHER V3 - VISUAL EDITION[/bold cyan]\n" +
            "[yellow]Authority Level: 11.0[/yellow] | [green]Commander: Bobby Don McWilliams II[/green]",
            border_style="bright_blue"
        ))
        
        # Discover servers
        self.discover_servers()
        
        # Launch sequence
        self.console.print("\n[bold yellow]🚀 LAUNCHING SERVERS...[/bold yellow]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            launch_task = progress.add_task("[cyan]Launching servers...", total=len(self.servers))
            
            for server_id in self.servers:
                server_name = self.servers[server_id]['name']
                progress.update(launch_task, description=f"[cyan]Launching {server_name}...")
                
                success = self.launch_server(server_id)
                progress.advance(launch_task)
                
                if success:
                    self.console.print(f"  [green]✅[/green] {server_name} - Port {self.servers[server_id]['port']} - PID {self.servers[server_id]['pid']}")
                else:
                    self.console.print(f"  [red]❌[/red] {server_name} - Failed to launch")
                
                time.sleep(0.5)  # Brief pause between launches
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_servers, daemon=True)
        monitor_thread.start()
        
        # Summary
        running = sum(1 for s in self.servers.values() if s['status'] == 'running')
        failed = sum(1 for s in self.servers.values() if s['status'] == 'failed')
        
        self.console.print("\n" + "="*60)
        self.console.print(Panel(
            f"[green]✅ Running: {running}[/green] | [red]❌ Failed: {failed}[/red] | [yellow]📊 Total: {len(self.servers)}[/yellow]\n" +
            f"[cyan]Dashboard: http://localhost:{self.config['dashboard_port']}[/cyan]",
            title="Launch Summary",
            border_style="green"
        ))
        
        # Show live status table
        self.console.print("\n[bold]Live Server Status:[/bold]")
        self.console.print("Press Ctrl+C to stop all servers and exit\n")
        
        try:
            with Live(self.create_status_table(), refresh_per_second=1, console=self.console) as live:
                while True:
                    time.sleep(1)
                    live.update(self.create_status_table())
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Shutting down...[/yellow]")
            self.shutdown()
    
    def shutdown(self):
        """Shutdown all servers"""
        self.console.print("\n[red]Stopping all servers...[/red]")
        
        for server_id, server in self.servers.items():
            if server['process'] and server['process'].poll() is None:
                server['process'].terminate()
                self.console.print(f"  • Stopped {server['name']}")
        
        self.console.print("[green]✅ All servers stopped[/green]")

# Install required packages if missing
def install_dependencies():
    """Install required packages"""
    required = ['rich', 'colorama', 'requests', 'pyyaml', 'psutil']
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

# Main entry
if __name__ == "__main__":
    os.chdir("E:/ECHO_XV4/MLS")
    
    # Install dependencies
    install_dependencies()
    
    # Run launcher
    launcher = VisualMasterLauncher()
    asyncio.run(launcher.run())
