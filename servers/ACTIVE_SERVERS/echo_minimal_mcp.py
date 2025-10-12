#!/usr/bin/env python3
"""
ECHO Minimal MCP Server
Bulletproof stdio-based MCP server for GitHub Copilot integration
Commander Bobby Don McWilliams II - Authority Level 11.0
"""

import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Create server instance
server = Server("echo-minimal")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="echo_test",
            description="Test tool that echoes back input - confirms MCP is working",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to echo back"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="execute_command",
            description="Execute a PowerShell command and return output",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "PowerShell command to execute"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="read_file_content",
            description="Read the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Full path to the file to read"
                    }
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "echo_test":
        message = arguments.get("message", "")
        return [TextContent(
            type="text",
            text=f"🔥 ECHO MCP Server Active! Message received: {message}"
        )]
    
    elif name == "execute_command":
        command = arguments.get("command", "")
        try:
            import subprocess
            result = subprocess.run(
                ["powershell.exe", "-Command", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout if result.stdout else result.stderr
            return [TextContent(
                type="text",
                text=f"Command: {command}\n\nOutput:\n{output}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error executing command: {str(e)}"
            )]
    
    elif name == "read_file_content":
        path = arguments.get("path", "")
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return [TextContent(
                type="text",
                text=f"File: {path}\n\nContent:\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error reading file: {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"❌ Unknown tool: {name}"
        )]

async def main():
    """Main entry point for MCP server"""
    print("🚀 ECHO Minimal MCP Server Starting...", file=sys.stderr, flush=True)
    print("⚡ Commander Bobby Don McWilliams II - Authority Level 11.0", file=sys.stderr, flush=True)
    print("✅ MCP Server Ready for stdio communication", file=sys.stderr, flush=True)
    
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"\n💀 Server crashed: {e}", file=sys.stderr, flush=True)
        sys.exit(1)
