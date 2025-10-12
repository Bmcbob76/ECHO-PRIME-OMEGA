"""
ECHO Process Naming Utility
Automatically sets process names for all ECHO servers
Commander Bobby Don McWilliams II - Authority Level 11.0
"""

import os
import sys

def set_process_name():
    """Set the process name from environment variable"""
    try:
        import setproctitle
        
        # Get server name from environment
        server_name = os.environ.get('SERVER_NAME', None)
        
        if server_name:
            # Set process title
            setproctitle.setproctitle(server_name)
            print(f"✅ Process name set: {server_name}")
            return True
        else:
            # Fallback: Try to derive from script name
            script_name = os.path.basename(sys.argv[0]).replace('.py', '').replace('_', ' ').title()
            port = os.environ.get('SERVER_PORT', 'Unknown')
            fallback_name = f"ECHO_XV4: {script_name} - Port {port}"
            setproctitle.setproctitle(fallback_name)
            print(f"✅ Process name set (fallback): {fallback_name}")
            return True
            
    except ImportError:
        print("⚠️ setproctitle not installed - process naming disabled")
        return False
    except Exception as e:
        print(f"⚠️ Failed to set process name: {e}")
        return False

# Auto-execute when imported
if __name__ != "__main__":
    set_process_name()
