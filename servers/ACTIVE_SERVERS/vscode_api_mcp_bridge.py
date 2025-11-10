#!/usr/bin/env python3
"""
VS CODE API MCP BRIDGE
Commander Bobby Don McWilliams II - Authority Level 11.0

Exposes VS Code API HTTP endpoints as MCP tools for Claude Desktop.
Similar architecture to Windows API MCP Bridge.

Backend: VS Code API Extension on port 9001
Protocol: MCP stdio (JSON-RPC 2.0)
"""

import sys
import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('E:/ECHO_XV4/MLS/logs/vscode_api_bridge.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('VSCodeAPIBridge')

# Backend configuration
VSCODE_API_BASE = "http://localhost:9001"
VSCODE_API_TIMEOUT = 30  # seconds

class VSCodeAPIBridge:
    """MCP bridge for VS Code API"""
    
    def __init__(self):
        self.request_id = 0
        logger.info("VS Code API MCP Bridge initializing...")
        
    def check_backend(self) -> bool:
        """Check if VS Code API backend is accessible"""
        try:
            response = requests.get(f"{VSCODE_API_BASE}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Backend health check failed: {e}")
            return False
    
    def call_backend(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Call VS Code API backend"""
        try:
            url = f"{VSCODE_API_BASE}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=VSCODE_API_TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=VSCODE_API_TIMEOUT)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=VSCODE_API_TIMEOUT)
            elif method == "DELETE":
                response = requests.delete(url, timeout=VSCODE_API_TIMEOUT)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            # Parse response
            if not response.text:
                return {"success": True}
            
            response_data = response.json()
            
            # CRITICAL FIX: VS Code backend returns JSON-RPC wrapped responses
            # Unwrap the "result" field if present (JSON-RPC envelope)
            if isinstance(response_data, dict) and "result" in response_data:
                logger.debug(f"Unwrapping JSON-RPC envelope from VS Code backend")
                return response_data["result"]
            
            return response_data
            
        except requests.exceptions.Timeout:
            return {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to VS Code API backend"}
        except Exception as e:
            return {"error": str(e)}
    
    def handle_initialize(self, params: Dict) -> Dict:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "vscode-api-bridge",
                "version": "1.0.0"
            }
        }
    
    def handle_tools_list(self, params: Dict) -> Dict:
        """List all available VS Code tools"""
        tools = [
            {
                "name": "vscode_health",
                "description": "Check VS Code API server health and status",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_open_file",
                "description": "Open a file in VS Code editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Full path to file"}
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "vscode_close_file",
                "description": "Close a file in VS Code editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Full path to file"}
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "vscode_save_file",
                "description": "Save the currently active file",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_get_active_file",
                "description": "Get information about the currently active file",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_list_open_files",
                "description": "List all currently open files in VS Code",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_read_file_content",
                "description": "Read the content of a file open in VS Code",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Full path to file"}
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "vscode_edit_text",
                "description": "Edit text at a specific location in the active file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "line": {"type": "number", "description": "Line number (0-based)"},
                        "character": {"type": "number", "description": "Character position (0-based)"},
                        "text": {"type": "string", "description": "Text to insert"}
                    },
                    "required": ["line", "character", "text"]
                }
            },
            {
                "name": "vscode_get_cursor_position",
                "description": "Get current cursor position in the active editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_set_cursor_position",
                "description": "Set cursor position in the active editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "line": {"type": "number", "description": "Line number (0-based)"},
                        "character": {"type": "number", "description": "Character position (0-based)"}
                    },
                    "required": ["line", "character"]
                }
            },
            {
                "name": "vscode_get_selection",
                "description": "Get current selection in the active editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_set_selection",
                "description": "Set selection range in the active editor",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "startLine": {"type": "number"},
                        "startCharacter": {"type": "number"},
                        "endLine": {"type": "number"},
                        "endCharacter": {"type": "number"}
                    },
                    "required": ["startLine", "startCharacter", "endLine", "endCharacter"]
                }
            },
            {
                "name": "vscode_execute_command",
                "description": "Execute a VS Code command",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command ID"},
                        "args": {"type": "array", "description": "Command arguments", "items": {}}
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "vscode_run_terminal_command",
                "description": "Run a command in the integrated terminal",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to execute"}
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "vscode_get_workspace_folders",
                "description": "Get list of workspace folders",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_find_files",
                "description": "Find files in workspace matching a glob pattern",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "Glob pattern (e.g., **/*.js)"}
                    },
                    "required": ["pattern"]
                }
            },
            {
                "name": "vscode_start_debug",
                "description": "Start a debug session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "configuration": {"type": "string", "description": "Debug configuration name"}
                    },
                    "required": ["configuration"]
                }
            },
            {
                "name": "vscode_stop_debug",
                "description": "Stop the current debug session",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "vscode_set_breakpoint",
                "description": "Set a breakpoint at a specific line",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string"},
                        "line": {"type": "number"}
                    },
                    "required": ["filepath", "line"]
                }
            },
            {
                "name": "vscode_remove_breakpoint",
                "description": "Remove a breakpoint at a specific line",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string"},
                        "line": {"type": "number"}
                    },
                    "required": ["filepath", "line"]
                }
            },
            {
                "name": "vscode_get_diagnostics",
                "description": "Get diagnostic messages (errors/warnings) for a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Full path to file (optional)"}
                    },
                    "required": []
                }
            }
        ]
        
        return {"tools": tools}
    
    def handle_tool_call(self, params: Dict) -> Dict:
        """Handle tool execution"""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        logger.info(f"Tool call: {tool_name} with args: {arguments}")
        
        # Map tool names to backend endpoints
        tool_map = {
            "vscode_health": ("/health", "GET", {}),
            "vscode_open_file": ("/api/editor/open", "POST", {"filepath": arguments.get("filepath")}),
            "vscode_close_file": ("/api/editor/close", "POST", {"filepath": arguments.get("filepath")}),
            "vscode_save_file": ("/api/editor/save", "POST", {}),
            "vscode_get_active_file": ("/api/editor/active", "GET", {}),
            "vscode_list_open_files": ("/api/editor/files", "GET", {}),
            "vscode_read_file_content": ("/api/editor/content", "GET", {"filepath": arguments.get("filepath")}),
            "vscode_edit_text": ("/api/editor/edit", "POST", arguments),
            "vscode_get_cursor_position": ("/api/editor/cursor", "GET", {}),
            "vscode_set_cursor_position": ("/api/editor/cursor", "POST", arguments),
            "vscode_get_selection": ("/api/editor/selection", "GET", {}),
            "vscode_set_selection": ("/api/editor/selection", "POST", arguments),
            "vscode_execute_command": ("/api/commands/execute", "POST", arguments),
            "vscode_run_terminal_command": ("/api/terminal/run", "POST", {"command": arguments.get("command")}),
            "vscode_get_workspace_folders": ("/api/workspace/folders", "GET", {}),
            "vscode_find_files": ("/api/workspace/find", "GET", {"pattern": arguments.get("pattern")}),
            "vscode_start_debug": ("/api/debug/start", "POST", arguments),
            "vscode_stop_debug": ("/api/debug/stop", "POST", {}),
            "vscode_set_breakpoint": ("/api/debug/breakpoint/add", "POST", arguments),
            "vscode_remove_breakpoint": ("/api/debug/breakpoint/remove", "POST", arguments),
            "vscode_get_diagnostics": ("/api/diagnostics", "GET", arguments)
        }
        
        if tool_name not in tool_map:
            return {"error": f"Unknown tool: {tool_name}"}
        
        endpoint, method, data = tool_map[tool_name]
        result = self.call_backend(endpoint, method, data)
        
        # Format result for MCP
        result_text = json.dumps(result, indent=2)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle MCP JSON-RPC request"""
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = self.handle_initialize(params)
            elif method == "tools/list":
                result = self.handle_tools_list(params)
            elif method == "tools/call":
                result = self.handle_tool_call(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            # Wrap result in JSON-RPC envelope
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def run(self):
        """Main event loop - stdio transport"""
        logger.info("VS Code API MCP Bridge ready for requests")
        logger.info(f"Backend: {VSCODE_API_BASE}")
        
        # Check backend availability
        if self.check_backend():
            logger.info("VS Code API backend is OPERATIONAL")
        else:
            logger.warning("VS Code API backend may not be available")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("Bridge shutdown")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    bridge = VSCodeAPIBridge()
    bridge.run()
