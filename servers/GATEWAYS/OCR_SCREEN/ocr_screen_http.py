#!/usr/bin/env python3
"""
OCR Screen HTTP Server - FastAPI Gateway
Port: 9416
Authority Level: 11.0
GS343 Foundation + Phoenix Auto-Heal Integrated
"""

import os
import sys
import time
import logging
import base64
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("OCRScreen_9416")
except ImportError:
    pass  # Optional dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OCRScreen")

# Dynamic port with fallback
DEFAULT_PORT = 9416
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

# Import OCR libraries
try:
    from PIL import ImageGrab, Image
    import pytesseract
    import io
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

app = FastAPI(
    title="OCR Screen HTTP Server", 
    version="1.0.0",
    description="OCR Screen Capture and Text Extraction Gateway"
)

# Enable CORS for Claude Web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GS343
if GS343_AVAILABLE:
    foundation = GS343UniversalFoundation()
    healer = PhoenixAutoHeal()

class CaptureRequest(BaseModel):
    region: dict = None  # {"x": 0, "y": 0, "width": 1920, "height": 1080}
    ocr: bool = True

class ScreenshotRequest(BaseModel):
    region: dict = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "OCR Screen HTTP Server",
        "port": PORT,
        "timestamp": datetime.now().isoformat(),
        "ocr_available": OCR_AVAILABLE,
        "gs343_available": GS343_AVAILABLE
    }

@app.post("/capture")
async def capture_screen(request: CaptureRequest):
    """Capture screen with optional OCR"""
    if not OCR_AVAILABLE:
        raise HTTPException(status_code=503, detail="OCR libraries not available")
    
    try:
        # Capture screen
        if request.region:
            bbox = (
                request.region.get("x", 0),
                request.region.get("y", 0),
                request.region.get("x", 0) + request.region.get("width", 1920),
                request.region.get("y", 0) + request.region.get("height", 1080)
            )
            screenshot = ImageGrab.grab(bbox=bbox)
        else:
            screenshot = ImageGrab.grab()
        
        # Convert to base64
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        result = {
            "success": True,
            "image_base64": img_base64,
            "width": screenshot.width,
            "height": screenshot.height
        }
        
        # OCR if requested
        if request.ocr:
            text = pytesseract.image_to_string(screenshot)
            result["text"] = text
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/screenshot")
async def take_screenshot(request: ScreenshotRequest):
    """Take screenshot without OCR"""
    return await capture_screen(CaptureRequest(region=request.region, ocr=False))

def main():
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "127.0.0.1")
            logger.info(f"🚀 Starting OCR Screen HTTP Server on {host}:{PORT}")
            print("=" * 60)
            uvicorn.run(
                "ocr_screen_http:app",
                host=host,
                port=PORT,
                reload=False,
                access_log=False,
                log_level="info"
            )
        except Exception as e:
            logger.error(f"❌ Server crashed: {e}. Restarting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
