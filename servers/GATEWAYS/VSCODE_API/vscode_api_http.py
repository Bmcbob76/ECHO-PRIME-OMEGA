"""
VS Code API HTTP Server - FastAPI Gateway
Port: 9013
Authority Level: 11.0
GS343 Foundation + Phoenix Auto-Heal Integrated
Direct VS Code programmatic control
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import httpx
from datetime import datetime
import sys

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

app = FastAPI(title="VS Code API HTTP Server", version="1.0.0")

# VS Code backend API
VSCODE_BACKEND = "http://localhost:9001"

# Initialize GS343
if GS343_AVAILABLE:
    foundation = GS343UniversalFoundation()
    healer = PhoenixAutoHeal()

class FileOpenRequest(BaseModel):
    path: str
    line: int = None
    column: int = None

class FileEditRequest(BaseModel):
    path: str
    content: str

class CommandRequest(BaseModel):
    command: str
    args: dict = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    vscode_available = False
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{VSCODE_BACKEND}/health", timeout=2.0)
            vscode_available = resp.status_code == 200
    except:
        pass
    
    return {
        "status": "healthy",
        "service": "VS Code API HTTP Server",
        "port": 9013,
        "timestamp": datetime.now().isoformat(),
        "vscode_backend_available": vscode_available,
        "gs343_available": GS343_AVAILABLE
    }

@app.post("/file/open")
async def open_file(req: FileOpenRequest):
    """Open file in VS Code"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{VSCODE_BACKEND}/file/open",
                json={"path": req.path, "line": req.line, "column": req.column},
                timeout=10.0
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/edit")
async def edit_file(req: FileEditRequest):
    """Edit file in VS Code"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{VSCODE_BACKEND}/file/edit",
                json={"path": req.path, "content": req.content},
                timeout=10.0
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/command/execute")
async def execute_command(req: CommandRequest):
    """Execute VS Code command"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{VSCODE_BACKEND}/command/execute",
                json={"command": req.command, "args": req.args},
                timeout=30.0
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🔥 VS Code API HTTP Server - Port 9013")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=9013)
