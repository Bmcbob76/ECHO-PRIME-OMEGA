"""MCP Filesystem Server"""
import asyncio

# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore', message='pkg_resources is deprecated')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic._internal._typing_extra')
import json
from pathlib import Path
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("filesystem")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="read_file", description="Read file contents",
                  inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        types.Tool(name="write_file", description="Write content to file",
                  inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}),
        types.Tool(name="list_directory", description="List directory contents",
                  inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]})
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    try:
        if name == "read_file":
            path = Path(arguments["path"])
            content = path.read_text(encoding='utf-8')
            return [types.TextContent(type="text", text=content)]
        elif name == "write_file":
            path = Path(arguments["path"])
            path.write_text(arguments["content"], encoding='utf-8')
            return [types.TextContent(type="text", text=f"✅ Wrote {len(arguments['content'])} bytes to {path}")]
        elif name == "list_directory":
            path = Path(arguments["path"])
            items = [str(p.name) for p in path.iterdir()]
            return [types.TextContent(type="text", text=json.dumps(items, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ Error: {str(e)}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="filesystem", server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}))
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    print("🚀 MCP Filesystem Server (Port 8001)")
    asyncio.run(main())
