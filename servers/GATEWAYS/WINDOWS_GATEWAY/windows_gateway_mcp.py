#!/usr/bin/env python3
"""
WINDOWS_GATEWAY - MCP Gateway (GATEWAYS)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Consolidated MCP stdio gateway for Windows operations
- Process management and monitoring
- System information and diagnostics
- Registry and Windows-specific operations

Discovery Hints:
- Type: MCP (stdio)
- Entry: stdio JSON-RPC server

Tools:
- wingw_health {}
- wingw_system_info {}
- wingw_process_list {}
- wingw_process_kill { pid }
"""

import sys
import json
import asyncio
import logging
import platform
from typing import Any, Dict

logger = logging.getLogger("WindowsGatewayMCP")
logging.basicConfig(level=logging.INFO)

class WindowsGatewayMCPServer:
    def __init__(self) -> None:
        self.client_type = "unknown"

    def get_tools(self):
        return [
            {"name": "wingw_health", "description": "Check Windows Gateway MCP health", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "wingw_system_info", "description": "Get Windows system information", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "wingw_process_list", "description": "List Windows processes", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "wingw_process_kill", "description": "Kill Windows process", "inputSchema": {"type": "object", "properties": {"pid": {"type": "number"}}, "required": ["pid"]}},
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "wingw_health":
                return {"success": True, "service": "WINDOWS_GATEWAY_MCP", "platform": platform.system()}
            elif name == "wingw_system_info":
                return {"success": True, "platform": platform.system(), "release": platform.release(), "version": platform.version(), "machine": platform.machine(), "processor": platform.processor()}
            elif name == "wingw_process_list":
                return {"success": True, "message": "Process list stub", "processes": []}
            elif name == "wingw_process_kill":
                return {"success": True, "message": "Kill stub", "pid": arguments.get("pid", 0), "killed": False}
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "error": str(e)}

async def handle_jsonrpc(server: WindowsGatewayMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")

    # CRITICAL FIX: Claude Desktop v0.14.4 Zod validation strictness
    # 1. Always coerce id to string (never null/undefined)
    # 2. Ensure method is always string
    # 3. Provide default empty objects for all optional fields
    if req_id is None:
        req_id = "0"  # Default ID instead of null
    else:
        req_id = str(req_id)
    
    if not method:
        method = "unknown"  # Default method instead of undefined
    
    # Ensure params is always an object
    if not isinstance(params, dict):
        params = {}

    if method == "initialize":
        server.client_type = params.get("clientInfo", {}).get("name", "unknown")
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "windows_gateway_mcp", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": server.get_tools()}
        }
    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        result = await server.execute_tool(tool_name, tool_args)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
            }
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        }

async def main_loop():
    server = WindowsGatewayMCPServer()
    logger.info("Windows Gateway MCP Server started (stdio)")

    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            request = json.loads(line.strip())
            response = await handle_jsonrpc(server, request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
