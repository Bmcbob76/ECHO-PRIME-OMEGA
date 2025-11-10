#!/usr/bin/env python3
"""
WINDOWS API MCP BRIDGE - EXPANDED VERSION
Commander Bobby Don McWilliams II - Authority Level 11.0

COMPLETE DVP INTEGRATION - 70+ Tools
Bridges Windows API Ultimate (225+ endpoints) to Claude Desktop via MCP

Architecture:
    Claude Desktop (MCP Client)
        ↓ MCP Protocol (stdio/JSON-RPC)
    This Bridge Server (70+ tools)
        ↓ HTTP REST
    Windows API Ultimate Server (Port 8343, 225+ endpoints)
"""

import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Only external dependency
try:
    import aiohttp
except ImportError:
    print(json.dumps({
        "jsonrpc": "2.0",
        "error": {"code": -32000, "message": "aiohttp not installed. Run: pip install aiohttp"}
    }), file=sys.stdout)
    sys.stdout.flush()
    sys.exit(1)

# PyAutoGUI for automation
try:
    import pyautogui
    AUTOMATION_AVAILABLE = True
    # Safety settings
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    pyautogui.PAUSE = 0.1  # Small pause between actions
except ImportError:
    AUTOMATION_AVAILABLE = False
    pyautogui = None

# Win32 APIs for direct window control
try:
    import win32gui
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    win32gui = None

# Configure logging
log_file = Path("E:/ECHO_XV4/MLS/logs/windows_api_bridge_expanded.log")
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - WINAPI_BRIDGE_EXPANDED - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Windows API Ultimate server URL
WINDOWS_API_URL = "http://localhost:8343"

