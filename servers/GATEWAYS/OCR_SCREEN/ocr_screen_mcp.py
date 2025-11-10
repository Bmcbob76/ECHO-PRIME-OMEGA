"""
OCR Screen Server - MLS Gateway for Screen Capture with OCR
Provides screen capture and text extraction capabilities to Claude
Manual MCP Protocol Implementation for Python 3.14 Compatibility
"""

import asyncio
import json
import sys
import base64
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

# Add parent to path for shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import shared utilities
try:
    from GATEWAYS.GS343_GATEWAY.utils.logging_config import setup_logger
    from GATEWAYS.GS343_GATEWAY.utils.debug_utils import DebugContext
except ImportError:
    def setup_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger
    class DebugContext:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

logger = setup_logger("OCR_SCREEN_SERVER")

# Try to import screen capture and OCR libraries
try:
    from PIL import ImageGrab, Image
    import pytesseract
    from mss import mss
    OCR_AVAILABLE = True
    MSS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"OCR libraries not available: {e}")
    OCR_AVAILABLE = False
    MSS_AVAILABLE = False

class OCRScreenMCPServer:
    def __init__(self) -> None:
        self.sct = None
        if MSS_AVAILABLE:
            try:
                self.sct = mss()
            except Exception as e:
                logger.warning(f"Failed to initialize MSS: {e}")
                self.sct = None

    def get_monitor_info(self) -> List[Dict[str, Any]]:
        """Get information about all connected monitors"""
        if not self.sct:
            return []
        
        monitors = []
        for i, mon in enumerate(self.sct.monitors):
            if i == 0:  # Skip the "all monitors" entry
                continue
            monitors.append({
                "index": i,
                "left": mon["left"],
                "top": mon["top"],
                "width": mon["width"],
                "height": mon["height"]
            })
        return monitors

    def get_tools(self):
        """List available OCR screen tools"""
        tools = []
        
        if OCR_AVAILABLE:
            tools.extend([
                {
                    "name": "list_monitors",
                    "description": "List all connected monitors with their index, position and resolution. Monitor index 1-4 can be used with capture_screen and ocr_screen.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "capture_screen",
                    "description": "Capture current screen or specific region. Returns image as base64. Use monitor parameter (1-4) to capture specific monitor.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "monitor": {"type": "number", "description": "Monitor index (1-4) to capture. Omit to capture all monitors."},
                            "x": {"type": "number", "description": "Top-left X coordinate (optional, relative to monitor if specified)"},
                            "y": {"type": "number", "description": "Top-left Y coordinate (optional, relative to monitor if specified)"},
                            "width": {"type": "number", "description": "Width of capture region (optional)"},
                            "height": {"type": "number", "description": "Height of capture region (optional)"}
                        }
                    }
                },
                {
                    "name": "ocr_screen",
                    "description": "Capture screen and extract text using OCR. Returns extracted text. Use monitor parameter (1-4) to capture specific monitor.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "monitor": {"type": "number", "description": "Monitor index (1-4) to capture. Omit to capture all monitors."},
                            "x": {"type": "number", "description": "Top-left X coordinate (optional, relative to monitor if specified)"},
                            "y": {"type": "number", "description": "Top-left Y coordinate (optional, relative to monitor if specified)"},
                            "width": {"type": "number", "description": "Width of capture region (optional)"},
                            "height": {"type": "number", "description": "Height of capture region (optional)"},
                            "lang": {"type": "string", "description": "OCR language (default: eng)", "default": "eng"}
                        }
                    }
                },
                {
                    "name": "ocr_image",
                    "description": "Extract text from an image file using OCR",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "image_path": {"type": "string", "description": "Path to image file"},
                            "lang": {"type": "string", "description": "OCR language (default: eng)", "default": "eng"}
                        },
                        "required": ["image_path"]
                    }
                }
            ])
        else:
            tools.append({
                "name": "ocr_status",
                "description": "Check OCR system status and requirements",
                "inputSchema": {"type": "object", "properties": {}}
            })
        
        return tools

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        with DebugContext(f"Tool: {name}", logger):
            try:
                if not OCR_AVAILABLE and name != "ocr_status":
                    return {"success": False, "error": "ERROR: OCR libraries not installed. Install: pip install pillow pytesseract"}
                
                if name == "list_monitors":
                    return await self.list_monitors()
                elif name == "capture_screen":
                    return await self.capture_screen(arguments or {})
                elif name == "ocr_screen":
                    return await self.ocr_screen(arguments or {})
                elif name == "ocr_image":
                    return await self.ocr_image(arguments or {})
                elif name == "ocr_status":
                    return await self.ocr_status()
                else:
                    return {"success": False, "error": f"Unknown tool: {name}"}
                    
            except Exception as e:
                logger.error(f"Tool execution failed: {e}", exc_info=True)
                return {"success": False, "error": f"ERROR: {str(e)}"}

    async def list_monitors(self) -> Dict[str, Any]:
        """List all connected monitors"""
        try:
            if not self.sct:
                return {"success": False, "error": "Multi-monitor support not available"}
            
            monitors = self.get_monitor_info()
            
            result = f"Found {len(monitors)} monitor(s):\n\n"
            for mon in monitors:
                result += f"Monitor {mon['index']}: {mon['width']}x{mon['height']} at ({mon['left']}, {mon['top']})\n"
            
            logger.info(f"Listed {len(monitors)} monitors")
            
            return {
                "success": True,
                "content": result,
                "monitors": monitors
            }
        except Exception as e:
            logger.error(f"List monitors failed: {e}")
            return {"success": False, "error": f"List monitors failed: {str(e)}"}

    async def capture_screen(self, args: dict) -> Dict[str, Any]:
        """Capture screen or region"""
        try:
            monitor_index = args.get('monitor')
            
            # Use MSS for monitor-specific capture if available and monitor specified
            if monitor_index and self.sct:
                if monitor_index < 1 or monitor_index >= len(self.sct.monitors):
                    return {"success": False, "error": f"Invalid monitor index: {monitor_index}. Use list_monitors to see available monitors."}
                
                # Get monitor bbox
                mon = self.sct.monitors[monitor_index]
                
                # Apply region offset if specified (relative to monitor)
                if all(k in args for k in ['x', 'y', 'width', 'height']):
                    x, y, w, h = args['x'], args['y'], args['width'], args['height']
                    bbox = {
                        "left": mon["left"] + x,
                        "top": mon["top"] + y,
                        "width": w,
                        "height": h
                    }
                else:
                    bbox = mon
                
                # Capture with MSS
                sct_img = self.sct.grab(bbox)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
                
                logger.info(f"Captured monitor {monitor_index}: {img.size}")
            else:
                # Fallback to PIL ImageGrab
                bbox = None
                if all(k in args for k in ['x', 'y', 'width', 'height']):
                    x, y, w, h = args['x'], args['y'], args['width'], args['height']
                    bbox = (x, y, x + w, y + h)
                
                img = ImageGrab.grab(bbox=bbox)
                logger.info(f"Screen captured: {img.size}")
            
            # Convert to base64
            from io import BytesIO
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "success": True,
                "content": img_base64,
                "mimeType": "image/png"
            }
        except Exception as e:
            logger.error(f"Screen capture failed: {e}")
            return {"success": False, "error": f"Screen capture failed: {str(e)}"}

    async def ocr_screen(self, args: dict) -> Dict[str, Any]:
        """Capture screen and extract text"""
        try:
            monitor_index = args.get('monitor')
            
            # Use MSS for monitor-specific capture if available and monitor specified
            if monitor_index and self.sct:
                if monitor_index < 1 or monitor_index >= len(self.sct.monitors):
                    return {"success": False, "error": f"Invalid monitor index: {monitor_index}. Use list_monitors to see available monitors."}
                
                # Get monitor bbox
                mon = self.sct.monitors[monitor_index]
                
                # Apply region offset if specified (relative to monitor)
                if all(k in args for k in ['x', 'y', 'width', 'height']):
                    x, y, w, h = args['x'], args['y'], args['width'], args['height']
                    bbox = {
                        "left": mon["left"] + x,
                        "top": mon["top"] + y,
                        "width": w,
                        "height": h
                    }
                else:
                    bbox = mon
                
                # Capture with MSS
                sct_img = self.sct.grab(bbox)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
                
                logger.info(f"Captured monitor {monitor_index} for OCR: {img.size}")
            else:
                # Fallback to PIL ImageGrab
                bbox = None
                if all(k in args for k in ['x', 'y', 'width', 'height']):
                    x, y, w, h = args['x'], args['y'], args['width'], args['height']
                    bbox = (x, y, x + w, y + h)
                
                img = ImageGrab.grab(bbox=bbox)
                logger.info(f"Screen captured for OCR: {img.size}")
            
            # Extract text
            lang = args.get('lang', 'eng')
            text = pytesseract.image_to_string(img, lang=lang)
            
            logger.info(f"OCR extracted {len(text)} characters from screen")
            
            return {
                "success": True,
                "content": f"Extracted text:\n{text}"
            }
        except Exception as e:
            logger.error(f"OCR screen failed: {e}")
            return {"success": False, "error": f"OCR screen failed: {str(e)}"}

    async def ocr_image(self, args: dict) -> Dict[str, Any]:
        """Extract text from image file"""
        try:
            image_path = Path(args['image_path'])
            if not image_path.exists():
                return {"success": False, "error": f"Image not found: {image_path}"}
            
            # Open image
            img = Image.open(image_path)
            
            # Extract text
            lang = args.get('lang', 'eng')
            text = pytesseract.image_to_string(img, lang=lang)
            
            logger.info(f"OCR extracted {len(text)} characters from {image_path.name}")
            
            return {
                "success": True,
                "content": f"Extracted text from {image_path.name}:\n{text}"
            }
        except Exception as e:
            logger.error(f"OCR image failed: {e}")
            return {"success": False, "error": f"OCR image failed: {str(e)}"}

    async def ocr_status(self) -> Dict[str, Any]:
        """Check OCR status"""
        status = {
            "ocr_available": OCR_AVAILABLE,
            "required_packages": ["pillow", "pytesseract"],
            "install_command": "pip install pillow pytesseract",
            "tesseract_required": "Also requires Tesseract-OCR binary installed"
        }
        
        return {
            "success": True,
            "content": json.dumps(status, indent=2)
        }

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05", 
            "capabilities": {"tools": {}}, 
            "serverInfo": {"name": "ocr-screen-server", "version": "1.0.0"}
        }

    async def handle_list_tools(self) -> Dict[str, Any]:
        return {"tools": self.get_tools()}

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments", {})
        result = await self.execute_tool(name, arguments)
        
        if result.get("success"):
            return {
                "content": [{"type": "text", "text": result.get("content", "Success")}],
                "isError": False
            }
        else:
            return {
                "content": [{"type": "text", "text": result.get("error", "Unknown error")}],
                "isError": True
            }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return await self.handle_initialize(params)
        elif method == "tools/list":
            return await self.handle_list_tools()
        elif method == "tools/call":
            return await self.handle_call_tool(params)
        else:
            return {"error": {"code": -32601, "message": f"Method not found: {method}"}}

    async def run(self) -> None:
        """Main MCP server loop"""
        logger.info("🔍 OCR Screen Server starting...")
        logger.info(f"OCR Available: {OCR_AVAILABLE}")
        
        loop = asyncio.get_event_loop()
        while True:
            try:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                request = json.loads(line)
                result = await self.handle_request(request)
                
                if "error" in result:
                    response = {"jsonrpc": "2.0", "id": request.get("id"), "error": result["error"]}
                else:
                    response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
                
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                # Invalid JSON, send error response
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                # General error handling
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

async def main():
    server = OCRScreenMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)
