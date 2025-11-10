"""
🚀 MASTER MODULAR LAUNCHER V3 - DISPLAY VERSION
Full console output with server details and messages
Authority Level 11.0 - Commander Bobby Don McWilliams II
"""

import sys
import os
import asyncio
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Back, Style
import psutil

# Initialize colorama for Windows console colors
try:
    init(autoreset=True)
    COLORS_AVAILABLE = True
except:
    COLORS_AVAILABLE = False

# Set working directory
os.chdir("E:/ECHO_XV4/MLS")
sys.path.insert(0, "E:/ECHO_XV4/MLS")

# Import the main launcher
from master_modular_launcher_enhanced import MasterModularLauncherV3

class DisplayLauncher(MasterModularLauncherV3):
    """Enhanced launcher with console display"""
    
    def __init__(self):
        super().__init__()
        self.display_thread = None
        self.start_time = datetime.now()
        
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                    MASTER MODULAR LAUNCHER V3 - ECHO_XV4                      ║
╠════════════════════════════════════════════════════════════════════════════╣
║  Authority Level: 11.0          Commander: Bobby Don McWilliams II           ║
║  System: ECHO_XV4 Production    Foundation: GS343 Divine Overseer           ║
║  Features: Auto-Discovery | Hot Reload | MCP Integration | Docker Support    ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
        if COLORS_AVAILABLE:
            print(Fore.CYAN + banner)
        else:
            print(banner)
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Initializing Master Launcher...")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Servers Directory: E:\\ECHO_XV4\\MLS\\servers")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Dashboard Port: {self.config['dashboard_port']}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Base Port: {self.config['base_port']}\n")
    
    def display_status(self):
        """Display continuous status updates"""
        while True:
            try:
                # Clear screen (Windows)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Print header
                self.print_banner()
                
                # Server discovery status
                print("=" * 80)
                if COLORS_AVAILABLE:
                    print(Fore.YELLOW + "📂 DISCOVERED SERVERS:")
                else:
                    print("📂 DISCOVERED SERVERS:")
                print("=" * 80)
                
                # Display each server
                for server_id, server in self.servers.items():
                    status_color = Fore.GREEN if server['status'] == 'running' else Fore.RED if server['status'] == 'failed' else Fore.YELLOW
                    status_symbol = "✅" if server['status'] == 'running' else "❌" if server['status'] == 'failed' else "⚠️"
                    
                    if COLORS_AVAILABLE:
                        print(f"{status_symbol} {status_color}{server['name']:<30}{Style.RESET_ALL} "
                              f"Port: {server['port']:<6} "
                              f"Status: {server['status']:<10} "
                              f"Restarts: {server['restart_count']}")
                    else:
                        print(f"{status_symbol} {server['name']:<30} "
                              f"Port: {server['port']:<6} "
                              f"Status: {server['status']:<10} "
                              f"Restarts: {server['restart_count']}")
                    
                    # Show instances
                    for i, instance in enumerate(server.get('instances', [])):
                        if instance:
                            print(f"    └─ Instance {i}: PID {instance.get('pid', 'N/A')} - {instance.get('status', 'unknown')}")
                
                # System metrics
                print("\n" + "=" * 80)
                if COLORS_AVAILABLE:
                    print(Fore.CYAN + "📊 SYSTEM METRICS:")
                else:
                    print("📊 SYSTEM METRICS:")
                print("=" * 80)
                
                uptime = (datetime.now() - self.start_time).total_seconds()
                hours = int(uptime // 3600)
                minutes = int((uptime % 3600) // 60)
                seconds = int(uptime % 60)
                
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                
                print(f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
                print(f"Total Servers: {len(self.servers)}")
                print(f"Running: {sum(1 for s in self.servers.values() if s['status'] == 'running')}")
                print(f"Failed: {sum(1 for s in self.servers.values() if s['status'] == 'failed')}")
                print(f"Servers Launched: {self.metrics['servers_launched']}")
                print(f"Health Checks: {self.metrics['health_checks']}")
                print(f"Auto Heals: {self.metrics['auto_heals']}")
                print(f"CPU Usage: {cpu_percent:.1f}%")
                print(f"Memory Usage: {memory.percent:.1f}%")
                
                # Recent events
                print("\n" + "=" * 80)
                if COLORS_AVAILABLE:
                    print(Fore.MAGENTA + "📜 RECENT EVENTS:")
                else:
                    print("📜 RECENT EVENTS:")
                print("=" * 80)
                
                # Get last few log entries (simplified)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] System monitoring active...")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Health checks running...")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Dashboard available at http://localhost:{self.config['dashboard_port']}")
                
                # Footer
                print("\n" + "=" * 80)
                if COLORS_AVAILABLE:
                    print(Fore.GREEN + "Press Ctrl+C to stop all servers and exit")
                else:
                    print("Press Ctrl+C to stop all servers and exit")
                print("=" * 80)
                
                # Wait before next update
                time.sleep(5)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Display error: {e}")
                time.sleep(5)
    
    def launch_server(self, server_id: str, instance_num: int = 0) -> bool:
        """Override to show launch messages"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if COLORS_AVAILABLE:
            print(f"\n{Fore.YELLOW}[{timestamp}] 🚀 Launching {server_id}...")
        else:
            print(f"\n[{timestamp}] 🚀 Launching {server_id}...")
        
        result = super().launch_server(server_id, instance_num)
        
        if result:
            if COLORS_AVAILABLE:
                print(f"{Fore.GREEN}[{timestamp}] ✅ {server_id} launched successfully on port {self.servers[server_id]['port']}")
            else:
                print(f"[{timestamp}] ✅ {server_id} launched successfully on port {self.servers[server_id]['port']}")
        else:
            if COLORS_AVAILABLE:
                print(f"{Fore.RED}[{timestamp}] ❌ Failed to launch {server_id}")
            else:
                print(f"[{timestamp}] ❌ Failed to launch {server_id}")
        
        return result
    
    async def run_with_display(self):
        """Run launcher with display"""
        # Print banner
        self.print_banner()
        
        # Start display thread
        self.display_thread = threading.Thread(target=self.display_status, daemon=True)
        self.display_thread.start()
        
        # Discover servers
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Discovering servers...")
        discovered = self.discover_servers()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Found {len(discovered)} servers")
        
        # Launch all servers
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚀 Launching all servers...")
        for server_id in self.servers:
            for i in range(self.config['num_instances_per_server']):
                self.launch_server(server_id, i)
                await asyncio.sleep(1)  # Stagger launches
        
        # Start file watcher
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 👁️ Starting file watcher for hot reload...")
        self.start_file_watcher()
        
        # Start dashboard
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Starting dashboard on http://localhost:{self.config['dashboard_port']}...")
        self.start_dashboard()
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ All systems operational!\n")
        
        # Main monitoring loop
        try:
            while True:
                # Perform health sweep
                unhealthy = self.perform_health_sweep()
                if unhealthy:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    if COLORS_AVAILABLE:
                        print(f"{Fore.YELLOW}[{timestamp}] ⚠️ Auto-healing servers: {unhealthy}")
                    else:
                        print(f"[{timestamp}] ⚠️ Auto-healing servers: {unhealthy}")
                
                await asyncio.sleep(self.config['health_check_interval'])
                
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛑 Shutdown signal received...")
        finally:
            await self.shutdown()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ All servers stopped. Goodbye!")

async def main():
    """Main entry point with display"""
    # Install colorama if not available
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "--quiet"], 
                      capture_output=True, timeout=10)
    except:
        pass
    
    launcher = DisplayLauncher()
    await launcher.run_with_display()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutdown complete.")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        input("Press Enter to exit...")
