#!/usr/bin/env python3
"""
DEVELOPER GATEWAY - MCP Gateway (GATEWAYS)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Consolidated MCP stdio gateway for developer operations
- Expose tools for code generation, API testing, and development tasks
- Integrate with GPU Inference Server

Discovery Hints:
- Type: MCP (stdio)
- Entry: stdio JSON-RPC server

Tools:
- devgw_health {}
- devgw_generate { prompt, model?, max_tokens? }
- devgw_code_assist { task, language? }
- devgw_api_test { endpoint, method?, data? }
"""

import sys
import json
import asyncio
import logging
from typing import Any, Dict

logger = logging.getLogger("DeveloperGatewayMCP")
logging.basicConfig(level=logging.INFO)

class DeveloperGatewayMCPServer:
    def __init__(self) -> None:
        self.client_type = "unknown"

    def get_tools(self):
        return [
            {"name": "devgw_health", "description": "Check Developer Gateway MCP health", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "devgw_generate", "description": "Generate code or text with AI", "inputSchema": {"type": "object", "properties": {"prompt": {"type": "string"}, "model": {"type": "string", "default": "google/gemini-flash-1.5-8b:free"}, "max_tokens": {"type": "number", "default": 2000}}, "required": ["prompt"]}},
            {"name": "devgw_code_assist", "description": "Get code assistance", "inputSchema": {"type": "object", "properties": {"task": {"type": "string"}, "language": {"type": "string", "default": "python"}}, "required": ["task"]}},
            {"name": "devgw_api_test", "description": "Test API endpoint", "inputSchema": {"type": "object", "properties": {"endpoint": {"type": "string"}, "method": {"type": "string", "default": "GET"}, "data": {"type": "object", "default": {}}}, "required": ["endpoint"]}},
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "devgw_health":
                return {"success": True, "service": "DEVELOPER_GATEWAY_MCP"}
            elif name == "devgw_generate":
                return {"success": True, "message": "Generate stub - integrate GPU inference", "prompt": arguments.get("prompt", "")}
            elif name == "devgw_code_assist":
                return {"success": True, "message": "Code assist stub", "task": arguments.get("task", "")}
            elif name == "devgw_api_test":
                return {"success": True, "message": "API test stub", "endpoint": arguments.get("endpoint", "")}
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "error": str(e)}

async def handle_jsonrpc(server: DeveloperGatewayMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")

    # CRITICAL FIX: Claude Desktop v0.14.4 has broken Zod validation for id field
    # Force all IDs to string to avoid union type validation bug
    if req_id is not None:
        req_id = str(req_id)

    if method == "initialize":
        server.client_type = params.get("clientInfo", {}).get("name", "unknown")
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "developer_gateway_mcp", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": server.get_tools()}}
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        result = await server.execute_tool(tool_name, tool_args)
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

async def main_loop():
    server = DeveloperGatewayMCPServer()
    logger.info("Developer Gateway MCP Server started (stdio)")

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
