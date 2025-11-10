#!/usr/bin/env python3
"""
WINDOWS_OPERATIONS - MCP stdio Server
Thin JSON-RPC (MCP) wrapper for Windows operations using psutil and stdlib.

Tools exposed:
- winops_health                  {}
- winops_system_info             {}
- winops_process_list            { limit? }
- winops_process_kill            { pid }
- winops_process_terminate       { pid }
- winops_process_suspend         { pid }
- winops_process_resume          { pid }
- winops_file_delete             { path }
- winops_file_mkdir              { path }
- winops_file_move               { src, dst }

Config loading:
- Loads MLS/MASTER_LAUNCHER_ULTIMATE/config.yaml (optional)
- Loads centralized API keys from E:/ECHO_XV4/CONFIG/echo_x_complete_api_keychain.env (non-destructive)
"""

import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

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

import ctypes
from ctypes import wintypes, byref, c_void_p, c_int, c_uint, c_size_t, c_ulong, c_ulonglong, c_wchar_p, c_byte, POINTER, Structure, WinDLL

# Load DLLs
kernel32 = WinDLL('kernel32', use_last_error=True)
advapi32 = WinDLL('advapi32', use_last_error=True)
user32 = WinDLL('user32', use_last_error=True)
psapi = WinDLL('psapi', use_last_error=True)
ntdll = WinDLL('ntdll', use_last_error=True)

# Define structures
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

# Function definitions (examples; full list implemented similarly)
kernel32.CreateProcessW.argtypes = [c_wchar_p, c_wchar_p, POINTER(SECURITY_ATTRIBUTES), POINTER(SECURITY_ATTRIBUTES), wintypes.BOOL, wintypes.DWORD, c_void_p, c_wchar_p, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]
kernel32.CreateProcessW.restype = wintypes.BOOL

kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.OpenProcess.restype = wintypes.HANDLE

# ... Add definitions for all 225 functions here

# ---------- Paths ----------
CURRENT_FILE = Path(__file__).resolve()
MLS_ROOT = CURRENT_FILE.parents[3]  # .../MLS
MLU_ROOT = MLS_ROOT / "MASTER_LAUNCHER_ULTIMATE"
CONFIG_YAML = MLU_ROOT / "config.yaml"
ENV_FILE = Path("E:/ECHO_XV4/CONFIG/echo_x_complete_api_keychain.env")

# ---------- Logging ----------
log_dir = MLS_ROOT / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "windows_operations_mcp.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - WINDOWS_OPS_MCP - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("WINDOWS_OPS_MCP")

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
                    import os
                    os.environ.setdefault(k.strip(), v.strip())
                logger.info(f"Env loaded (manual) from {ENV_FILE}")
    except Exception as e:
        logger.warning(f"Env load failed: {e}")

def _load_config() -> dict:
    try:
        if CONFIG_YAML.exists():
            return yaml.safe_load(CONFIG_YAML.read_text(encoding="utf-8")) or {}
    except Exception as e:
        logger.debug(f"Config load skipped: {e}")
    return {}

_load_env_api_keys()
CONFIG = _load_config()

