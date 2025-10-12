"""MCP Orchestrator Server"""
import asyncio

# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore', message='pkg_resources is deprecated')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic._internal._typing_extra')
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("orchestrator")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="health_check", description="Check orchestrator health",
                  inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="list_servers", description="List all registered servers",
                  inputSchema={"type": "object", "properties": {}})
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name == "health_check":
        return [types.TextContent(type="text", text="✅ Orchestrator healthy")]
    elif name == "list_servers":
        servers = ["filesystem", "windows", "process", "crystal", "workflow", "voice", "network", "healing"]
        return [types.TextContent(type="text", text=f"Servers: {', '.join(servers)}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="orchestrator", server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}))
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    print("🚀 MCP Orchestrator Server (Port 8000)")
    asyncio.run(main())
