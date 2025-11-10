"""
⚡ ULTRA SPEED CORE MCP SERVER - Built on GS343 Foundation
MCP Protocol Integration for Claude Desktop
File Operations: write, edit, read, move, delete, batch operations
Authority Level 9.5
"""

import sys
import asyncio
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

# MCP Server imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️ MCP not available - install with: pip install mcp")

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# GS343 Foundation Integration
GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

class UltraSpeedMCPServer:
    def __init__(self):
        self.server = Server("ultra-speed-core")
        self.authority_level = 9.5
        self.log_path = Path("E:/ECHO_XV4/LOGS")
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logging()
        
        # GS343 initialization
        if GS343_AVAILABLE:
            self.gs343 = GS343UniversalFoundation("UltraSpeedMCP", authority_level=9.5)
            self.phoenix = PhoenixAutoHeal("UltraSpeedMCP", authority_level=9.5)
            self.phoenix.start_monitoring()
            self.logger.info("⚡ MCP Server registered with GS343 Foundation")
        else:
            self.gs343 = None
            self.phoenix = None
        
        # Performance metrics
        self.metrics = {
            'files_written': 0,
            'files_read': 0,
            'files_edited': 0,
            'files_moved': 0,
            'files_deleted': 0,
            'total_operations': 0
        }
        
        self._register_tools()
        self.logger.info("⚡ Ultra Speed MCP Server initialized")

    def _setup_logging(self):
        log_file = self.log_path / "ultra_speed_mcp_server.log"
        logger = logging.getLogger("UltraSpeedMCP")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('⚡ %(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def _register_tools(self):
        """Register all MCP tools"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="ultra_speed_write",
                    description="Ultra-fast file writing with atomic operations. Creates parent directories automatically.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Full file path (e.g., E:/ECHO_XV4/test.txt)"},
                            "content": {"type": "string", "description": "File content to write"},
                            "encoding": {"type": "string", "default": "utf-8", "description": "File encoding"}
                        },
                        "required": ["path", "content"]
                    }
                ),
                Tool(
                    name="ultra_speed_read",
                    description="Ultra-fast file reading with caching optimization",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Full file path to read"},
                            "encoding": {"type": "string", "default": "utf-8"}
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="ultra_speed_edit",
                    description="Fast file editing with string replacement. Supports regex patterns.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Full file path"},
                            "old_text": {"type": "string", "description": "Text to find and replace"},
                            "new_text": {"type": "string", "description": "Replacement text"},
                            "use_regex": {"type": "boolean", "default": False}
                        },
                        "required": ["path", "old_text", "new_text"]
                    }
                ),
                Tool(
                    name="ultra_speed_move",
                    description="Move or rename files/directories with conflict resolution",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "description": "Source path"},
                            "destination": {"type": "string", "description": "Destination path"},
                            "overwrite": {"type": "boolean", "default": False}
                        },
                        "required": ["source", "destination"]
                    }
                ),
                Tool(
                    name="ultra_speed_delete",
                    description="Delete files or directories. Use with caution.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to delete"},
                            "recursive": {"type": "boolean", "default": False, "description": "Delete directories recursively"}
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="ultra_speed_batch_write",
                    description="Batch write multiple files in one operation for maximum speed",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string"},
                                        "content": {"type": "string"}
                                    },
                                    "required": ["path", "content"]
                                }
                            }
                        },
                        "required": ["files"]
                    }
                ),
                Tool(
                    name="ultra_speed_stats",
                    description="Get server performance statistics and metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                self.metrics['total_operations'] += 1
                
                if name == "ultra_speed_write":
                    result = await self._ultra_write(arguments)
                elif name == "ultra_speed_read":
                    result = await self._ultra_read(arguments)
                elif name == "ultra_speed_edit":
                    result = await self._ultra_edit(arguments)
                elif name == "ultra_speed_move":
                    result = await self._ultra_move(arguments)
                elif name == "ultra_speed_delete":
                    result = await self._ultra_delete(arguments)
                elif name == "ultra_speed_batch_write":
                    result = await self._ultra_batch_write(arguments)
                elif name == "ultra_speed_stats":
                    result = self._get_stats()
                else:
                    result = {"error": f"Unknown tool: {name}"}
                
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            except Exception as e:
                self.logger.error(f"⚡ Tool error [{name}]: {e}")
                if self.phoenix:
                    self.phoenix.heal_error(e, name)
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

    async def _ultra_write(self, args: dict) -> dict:
        """Ultra-fast file write with atomic operation"""
        path = Path(args['path'])
        content = args['content']
        encoding = args.get('encoding', 'utf-8')
        
        # Create parent directories
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Atomic write
        temp_path = path.with_suffix(path.suffix + '.tmp')
        temp_path.write_text(content, encoding=encoding)
        temp_path.replace(path)
        
        self.metrics['files_written'] += 1
        self.logger.info(f"⚡ WRITE: {path} ({len(content)} bytes)")
        
        return {
            "success": True,
            "path": str(path),
            "bytes_written": len(content.encode(encoding)),
            "operation": "write"
        }

    async def _ultra_read(self, args: dict) -> dict:
        """Ultra-fast file read"""
        path = Path(args['path'])
        encoding = args.get('encoding', 'utf-8')
        
        if not path.exists():
            return {"error": f"File not found: {path}"}
        
        content = path.read_text(encoding=encoding)
        self.metrics['files_read'] += 1
        self.logger.info(f"⚡ READ: {path} ({len(content)} bytes)")
        
        return {
            "success": True,
            "path": str(path),
            "content": content,
            "size_bytes": len(content.encode(encoding)),
            "operation": "read"
        }

    async def _ultra_edit(self, args: dict) -> dict:
        """Ultra-fast file edit with replacement"""
        import re
        
        path = Path(args['path'])
        old_text = args['old_text']
        new_text = args['new_text']
        use_regex = args.get('use_regex', False)
        
        if not path.exists():
            return {"error": f"File not found: {path}"}
        
        content = path.read_text(encoding='utf-8')
        
        if use_regex:
            new_content = re.sub(old_text, new_text, content)
            replacements = len(re.findall(old_text, content))
        else:
            new_content = content.replace(old_text, new_text)
            replacements = content.count(old_text)
        
        path.write_text(new_content, encoding='utf-8')
        
        self.metrics['files_edited'] += 1
        self.logger.info(f"⚡ EDIT: {path} ({replacements} replacements)")
        
        return {
            "success": True,
            "path": str(path),
            "replacements": replacements,
            "operation": "edit"
        }

    async def _ultra_move(self, args: dict) -> dict:
        """Ultra-fast file/directory move"""
        source = Path(args['source'])
        destination = Path(args['destination'])
        overwrite = args.get('overwrite', False)
        
        if not source.exists():
            return {"error": f"Source not found: {source}"}
        
        if destination.exists() and not overwrite:
            return {"error": f"Destination exists: {destination}"}
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        
        self.metrics['files_moved'] += 1
        self.logger.info(f"⚡ MOVE: {source} -> {destination}")
        
        return {
            "success": True,
            "source": str(source),
            "destination": str(destination),
            "operation": "move"
        }

    async def _ultra_delete(self, args: dict) -> dict:
        """Ultra-fast file/directory deletion"""
        path = Path(args['path'])
        recursive = args.get('recursive', False)
        
        if not path.exists():
            return {"error": f"Path not found: {path}"}
        
        if path.is_dir():
            if recursive:
                shutil.rmtree(path)
            else:
                return {"error": "Use recursive=true to delete directories"}
        else:
            path.unlink()
        
        self.metrics['files_deleted'] += 1
        self.logger.info(f"⚡ DELETE: {path}")
        
        return {
            "success": True,
            "path": str(path),
            "operation": "delete"
        }

    async def _ultra_batch_write(self, args: dict) -> dict:
        """Ultra-fast batch file writing"""
        files = args['files']
        results = []
        
        for file_data in files:
            result = await self._ultra_write(file_data)
            results.append(result)
        
        self.logger.info(f"⚡ BATCH_WRITE: {len(files)} files")
        
        return {
            "success": True,
            "files_written": len(files),
            "results": results,
            "operation": "batch_write"
        }

    def _get_stats(self) -> dict:
        """Get performance statistics"""
        return {
            "server": "UltraSpeedMCP",
            "authority_level": self.authority_level,
            "metrics": self.metrics,
            "gs343_active": GS343_AVAILABLE,
            "phoenix_active": self.phoenix.healing_active if self.phoenix else False,
            "timestamp": datetime.now().isoformat()
        }

async def main():
    if not MCP_AVAILABLE:
        print("⚡ ERROR: MCP package not installed")
        print("⚡ Install: pip install mcp")
        sys.exit(1)
    
    print("⚡ ECHO_XV4 Ultra Speed Core MCP Server")
    print("⚡ Commander Bobby Don McWilliams II - Authority Level 11.0")
    print("⚡ MCP Protocol Active")
    print("=" * 60)
    
    server = UltraSpeedMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            server.server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
