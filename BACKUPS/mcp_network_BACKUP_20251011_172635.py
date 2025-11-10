"""MCP network Server - Network operations"""
import asyncio

# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore', message='pkg_resources is deprecated')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic._internal._typing_extra')
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("network")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="ping", description="Ping the network server",
                  inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="status", description="Get network server status",
                  inputSchema={"type": "object", "properties": {}})
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name == "ping":
        return [types.TextContent(type="text", text="✅ Pong from network")]
    elif name == "status":
        return [types.TextContent(type="text", text="✅ network operational on port 8007")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="network", server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}))
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    print("🚀 MCP NETWORK Server (Port 8007)")
    asyncio.run(main())
