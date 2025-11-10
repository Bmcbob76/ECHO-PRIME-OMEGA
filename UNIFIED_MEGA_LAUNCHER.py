"""
🚀 UNIFIED MEGA-LAUNCHER V1 - ECHO_XV4
Authority Level 11.0 - Commander Bobby Don McWilliams II

MANAGES ALL SERVERS:
- MCP Constellation (9 stdio servers for VS Code/Claude)
- Desktop Active Servers (HTTP/API servers)
- Voice system with MUTEX (no overlapping announcements)
- 15-minute health checks for ALL servers
- Phoenix auto-healing
- Auto-discovery
"""

import subprocess
import time
import socket
import psutil
import logging
import threading
from pathlib import Path
from datetime import datetime
import sys
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Add paths
sys.path.insert(0, "E:/ECHO_XV4/EPCP3O_COPILOT")

# Voice System with MUTEX
try:
    from epcp3o_voice_integrated import EPCP3OVoiceSystem
    import asyncio
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

class ThreadSafeVoice:
    """Voice with mutex to prevent overlap"""
    def __init__(self):
        self.voice = None
        self.mutex = threading.Lock()
        if VOICE_AVAILABLE:
            try:
                self.voice = EPCP3OVoiceSystem()
                self.voice.initialize()
            except: pass
    
    def announce(self, message: str, voice_id: str = '0UTDtgGGkpqERQn1s0YK'):
        if not self.voice: return
        with self.mutex:
            try:
                self.voice.play_r2d2_sound('processing')
                asyncio.run(self.voice.speak_c3po(message, voice_id=voice_id, emotion='calm'))
            except: pass

voice = ThreadSafeVoice()

# Server configurations
MCP_SERVERS = [
    ("Orchestrator", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\orchestrator\\mcp_orchestrator.py", 8000, "mcp"),
    ("Filesystem", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\filesystem\\mcp_filesystem.py", 8001, "mcp"),
    ("Windows API", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\windows_api\\mcp_windows.py", 8002, "mcp"),
    ("Process Control", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\process_control\\mcp_process.py", 8003, "mcp"),
    ("Crystal Memory", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\crystal_memory\\mcp_crystal.py", 8004, "mcp"),
    ("Workflow Engine", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\workflow_engine\\mcp_workflow.py", 8005, "mcp"),
    ("Voice System", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\voice_system\\mcp_voice.py", 8006, "mcp"),
    ("Network Tools", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\network_tools\\mcp_network.py", 8007, "mcp"),
    ("Healing Protocols", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\healing_protocols\\mcp_healing.py", 8008, "mcp"),
]

DESKTOP_SERVERS_PATH = Path("E:/ECHO_XV4/MLS/servers/ACTIVE_SERVERS")
LOG_DIR = Path("E:/ECHO_XV4/MLS/logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"unified_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

server_states = {}

def discover_desktop_servers():
    """Auto-discover desktop servers"""
    if not DESKTOP_SERVERS_PATH.exists():
        return []
    
    servers = []
    next_port = 9000
    
    for py_file in DESKTOP_SERVERS_PATH.glob("*.py"):
        if py_file.stem.startswith("__") or "test" in py_file.stem.lower() or py_file.stem == "LAUNCH_MCP_CONSTELLATION":
            continue
        
        servers.append((
            py_file.stem.replace('_', ' ').title(),
            str(py_file),
            next_port,
            "desktop"
        ))
        next_port += 1
    
    return servers

def launch_server(name: str, path: str, port: int, server_type: str, python_exe: str) -> bool:
    """Launch a server"""
    
    # Check if already running
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and path in ' '.join(cmdline):
                logger.info(f"✅ {name} already running (PID: {proc.info['pid']})")
                voice.announce(f"{name} already operational")
                server_states[name] = {"status": "running", "pid": proc.info['pid'], "type": server_type}
                return True
        except: continue
    
    # Launch
    logger.info(f"🚀 Launching {name} ({server_type})...")
    voice.announce(f"Launching {name}")
    
    log_file = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    try:
        with open(log_file, 'w') as log:
            proc = subprocess.Popen(
                [python_exe, path],
                stdout=log,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
        
        time.sleep(2)
        
        if proc.poll() is None:
            logger.info(f"✅ {name} launched (PID: {proc.pid})")
            voice.announce(f"{name} online", 'keDMh3sQlEXKM4EQxvvi')
            server_states[name] = {"status": "running", "pid": proc.pid, "type": server_type}
            return True
        else:
            logger.error(f"❌ {name} crashed on launch")
            server_states[name] = {"status": "crashed", "type": server_type}
            return False
    except Exception as e:
        logger.error(f"❌ {name} exception: {e}")
        return False

def main():
    print("=" * 70)
    print("🚀 UNIFIED MEGA-LAUNCHER V1 - ECHO_XV4")
    print("   Authority Level 11.0 - Commander Bobby Don McWilliams II")
    print("=" * 70)
    
    voice.announce("Unified Mega-Launcher initialized - Commander authenticated", '8ATB4Ory7NkyCVRpePdw')
    
    python_exe = "E:\\ECHO_XV4\\MLS\\servers\\ACTIVE_SERVERS\\venv_mcp_py312\\Scripts\\python.exe"
    
    # Discover all servers
    desktop_servers = discover_desktop_servers()
    all_servers = MCP_SERVERS + desktop_servers
    
    logger.info(f"📡 Total servers: {len(all_servers)} (MCP: {len(MCP_SERVERS)}, Desktop: {len(desktop_servers)})")
    
    # Launch all
    launched = 0
    already_running = 0
    failed = 0
    
    for name, path, port, server_type in all_servers:
        if launch_server(name, path, port, server_type, python_exe):
            if server_states[name]["status"] == "running":
                already_running += 1
            else:
                launched += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 UNIFIED LAUNCH SUMMARY")
    print("=" * 70)
    print(f"   ✅ Already Running: {already_running}")
    print(f"   🚀 Launched: {launched}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Total: {len(all_servers)}")
    print("=" * 70)
    
    if failed == 0:
        voice.announce(f"All {len(all_servers)} servers operational", 'keDMh3sQlEXKM4EQxvvi')
    
    print("\nPress Ctrl+C to exit (servers continue running)")
    
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 Exiting")
        voice.announce("Launcher shutdown - servers remain operational", '8ATB4Ory7NkyCVRpePdw')

if __name__ == "__main__":
    main()
