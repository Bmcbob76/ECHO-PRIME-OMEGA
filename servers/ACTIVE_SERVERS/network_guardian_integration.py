#!/usr/bin/env python3
"""
ECHO Network Guardian Integration
Integrates Network Guardian into main Quantum Defender dashboard
"""

import sys
import os
import subprocess
import threading
import time
import json
from pathlib import Path

# Add network guardian to path
network_guardian_path = Path(__file__).parent / "NETWORK_GUARDIAN"
sys.path.append(str(network_guardian_path))

try:
    from NETWORK_GUARDIAN.network_guardian import NetworkGuardian
    from NETWORK_GUARDIAN.network_guardian_web import app, socketio
except ImportError as e:
    print(f"Warning: Network Guardian modules not found: {e}")
    NetworkGuardian = None

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

class NetworkGuardianManager:
    """Manages Network Guardian integration"""
    
    def __init__(self):
        self.guardian = None
        self.web_server_process = None
        self.guardian_thread = None
        self.is_running = False
        
    def start_guardian(self):
        """Start Network Guardian monitoring"""
        try:
            if NetworkGuardian is None:
                return False, "Network Guardian modules not available"
            
            if self.guardian is None:
                self.guardian = NetworkGuardian()
            
            if not self.is_running:
                # Start guardian monitoring in separate thread
                self.guardian_thread = threading.Thread(
                    target=self._run_guardian_monitoring,
                    daemon=True
                )
                self.guardian_thread.start()
                self.is_running = True
                
                return True, "Network Guardian started successfully"
            else:
                return True, "Network Guardian already running"
                
        except Exception as e:
            return False, f"Failed to start Network Guardian: {str(e)}"
    
    def stop_guardian(self):
        """Stop Network Guardian monitoring"""
        try:
            if self.guardian and self.is_running:
                self.guardian.running = False
                self.is_running = False
                return True, "Network Guardian stopped"
            else:
                return True, "Network Guardian not running"
                
        except Exception as e:
            return False, f"Failed to stop Network Guardian: {str(e)}"
    
    def _run_guardian_monitoring(self):
        """Run guardian monitoring loop"""
        try:
            import asyncio
            asyncio.run(self.guardian.start_monitoring())
        except Exception as e:
            print(f"Guardian monitoring error: {e}")
            self.is_running = False
    
    def start_web_interface(self, port=5001):
        """Start Network Guardian web interface"""
        try:
            if self.web_server_process is None or self.web_server_process.poll() is not None:
                # Start web server in separate process
                web_script = network_guardian_path / "network_guardian_web.py"
                
                self.web_server_process = subprocess.Popen([
                    sys.executable, str(web_script)
                ], cwd=str(network_guardian_path))
                
                # Give server time to start
                time.sleep(3)
                
                return True, f"Network Guardian web interface started on port {port}"
            else:
                return True, "Web interface already running"
                
        except Exception as e:
            return False, f"Failed to start web interface: {str(e)}"
    
    def stop_web_interface(self):
        """Stop Network Guardian web interface"""
        try:
            if self.web_server_process and self.web_server_process.poll() is None:
                self.web_server_process.terminate()
                self.web_server_process.wait(timeout=5)
                return True, "Web interface stopped"
            else:
                return True, "Web interface not running"
                
        except Exception as e:
            return False, f"Failed to stop web interface: {str(e)}"
    
    def get_status(self):
        """Get Network Guardian status"""
        try:
            if self.guardian:
                status = self.guardian.get_system_status()
                status['web_interface_running'] = (
                    self.web_server_process is not None and 
                    self.web_server_process.poll() is None
                )
                return status
            else:
                return {
                    'running': False,
                    'web_interface_running': False,
                    'devices': {'total': 0, 'online': 0, 'blocked': 0},
                    'connections': {'active': 0},
                    'error': 'Guardian not initialized'
                }
                
        except Exception as e:
            return {
                'running': False,
                'error': str(e)
            }
    
    def get_devices(self):
        """Get discovered devices"""
        try:
            if self.guardian:
                devices = []
                for device in self.guardian.devices.values():
                    devices.append({
                        'ip': device.ip,
                        'mac': device.mac,
                        'hostname': device.hostname,
                        'device_type': device.device_type,
                        'vendor': device.vendor,
                        'status': device.status,
                        'custom_name': device.custom_name,
                        'is_authorized': device.is_authorized,
                        'threat_level': device.threat_level,
                        'is_blocked': device.ip in self.guardian.blocked_devices
                    })
                return devices
            else:
                return []
                
        except Exception as e:
            print(f"Error getting devices: {e}")
            return []
    
    def get_connections(self):
        """Get active connections"""
        try:
            if self.guardian:
                connections = []
                for conn in list(self.guardian.connections.values())[:50]:  # Limit to 50
                    connections.append({
                        'local_ip': conn.local_ip,
                        'local_port': conn.local_port,
                        'remote_ip': conn.remote_ip,
                        'remote_port': conn.remote_port,
                        'protocol': conn.protocol,
                        'status': conn.status,
                        'process_name': conn.process_name,
                        'process_id': conn.process_id
                    })
                return connections
            else:
                return []
                
        except Exception as e:
            print(f"Error getting connections: {e}")
            return []
    
    def block_device(self, ip, reason="Blocked from dashboard"):
        """Block a device"""
        try:
            if self.guardian:
                success = self.guardian.block_device(ip, reason)
                if success:
                    return True, f"Device {ip} blocked successfully"
                else:
                    return False, f"Failed to block device {ip}"
            else:
                return False, "Guardian not initialized"
                
        except Exception as e:
            return False, f"Error blocking device: {str(e)}"
    
    def unblock_device(self, ip):
        """Unblock a device"""
        try:
            if self.guardian:
                success = self.guardian.unblock_device(ip)
                if success:
                    return True, f"Device {ip} unblocked successfully"
                else:
                    return False, f"Failed to unblock device {ip}"
            else:
                return False, "Guardian not initialized"
                
        except Exception as e:
            return False, f"Error unblocking device: {str(e)}"
    
    def discover_devices(self):
        """Trigger device discovery"""
        try:
            if self.guardian:
                import asyncio
                
                # Run discovery in thread
                def run_discovery():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    devices = loop.run_until_complete(self.guardian.discover_network_devices())
                    loop.close()
                    return devices
                
                discovery_thread = threading.Thread(target=run_discovery, daemon=True)
                discovery_thread.start()
                
                return True, "Device discovery started"
            else:
                return False, "Guardian not initialized"
                
        except Exception as e:
            return False, f"Error starting discovery: {str(e)}"

