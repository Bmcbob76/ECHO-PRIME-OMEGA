"""
Desktop Commander HTTP Server - FastAPI Gateway
Port: 9012
Authority Level: 11.0
GS343 Foundation + Phoenix Auto-Heal Integrated
Complete filesystem and system control
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import subprocess
from datetime import datetime
from pathlib import Path
import sys
import os

# Add GS343 Foundation
sys.path.append("E:\\GS343\\FOUNDATION")
try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False

app = FastAPI(title="Desktop Commander HTTP Server", version="1.0.0")

# Initialize GS343
if GS343_AVAILABLE:
    foundation = GS343UniversalFoundation()
    healer = PhoenixAutoHeal()

class FileReadRequest(BaseModel):
    path: str

class FileWriteRequest(BaseModel):
    path: str
    content: str
    mode: str = "write"  # write or append

class DirectoryRequest(BaseModel):
    path: str

class CommandRequest(BaseModel):
    command: str
    shell: str = "powershell"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Desktop Commander HTTP Server",
        "port": 9012,
        "timestamp": datetime.now().isoformat(),
        "gs343_available": GS343_AVAILABLE
    }

@app.post("/file/read")
async def read_file(req: FileReadRequest):
    """Read file contents"""
    try:
        with open(req.path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"success": True, "content": content, "path": req.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/write")
async def write_file(req: FileWriteRequest):
    """Write content to file"""
    try:
        file_mode = 'a' if req.mode == "append" else 'w'
        with open(req.path, file_mode, encoding='utf-8') as f:
            f.write(req.content)
        return {"success": True, "path": req.path, "mode": req.mode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/directory/list")
async def list_directory(req: DirectoryRequest):
    """List directory contents"""
    try:
        items = []
        path = Path(req.path)
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "path": str(item)
            })
        return {"success": True, "items": items, "path": req.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/command/execute")
async def execute_command(req: CommandRequest):
    """Execute system command"""
    try:
        result = subprocess.run(
            req.command,
            shell=True,
            capture_output=True,
            text=True,
            executable=req.shell if req.shell != "powershell" else "powershell.exe"
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Process naming
    try:
        from setproctitle import setproctitle
        setproctitle("DesktopCmd_9408")
    except ImportError:
        pass
    
    import os
    PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", 9408)))
    print(f"🔥 Desktop Commander HTTP Server - Port {PORT}")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=PORT)
