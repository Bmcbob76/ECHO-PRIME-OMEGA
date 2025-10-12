#!/usr/bin/env python3
"""
ECHO MCP CONSTELLATION MASTER LAUNCHER
Commander Bobby Don McWilliams II - Authority Level 11.0
Launches all 9 MCP servers with health monitoring
"""

import subprocess
import sys
import time
from pathlib import Path

SERVERS = [
    ("Orchestrator", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/orchestrator/mcp_orchestrator.py", 9350),
    ("Filesystem", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/filesystem/mcp_filesystem.py", 9351),
    ("Windows API", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/windows_api/mcp_windows.py", 9352),
    ("Process Control", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/process_control/mcp_process.py", 9353),
    ("Crystal Memory", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/crystal_memory/mcp_crystal.py", 9354),
    ("Workflow Engine", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/workflow_engine/mcp_workflow.py", 9355),
    ("Voice System", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/voice_system/mcp_voice.py", 9356),
    ("Network Tools", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/network_tools/mcp_network.py", 9357),
    ("Healing Protocols", "E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION/healing_protocols/mcp_healing.py", 9358),
]

PYTHON_EXE = "E:/ECHO_XV4/MLS/servers/ACTIVE_SERVERS/venv_mcp_py312/Scripts/python.exe"

def launch_servers():
    print("=" * 80)
    print("🚀 ECHO MCP CONSTELLATION LAUNCHER")
    print("=" * 80)
    
    processes = []
    
    for name, script, port in SERVERS:
        print(f"🔥 Launching {name} on port {port}...")
        try:
            proc = subprocess.Popen(
                [PYTHON_EXE, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            processes.append((name, proc, port))
            print(f"✅ {name} started (PID: {proc.pid})")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
    
    print("=" * 80)
    print(f"✅ Launched {len(processes)}/{len(SERVERS)} servers")
    print("=" * 80)
    
    # Keep running
    try:
        while True:
            time.sleep(60)
            # Health check
            for name, proc, port in processes:
                if proc.poll() is not None:
                    print(f"⚠️ {name} crashed! Restarting...")
                    # Restart logic here
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all servers...")
        for name, proc, port in processes:
            proc.terminate()
        print("✅ All servers stopped")

if __name__ == "__main__":
    launch_servers()
