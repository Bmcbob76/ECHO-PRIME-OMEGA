import re
from pathlib import Path

# Read file
launcher_path = Path("E:/ECHO_XV4/MLS/LAUNCH_MCP_CONSTELLATION.py")
content = launcher_path.read_text()

# New launch_server function
new_function = '''def launch_server(name: str, path: str, port: int, python_exe: str, force: bool = False) -> bool:
    """Launch a server with full protection (supports stdio MCP servers)"""
    
    file_path = Path(path)
    
    # Check if already running by finding process with this script path
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and path in ' '.join(cmdline):
                if not force:
                    logger.info(f"✅ {name} already running (PID: {proc.info['pid']})")
                    voice.c3po_announce(f"{name} already operational")
                    server_states[name] = {"status": "running", "pid": proc.info['pid'], "port": port}
                    lock_file(file_path)
                    return True
                else:
                    # Force restart - kill existing
                    logger.info(f"🔄 Force restarting {name} (killing PID: {proc.info['pid']})")
                    proc.kill()
                    time.sleep(1)
        except:
            continue
    
    # Create backup before launch
    unlock_file(file_path)
    backup = create_backup(file_path)
    
    # Launch the server
    logger.info(f"🚀 Launching {name}...")
    voice.c3po_announce(f"Launching {name}")
    
    log_file = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    try:
        with open(log_file, 'w') as log:
            proc = subprocess.Popen(
                [python_exe, path],
                stdout=log,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
        
        # Wait for process to stabilize
        time.sleep(2)
        
        # Verify: check if process is still alive (not port!)
        if proc.poll() is None:
            logger.info(f"✅ {name} launched successfully (PID: {proc.pid})")
            voice.echo_announce(f"{name} online and operational")
            
            server_states[name] = {"status": "running", "pid": proc.pid, "port": port, "log": log_file}
            crash_counts[name] = 0
            
            # Lock file after successful launch
            lock_file(file_path)
            
            return True
        else:
            # Process died immediately
            error_output = log_file.read_text() if log_file.exists() else "Process died immediately"
            logger.error(f"❌ {name} crashed on launch: {error_output[:200]}")
            voice.bree_roast(f"{name} just crashed on launch! What kind of broken-ass shit is this?!")
            
            server_states[name] = {"status": "crashed", "error": error_output}
            crash_counts[name] = crash_counts.get(name, 0) + 1
            
            return False
            
    except Exception as e:
        logger.error(f"❌ {name} exception: {e}")
        voice.bree_roast(f"{name} threw an exception: {e}")
        server_states[name] = {"status": "error", "error": str(e)}
        return False'''

# Replace the launch_server function
pattern = r'def launch_server\(.*?\n(?:.*?\n)*?        return False'
content = re.sub(pattern, new_function, content, count=1, flags=re.DOTALL)

# Save
launcher_path.write_text(content)
print("✅ launch_server function replaced!")
