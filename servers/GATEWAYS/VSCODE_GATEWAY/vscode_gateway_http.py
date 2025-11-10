#!/usr/bin/env python3
"""
VS Code Gateway HTTP Server - FastAPI Gateway
Port: 9415
Authority Level: 11.0
GS343 Foundation + Phoenix Auto-Heal Integrated
Provides VS Code Extension API Integration
"""

import os
import sys
import time
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import httpx

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("VSCodeGateway_9415")
except ImportError:
    pass  # Optional dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VSCodeGateway")

# Dynamic port with fallback
DEFAULT_PORT = 9415
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

app = FastAPI(
    title="VS Code Gateway HTTP Server", 
    version="1.0.0",
    description="VS Code Extension API Integration Gateway"
)

# Enable CORS for Claude Web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

app = FastAPI(title="VS Code Gateway HTTP Server", version="1.0.0")

# VS Code Extension API endpoint
VSCODE_API_BASE = "http://localhost:3000"

# Initialize GS343
if GS343_AVAILABLE:
    foundation = GS343UniversalFoundation()
    healer = PhoenixAutoHeal()

class FileOperation(BaseModel):
    path: str
    content: str = None
    line: int = None
    column: int = None

class CommandRequest(BaseModel):
    command: str
    args: dict = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check VS Code API availability
    vscode_available = False
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{VSCODE_API_BASE}/health", timeout=2.0)
            vscode_available = resp.status_code == 200
    except:
        pass
    
    return {
        "status": "ok",
        "service": "VS Code Gateway HTTP Server",
        "port": PORT,
        "timestamp": datetime.now().isoformat(),
        "vscode_api_available": vscode_available,
        "gs343_available": GS343_AVAILABLE
    }

@app.post("/file/open")
async def open_file(req: FileOperation):
    """Open file in VS Code"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{VSCODE_API_BASE}/file/open",
                json={"path": req.path, "line": req.line, "column": req.column},
                timeout=10.0
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/save")
async def save_file(req: FileOperation):
    """Save file in VS Code"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{VSCODE_API_BASE}/file/save",
                json={"path": req.path, "content": req.content},
                timeout=10.0
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/command")
async def execute_command(req: CommandRequest):
    """Execute VS Code command"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{VSCODE_API_BASE}/command",
                json={"command": req.command, "args": req.args},
                timeout=30.0
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "127.0.0.1")
            logger.info(f"🚀 Starting VS Code Gateway HTTP Server on {host}:{PORT}")
            print("=" * 60)
            uvicorn.run(
                "vscode_gateway_http:app",
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