# Global guardian manager instance
guardian_manager = NetworkGuardianManager()

def get_guardian_manager():
    """Get the global guardian manager instance"""
    return guardian_manager

def start_network_guardian():
    """Start Network Guardian system"""
    manager = get_guardian_manager()
    
    # Start monitoring
    success, message = manager.start_guardian()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Start web interface
    success, message = manager.start_web_interface()
    if success:
        print(f"✅ {message}")
        print(f"🌐 Network Guardian Dashboard: http://localhost:5001")
    else:
        print(f"❌ {message}")
    
    return True

def stop_network_guardian():
    """Stop Network Guardian system"""
    manager = get_guardian_manager()
    
    # Stop monitoring
    success, message = manager.stop_guardian()
    print(f"🛑 {message}")
    
    # Stop web interface
    success, message = manager.stop_web_interface()
    print(f"🛑 {message}")
    
    return True

def get_network_guardian_status():
    """Get Network Guardian status"""
    manager = get_guardian_manager()
    return manager.get_status()

def get_network_devices():
    """Get network devices"""
    manager = get_guardian_manager()
    return manager.get_devices()

def get_network_connections():
    """Get active network connections"""
    manager = get_guardian_manager()
    return manager.get_connections()

if __name__ == "__main__":
    print("🛡️ ECHO Network Guardian Integration")
    print("=====================================")
    
    try:
        start_network_guardian()
        
        print("\n📊 System Status:")
        status = get_network_guardian_status()
        print(json.dumps(status, indent=2))
        
        print("\n🔄 Running... (Press Ctrl+C to stop)")
        while True:
            time.sleep(10)
            status = get_network_guardian_status()
            devices = len(get_network_devices())
            connections = len(get_network_connections())
            print(f"📈 {devices} devices, {connections} connections, Running: {status.get('running', False)}")
            
    except KeyboardInterrupt:
        print("\n⚠️ Shutdown requested...")
        stop_network_guardian()
        print("✅ Network Guardian stopped")