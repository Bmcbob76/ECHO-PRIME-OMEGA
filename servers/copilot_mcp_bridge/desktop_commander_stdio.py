#!/usr/bin/env python3
"""
Desktop Commander MCP STDIO Server
Authority Level: 11.0
Commander: Bobby Don McWilliams II

Pure Python MCP server for VS Code Copilot integration.
Exposes Desktop Commander tools via MCP protocol over STDIO.
"""

import sys
import os
import json
import asyncio
from typing import Any, Dict, List
from pathlib import Path
import subprocess

# Simple STDIO-based MCP server implementation
class MCPStdioServer:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools: List[Dict[str, Any]] = []
        
    def add_tool(self, name: str, description: str, input_schema: Dict[str, Any]):
        """Register a tool with the server"""
        self.tools.append({
            "name": name,
            "description": description,
            "inputSchema": input_schema
        })
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method", "")
        
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
        
        elif method == "tools/list":
            return {
                "tools": self.tools
            }
        
        elif method == "tools/call":
            # Handle tool execution
            params = request.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            
            # Execute the tool
            result = await self.execute_tool(tool_name, arguments)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }
        
        else:
            raise Exception(f"Unknown method: {method}")
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a Desktop Commander tool"""
        try:
            if tool_name == "read_file":
                path = arguments.get("path", "")
                if not path:
                    return json.dumps({"error": "Missing path parameter"})
                
                file_path = Path(path)
                if not file_path.exists():
                    return json.dumps({"error": f"File not found: {path}"})
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return json.dumps({
                    "content": content,
                    "path": str(file_path.absolute()),
                    "size": len(content)
                })
            
            elif tool_name == "write_file":
                path = arguments.get("path", "")
                content = arguments.get("content", "")
                
                if not path:
                    return json.dumps({"error": "Missing path parameter"})
                
                file_path = Path(path)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return json.dumps({
                    "path": str(file_path.absolute()),
                    "size": len(content),
                    "success": True
                })
            
            elif tool_name == "list_directory":
                path = arguments.get("path", "")
                if not path:
                    return json.dumps({"error": "Missing path parameter"})
                
                dir_path = Path(path)
                if not dir_path.exists():
                    return json.dumps({"error": f"Directory not found: {path}"})
                
                entries = []
                for item in dir_path.iterdir():
                    entries.append({
                        "name": item.name,
                        "path": str(item.absolute()),
                        "type": "directory" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else 0
                    })
                
                return json.dumps({
                    "path": str(dir_path.absolute()),
                    "entries": entries,
                    "count": len(entries)
                })
            
            elif tool_name == "execute_command":
                command = arguments.get("command", "")
                if not command:
                    return json.dumps({"error": "Missing command parameter"})
                
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                return json.dumps({
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                    "success": result.returncode == 0
                })
            
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
        
        except Exception as e:
            return json.dumps({"error": f"Tool execution failed: {str(e)}"})
    
    async def run(self):
        """Main server loop - read from stdin, write to stdout"""
        while True:
            try:
                # Read JSON-RPC request from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                request = json.loads(line)
                request_id = request.get("id")
                
                # Handle the request
                try:
                    result = await self.handle_request(request)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }
                
                # Write response to stdout
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except Exception as e:
                # Log error to stderr (not stdout, which is for MCP protocol)
                sys.stderr.write(f"Error: {e}\n")
                sys.stderr.flush()


async def main():
    """Main entry point"""
    # Create server
    server = MCPStdioServer("desktop-commander", "1.0.0")
    
    # Register Desktop Commander tools
    server.add_tool(
        "read_file",
        "Read the contents of a file",
        {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["path"]
        }
    )
    
    server.add_tool(
        "write_file",
        "Write content to a file",
        {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["path", "content"]
        }
    )
    
    server.add_tool(
        "list_directory",
        "List contents of a directory",
        {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the directory to list"
                }
            },
            "required": ["path"]
        }
    )
    
    server.add_tool(
        "execute_command",
        "Execute a shell command",
        {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute"
                }
            },
            "required": ["command"]
        }
    )
    
    # Log startup to stderr
    sys.stderr.write("🎖️ Desktop Commander MCP STDIO Server starting...\n")
    sys.stderr.write(f"Registered {len(server.tools)} tools\n")
    sys.stderr.flush()
    
    # Run the server
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