# ---------- MCP Server ----------
class WinOpsMCPServer:
    def __init__(self) -> None:
        self.client_type = "unknown"

    def get_tools(self):
        tools = [
            {"name": "winops_health", "description": "Check Windows Operations MCP health", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "winops_system_info", "description": "Get system CPU/memory/disk info", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {
                "name": "winops_process_list",
                "description": "List running processes (limited for performance)",
                "inputSchema": {
                    "type": "object",
                    "properties": {"limit": {"type": "number", "default": 200}},
                    "required": []
                }
            },
            {"name": "winops_process_kill", "description": "Kill process by PID", "inputSchema": {"type": "object", "properties": {"pid": {"type": "number"}}, "required": ["pid"]}},
            {"name": "winops_process_terminate", "description": "Terminate process by PID", "inputSchema": {"type": "object", "properties": {"pid": {"type": "number"}}, "required": ["pid"]}},
            {"name": "winops_process_suspend", "description": "Suspend process by PID", "inputSchema": {"type": "object", "properties": {"pid": {"type": "number"}}, "required": ["pid"]}},
            {"name": "winops_process_resume", "description": "Resume process by PID", "inputSchema": {"type": "object", "properties": {"pid": {"type": "number"}}, "required": ["pid"]}},
            {
                "name": "winops_file_delete",
                "description": "Delete a file or directory recursively",
                "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
            },
            {"name": "winops_file_mkdir", "description": "Create directory (parents ok)", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
            {
                "name": "winops_file_move",
                "description": "Move/rename file or directory",
                "inputSchema": {"type": "object", "properties": {"src": {"type": "string"}, "dst": {"type": "string"}}, "required": ["src", "dst"]}
            },
        ]
        # Add tools for all Windows APIs
        # Example
        tools.append({"name": "winops_create_process", "description": "Create a new process", "inputSchema": {"type": "object", "properties": {"app_name": {"type": "string"}, "cmd_line": {"type": "string"}}, "required": ["cmd_line"]}})
        tools.append({"name": "winops_open_process", "description": "Open an existing process", "inputSchema": {"type": "object", "properties": {"pid": {"type": "number"}, "access": {"type": "number", "default": 0x1F0FFF}}, "required": ["pid"]}})
        # ... Add inputSchema for all 225 functions similarly
        return tools

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "winops_health":
                return {"success": True, "service": "WINDOWS_OPERATIONS_MCP"}

            if name == "winops_system_info":
                if not PSUTIL_AVAILABLE:
                    return {"success": False, "error": "psutil not available"}
                try:
                    cpu = psutil.cpu_percent(interval=0.0)
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
                        "cpu_percent": cpu,
                        "memory": {"total": vm.total, "available": vm.available, "percent": vm.percent, "used": vm.used, "free": vm.free},
                        "disks": disks,
                    }
                except Exception as e:
                    return {"success": False, "error": str(e)}

            if name == "winops_process_list":
                if not PSUTIL_AVAILABLE:
                    return {"success": False, "error": "psutil not available"}
                limit = int(arguments.get("limit", 200))
                procs = []
                try:
                    for i, p in enumerate(psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'exe'])):
                        if i >= limit:
                            break
                        info = p.info
                        procs.append({
                            "pid": info.get("pid"),
                            "name": info.get("name"),
                            "user": info.get("username"),
                            "cpu": info.get("cpu_percent"),
                            "mem": info.get("memory_percent"),
                            "exe": info.get("exe"),
                        })
                    return {"success": True, "processes": procs, "count": len(procs), "limited": True}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            def _proc_by_pid(pid: int) -> psutil.Process:
                try:
                    return psutil.Process(int(pid))
                except psutil.NoSuchProcess:
                    raise RuntimeError(f"Process {pid} not found")
                except Exception as e:
                    raise RuntimeError(f"Invalid PID: {e}")

            if name == "winops_process_kill":
                if not PSUTIL_AVAILABLE:
                    return {"success": False, "error": "psutil not available"}
                pid = int(arguments["pid"])
                try:
                    _proc_by_pid(pid).kill()
                    return {"success": True, "pid": pid}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            if name == "winops_process_terminate":
                if not PSUTIL_AVAILABLE:
                    return {"success": False, "error": "psutil not available"}
                pid = int(arguments["pid"])
                try:
                    _proc_by_pid(pid).terminate()
                    return {"success": True, "pid": pid}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            if name == "winops_process_suspend":
                if not PSUTIL_AVAILABLE:
                    return {"success": False, "error": "psutil not available"}
                pid = int(arguments["pid"])
                try:
                    _proc_by_pid(pid).suspend()
                    return {"success": True, "pid": pid}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            if name == "winops_process_resume":
                if not PSUTIL_AVAILABLE:
                    return {"success": False, "error": "psutil not available"}
                pid = int(arguments["pid"])
                try:
                    _proc_by_pid(pid).resume()
                    return {"success": True, "pid": pid}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            if name == "winops_file_delete":
                from pathlib import Path
                import shutil
                p = Path(arguments["path"])
                if not p.exists():
                    return {"success": False, "error": "Path not found"}
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                return {"success": True, "path": str(p)}

            if name == "winops_file_mkdir":
                from pathlib import Path
                p = Path(arguments["path"])
                p.mkdir(parents=True, exist_ok=True)
                return {"success": True, "path": str(p)}

            if name == "winops_file_move":
                from pathlib import Path
                import shutil
                src = Path(arguments["src"])
                dst = Path(arguments["dst"])
                if not src.exists():
                    return {"success": False, "error": "Source not found"}
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                return {"success": True, "src": str(src), "dst": str(dst)}

            # Example handler for create_process
            if name == "winops_create_process":
                try:
                    pi = PROCESS_INFORMATION()
                    si = STARTUPINFO()
                    success = kernel32.CreateProcessW(
                        arguments.get("app_name"),
                        arguments["cmd_line"],
                        None, None, False, 0, None, None, byref(si), byref(pi)
                    )
                    return {"success": bool(success), "pid": pi.dwProcessId}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            # Example for open_process
            if name == "winops_open_process":
                try:
                    handle = kernel32.OpenProcess(
                        arguments.get("access", 0x1F0FFF),
                        False,
                        arguments["pid"]
                    )
                    return {"success": handle != 0, "handle": handle}
                except Exception as e:
                    return {"success": False, "error": str(e)}

            # ... Add handlers for all 225 functions similarly

            return {"success": False, "error": f"Unknown tool: {name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "error": str(e)}

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        client_info = params.get("clientInfo", {})
        name = client_info.get("name", "unknown").lower()
        if "copilot" in name:
            self.client_type = "vscode_copilot"
        elif "claude" in name:
            self.client_type = "claude_desktop"
        else:
            self.client_type = "generic_mcp"
        return {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "windows-operations", "version": "1.0.0"}}

    async def handle_list_tools(self) -> Dict[str, Any]:
        return {"tools": self.get_tools()}

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments", {})
        result = await self.execute_tool(name, arguments)
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}], "isError": not bool(result.get("success", False))}

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        if method == "initialize":
            return await self.handle_initialize(params)
        elif method == "tools/list":
            return await self.handle_list_tools()
        elif method == "tools/call":
            return await self.handle_call_tool(params)
        else:
            return {"error": {"code": -32601, "message": f"Method not found: {method}"}}

    async def run(self) -> None:
        logger.info("WINDOWS_OPERATIONS MCP starting... Ready for MCP requests")
        loop = asyncio.get_event_loop()
        while True:
            try:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                request = json.loads(line)
                req_id = request.get("id")
                if req_id is not None:
                    req_id = str(req_id)
                result = await self.handle_request(request)
                if "error" in result:
                    response = {"jsonrpc": "2.0", "id": req_id, "error": result["error"]}
                else:
                    response = {"jsonrpc": "2.0", "id": req_id, "result": result}
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
        logger.info("WINDOWS_OPERATIONS MCP shutting down")

async def main():
    kernel32.SetConsoleTitleW("WINDOWS_OPERATIONS_MCP")
    server = WinOpsMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
