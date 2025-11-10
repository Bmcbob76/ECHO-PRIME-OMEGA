"""
VS Code API MCP Server
Authority Level: 11.0
GS343 Foundation + Phoenix Auto-Heal Integrated
Direct VS Code programmatic control
Manual MCP Protocol Implementation for Python 3.14 Compatibility
"""

import asyncio
import json
import sys
import httpx
from typing import Any, Dict, List, Optional

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

# VS Code API endpoint
VSCODE_API_BASE = "http://localhost:9001"

class VSCodeApiMCPServer:
    def __init__(self) -> None:
        # Initialize GS343
        if GS343_AVAILABLE:
            self.foundation = GS343UniversalFoundation()
            self.healer = PhoenixAutoHeal()
        else:
            self.foundation = None
            self.healer = None

    def get_tools(self):
        """List available VS Code API tools"""
        return [
            {
                "name": "vscode_open_file",
                "description": "Open file in VS Code editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "line": {"type": "number"},
                        "column": {"type": "number"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "vscode_edit_file",
                "description": "Edit file in VS Code",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "vscode_run_command",
                "description": "Execute VS Code command",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"},
                        "args": {"type": "object"}
                    },
                    "required": ["command"]
                }
            },
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        
        try:
            async with httpx.AsyncClient() as client:
                if name == "vscode_open_file":
                    resp = await client.post(
                        f"{VSCODE_API_BASE}/file/open",
                        json=arguments,
                        timeout=10.0
                    )
                    result = resp.json()
                    return {"success": True, "content": json.dumps(result, indent=2)}
                
                elif name == "vscode_edit_file":
                    resp = await client.post(
                        f"{VSCODE_API_BASE}/file/edit",
                        json=arguments,
                        timeout=10.0
                    )
                    result = resp.json()
                    return {"success": True, "content": json.dumps(result, indent=2)}
                
                elif name == "vscode_run_command":
                    resp = await client.post(
                        f"{VSCODE_API_BASE}/command/execute",
                        json=arguments,
                        timeout=30.0
                    )
                    result = resp.json()
                    return {"success": True, "content": json.dumps(result, indent=2)}
                
                else:
                    return {"success": False, "error": f"Unknown tool: {name}"}
        
        except Exception as e:
            return {"success": False, "error": f"Error: {str(e)}"}

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05", 
            "capabilities": {"tools": {}}, 
            "serverInfo": {"name": "vscode-api", "version": "1.0.0"}
        }

    async def handle_list_tools(self) -> Dict[str, Any]:
        return {"tools": self.get_tools()}

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments", {})
        result = await self.execute_tool(name, arguments)
        
        if result.get("success"):
            return {
                "content": [{"type": "text", "text": result.get("content", "Success")}],
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
    server = VSCodeApiMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)
