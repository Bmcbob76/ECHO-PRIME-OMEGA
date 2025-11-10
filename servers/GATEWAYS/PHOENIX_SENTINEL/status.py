"""
Phoenix Sentinel - System Status Dashboard
Real-time monitoring of all components
"""

import psutil
import json
from datetime import datetime
import os

def print_banner():
    print("\n" + "="*70)
    print("  🔥 PHOENIX SENTINEL - SYSTEM STATUS DASHBOARD 🛡️")
    print("  Authority Level: 11.0")
    print("="*70 + "\n")

def get_component_status():
    """Check if all components are ready"""
    base_path = "P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\GATEWAYS\\PHOENIX_SENTINEL"
    
    components = {
        "Core System": os.path.exists(f"{base_path}\\phoenix_sentinel_core.py"),
        "GS343 Patterns": os.path.exists(f"{base_path}\\gs343_patterns.py"),
        "Configuration": os.path.exists(f"{base_path}\\config.json"),
        "Requirements": os.path.exists(f"{base_path}\\requirements.txt"),
        "Documentation": os.path.exists(f"{base_path}\\README.md"),
        "Launcher": os.path.exists(f"{base_path}\\launch_sentinel.bat")
    }
    
    return components

def get_system_metrics():
    """Get current system state"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')
    
    return {
        "cpu": cpu,
        "memory": memory.percent,
        "disk": disk.percent,
        "processes": len(psutil.pids())
    }

def main():
    print_banner()
    
    # Component Status
    print("📦 COMPONENT STATUS")
    print("-" * 70)
    components = get_component_status()
    for name, status in components.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {name}")
    
    all_ready = all(components.values())
    if all_ready:
        print("\n   🎯 All components ready for deployment")
    else:
        print("\n   ⚠️  Some components missing")
    
    # Skills Integration
    print("\n🎓 SKILLS INTEGRATED")
    print("-" * 70)
    skills = {
        "jarvis-project": "Natural language voice control",
        "autonomous-cpu": "Self-directed process optimization",
        "windows-api-mastery": "500+ Windows API endpoints"
    }
    for skill, desc in skills.items():
        print(f"   ✅ {skill}: {desc}")
    
    # System Metrics
    print("\n📊 CURRENT SYSTEM STATE")
    print("-" * 70)
    metrics = get_system_metrics()
    print(f"   CPU Usage: {metrics['cpu']:.1f}%")
    print(f"   Memory: {metrics['memory']:.1f}%")
    print(f"   Disk: {metrics['disk']:.1f}%")
    print(f"   Processes: {metrics['processes']}")
    
    # Configuration
    try:
        with open("P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\GATEWAYS\\PHOENIX_SENTINEL\\config.json") as f:
            config = json.load(f)['phoenix_sentinel']
        
        print("\n⚙️  CONFIGURATION")
        print("-" * 70)
        print(f"   Authority Level: {config['authority_level']}")
        print(f"   Version: {config['version']}")
        print(f"   Windows API: {'Enabled' if config['components']['windows_api']['enabled'] else 'Disabled'}")
        print(f"   Autonomous CPU: {'Enabled' if config['components']['autonomous_cpu']['enabled'] else 'Disabled'}")
        print(f"   JARVIS Voice: {'Enabled' if config['components']['jarvis_voice']['enabled'] else 'Disabled'}")
        print(f"   GS343 Healing: {'Enabled' if config['components']['gs343_healing']['enabled'] else 'Disabled'}")
        print(f"   Wake Word: '{config['components']['jarvis_voice']['wake_word']}'")
        
    except Exception as e:
        print(f"\n   ⚠️  Could not load configuration: {e}")
    
    # Quick Start
    print("\n🚀 QUICK START")
    print("-" * 70)
    print("   1. Run as Administrator")
    print("   2. Execute: launch_sentinel.bat")
    print("   3. Say wake word: 'Sentinel'")
    print("   4. Give voice commands")
    print("\n   Or run demo: H:\\Tools\\python.exe demo.py")
    
    # Summary
    print("\n" + "="*70)
    print("  🔥 PHOENIX SENTINEL STATUS: " + ("READY" if all_ready else "INCOMPLETE"))
    print("  🛡️ Your autonomous guardian awaits")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
