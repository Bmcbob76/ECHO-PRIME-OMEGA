#!/usr/bin/env python3
"""
OMEGA SWARM BRAIN MCP GATEWAY
MCP Server exposing OMEGA Swarm Brain functionality to Claude
Manual MCP Protocol Implementation for Python 3.14 Compatibility
"""

import sys
import os
sys.path.insert(0, r'P:\ECHO_PRIME\OMEGA_SWARM_BRAIN')

import asyncio
import json
from typing import Any, Dict, Optional
from datetime import datetime

# OMEGA imports
try:
    from omega_core import OmegaCore
    OMEGA_AVAILABLE = True
except ImportError as e:
    OMEGA_AVAILABLE = False

class OmegaSwarmBrainMCPServer:
    def __init__(self) -> None:
        self.omega_instance: Optional[OmegaCore] = None

    def get_tools(self):
        """List available OMEGA tools"""
        return [
            {
                "name": "omega_health",
                "description": "Check OMEGA Swarm Brain health status",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "omega_status",
                "description": "Get comprehensive OMEGA system status including agents, trinity, guilds",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "omega_list_agents",
                "description": "List all active agents in the swarm",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "omega_swarm_metrics",
                "description": "Get swarm intelligence metrics and performance data",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "omega_trinity_query",
                "description": "Query Trinity consciousness (SAGE, THORNE, NYX)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query for Trinity consciousness"
                        },
                        "mode": {
                            "type": "string",
                            "description": "Trinity mode: fused, sage, thorne, nyx",
                            "default": "fused"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "omega_submit_task",
                "description": "Submit task to swarm intelligence",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_type": {
                            "type": "string",
                            "description": "Type of task"
                        },
                        "task_data": {
                            "type": "object",
                            "description": "Task data/parameters"
                        },
                        "priority": {
                            "type": "number",
                            "description": "Task priority 1-10",
                            "default": 5
                        },
                        "guild": {
                            "type": "string",
                            "description": "Target guild (optional)"
                        }
                    },
                    "required": ["task_type", "task_data"]
                }
            },
            {
                "name": "omega_guild_status",
                "description": "Get status of a specific guild",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "guild_name": {
                            "type": "string",
                            "description": "Name of the guild"
                        }
                    },
                    "required": ["guild_name"]
                }
            },
            {
                "name": "omega_memory_stats",
                "description": "Get memory orchestrator statistics",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

    async def initialize_omega(self):
        """Initialize OMEGA instance if needed"""
        if not self.omega_instance and OMEGA_AVAILABLE:
            try:
                self.omega_instance = OmegaCore()
                await self.omega_instance.initialize()
            except Exception as e:
                return {"success": False, "error": f"OMEGA initialization failed: {str(e)}"}
        return {"success": True}

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        
        # Initialize OMEGA if needed
        if name not in ["omega_health"]:
            init_result = await self.initialize_omega()
            if not init_result["success"]:
                return init_result

        try:
            # Health check
            if name == "omega_health":
                return {
                    "success": True,
                    "content": json.dumps({
                        "status": "online",
                        "service": "OMEGA Swarm Brain",
                        "omega_available": OMEGA_AVAILABLE,
                        "timestamp": datetime.now().isoformat()
                    }, indent=2)
                }
            
            # Status
            elif name == "omega_status":
                status = {
                    "online": True,
                    "total_agents": self.omega_instance.agent_manager.get_agent_count(),
                    "max_agents": self.omega_instance.config.get('max_agents', 1200),
                    "trinity_harmony": self.omega_instance.trinity.get_harmony_level(),
                    "guilds": self.omega_instance.guild_system.get_guild_status(),
                    "timestamp": datetime.now().isoformat()
                }
                return {"success": True, "content": json.dumps(status, indent=2)}
            
            # List agents
            elif name == "omega_list_agents":
                agents = self.omega_instance.agent_manager.list_agents()
                return {
                    "success": True,
                    "content": json.dumps({"agents": agents, "count": len(agents)}, indent=2)
                }
            
            # Swarm metrics
            elif name == "omega_swarm_metrics":
                metrics = self.omega_instance.swarm.get_swarm_metrics()
                return {"success": True, "content": json.dumps(metrics, indent=2)}
            
            # Trinity query
            elif name == "omega_trinity_query":
                args = arguments or {}
                query = args.get("query", "")
                mode = args.get("mode", "fused")
                
                if mode == "fused":
                    response = await self.omega_instance.trinity.fused_response(query)
                elif mode == "sage":
                    response = await self.omega_instance.trinity.sage_response(query)
                elif mode == "thorne":
                    response = await self.omega_instance.trinity.thorne_response(query)
                elif mode == "nyx":
                    response = await self.omega_instance.trinity.nyx_response(query)
                else:
                    return {"success": False, "error": f"Invalid mode: {mode}"}
                
                result = {
                    "mode": mode,
                    "response": response,
                    "harmony": self.omega_instance.trinity.get_harmony_level()
                }
                return {"success": True, "content": json.dumps(result, indent=2)}
            
            # Submit task
            elif name == "omega_submit_task":
                args = arguments or {}
                task_id = await self.omega_instance.swarm.submit_task(
                    task_type=args.get("task_type"),
                    task_data=args.get("task_data", {}),
                    priority=args.get("priority", 5),
                    guild=args.get("guild")
                )
                
                return {
                    "success": True,
                    "content": json.dumps({"success": True, "task_id": task_id}, indent=2)
                }
            
            # Guild status
            elif name == "omega_guild_status":
                args = arguments or {}
                guild_name = args.get("guild_name", "")
                status = self.omega_instance.guild_system.get_guild_status(guild_name)
                return {"success": True, "content": json.dumps(status, indent=2)}
            
            # Memory stats
            elif name == "omega_memory_stats":
                stats = self.omega_instance.memory.get_stats()
                return {"success": True, "content": json.dumps(stats, indent=2)}
            
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
                
        except Exception as e:
            return {"success": False, "error": f"Error: {str(e)}"}

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05", 
            "capabilities": {"tools": {}}, 
            "serverInfo": {"name": "omega-swarm-brain", "version": "1.0.0"}
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
    server = OmegaSwarmBrainMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)
