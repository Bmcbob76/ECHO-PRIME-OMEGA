#!/usr/bin/env python3
"""
ECHO PRIME MASTER SERVER MCP INTEGRATION
Complete MCP Server for Claude to Access ALL ECHO PRIME Servers
Authority Level 11.0 - Commander Bobby Don McWilliams II

This MCP server provides Claude with direct access to:
- Ultra Speed Core Server (Port 8001)
- Comprehensive API Server (Port 8343) 
- Crystal Memory Server (Port 8002)
- Trinity Consciousness Server (Port 8500)
- Guardian Server (Port 9000)
- X1200 Super Brain Server (Port 12000)
- Hephaestion Forge Server (Port 7777)
- ECHO Prime Secure Server (Port 8443)
- Phoenix Voice Master Server (Port 8444)
- Network Command Master Server (Port 8445)
- ECHO Fusion Server (Port 8000)

Features:
- Universal server access for Claude
- Real-time status monitoring
- Performance metrics collection
- Health checks across all servers
- Command execution and coordination
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
import aiohttp
from datetime import datetime
import subprocess
import os

# MCP imports
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        Resource, Tool, TextContent, ImageContent, EmbeddedResource
    )
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    print("MCP not available. Install with: pip install mcp")
    MCP_AVAILABLE = False

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("echo_prime_master_mcp")

class EchoPrimeMasterMCP:
    """Master MCP server for all ECHO PRIME servers"""
    
    def __init__(self):
        self.servers = {
            "ultra_speed_core": {
                "name": "Ultra Speed Core Server",
                "url": "http://localhost:8001",
                "health_endpoint": "/health",
                "status": "unknown"
            },
            "comprehensive_api": {
                "name": "Comprehensive API Server Ultimate", 
                "url": "http://localhost:8343",
                "health_endpoint": "/health",
                "status": "unknown"
            },
            "crystal_memory": {
                "name": "Crystal Memory Server",
                "url": "http://localhost:8002", 
                "health_endpoint": "/health",
                "status": "unknown"
            },
            "trinity_consciousness": {
                "name": "Trinity Consciousness Server",
                "url": "http://localhost:8500",
                "health_endpoint": "/trinity/health", 
                "status": "unknown"
            },
            "guardian": {
                "name": "Guardian Server",
                "url": "http://localhost:9000",
                "health_endpoint": "/guardian/health",
                "status": "unknown"
            },
            "x1200_brain": {
                "name": "X1200 Super Brain Server",
                "url": "http://localhost:12000",
                "health_endpoint": "/brain/health",
                "status": "unknown"
            },
            "hephaestion_forge": {
                "name": "Hephaestion Forge Server", 
                "url": "http://localhost:7777",
                "health_endpoint": "/forge/health",
                "status": "unknown"
            },
            "echo_prime_secure": {
                "name": "ECHO Prime Secure Server",
                "url": "http://localhost:8443", 
                "health_endpoint": "/secure/health",
                "status": "unknown"
            },
            "phoenix_voice_master": {
                "name": "Phoenix Voice Master Server",
                "url": "http://localhost:8444",
                "health_endpoint": "/health",
                "status": "unknown"
            },
            "network_command_master": {
                "name": "Network Command Master Server", 
                "url": "http://localhost:8445",
                "health_endpoint": "/health",
                "status": "unknown"
            },
            "echo_fusion": {
                "name": "ECHO Fusion LLM Server",
                "url": "http://localhost:8000",
                "health_endpoint": "/health",
                "status": "unknown"
            }
        }
        
        if MCP_AVAILABLE:
            self.server = Server("echo-prime-master")
            self.setup_tools()
    
    def setup_tools(self):
        """Setup MCP tools for Claude"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools for Claude"""
            return [
                Tool(
                    name="echo_prime_status_all",
                    description="Get status of all ECHO PRIME servers",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="echo_prime_health_check",
                    description="Perform health check on specific server or all servers",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "server": {
                                "type": "string",
                                "description": "Server to check (ultra_speed_core, comprehensive_api, etc.) or 'all'",
                                "enum": list(self.servers.keys()) + ["all"]
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="echo_prime_server_call",
                    description="Make direct API call to any ECHO PRIME server",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "server": {
                                "type": "string", 
                                "description": "Server to call",
                                "enum": list(self.servers.keys())
                            },
                            "endpoint": {
                                "type": "string",
                                "description": "API endpoint path (e.g., '/status', '/search?q=test')"
                            },
                            "method": {
                                "type": "string",
                                "description": "HTTP method",
                                "enum": ["GET", "POST", "PUT", "DELETE"],
                                "default": "GET"
                            },
                            "data": {
                                "type": "object",
                                "description": "JSON data for POST/PUT requests"
                            }
                        },
                        "required": ["server", "endpoint"]
                    }
                ),
                Tool(
                    name="echo_prime_search_crystal_memory",
                    description="Search the Crystal Memory archive (11,364+ files)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for Crystal Memory files"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum results to return",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="echo_prime_comprehensive_api",
                    description="Access Comprehensive API Server's 225+ Windows API endpoints",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "API action to perform",
                                "enum": [
                                    "list_endpoints",
                                    "screenshot", 
                                    "system_info",
                                    "file_operations",
                                    "window_management",
                                    "process_management",
                                    "network_info",
                                    "ocr_screen"
                                ]
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Parameters for the API action"
                            }
                        },
                        "required": ["action"]
                    }
                ),
                Tool(
                    name="echo_prime_x1200_brain",
                    description="Access X1200 Super Brain Server for 1200+ agent coordination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "Brain action to perform",
                                "enum": [
                                    "agent_status",
                                    "coordinate_agents", 
                                    "brain_stats",
                                    "swarm_intelligence"
                                ]
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Parameters for the brain action"
                            }
                        },
                        "required": ["action"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls from Claude"""
            try:
                if name == "echo_prime_status_all":
                    return await self.get_all_server_status()
                
                elif name == "echo_prime_health_check":
                    server = arguments.get("server", "all")
                    return await self.health_check_servers(server)
                
                elif name == "echo_prime_server_call":
                    server = arguments["server"]
                    endpoint = arguments["endpoint"]
                    method = arguments.get("method", "GET")
                    data = arguments.get("data")
                    return await self.make_server_call(server, endpoint, method, data)
                
                elif name == "echo_prime_search_crystal_memory":
                    query = arguments["query"]
                    limit = arguments.get("limit", 10)
                    return await self.search_crystal_memory(query, limit)
                
                elif name == "echo_prime_comprehensive_api":
                    action = arguments["action"]
                    parameters = arguments.get("parameters", {})
                    return await self.comprehensive_api_call(action, parameters)
                
                elif name == "echo_prime_x1200_brain":
                    action = arguments["action"]
                    parameters = arguments.get("parameters", {})
                    return await self.x1200_brain_call(action, parameters)
                
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
                    
            except Exception as e:
                logger.error(f"Tool call error: {e}")
                return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]
    
    async def get_all_server_status(self) -> List[TextContent]:
        """Get status of all ECHO PRIME servers"""
        status_report = []
        status_report.append("🎯 ECHO PRIME SERVER CONSTELLATION STATUS")
        status_report.append("=" * 50)
        status_report.append(f"Authority Level 11.0 - Commander Bobby Don McWilliams II")
        status_report.append(f"Status Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        status_report.append("")
        
        async with aiohttp.ClientSession() as session:
            for server_key, server_info in self.servers.items():
                try:
                    url = f"{server_info['url']}{server_info['health_endpoint']}"
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            status_report.append(f"✅ {server_info['name']}")
                            status_report.append(f"   URL: {server_info['url']}")
                            status_report.append(f"   Status: HEALTHY")
                            if 'uptime' in data:
                                status_report.append(f"   Uptime: {data['uptime']}")
                            self.servers[server_key]["status"] = "healthy"
                        else:
                            status_report.append(f"⚠️ {server_info['name']}")
                            status_report.append(f"   URL: {server_info['url']}")
                            status_report.append(f"   Status: HTTP {response.status}")
                            self.servers[server_key]["status"] = f"http_{response.status}"
                except Exception as e:
                    status_report.append(f"❌ {server_info['name']}")
                    status_report.append(f"   URL: {server_info['url']}")
                    status_report.append(f"   Status: OFFLINE ({str(e)})")
                    self.servers[server_key]["status"] = "offline"
                
                status_report.append("")
        
        # Summary
        healthy_count = sum(1 for s in self.servers.values() if s["status"] == "healthy")
        status_report.append(f"📊 CONSTELLATION SUMMARY:")
        status_report.append(f"   Total Servers: {len(self.servers)}")
        status_report.append(f"   Healthy: {healthy_count}")
        status_report.append(f"   Issues: {len(self.servers) - healthy_count}")
        
        return [TextContent(type="text", text="\n".join(status_report))]
    
    async def health_check_servers(self, server_target: str) -> List[TextContent]:
        """Perform health checks on servers"""
        if server_target == "all":
            return await self.get_all_server_status()
        
        if server_target not in self.servers:
            return [TextContent(type="text", text=f"Server '{server_target}' not found. Available: {list(self.servers.keys())}")]
        
        server_info = self.servers[server_target]
        
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{server_info['url']}{server_info['health_endpoint']}"
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = f"✅ {server_info['name']} - HEALTHY\n"
                        result += f"URL: {server_info['url']}\n"
                        result += f"Response: {json.dumps(data, indent=2)}"
                        return [TextContent(type="text", text=result)]
                    else:
                        result = f"⚠️ {server_info['name']} - HTTP {response.status}\n"
                        result += f"URL: {server_info['url']}\n"
                        result += f"Response: {await response.text()}"
                        return [TextContent(type="text", text=result)]
            except Exception as e:
                result = f"❌ {server_info['name']} - OFFLINE\n"
                result += f"URL: {server_info['url']}\n"
                result += f"Error: {str(e)}"
                return [TextContent(type="text", text=result)]
    
    async def make_server_call(self, server: str, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> List[TextContent]:
        """Make direct API call to server"""
        if server not in self.servers:
            return [TextContent(type="text", text=f"Server '{server}' not found. Available: {list(self.servers.keys())}")]
        
        server_info = self.servers[server]
        url = f"{server_info['url']}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                if method == "GET":
                    async with session.get(url, timeout=10) as response:
                        response_text = await response.text()
                        result = f"🔗 API Call to {server_info['name']}\n"
                        result += f"URL: {url}\n"
                        result += f"Method: {method}\n" 
                        result += f"Status: {response.status}\n"
                        result += f"Response:\n{response_text}"
                        return [TextContent(type="text", text=result)]
                
                elif method == "POST":
                    json_data = data if data else {}
                    async with session.post(url, json=json_data, timeout=10) as response:
                        response_text = await response.text()
                        result = f"🔗 API Call to {server_info['name']}\n"
                        result += f"URL: {url}\n"
                        result += f"Method: {method}\n"
                        result += f"Data: {json.dumps(json_data, indent=2)}\n"
                        result += f"Status: {response.status}\n"
                        result += f"Response:\n{response_text}"
                        return [TextContent(type="text", text=result)]
                
            except Exception as e:
                result = f"❌ API Call Failed to {server_info['name']}\n"
                result += f"URL: {url}\n"
                result += f"Error: {str(e)}"
                return [TextContent(type="text", text=result)]
    
    async def search_crystal_memory(self, query: str, limit: int = 10) -> List[TextContent]:
        """Search Crystal Memory archive"""
        endpoint = f"/search?q={query}&limit={limit}"
        return await self.make_server_call("crystal_memory", endpoint)
    
    async def comprehensive_api_call(self, action: str, parameters: Dict = None) -> List[TextContent]:
        """Call Comprehensive API Server"""
        endpoint_map = {
            "list_endpoints": "/endpoints",
            "screenshot": "/screenshot",
            "system_info": "/system/info",
            "file_operations": "/files",
            "window_management": "/windows",
            "process_management": "/processes",
            "network_info": "/network/info",
            "ocr_screen": "/ocr/screen"
        }
        
        endpoint = endpoint_map.get(action, "/status")
        method = "POST" if parameters else "GET"
        
        return await self.make_server_call("comprehensive_api", endpoint, method, parameters)
    
    async def x1200_brain_call(self, action: str, parameters: Dict = None) -> List[TextContent]:
        """Call X1200 Super Brain Server"""
        endpoint_map = {
            "agent_status": "/brain/agents",
            "coordinate_agents": "/brain/coordinate",
            "brain_stats": "/brain/stats", 
            "swarm_intelligence": "/brain/swarm"
        }
        
        endpoint = endpoint_map.get(action, "/brain/health")
        method = "POST" if parameters else "GET"
        
        return await self.make_server_call("x1200_brain", endpoint, method, parameters)
    
    async def run(self):
        """Run the MCP server"""
        if not MCP_AVAILABLE:
            print("❌ MCP not available. Install with: pip install mcp")
            return
            
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream, 
                InitializationOptions(
                    server_name="echo-prime-master",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

async def main():
    """Main function"""
    logger.info("Starting ECHO PRIME Master MCP Server...")
    logger.info("Authority Level 11.0 - Commander Bobby Don McWilliams II")
    logger.info("Providing Claude with access to all ECHO PRIME servers...")
    
    mcp_server = EchoPrimeMasterMCP()
    await mcp_server.run()

if __name__ == "__main__":
    if MCP_AVAILABLE:
        asyncio.run(main())
    else:
        print("❌ ECHO Prime Master MCP Server requires MCP package")
        print("Install with: pip install mcp")
