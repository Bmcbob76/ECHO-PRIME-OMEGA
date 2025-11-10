"""
VS Code API Gateway - MLS Gateway for VS Code Integration
Provides access to VS Code extension API capabilities
Manual MCP Protocol Implementation for Python 3.14 Compatibility
"""

import asyncio
import json
import sys
import http.client
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import shared utilities
try:
    from GATEWAYS.GS343_GATEWAY.utils.logging_config import setup_logger
    from GATEWAYS.GS343_GATEWAY.utils.debug_utils import DebugContext
except ImportError:
    def setup_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger
    class DebugContext:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

logger = setup_logger("VSCODE_GATEWAY")

# VS Code API endpoint
VSCODE_API_HOST = "localhost"
VSCODE_API_PORT = 3000

def call_vscode_api(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Call VS Code extension API"""
    try:
        conn = http.client.HTTPConnection(VSCODE_API_HOST, VSCODE_API_PORT, timeout=10)
        
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data) if data else None
        
        conn.request(method, endpoint, body=body, headers=headers)
        response = conn.getresponse()
        
        result = json.loads(response.read().decode())
        conn.close()
        
        return result
        
    except Exception as e:
        logger.error(f"VS Code API call failed: {e}")
        return {"error": str(e), "available": False}

class VSCodeGatewayMCPServer:
    def __init__(self) -> None:
        pass

    def get_tools(self):
        """List available VS Code tools"""
        return [
            {
                "name": "vscode_status",
                "description": "Check VS Code extension API status",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "vscode_get_workspace",
                "description": "Get current VS Code workspace information",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "vscode_get_files",
                "description": "List files in workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "Glob pattern (optional)"}
                    }
                }
            },
            {
                "name": "vscode_read_file",
                "description": "Read file content from VS Code workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Relative path in workspace"}
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "vscode_write_file",
                "description": "Write content to file in VS Code workspace",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Relative path in workspace"},
                        "content": {"type": "string", "description": "File content"}
                    },
                    "required": ["file_path", "content"]
                }
            },
            {
                "name": "vscode_execute_command",
                "description": "Execute VS Code command",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command ID"},
                        "args": {"type": "array", "description": "Command arguments (optional)"}
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "vscode_get_diagnostics",
                "description": "Get diagnostics (errors/warnings) for workspace",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "vscode_search",
                "description": "Search in workspace files",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "include_pattern": {"type": "string", "description": "Include pattern (optional)"},
                        "exclude_pattern": {"type": "string", "description": "Exclude pattern (optional)"}
                    },
                    "required": ["query"]
                }
            }
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        with DebugContext(f"Tool: {name}", logger):
            try:
                args = arguments or {}
                
                # Map tool names to endpoints
                endpoint_map = {
                    "vscode_status": ("/status", "GET"),
                    "vscode_get_workspace": ("/workspace", "GET"),
                    "vscode_get_files": ("/files", "POST"),
                    "vscode_read_file": ("/file/read", "POST"),
                    "vscode_write_file": ("/file/write", "POST"),
                    "vscode_execute_command": ("/command", "POST"),
                    "vscode_get_diagnostics": ("/diagnostics", "GET"),
                    "vscode_search": ("/search", "POST")
                }
                
                if name not in endpoint_map:
                    return {"success": False, "error": f"Unknown tool: {name}"}
                
                endpoint, method = endpoint_map[name]
                result = call_vscode_api(endpoint, method, args if method == "POST" else None)
                
                logger.info(f"Tool {name} executed successfully")
                
                return {
                    "success": True,
                    "content": json.dumps(result, indent=2)
                }
                
            except Exception as e:
                logger.error(f"Tool execution failed: {e}", exc_info=True)
                return {"success": False, "error": f"ERROR: {str(e)}"}

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05", 
            "capabilities": {"tools": {}}, 
            "serverInfo": {"name": "vscode-gateway", "version": "1.0.0"}
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
        logger.info("🔌 VS Code Gateway starting...")
        logger.info(f"Connecting to VS Code API at {VSCODE_API_HOST}:{VSCODE_API_PORT}")
        
        # Test connection
        try:
            status = call_vscode_api("/status")
            logger.info(f"VS Code API status: {status}")
        except Exception as e:
            logger.warning(f"Could not connect to VS Code API: {e}")
            logger.info("Make sure VS Code extension is running")
        
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
    server = VSCodeGatewayMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)
