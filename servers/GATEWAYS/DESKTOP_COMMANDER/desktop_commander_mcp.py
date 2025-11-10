"""
Desktop Commander MCP Server
Authority Level: 11.0
GS343 Foundation + Phoenix Auto-Heal Integrated
Complete filesystem and system control
Manual MCP Protocol Implementation for Python 3.14 Compatibility
"""

import asyncio
import json
import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

class DesktopCommanderMCPServer:
    def __init__(self) -> None:
        # Initialize GS343
        if GS343_AVAILABLE:
            self.foundation = GS343UniversalFoundation()
            self.healer = PhoenixAutoHeal()
        else:
            self.foundation = None
            self.healer = None

    def get_tools(self):
        """List available Desktop Commander tools"""
        return [
            {
                "name": "read_file",
                "description": "Read file contents from any drive",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Full file path"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                        "mode": {"type": "string", "enum": ["write", "append"], "default": "write"}
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "list_directory",
                "description": "List directory contents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "execute_command",
                "description": "Execute system command",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"},
                        "shell": {"type": "string", "default": "powershell"}
                    },
                    "required": ["command"]
                }
            },
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        try:
            if name == "read_file":
                path = arguments.get("path")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"success": True, "content": content}
            
            elif name == "write_file":
                path = arguments.get("path")
                content = arguments.get("content")
                mode = arguments.get("mode", "write")
                
                file_mode = 'a' if mode == "append" else 'w'
                with open(path, file_mode, encoding='utf-8') as f:
                    f.write(content)
                return {"success": True, "message": f"File written: {path}"}
            
            elif name == "list_directory":
                path = arguments.get("path")
                items = []
                for item in Path(path).iterdir():
                    prefix = "[DIR]" if item.is_dir() else "[FILE]"
                    items.append(f"{prefix} {item.name}")
                return {"success": True, "content": "\n".join(items)}
            
            elif name == "execute_command":
                command = arguments.get("command")
                shell = arguments.get("shell", "powershell")
                
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    executable=shell if shell != "powershell" else "powershell.exe"
                )
                output = result.stdout if result.returncode == 0 else result.stderr
                return {"success": True, "content": output}
            
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
        
        except Exception as e:
            return {"success": False, "error": f"Error: {str(e)}"}

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05", 
            "capabilities": {"tools": {}}, 
            "serverInfo": {"name": "desktop-commander", "version": "1.0.0"}
        }

    async def handle_list_tools(self) -> Dict[str, Any]:
        return {"tools": self.get_tools()}

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments", {})
        result = await self.execute_tool(name, arguments)
        
        if result.get("success"):
            return {
                "content": [{"type": "text", "text": result.get("content", result.get("message", "Success"))}],
                "isError": False
            }
        else:
            return {
                "content": [{"type": "text", "text": result.get("error", "Unknown error")}],
                "isError": True
            }

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
        """Main MCP server loop"""
        loop = asyncio.get_event_loop()
        while True:
            try:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                request = json.loads(line)
                result = await self.handle_request(request)
                
                if "error" in result:
                    response = {"jsonrpc": "2.0", "id": request.get("id"), "error": result["error"]}
                else:
                    response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
                
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                # Invalid JSON, send error response
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                # General error handling
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

async def main():
    server = DesktopCommanderMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)