class WindowsAPIMCPBridgeExpanded:
    """EXPANDED MCP Bridge for Windows API Ultimate - 70+ Tools"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        logger.info("Windows API MCP Bridge EXPANDED initialized - 70+ tools available")
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def _call_api(self, endpoint: str, method: str = "GET", 
                       params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Call Windows API Ultimate endpoint"""
        await self._ensure_session()
        
        url = f"{WINDOWS_API_URL}{endpoint}"
        
        try:
            if method == "GET":
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"HTTP {response.status}: {error_text}"}
            elif method == "POST":
                async with self.session.post(url, json=json_data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"HTTP {response.status}: {error_text}"}
        except aiohttp.ClientError as e:
            logger.error(f"API call failed: {endpoint} - {str(e)}")
            return {
                "success": False,
                "error": f"Connection error: {str(e)}. Is Windows API server running on port 8343?"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return all 70+ available MCP tools - COMPREHENSIVE DVP SYSTEM"""
        tools = []
        
        # ==================== TIER 0: CORE SYSTEM (4 tools) ====================
        tools.extend([
            {
                "name": "windows_health",
                "description": "Get Windows API server health status",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_system_info",
                "description": "Get comprehensive system information",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_performance",
                "description": "Get current system performance metrics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_live_performance",
                "description": "Get real-time CPU, memory, disk, network stats",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
        ])
        
        # ==================== TIER 1: PROCESS MANAGEMENT (4 tools) ====================
        tools.extend([
            {
                "name": "windows_process_list",
                "description": "List all running processes",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_process_info",
                "description": "Get detailed process information by PID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "number", "description": "Process ID"}
                    },
                    "required": ["pid"]
                }
            },
            {
                "name": "windows_process_kill",
                "description": "Terminate a process by PID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "number", "description": "Process ID to kill"}
                    },
                    "required": ["pid"]
                }
            },
            {
                "name": "windows_process_handles",
                "description": "Get process handles and resources",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "number", "description": "Process ID"}
                    },
                    "required": ["pid"]
                }
            },
        ])
        
        # ==================== TIER 2: MEMORY MANAGEMENT (3 tools) ====================
        tools.extend([
            {
                "name": "windows_memory_stats",
                "description": "Get memory statistics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_memory_maps",
                "description": "Get memory maps for a process",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "number", "description": "Process ID"}
                    },
                    "required": ["pid"]
                }
            },
            {
                "name": "windows_memory_analyze",
                "description": "Analyze memory usage patterns",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "number", "description": "Process ID to analyze"}
                    },
                    "required": ["pid"]
                }
            },
        ])
        
        # ==================== TIER 3: HARDWARE MONITORING (5 tools) ====================
        tools.extend([
            {
                "name": "windows_hardware_usb",
                "description": "List all USB devices",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_hardware_pci",
                "description": "List all PCI devices",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_hardware_sensors",
                "description": "Get hardware sensor readings (temp, fan, voltage)",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_hardware_storage",
                "description": "Get storage device information",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_system_sensors",
                "description": "Get system sensor data",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
        ])
        
        # ==================== TIER 4: NETWORK (7 tools) ====================
        tools.extend([
            {
                "name": "windows_network_connections",
                "description": "List all active network connections",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_network_interfaces",
                "description": "List all network interfaces",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_network_stats",
                "description": "Get network statistics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_network_topology",
                "description": "Get network topology information",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_network_ping",
                "description": "Ping a host",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "host": {"type": "string", "description": "Hostname or IP to ping"},
                        "count": {"type": "number", "description": "Number of pings (default: 4)", "default": 4}
                    },
                    "required": ["host"]
                }
            },
        ])
        
        # ==================== TIER 5: FILE OPERATIONS (8 tools) ====================
        tools.extend([
            {
                "name": "windows_file_list",
                "description": "List files in a directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path"},
                        "pattern": {"type": "string", "description": "File pattern (e.g., *.py)"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "windows_file_info",
                "description": "Get file information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "windows_file_read",
                "description": "Read file contents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path to read"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "windows_file_write",
                "description": "Write to a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path to write"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "windows_file_delete",
                "description": "Delete a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path to delete"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "windows_file_move",
                "description": "Move/rename a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Source path"},
                        "destination": {"type": "string", "description": "Destination path"}
                    },
                    "required": ["source", "destination"]
                }
            },
            {
                "name": "windows_file_copy",
                "description": "Copy a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Source path"},
                        "destination": {"type": "string", "description": "Destination path"}
                    },
                    "required": ["source", "destination"]
                }
            },
            {
                "name": "windows_file_permissions",
                "description": "Get file permissions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "windows_directory_tree",
                "description": "Get directory tree structure",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path"},
                        "depth": {"type": "number", "description": "Max depth (default: 2)", "default": 2}
                    },
                    "required": ["path"]
                }
            },
        ])
        
        # ==================== TIER 6: REGISTRY (4 tools) ====================
        tools.extend([
            {
                "name": "windows_registry_read",
                "description": "Read registry value",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Registry key path"},
                        "value": {"type": "string", "description": "Value name"}
                    },
                    "required": ["key"]
                }
            },
            {
                "name": "windows_registry_write",
                "description": "Write registry value",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Registry key path"},
                        "value": {"type": "string", "description": "Value name"},
                        "data": {"type": "string", "description": "Data to write"}
                    },
                    "required": ["key", "value", "data"]
                }
            },
            {
                "name": "windows_registry_keys",
                "description": "List registry subkeys",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Registry key path"}
                    },
                    "required": ["key"]
                }
            },
            {
                "name": "windows_registry_search",
                "description": "Search registry",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "Search pattern"}
                    },
                    "required": ["pattern"]
                }
            },
        ])
        
        # ==================== TIER 7: SERVICES (4 tools) ====================
        tools.extend([
            {
                "name": "windows_service_list",
                "description": "List all Windows services",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_service_status",
                "description": "Get service status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Service name"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "windows_service_control",
                "description": "Control a service (start/stop/restart)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Service name"},
                        "action": {"type": "string", "description": "Action: start, stop, restart"}
                    },
                    "required": ["name", "action"]
                }
            },
            {
                "name": "windows_service_dependencies",
                "description": "Get service dependencies",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Service name"}
                    },
                    "required": ["name"]
                }
            },
        ])
        
        # ==================== TIER 8: EVENT LOGS (3 tools) ====================
        tools.extend([
            {
                "name": "windows_eventlog_system",
                "description": "Get system event log entries",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "number", "description": "Number of entries (default: 100)", "default": 100}
                    }
                }
            },
            {
                "name": "windows_eventlog_application",
                "description": "Get application event log entries",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "number", "description": "Number of entries (default: 100)", "default": 100}
                    }
                }
            },
            {
                "name": "windows_eventlog_security",
                "description": "Get security event log entries",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "number", "description": "Number of entries (default: 100)", "default": 100}
                    }
                }
            },
        ])
        
        # ==================== TIER 9: CRYPTOGRAPHY & SECURITY (5 tools) ====================
        tools.extend([
            {
                "name": "windows_crypto_hash",
                "description": "Calculate file/text hash",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "Data to hash or file path"},
                        "algorithm": {"type": "string", "description": "Hash algorithm (md5, sha1, sha256)", "default": "sha256"}
                    },
                    "required": ["data"]
                }
            },
            {
                "name": "windows_crypto_encrypt",
                "description": "Encrypt data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "Data to encrypt"},
                        "key": {"type": "string", "description": "Encryption key"}
                    },
                    "required": ["data", "key"]
                }
            },
            {
                "name": "windows_crypto_decrypt",
                "description": "Decrypt data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "Data to decrypt"},
                        "key": {"type": "string", "description": "Decryption key"}
                    },
                    "required": ["data", "key"]
                }
            },
            {
                "name": "windows_security_audit",
                "description": "Perform security audit",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_security_certificates",
                "description": "List security certificates",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
        ])
        
        # ==================== TIER 10: OCR SYSTEM (4 tools) ====================
        tools.extend([
            {
                "name": "windows_ocr_screens_all",
                "description": "OCR all 4 screens simultaneously",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_ocr_screen",
                "description": "OCR a specific screen (1-4)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "screen_number": {
                            "type": "number",
                            "description": "Screen number (1-4)",
                            "minimum": 1,
                            "maximum": 4
                        }
                    },
                    "required": ["screen_number"]
                }
            },
            {
                "name": "windows_ocr_search",
                "description": "Search for text across all screens",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to search for"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "windows_ocr_extract",
                "description": "Extract text from specific region",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "X coordinate"},
                        "y": {"type": "number", "description": "Y coordinate"},
                        "width": {"type": "number", "description": "Width"},
                        "height": {"type": "number", "description": "Height"}
                    },
                    "required": ["x", "y", "width", "height"]
                }
            },
            {
                "name": "windows_monitor_layout",
                "description": "Get monitor layout information",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
        ])
        
        # ==================== TIER 11: AUTOMATION (8 tools) ====================
        if AUTOMATION_AVAILABLE:
            tools.extend([
                {
                    "name": "mouse_move",
                    "description": "Move mouse cursor to specific coordinates",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "X coordinate"},
                            "y": {"type": "number", "description": "Y coordinate"},
                            "duration": {"type": "number", "description": "Duration in seconds (default: 0.25)", "default": 0.25}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "mouse_click",
                    "description": "Click mouse at current position or specified coordinates",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "X coordinate (optional)"},
                            "y": {"type": "number", "description": "Y coordinate (optional)"},
                            "button": {"type": "string", "description": "Mouse button: left, right, middle", "default": "left"},
                            "clicks": {"type": "number", "description": "Number of clicks (default: 1)", "default": 1}
                        }
                    }
                },
                {
                    "name": "mouse_drag",
                    "description": "Drag mouse from current position to target coordinates",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "Target X coordinate"},
                            "y": {"type": "number", "description": "Target Y coordinate"},
                            "duration": {"type": "number", "description": "Duration in seconds (default: 0.5)", "default": 0.5},
                            "button": {"type": "string", "description": "Mouse button to hold (default: left)", "default": "left"}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "keyboard_type",
                    "description": "Type text as if typing on keyboard",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to type"},
                            "interval": {"type": "number", "description": "Seconds between keystrokes (default: 0.01)", "default": 0.01}
                        },
                        "required": ["text"]
                    }
                },
                {
                    "name": "keyboard_press",
                    "description": "Press a single key or key combination",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "keys": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Key(s) to press. Examples: ['enter'], ['ctrl', 'c'], ['alt', 'tab']"
                            }
                        },
                        "required": ["keys"]
                    }
                },
                {
                    "name": "get_mouse_position",
                    "description": "Get current mouse cursor position",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "get_screen_size",
                    "description": "Get screen resolution/size",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "screenshot",
                    "description": "Take a screenshot (full screen or region)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "object",
                                "description": "Optional region {x, y, width, height}",
                                "properties": {
                                    "x": {"type": "number"},
                                    "y": {"type": "number"},
                                    "width": {"type": "number"},
                                    "height": {"type": "number"}
                                }
                            }
                        }
                    }
                },
            ])
        
        # ==================== TIER 12: WINDOW CONTROL (7 tools) ====================
        if WIN32_AVAILABLE:
            tools.extend([
                {
                    "name": "window_list",
                    "description": "List all open windows with titles and handles",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "window_find",
                    "description": "Find window by title (partial match supported)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Window title or partial title to search"}
                        },
                        "required": ["title"]
                    }
                },
                {
                    "name": "window_click",
                    "description": "Click in a specific window WITHOUT moving physical cursor",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "window_title": {"type": "string", "description": "Window title or partial title"},
                            "x": {"type": "number", "description": "X coordinate relative to window"},
                            "y": {"type": "number", "description": "Y coordinate relative to window"},
                            "button": {"type": "string", "description": "left, right, or middle", "default": "left"}
                        },
                        "required": ["window_title", "x", "y"]
                    }
                },
                {
                    "name": "window_type",
                    "description": "Type text in a specific window WITHOUT affecting your keyboard",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "window_title": {"type": "string", "description": "Window title or partial title"},
                            "text": {"type": "string", "description": "Text to type"}
                        },
                        "required": ["window_title", "text"]
                    }
                },
                {
                    "name": "window_send_keys",
                    "description": "Send key combination to specific window (Ctrl+C, Alt+Tab, etc.)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "window_title": {"type": "string", "description": "Window title or partial title"},
                            "keys": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Keys to send. Examples: ['ctrl', 'c'], ['alt', 'tab'], ['enter']"
                            }
                        },
                        "required": ["window_title", "keys"]
                    }
                },
                {
                    "name": "window_focus",
                    "description": "Bring window to foreground",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "window_title": {"type": "string", "description": "Window title or partial title"}
                        },
                        "required": ["window_title"]
                    }
                },
                {
                    "name": "window_get_rect",
                    "description": "Get window position and size",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "window_title": {"type": "string", "description": "Window title or partial title"}
                        },
                        "required": ["window_title"]
                    }
                },
            ])
        
        # ==================== TIER 13: SYSTEM INTELLIGENCE (3 tools) ====================
        tools.extend([
            {
                "name": "windows_ai_metrics",
                "description": "Get AI/ML system metrics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_predictive_analysis",
                "description": "Get predictive system analysis",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_command_run",
                "description": "Run a command",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to execute"}
                    },
                    "required": ["command"]
                }
            },
        ])
        
        return tools
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name - COMPREHENSIVE ROUTING"""
        
        # Handle automation tools
        automation_tools = [
            "mouse_move", "mouse_click", "mouse_drag", "keyboard_type",
            "keyboard_press", "get_mouse_position", "get_screen_size", "screenshot"
        ]
        if name in automation_tools:
            return await self._execute_automation(name, arguments)
        
        # Handle window control tools
        window_tools = [
            "window_list", "window_find", "window_click", "window_type",
            "window_send_keys", "window_focus", "window_get_rect"
        ]
        if name in window_tools:
            return await self._execute_window_control(name, arguments)
        
        # Map tool names to API endpoints (GET requests)
        get_tool_map = {
            # Core System
            "windows_health": "/health",
            "windows_system_info": "/system/info",
            "windows_performance": "/performance",
            "windows_live_performance": "/system/performance/live",
            
            # Process Management
            "windows_process_list": "/process/list",
            "windows_process_handles": "/process/handles",
            
            # Memory
            "windows_memory_stats": "/memory/stats",
            "windows_memory_maps": "/memory/maps",
            
            # Hardware
            "windows_hardware_usb": "/hardware/usb",
            "windows_hardware_pci": "/hardware/pci",
            "windows_hardware_sensors": "/hardware/sensors",
            "windows_hardware_storage": "/hardware/storage",
            "windows_system_sensors": "/system/sensors",
            
            # Network
            "windows_network_connections": "/network/connections",
            "windows_network_interfaces": "/network/interfaces",
            "windows_network_stats": "/network/stats",
            "windows_network_topology": "/network/topology",
            
            # File Operations (GET)
            "windows_file_list": "/file/list",
            "windows_file_info": "/file/info",
            "windows_file_permissions": "/file/permissions",
            "windows_directory_tree": "/directory/tree",
            
            # Registry (GET)
            "windows_registry_read": "/registry/read",
            "windows_registry_keys": "/registry/keys",
            "windows_registry_search": "/registry/search",
            
            # Services
            "windows_service_list": "/service/list",
            "windows_service_status": "/service/status",
            "windows_service_dependencies": "/service/dependencies",
            
            # Event Logs
            "windows_eventlog_system": "/eventlog/system",
            "windows_eventlog_application": "/eventlog/application",
            "windows_eventlog_security": "/eventlog/security",
            
            # Cryptography (GET)
            "windows_crypto_hash": "/crypto/hash",
            "windows_security_audit": "/security/audit",
            "windows_security_certificates": "/security/certificates",
            
            # OCR
            "windows_ocr_screens_all": "/ocr/screens/all",
            "windows_ocr_search": "/ocr/search",
            "windows_monitor_layout": "/ocr/monitor/layout",
            
            # System Intelligence
            "windows_ai_metrics": "/system/ai/metrics",
            "windows_predictive_analysis": "/system/predictive",
        }
        
        # Map tool names to API endpoints (POST requests)
        post_tool_map = {
            # Process
            "windows_process_info": "/process/info",
            "windows_process_kill": "/process/kill",
            
            # Memory
            "windows_memory_analyze": "/memory/analyze",
            
            # Network
            "windows_network_ping": "/network/ping",
            
            # File Operations (POST)
            "windows_file_read": "/file/read",
            "windows_file_write": "/file/write",
            "windows_file_delete": "/file/delete",
            "windows_file_move": "/file/move",
            "windows_file_copy": "/file/copy",
            
            # Registry (POST)
            "windows_registry_write": "/registry/write",
            
            # Services
            "windows_service_control": "/service/control",
            
            # Cryptography (POST)
            "windows_crypto_encrypt": "/crypto/encrypt",
            "windows_crypto_decrypt": "/crypto/decrypt",
            
            # OCR
            "windows_ocr_extract": "/ocr/extract",
            
            # Command execution
            "windows_command_run": "/command/run",
        }
        
        # Handle dynamic OCR screen endpoint
        if name == "windows_ocr_screen":
            screen_num = arguments.get("screen_number", 1)
            endpoint = f"/ocr/screen/{screen_num}"
            return await self._call_api(endpoint, method="GET")
        
        # Handle GET tools
        if name in get_tool_map:
            endpoint = get_tool_map[name]
            return await self._call_api(endpoint, method="GET", params=arguments)
        
        # Handle POST tools
        if name in post_tool_map:
            endpoint = post_tool_map[name]
            return await self._call_api(endpoint, method="POST", json_data=arguments)
        
        return {"success": False, "error": f"Unknown tool: {name}"}


    # ========== AUTOMATION & WINDOW HANDLERS ==========
