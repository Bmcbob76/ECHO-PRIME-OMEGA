"""
SIMPLIFIED VISUAL LAUNCHER - WORKING VERSION
Shows real-time server status in console
"""

import sys
import os
import subprocess
import time
import socket
from pathlib import Path
from datetime import datetime
import threading

# Change to MLS directory
os.chdir("E:\\ECHO_XV4\\MLS")

class SimpleLauncher:
    def __init__(self):
        self.servers_path = Path("E:/ECHO_XV4/MLS/servers")
        self.servers = {}
        self.next_port = 8000
        
    def print_header(self):
        """Print header"""
        print("="*70)
        print(" "*20 + "ECHO_XV4 MASTER LAUNCHER V3")
        print(" "*15 + "Authority Level: 11.0 - ACTIVE")
        print("="*70)
        print()
        
    def get_free_port(self):
        """Get free port"""
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', self.next_port))
                sock.close()
                port = self.next_port
                self.next_port += 1
                return port
            except:
                self.next_port += 1
                
    def discover_servers(self):
        """Find all Python servers"""
        print("[DISCOVERY] Scanning servers directory...")
        print("-"*50)
        
        for py_file in self.servers_path.glob("*.py"):
            server_id = py_file.stem
            port = self.get_free_port()
            self.servers[server_id] = {
                'path': py_file,
                'port': port,
                'process': None,
                'status': 'discovered'
            }
            print(f"  ✓ Found: {server_id:<30} Port: {port}")
            
        print(f"\n[RESULT] Discovered {len(self.servers)} servers")
        print("="*70)
        return len(self.servers)
        
    def launch_server(self, server_id):
        """Launch a single server"""
        server = self.servers[server_id]
        
        try:
            cmd = [sys.executable, str(server['path']), str(server['port'])]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            server['process'] = process
            server['pid'] = process.pid
            server['status'] = 'starting'
            
            # Check if running
            time.sleep(1)
            if process.poll() is None:
                server['status'] = 'running'
                return True, process.pid
            else:
                server['status'] = 'failed'
                return False, None
                
        except Exception as e:
            server['status'] = 'error'
            return False, str(e)
            
    def launch_all(self):
        """Launch all servers"""
        print("\n[LAUNCHING] Starting all servers...")
        print("-"*50)
        
        success_count = 0
        fail_count = 0
        
        for server_id in self.servers:
            print(f"  Launching: {server_id:<30}", end="")
            
            success, pid = self.launch_server(server_id)
            
            if success:
                print(f" ✓ RUNNING [Port: {self.servers[server_id]['port']}, PID: {pid}]")
                success_count += 1
            else:
                print(f" ✗ FAILED")
                fail_count += 1
                
            # Small delay between launches
            time.sleep(0.5)
            
        print("="*70)
        print(f"\n[SUMMARY] Launch Complete")
        print(f"  ✓ Successful: {success_count}")
        print(f"  ✗ Failed: {fail_count}")
        print(f"  Total: {len(self.servers)}")
        print("="*70)
        
        return success_count, fail_count
        
    def show_status(self):
        """Show current status"""
        print("\n[STATUS] Current Server Status")
        print("-"*70)
        print(f"{'Server':<30} {'Port':<8} {'PID':<10} {'Status':<10}")
        print("-"*70)
        
        for server_id, server in self.servers.items():
            name = server_id[:28]
            port = server['port']
            pid = server.get('pid', '-')
            status = server['status'].upper()
            
            # Color codes for status
            if status == 'RUNNING':
                status_display = f"✓ {status}"
            elif status == 'FAILED':
                status_display = f"✗ {status}"
            else:
                status_display = f"  {status}"
                
            print(f"{name:<30} {port:<8} {str(pid):<10} {status_display:<10}")
            
        print("-"*70)
        
    def monitor_loop(self):
        """Monitor servers"""
        while True:
            time.sleep(30)
            # Check each server
            for server_id, server in self.servers.items():
                if server['process'] and server['process'].poll() is not None:
                    server['status'] = 'stopped'
                    print(f"\n[ALERT] Server {server_id} has stopped!")
                    
    def run(self):
        """Main run method"""
        self.print_header()
        
        # Discover
        count = self.discover_servers()
        
        if count == 0:
            print("[ERROR] No servers found in servers directory!")
            return
            
        # Launch
        success, failed = self.launch_all()
        
        # Show status
        self.show_status()
        
        # Start monitoring
        monitor = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor.start()
        
        # Keep running
        print("\n[INFO] Dashboard: http://localhost:9000")
        print("[INFO] Press Ctrl+C to stop all servers and exit")
        print("\n[MONITORING] System is running...")
        
        try:
            while True:
                time.sleep(60)
                # Refresh status every minute
                self.show_status()
        except KeyboardInterrupt:
            print("\n\n[SHUTDOWN] Stopping all servers...")
            self.shutdown()
            
    def shutdown(self):
        """Stop all servers"""
        for server_id, server in self.servers.items():
            if server['process']:
                try:
                    server['process'].terminate()
                    print(f"  ✓ Stopped: {server_id}")
                except:
                    pass
                    
        print("\n[COMPLETE] All servers stopped")
        print("="*70)

if __name__ == "__main__":
    launcher = SimpleLauncher()
    launcher.run()
