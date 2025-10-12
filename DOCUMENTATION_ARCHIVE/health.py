import requests
import subprocess

from pathlib import Path
import sys

# GS343 Foundation Integration - MANDATORY
GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    print("?? WARNING: GS343 Foundation not loaded - Limited functionality")
def check_http_health(port):
    try:
        resp = requests.get(f"http://localhost:{port}/health", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False

def check_custom_health(script_path, port):
    try:
        proc = subprocess.run([script_path, str(port)], capture_output=True, timeout=2)
        return proc.returncode == 0
    except Exception:
        return False
