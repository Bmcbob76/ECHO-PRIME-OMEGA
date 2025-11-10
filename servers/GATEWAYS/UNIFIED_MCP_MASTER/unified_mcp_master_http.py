#!/usr/bin/env python3
"""
UNIFIED_MCP_MASTER - HTTP Gateway (Port 9409)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Central coordination hub for all MCP servers
- Route requests to appropriate MCP endpoints
- Aggregate MCP capabilities discovery
- Master control for MCP ecosystem

Exposes:
- GET /health
- GET /mcp/servers
- POST /mcp/route { server, tool, arguments }
- GET /mcp/capabilities
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("UnifiedMCP_Gateway_9412")
except ImportError:
    pass  # Optional dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UnifiedMCPMaster")

# Dynamic port with fallback
DEFAULT_PORT = 9412
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

app = FastAPI(
    title="Unified MCP Master",
    description="Central MCP Coordination Hub",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRouteRequest(BaseModel):
    server: str
    tool: str
    arguments: Optional[Dict[str, Any]] = {}

@app.get("/health")
async def health():
    return {"status": "operational", "service": "UNIFIED_MCP_MASTER", "port": PORT}

@app.get("/mcp/servers")
async def list_servers():
    return {
        "success": True,
        "servers": [
            "CRYSTAL_MEMORY_HUB",
            "DESKTOP_COMMANDER",
            "DEVELOPER_GATEWAY",
            "EPCP3O_AGENT",
            "GS343_GATEWAY",
            "HARVESTERS_GATEWAY",
            "HEALING_ORCHESTRATOR",
            "MASTER_ORCHESTRATOR_HUB",
            "MEMORY_ORCHESTRATION_SERVER",
            "NETWORK_GUARDIAN",
            "OCR_SCREEN",
            "TRAINERS_GATEWAY",
            "VOICE_SYSTEM_HUB",
            "VSCODE_API",
            "VSCODE_GATEWAY",
            "WINDOWS_GATEWAY",
            "WINDOWS_OPERATIONS"
        ],
        "count": 17
    }

@app.post("/mcp/route")
async def route_request(request: MCPRouteRequest):
    return {
        "success": True,
        "message": "Route stub - MCP routing pending",
        "server": request.server,
        "tool": request.tool,
        "routed": False
    }

@app.get("/mcp/capabilities")
async def get_capabilities():
    return {
        "success": True,
        "message": "Capabilities aggregation stub",
        "total_tools": 0,
        "servers_online": 0
    }

def main():
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "127.0.0.1")
            logger.info(f"🚀 Starting Unified MCP Master on {host}:{PORT}")
            uvicorn.run(
                "unified_mcp_master_http:app",
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
