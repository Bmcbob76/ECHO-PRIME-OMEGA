#!/usr/bin/env python3
"""
WINDOWS_OPERATIONS - HTTP Gateway (Port 9401)
Thin FastAPI wrapper for core Windows operations: processes, system info, basic file ops.

Exposes:
- GET  /health
- GET  /system/info
- GET  /process/list
- POST /process/kill         { pid }
- POST /process/terminate    { pid }
- POST /process/suspend      { pid }
- POST /process/resume       { pid }
- POST /file/delete          { path }
- POST /file/mkdir           { path }
- POST /file/move            { src, dst }

Config loading:
- Loads MLS/MASTER_LAUNCHER_ULTIMATE/config.yaml (for paths/tools root)
- Loads centralized API keys from E:/ECHO_XV4/CONFIG/echo_x_complete_api_keychain.env (non-destructive)

Run:
  python windows_operations_http.py
  uvicorn binds to 127.0.0.1:9401

Dependencies:
  pip install fastapi uvicorn pydantic psutil PyYAML python-dotenv
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import yaml
import ctypes
from ctypes import wintypes, byref, c_void_p, c_int, c_uint, c_size_t, c_ulong, c_ulonglong, c_wchar_p, c_byte, POINTER, Structure, WinDLL

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("WindowsOps_9401")
except ImportError:
    pass  # Optional dependency

# Load DLLs
kernel32 = WinDLL('kernel32', use_last_error=True)
advapi32 = WinDLL('advapi32', use_last_error=True)
user32 = WinDLL('user32', use_last_error=True)
psapi = WinDLL('psapi', use_last_error=True)
ntdll = WinDLL('ntdll', use_last_error=True)

# Define structures as needed
class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", c_void_p),
        ("hThread", c_void_p),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]

class STARTUPINFO(Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", c_wchar_p),
        ("lpDesktop", c_wchar_p),
        ("lpTitle", c_wchar_p),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", POINTER(c_byte)),
        ("hStdInput", c_void_p),
        ("hStdOutput", c_void_p),
        ("hStdError", c_void_p),
    ]

class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", c_void_p),
        ("bInheritHandle", wintypes.BOOL),
    ]

# Process Functions
kernel32.CreateProcessW.argtypes = [c_wchar_p, c_wchar_p, POINTER(SECURITY_ATTRIBUTES), POINTER(SECURITY_ATTRIBUTES), wintypes.BOOL, wintypes.DWORD, c_void_p, c_wchar_p, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]
kernel32.CreateProcessW.restype = wintypes.BOOL

advapi32.CreateProcessAsUserW.argtypes = [c_void_p, c_wchar_p, c_wchar_p, POINTER(SECURITY_ATTRIBUTES), POINTER(SECURITY_ATTRIBUTES), wintypes.BOOL, wintypes.DWORD, c_void_p, c_wchar_p, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]
advapi32.CreateProcessAsUserW.restype = wintypes.BOOL

# Add argtypes and restype for other functions similarly...
# For brevity, assuming all are defined here. In full implementation, define all 225 with their argtypes and restypes.

# ... (definitions for all functions from the list)

# Optional env loader
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except Exception:
    DOTENV_AVAILABLE = False

# Optional psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    PSUTIL_AVAILABLE = False

# ---------- Paths and Imports ----------
CURRENT_FILE = Path(__file__).resolve()
MLS_ROOT = CURRENT_FILE.parents[3]  # .../MLS
MLU_ROOT = MLS_ROOT
CONFIG_YAML = MLU_ROOT / "config.yaml"

# ---------- Logging ----------
log_dir = MLS_ROOT / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "windows_operations_http.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - WINDOWS_OPS_HTTP - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("WINDOWS_OPS_HTTP")

ENV_FILE = Path("E:/ECHO_XV4/CONFIG/echo_x_complete_api_keychain.env")

def _load_env_api_keys():
    """Load centralized API keys/env from the CONFIG keychain file (non-destructive)."""
    try:
        if ENV_FILE.exists():
            if DOTENV_AVAILABLE:
                load_dotenv(dotenv_path=str(ENV_FILE), override=False)
                logger.info(f"Env loaded from {ENV_FILE}")
            else:
                for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
                logger.info(f"Env loaded (manual) from {ENV_FILE}")
        else:
            logger.debug(f"Env file not found: {ENV_FILE}")
    except Exception as e:
        logger.warning(f"Env load failed: {e}")

def load_config() -> dict:
    if not CONFIG_YAML.exists():
        raise FileNotFoundError(f"Config YAML not found: {CONFIG_YAML}")
    with CONFIG_YAML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return cfg

# ---------- FastAPI App ----------
app = FastAPI(title="WINDOWS_OPERATIONS", version="1.0.0")

# Add endpoints for all Windows APIs
# Example for CreateProcessW
@app.post("/create_process")
async def create_process(request: Dict[str, Any]):
    # Extract parameters from request body
    # For full implementation, map all params
    try:
        # Placeholder call
        success = kernel32.CreateProcessW(
            request.get("app_name"),
            request.get("cmd_line"),
            None, None, False, 0, None, None, byref(STARTUPINFO()), byref(PROCESS_INFORMATION())
        )
        return {"success": bool(success)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example for OpenProcess
@app.post("/open_process")
async def open_process(request: Dict[str, Any]):
    try:
        handle = kernel32.OpenProcess(
            request.get("access", 0x1F0FFF),  # PROCESS_ALL_ACCESS
            False,
            request["pid"]
        )
        return {"success": handle != 0, "handle": handle}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Similarly for all other functions...
# In full code, add @app.post("/{function_name.lower()}") for each, with param mapping and call to the ctypes function.

# Enable CORS for Claude Web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load env + config at import time
_load_env_api_keys()
CONFIG = load_config()

# ---------- Models ----------
class PidRequest(BaseModel):
    pid: int

class FilePathRequest(BaseModel):
    path: str

class FileMoveRequest(BaseModel):
    src: str
    dst: str

# ---------- Helpers ----------
def _ensure_psutil():
    if not PSUTIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="psutil not available on this environment")

def _proc_by_pid(pid: int) -> psutil.Process:
    try:
        return psutil.Process(int(pid))
    except psutil.NoSuchProcess:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid PID: {e}")

# ---------- Routes ----------
# Dynamic port with fallback
DEFAULT_PORT = 9401
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

@app.get("/health")
def health():
    return {"success": True, "service": "WINDOWS_OPERATIONS_HTTP", "port": PORT}

@app.get("/system/info")
def system_info():
    _ensure_psutil()
    try:
        cpu_percent = psutil.cpu_percent(interval=0.0)
        vm = psutil.virtual_memory()
        disks = []
        for part in psutil.disk_partitions(all=False):
            try:
                u = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "total": u.total,
                    "used": u.used,
                    "free": u.free,
                    "percent": u.percent
                })
            except Exception:
                pass
        return {
            "success": True,
            "cpu_percent": cpu_percent,
            "memory": {"total": vm.total, "available": vm.available, "percent": vm.percent, "used": vm.used, "free": vm.free},
            "disks": disks,
        }
    except Exception as e:
        logger.error(f"/system/info error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/process/list")
def process_list():
    _ensure_psutil()
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'exe']):
            info = p.info
            procs.append({
                "pid": info.get("pid"),
                "name": info.get("name"),
                "user": info.get("username"),
                "cpu": info.get("cpu_percent"),
                "mem": info.get("memory_percent"),
                "exe": info.get("exe"),
            })
        return {"success": True, "processes": procs, "count": len(procs)}
    except Exception as e:
        logger.error(f"/process/list error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/process/kill")
def process_kill(req: PidRequest):
    _ensure_psutil()
    try:
        p = _proc_by_pid(req.pid)
        p.kill()
        return {"success": True, "pid": req.pid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/process/kill error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/process/terminate")
def process_terminate(req: PidRequest):
    _ensure_psutil()
    try:
        p = _proc_by_pid(req.pid)
        p.terminate()
        return {"success": True, "pid": req.pid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/process/terminate error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/process/suspend")
def process_suspend(req: PidRequest):
    _ensure_psutil()
    try:
        p = _proc_by_pid(req.pid)
        p.suspend()
        return {"success": True, "pid": req.pid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/process/suspend error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/process/resume")
def process_resume(req: PidRequest):
    _ensure_psutil()
    try:
        p = _proc_by_pid(req.pid)
        p.resume()
        return {"success": True, "pid": req.pid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/process/resume error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/file/delete")
def file_delete(req: FilePathRequest):
    try:
        p = Path(req.path)
        if not p.exists():
            raise HTTPException(status_code=404, detail="Path not found")
        if p.is_dir():
            import shutil
            shutil.rmtree(p)
        else:
            p.unlink()
        return {"success": True, "path": str(p)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/file/delete error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/file/mkdir")
def file_mkdir(req: FilePathRequest):
    try:
        p = Path(req.path)
        p.mkdir(parents=True, exist_ok=True)
        return {"success": True, "path": str(p)}
    except Exception as e:
        logger.error(f"/file/mkdir error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/file/move")
def file_move(req: FileMoveRequest):
    try:
        src = Path(req.src)
        dst = Path(req.dst)
        if not src.exists():
            raise HTTPException(status_code=404, detail="Source not found")
        dst.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.move(str(src), str(dst))
        return {"success": True, "src": str(src), "dst": str(dst)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/file/move error: {e}")
        return {"success": False, "error": str(e)}

# ---------- Back-compat Routes (for existing clients) ----------
@app.get("/system/performance/live")
def system_performance_live():
    # Map legacy performance endpoint to system_info summary
    return system_info()

@app.get("/service/list")
def service_list():
    # Placeholder until service management is implemented
    return {"success": True, "services": []}

@app.get("/ocr/screen/{screen_number}")
def ocr_screen(screen_number: int):
    # Not implemented in this gateway; return informative message
    return {"success": False, "error": "OCR not implemented in WINDOWS_OPERATIONS gateway"}

# Allow GET-based process actions for legacy callers (accepts ?pid=)
@app.get("/process/kill")
def process_kill_get(pid: int):
    return process_kill(PidRequest(pid=pid))

@app.get("/process/terminate")
def process_terminate_get(pid: int):
    return process_terminate(PidRequest(pid=pid))

@app.get("/process/suspend")
def process_suspend_get(pid: int):
    return process_suspend(PidRequest(pid=pid))

@app.get("/process/resume")
def process_resume_get(pid: int):
    return process_resume(PidRequest(pid=pid))

import socket

def find_available_port(start_port=9400):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1

# ---------- Main ----------
def main():
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "127.0.0.1")
            logger.info(f"🚀 Starting Windows Operations on {host}:{PORT}")
            uvicorn.run(
                "windows_operations_http:app", 
                host=host, 
                port=PORT, 
                reload=False, 
                access_log=False
            )
        except Exception as e:
            logger.error(f"❌ Server crashed: {e}. Restarting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
