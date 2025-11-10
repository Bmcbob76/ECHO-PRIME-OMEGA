#!/usr/bin/env python3
"""
WINDOWS API MCP BRIDGE - FIXED VERSION
Commander Bobby Don McWilliams II - Authority Level 11.0

FIXES:
1. Added missing _execute_automation() method
2. Fixed schema validation issues (removed problematic defaults)
3. Improved error handling
4. Complete pyautogui integration

Bridges Windows API Ultimate HTTP server to Claude Desktop via MCP protocol.
Uses raw JSON-RPC over stdio - NO external dependencies except aiohttp.

Architecture:
    Claude Desktop (MCP Client)
        ↓ MCP Protocol (stdio/JSON-RPC)
    This Bridge Server
        ↓ HTTP REST
    Windows API Ultimate Server (Port 8343)
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

# Win32 APIs for direct window control (no cursor movement)
try:
    import win32gui
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    win32gui = None

# Configure logging
log_file = Path("E:/ECHO_XV4/MLS/logs/windows_api_bridge.log")
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - WINAPI_BRIDGE - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Windows API Ultimate server URL
WINDOWS_API_URL = "http://localhost:8343"

class WindowsAPIMCPBridge:
    """MCP Bridge for Windows API Ultimate - Raw JSON-RPC Implementation"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        logger.info("Windows API MCP Bridge initialized (FIXED version)")
        if not AUTOMATION_AVAILABLE:
            logger.warning("pyautogui not available - automation tools will be disabled")
        if not WIN32_AVAILABLE:
            logger.warning("pywin32 not available - window control tools will be disabled")
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def _call_api(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None) -> Dict[str, Any]:
        """Call Windows API Ultimate endpoint"""
        await self._ensure_session()
        
        url = f"{WINDOWS_API_URL}{endpoint}"
        
        try:
            async with self.session.request(method, url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}: {error_text}"
                    }
        except aiohttp.ClientError as e:
            logger.error(f"API call failed: {endpoint} - {str(e)}")
            return {
                "success": False,
                "error": f"Connection error: {str(e)}. Is Windows API server running on port 8343?"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return all available MCP tools"""
        tools = [
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
                "name": "windows_memory_stats",
                "description": "Get memory statistics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_network_connections",
                "description": "List all active network connections",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_service_list",
                "description": "List all Windows services",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "windows_service_status",
                "description": "Get status of a specific Windows service",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Service name"}
                    },
                    "required": ["name"]
                }
            },
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
        ]
        
        # Add automation tools if available
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
                            "duration": {"type": "number", "description": "Duration in seconds (default: 0.25)"}
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
                            "button": {"type": "string", "description": "Mouse button: left, right, middle"},
                            "clicks": {"type": "number", "description": "Number of clicks (default: 1)"}
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
                            "duration": {"type": "number", "description": "Duration in seconds (default: 0.5)"},
                            "button": {"type": "string", "description": "Mouse button to hold (default: left)"}
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
                            "interval": {"type": "number", "description": "Seconds between keystrokes (default: 0.01)"}
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
        
        # Add window control tools if available
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
                            "button": {"type": "string", "description": "left, right, or middle"}
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
        
        return tools
    
    async def _execute_automation(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute automation tools using pyautogui"""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "pyautogui not available. Install with: pip install pyautogui"
            }
        
        try:
            if name == "mouse_move":
                x = int(arguments["x"])
                y = int(arguments["y"])
                duration = float(arguments.get("duration", 0.25))
                
                pyautogui.moveTo(x, y, duration=duration)
                
                return {
                    "success": True,
                    "action": "mouse_move",
                    "position": {"x": x, "y": y},
                    "duration": duration
                }
            
            elif name == "mouse_click":
                x = arguments.get("x")
                y = arguments.get("y")
                button = arguments.get("button", "left")
                clicks = int(arguments.get("clicks", 1))
                
                if x is not None and y is not None:
                    pyautogui.click(x=int(x), y=int(y), clicks=clicks, button=button)
                else:
                    pyautogui.click(clicks=clicks, button=button)
                
                return {
                    "success": True,
                    "action": "mouse_click",
                    "position": {"x": x, "y": y} if x and y else None,
                    "button": button,
                    "clicks": clicks
                }
            
            elif name == "mouse_drag":
                x = int(arguments["x"])
                y = int(arguments["y"])
                duration = float(arguments.get("duration", 0.5))
                button = arguments.get("button", "left")
                
                pyautogui.drag(x, y, duration=duration, button=button)
                
                return {
                    "success": True,
                    "action": "mouse_drag",
                    "target": {"x": x, "y": y},
                    "duration": duration,
                    "button": button
                }
            
            elif name == "keyboard_type":
                text = arguments["text"]
                interval = float(arguments.get("interval", 0.01))
                
                pyautogui.write(text, interval=interval)
                
                return {
                    "success": True,
                    "action": "keyboard_type",
                    "text": text,
                    "length": len(text),
                    "interval": interval
                }
            
            elif name == "keyboard_press":
                keys = arguments["keys"]
                
                # Handle key combinations
                if len(keys) == 1:
                    pyautogui.press(keys[0])
                else:
                    pyautogui.hotkey(*keys)
                
                return {
                    "success": True,
                    "action": "keyboard_press",
                    "keys": keys
                }
            
            elif name == "get_mouse_position":
                pos = pyautogui.position()
                
                return {
                    "success": True,
                    "position": {"x": pos.x, "y": pos.y}
                }
            
            elif name == "get_screen_size":
                size = pyautogui.size()
                
                return {
                    "success": True,
                    "size": {"width": size.width, "height": size.height}
                }
            
            elif name == "screenshot":
                region = arguments.get("region")
                
                if region:
                    screenshot = pyautogui.screenshot(region=(
                        region["x"], region["y"], 
                        region["width"], region["height"]
                    ))
                else:
                    screenshot = pyautogui.screenshot()
                
                # Save to temp file
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                screenshot.save(temp_file.name)
                
                return {
                    "success": True,
                    "action": "screenshot",
                    "filepath": temp_file.name,
                    "region": region
                }
            
            return {"success": False, "error": f"Unknown automation tool: {name}"}
            
        except Exception as e:
            logger.error(f"Automation error: {name} - {str(e)}")
            return {
                "success": False,
                "error": f"Automation failed: {str(e)}"
            }
    
    async def _execute_window_control(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute window control tools using Win32 APIs - no cursor movement"""
        if not WIN32_AVAILABLE:
            return {
                "success": False,
                "error": "pywin32 not available. Install with: pip install pywin32"
            }
        
        try:
            if name == "window_list":
                windows = []
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            windows.append({
                                "handle": hwnd,
                                "title": title,
                                "class": win32gui.GetClassName(hwnd)
                            })
                
                win32gui.EnumWindows(callback, None)
                return {
                    "success": True,
                    "windows": windows,
                    "count": len(windows)
                }
            
elif name == "window_find":
                title_search = arguments.get("title", "").lower()
                found_windows = []
                
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title and title_search in title.lower():
                            found_windows.append({
                                "handle": hwnd,
                                "title": title,
                                "class": win32gui.GetClassName(hwnd)
                            })
                
                win32gui.EnumWindows(callback, None)
                return {
                    "success": True,
                    "windows": found_windows,
                    "count": len(found_windows)
                }
            
            elif name == "window_click":
                title_search = arguments.get("window_title", "").lower()
                x = int(arguments.get("x"))
                y = int(arguments.get("y"))
                button = arguments.get("button", "left")
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Calculate lparam for position
                lparam = win32api.MAKELONG(x, y)
                
                # Send click messages (down + up)
                if button == "left":
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
                elif button == "right":
                    win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
                    win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lparam)
                
                return {
                    "success": True,
                    "action": "window_click",
                    "window": win32gui.GetWindowText(hwnd),
                    "position": {"x": x, "y": y},
                    "button": button
                }
            
            elif name == "window_type":
                title_search = arguments.get("window_title", "").lower()
                text = arguments.get("text", "")
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Send WM_CHAR for each character
                for char in text:
                    win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
                
                return {
                    "success": True,
                    "action": "window_type",
                    "window": win32gui.GetWindowText(hwnd),
                    "text": text,
                    "length": len(text)
                }
            
            elif name == "window_send_keys":
                title_search = arguments.get("window_title", "").lower()
                keys = arguments.get("keys", [])
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Map key names to virtual key codes
                vk_map = {
                    "enter": win32con.VK_RETURN,
                    "tab": win32con.VK_TAB,
                    "esc": win32con.VK_ESCAPE,
                    "space": win32con.VK_SPACE,
                    "ctrl": win32con.VK_CONTROL,
                    "alt": win32con.VK_MENU,
                    "shift": win32con.VK_SHIFT,
                    "delete": win32con.VK_DELETE,
                    "backspace": win32con.VK_BACK,
                    "home": win32con.VK_HOME,
                    "end": win32con.VK_END,
                    "pageup": win32con.VK_PRIOR,
                    "pagedown": win32con.VK_NEXT,
                }
                
                # Send key down for all keys
                for key in keys:
                    vk = vk_map.get(key.lower(), ord(key.upper()))
                    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk, 0)
                
                # Send key up in reverse order
                for key in reversed(keys):
                    vk = vk_map.get(key.lower(), ord(key.upper()))
                    win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk, 0)
                
                return {
                    "success": True,
                    "action": "window_send_keys",
                    "window": win32gui.GetWindowText(hwnd),
                    "keys": keys
                }
            
            elif name == "window_focus":
                title_search = arguments.get("window_title", "").lower()
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Bring to foreground
                win32gui.SetForegroundWindow(hwnd)
                
                return {
                    "success": True,
                    "action": "window_focus",
                    "window": win32gui.GetWindowText(hwnd)
                }
            
            elif name == "window_get_rect":
                title_search = arguments.get("window_title", "").lower()
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Get window rectangle
                rect = win32gui.GetWindowRect(hwnd)
                
                return {
                    "success": True,
                    "window": win32gui.GetWindowText(hwnd),
                    "rect": {
                        "left": rect[0],
                        "top": rect[1],
                        "right": rect[2],
                        "bottom": rect[3],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1]
                    }
                }
            
            return {"success": False, "error": f"Unknown window control tool: {name}"}
            
        except Exception as e:
            logger.error(f"Window control error: {name} - {str(e)}")
            return {
                "success": False,
                "error": f"Window control failed: {str(e)}"
            }

            
            elif name == "window_find":
                title_search = arguments.get("title", "").lower()
                found_windows = []
                
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title and title_search in title.lower():
                            found_windows.append({
                                "handle": hwnd,
                                "title": title,
                                "class": win32gui.GetClassName(hwnd)
                            })
                
                win32gui.EnumWindows(callback, None)
                return {
                    "success": True,
                    "windows": found_windows,
                    "count": len(found_windows)
                }
            
            elif name == "window_click":
                title_search = arguments.get("window_title", "").lower()
                x = int(arguments.get("x"))
                y = int(arguments.get("y"))
                button = arguments.get("button", "left")
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Calculate lparam for position
                lparam = win32api.MAKELONG(x, y)
                
                # Send click messages (down + up)
                if button == "left":
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
                elif button == "right":
                    win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
                    win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lparam)
                
                return {
                    "success": True,
                    "action": "window_click",
                    "window": win32gui.GetWindowText(hwnd),
                    "position": {"x": x, "y": y},
                    "button": button
                }
            
            elif name == "window_type":
                title_search = arguments.get("window_title", "").lower()
                text = arguments.get("text", "")
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Send WM_CHAR for each character
                for char in text:
                    win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
                
                return {
                    "success": True,
                    "action": "window_type",
                    "window": win32gui.GetWindowText(hwnd),
                    "text": text,
                    "length": len(text)
                }
            
            elif name == "window_send_keys":
                title_search = arguments.get("window_title", "").lower()
                keys = arguments.get("keys", [])
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Map key names to virtual key codes
                vk_map = {
                    "enter": win32con.VK_RETURN,
                    "tab": win32con.VK_TAB,
                    "esc": win32con.VK_ESCAPE,
                    "space": win32con.VK_SPACE,
                    "ctrl": win32con.VK_CONTROL,
                    "alt": win32con.VK_MENU,
                    "shift": win32con.VK_SHIFT,
                    "delete": win32con.VK_DELETE,
                    "backspace": win32con.VK_BACK,
                    "home": win32con.VK_HOME,
                    "end": win32con.VK_END,
                    "pageup": win32con.VK_PRIOR,
                    "pagedown": win32con.VK_NEXT,
                }
                
                # Send key down for all keys
                for key in keys:
                    vk = vk_map.get(key.lower(), ord(key.upper()))
                    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk, 0)
                
                # Send key up in reverse order
                for key in reversed(keys):
                    vk = vk_map.get(key.lower(), ord(key.upper()))
                    win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk, 0)
                
                return {
                    "success": True,
                    "action": "window_send_keys",
                    "window": win32gui.GetWindowText(hwnd),
                    "keys": keys
                }
            
            elif name == "window_focus":
                title_search = arguments.get("window_title", "").lower()
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Bring to foreground
                win32gui.SetForegroundWindow(hwnd)
                
                return {
                    "success": True,
                    "action": "window_focus",
                    "window": win32gui.GetWindowText(hwnd)
                }
            
            elif name == "window_get_rect":
                title_search = arguments.get("window_title", "").lower()
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Get window rectangle
                rect = win32gui.GetWindowRect(hwnd)
                
                return {
                    "success": True,
                    "window": win32gui.GetWindowText(hwnd),
                    "rect": {
                        "left": rect[0],
                        "top": rect[1],
                        "right": rect[2],
                        "bottom": rect[3],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1]
                    }
                }
            
            return {"success": False, "error": f"Unknown window control tool: {name}"}
            
        except Exception as e:
            logger.error(f"Window control error: {name} - {str(e)}")
            return {
                "success": False,
                "error": f"Window control failed: {str(e)}"
            }
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name"""
        
        # Handle automation tools separately
        automation_tools = [
            "mouse_move", "mouse_click", "mouse_drag", "keyboard_type",
            "keyboard_press", "get_mouse_position", "get_screen_size", "screenshot"
        ]
        
        # Handle window control tools separately
        window_tools = [
            "window_list", "window_find", "window_click", "window_type",
            "window_send_keys", "window_focus", "window_get_rect"
        ]
        
        if name in automation_tools:
            return await self._execute_automation(name, arguments)
        
        if name in window_tools:
            return await self._execute_window_control(name, arguments)
        
        # Map tool names to API endpoints
        tool_map = {
            "windows_health": "/health",
            "windows_system_info": "/system/info",
            "windows_performance": "/performance",
            "windows_live_performance": "/system/performance/live",
            "windows_process_list": "/process/list",
            "windows_process_info": "/process/info",
            "windows_process_kill": "/process/kill",
            "windows_memory_stats": "/memory/stats",
            "windows_network_connections": "/network/connections",
            "windows_service_list": "/service/list",
            "windows_service_status": "/service/status",
            "windows_ocr_screens_all": "/ocr/screens/all",
            "windows_ocr_screen": lambda args: f"/ocr/screen/{args.get('screen_number', 1)}",
        }
        
        if name not in tool_map:
            return {"success": False, "error": f"Unknown tool: {name}"}
        
        endpoint_info = tool_map[name]
        
        # Handle dynamic endpoints
        if callable(endpoint_info):
            endpoint = endpoint_info(arguments)
        else:
            endpoint = endpoint_info
        
        # Call the API
        result = await self._call_api(endpoint, method="GET", params=arguments)
        return result
    
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        logger.info("MCP Initialize request")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {
                "name": "windows-api-bridge",
                "version": "1.0.1-fixed"
            }
        }
    
    async def handle_list_tools(self) -> Dict[str, Any]:
        """Handle tools/list request"""
        logger.info("Listing tools")
        return {"tools": self.get_tools()}
    
    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Tool call: {name}")
        
        try:
            result = await self.execute_tool(name, arguments)
            
            # Format response
            content_text = json.dumps(result, indent=2)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": content_text
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Tool execution error: {str(e)}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"success": False, "error": str(e)}, indent=2)
                    }
                ],
                "isError": True
            }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return await self.handle_initialize(params)
        elif method == "tools/list":
            return await self.handle_list_tools()
        elif method == "tools/call":
            return await self.handle_call_tool(params)
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    async def run(self):
        """Main MCP server loop - read from stdin, write to stdout"""
        logger.info(f"Windows API MCP Bridge starting (FIXED version)...")
        logger.info(f"Backend: {WINDOWS_API_URL}")
        logger.info(f"Automation available: {AUTOMATION_AVAILABLE}")
        logger.info(f"Window control available: {WIN32_AVAILABLE}")
        logger.info("Ready for MCP requests")
        
        # Read from stdin line by line
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Read one line from stdin
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                # Parse JSON-RPC request
                request = json.loads(line)
                
                # Handle request
                result = await self.handle_request(request)
                
                # Build proper JSON-RPC response
                if "error" in result:
                    # Error response
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": result["error"]
                    }
                else:
                    # Success response - wrap in "result"
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": result
                    }
                
                # Write response to stdout
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
        
        # Cleanup
        if self.session:
            await self.session.close()
        
        logger.info("Windows API MCP Bridge shutting down")


async def main():
    """Main entry point"""
    bridge = WindowsAPIMCPBridge()
    await bridge.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
