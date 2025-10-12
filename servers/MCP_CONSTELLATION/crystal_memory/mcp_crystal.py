"""MCP crystal Server - REAL Crystal Memory Access"""
import asyncio
import os
import json
from pathlib import Path

# Suppress deprecation warnings
import warnings
warnings.filterwarnings('ignore', message='pkg_resources is deprecated')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic._internal._typing_extra')
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("crystal")

# Crystal memory base path
CRYSTAL_BASE = Path("M:/MASTER_EKM")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_crystals",
            description="Search crystal memory by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "number", "default": 5}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="read_crystal",
            description="Read specific crystal file",
            inputSchema={
                "type": "object",
                "properties": {
                    "crystal_path": {"type": "string", "description": "Path to crystal file"}
                },
                "required": ["crystal_path"]
            }
        ),
        types.Tool(
            name="save_crystal",
            description="Save new crystal memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Crystal name"},
                    "content": {"type": "string", "description": "Crystal content"},
                    "category": {"type": "string", "description": "Category folder", "default": "general"}
                },
                "required": ["name", "content"]
            }
        ),
        types.Tool(
            name="list_crystals",
            description="List all available crystals",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Filter by category"}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}
    
    if name == "search_crystals":
        query = args.get("query", "").lower()
        max_results = args.get("max_results", 5)
        results = []
        
        for root, dirs, files in os.walk(CRYSTAL_BASE):
            for file in files:
                if file.endswith(('.md', '.txt', '.json')):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if query in content.lower() or query in file.lower():
                            results.append(f"📍 {file_path}\n{content[:200]}...\n")
                            if len(results) >= max_results:
                                break
                    except: pass
            if len(results) >= max_results: break
        
        return [types.TextContent(type="text", text=f"🔍 Found {len(results)} crystals:\n\n" + "\n---\n".join(results) if results else "❌ No crystals found")]
    
    elif name == "read_crystal":
        crystal_path = Path(args.get("crystal_path", ""))
        try:
            content = crystal_path.read_text(encoding='utf-8')
            return [types.TextContent(type="text", text=f"💎 {crystal_path.name}\n\n{content}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"❌ Error reading crystal: {e}")]
    
    elif name == "save_crystal":
        name = args.get("name", "")
        content = args.get("content", "")
        category = args.get("category", "general")
        
        category_path = CRYSTAL_BASE / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        crystal_path = category_path / f"{name}.md"
        crystal_path.write_text(content, encoding='utf-8')
        
        return [types.TextContent(type="text", text=f"✅ Crystal saved: {crystal_path}")]
    
    elif name == "list_crystals":
        category = args.get("category")
        search_path = CRYSTAL_BASE / category if category else CRYSTAL_BASE
        
        crystals = []
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.endswith(('.md', '.txt', '.json')):
                    rel_path = Path(root).relative_to(CRYSTAL_BASE) / file
                    crystals.append(str(rel_path))
        
        return [types.TextContent(type="text", text=f"💎 {len(crystals)} crystals:\n" + "\n".join(crystals[:50]))]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="crystal", server_version="2.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}))
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    print("🚀 MCP CRYSTAL Server v2.0 - REAL Memory Access (Port 8004)")
    asyncio.run(main())
