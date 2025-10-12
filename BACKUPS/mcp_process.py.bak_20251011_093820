"""MCP process Server - Process management"""
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("process")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="ping", description="Ping the process server",
                  inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="status", description="Get process server status",
                  inputSchema={"type": "object", "properties": {}})
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name == "ping":
        return [types.TextContent(type="text", text="✅ Pong from process")]
    elif name == "status":
        return [types.TextContent(type="text", text="✅ process operational on port 8003")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="process", server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}))
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    print("🚀 MCP PROCESS Server (Port 8003)")
    asyncio.run(main())
