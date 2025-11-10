#!/usr/bin/env python3
"""
MASTER_ORCHESTRATOR_HUB - MCP Gateway (GATEWAYS)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Consolidated MCP stdio gateway for LLM orchestration
- Expose tools for multi-model routing and defense
- Coordinate between different AI models and services

Discovery Hints:
- Type: MCP (stdio)
- Entry: stdio JSON-RPC server

Tools:
- masterorch_health {}
- masterorch_route { prompt, strategy? }
- masterorch_multi_query { prompt, models? }
- masterorch_consensus { task, models? }
"""

import sys
import json
import asyncio
import logging
from typing import Any, Dict

logger = logging.getLogger("MasterOrchestratorMCP")
logging.basicConfig(level=logging.INFO)

class MasterOrchestratorMCPServer:
    def __init__(self) -> None:
        self.client_type = "unknown"

    def get_tools(self):
        return [
            {"name": "masterorch_health", "description": "Check Master Orchestrator MCP health", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "masterorch_route", "description": "Route prompt to best model", "inputSchema": {"type": "object", "properties": {"prompt": {"type": "string"}, "strategy": {"type": "string", "default": "auto"}}, "required": ["prompt"]}},
            {"name": "masterorch_multi_query", "description": "Query multiple models", "inputSchema": {"type": "object", "properties": {"prompt": {"type": "string"}, "models": {"type": "array", "default": []}}, "required": ["prompt"]}},
            {"name": "masterorch_consensus", "description": "Get consensus from models", "inputSchema": {"type": "object", "properties": {"task": {"type": "string"}, "models": {"type": "array", "default": []}}, "required": ["task"]}},
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "masterorch_health":
                return {"success": True, "service": "MASTER_ORCHESTRATOR_HUB_MCP", "status": "routing_active"}
            elif name == "masterorch_route":
                return {"success": True, "message": "Route stub - model selection pending", "prompt": arguments.get("prompt", "")}
            elif name == "masterorch_multi_query":
                return {"success": True, "message": "Multi-query stub", "prompt": arguments.get("prompt", ""), "models_queried": 0}
            elif name == "masterorch_consensus":
                return {"success": True, "message": "Consensus stub", "task": arguments.get("task", ""), "agreement": "pending"}
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "error": str(e)}

async def handle_jsonrpc(server: MasterOrchestratorMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")
    
    # CRITICAL FIX: Claude Desktop v0.14.4 has broken Zod validation for id field
    # Force all IDs to string to avoid union type validation bug
    if req_id is not None:
        req_id = str(req_id)

    if method == "initialize":
        server.client_type = params.get("clientInfo", {}).get("name", "unknown")
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "master_orchestrator_hub_mcp", "version": "1.0.0"}}}
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
    server = MasterOrchestratorMCPServer()
    logger.info("Master Orchestrator Hub MCP Server started (stdio)")

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
