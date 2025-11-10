"""
MASTER LAUNCHER ULTIMATE - Quick Status Check
Commander Bobby Don McWilliams II - Authority Level 11.0

Provides instant system health overview.
"""

import os
import sys
import psutil
from datetime import datetime
from pathlib import Path

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check_processes():
    """Check if Master Launcher is running"""
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'master_launcher.py' in ' '.join(cmdline):
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None

def check_servers():
    """Count active MCP servers"""
    server_dir = Path("E:/ECHO_XV4/MLS/servers/ACTIVE_SERVERS")
    if server_dir.exists():
        servers = [f for f in server_dir.rglob("*.py") if f.is_file()]
        return len(servers)
    return 0

def check_hardware():
    """Get quick hardware stats"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, memory, disk

def check_logs():
    """Check log directory"""
    log_dir = Path("E:/ECHO_XV4/MLS/logs")
    if not log_dir.exists():
        return 0, "❌ Not found"
    
    log_files = list(log_dir.glob("*.log"))
    if log_files:
        latest = max(log_files, key=lambda f: f.stat().st_mtime)
        age = datetime.now() - datetime.fromtimestamp(latest.stat().st_mtime)
        return len(log_files), f"Latest: {age.seconds // 60}m ago"
    return 0, "No logs"

def main():
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{GREEN}🎖️  MASTER LAUNCHER ULTIMATE - QUICK STATUS{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    # Master Launcher Status
    print(f"{BLUE}🚀 MASTER LAUNCHER{RESET}")
    running, pid = check_processes()
    if running:
        print(f"{GREEN}  ✅ Running (PID: {pid}){RESET}")
    else:
        print(f"{YELLOW}  ⏸️  Not running{RESET}")
    
    # Server Count
    print(f"\n{BLUE}🌐 MCP SERVERS{RESET}")
    server_count = check_servers()
    print(f"{GREEN}  📊 Discovered: {server_count} servers{RESET}")
    
    # Hardware
    print(f"\n{BLUE}💻 HARDWARE{RESET}")
    cpu, memory, disk = check_hardware()
    
    cpu_color = GREEN if cpu < 70 else YELLOW if cpu < 90 else RED
    mem_color = GREEN if memory < 70 else YELLOW if memory < 90 else RED
    disk_color = GREEN if disk < 70 else YELLOW if disk < 90 else RED
    
    print(f"{cpu_color}  🔥 CPU: {cpu:.1f}%{RESET}")
    print(f"{mem_color}  💾 Memory: {memory:.1f}%{RESET}")
    print(f"{disk_color}  💿 Disk: {disk:.1f}%{RESET}")
    
    # Logs
    print(f"\n{BLUE}📝 LOGS{RESET}")
    log_count, log_status = check_logs()
    print(f"{GREEN}  📁 Files: {log_count} - {log_status}{RESET}")
    
    # Directories
    print(f"\n{BLUE}📁 DIRECTORIES{RESET}")
    dirs = {
        "Logs": "E:/ECHO_XV4/MLS/logs",
        "Backups": "E:/ECHO_XV4/MLS/backups",
        "Quarantine": "E:/ECHO_XV4/MLS/quarantine",
        "Databases": "E:/ECHO_XV4/MLS/databases"
    }
    
    for name, path in dirs.items():
        exists = os.path.exists(path)
        status = f"{GREEN}✅{RESET}" if exists else f"{RED}❌{RESET}"
        print(f"  {status} {name}: {path}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{GREEN}Status check complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

if __name__ == "__main__":
    main()
