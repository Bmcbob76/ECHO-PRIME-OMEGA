#!/usr/bin/env python3
"""
MEMORY_ORCHESTRATION_SERVER - HTTP Gateway (Port 9408)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Memory operations orchestration across all systems
- Crystal Memory Hub coordination
- G: Drive and M: Drive synchronization
- EKM generation and query routing

Exposes:
- GET /health
- POST /memory/store { content, tier?, tags? }
- POST /memory/query { query, source? }
- GET /memory/stats
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("MemoryOrch_Gateway_9413")
except ImportError:
    pass  # Optional dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MemoryOrchestrationServer")

# Dynamic port with fallback
DEFAULT_PORT = 9413
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

app = FastAPI(
    title="Memory Orchestration Server",
    description="Unified Memory Operations Gateway",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MemoryStoreRequest(BaseModel):
    content: str
    tier: Optional[str] = "M"
    tags: Optional[list] = []

class MemoryQueryRequest(BaseModel):
    query: str
    source: Optional[str] = "ALL"

@app.get("/health")
async def health():
    return {"status": "operational", "service": "MEMORY_ORCHESTRATION_SERVER", "port": PORT}

@app.post("/memory/store")
async def store_memory(request: MemoryStoreRequest):
    return {
        "success": True,
        "message": "Memory storage stub",
        "content_length": len(request.content),
        "tier": request.tier,
        "tags": request.tags
    }

@app.post("/memory/query")
async def query_memory(request: MemoryQueryRequest):
    return {
        "success": True,
        "message": "Memory query stub",
        "query": request.query,
        "source": request.source,
        "results": []
    }

@app.get("/memory/stats")
async def memory_stats():
    return {
        "success": True,
        "m_drive_crystals": 0,
        "g_drive_memories": 0,
        "total_ekm": 0,
        "sync_status": "pending"
    }

def main():
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "127.0.0.1")
            logger.info(f"🚀 Starting Memory Orchestration Server on {host}:{PORT}")
            uvicorn.run(
                "memory_orchestration_http:app",
                host=host,
                port=PORT,
                reload=False,
                access_log=False
            )
        except Exception as e:
            logger.error(f"❌ Server crashed: {e}. Restarting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
