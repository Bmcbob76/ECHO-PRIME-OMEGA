#!/usr/bin/env python3
"""
OMEGA SWARM BRAIN HTTP GATEWAY
Wraps P:\ECHO_PRIME\OMEGA_SWARM_BRAIN functionality as HTTP API
Port: 5200 (OMEGA Master Brain)
"""

import sys
import os

# Add OMEGA_SWARM_BRAIN to path
sys.path.insert(0, r'P:\ECHO_PRIME\OMEGA_SWARM_BRAIN')

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import uvicorn
from datetime import datetime
import asyncio

# Import OMEGA components
from omega_core import OmegaCore
from omega_swarm import SwarmIntelligence
from omega_trinity import TrinityBrain
from omega_guilds import GuildSystem
from omega_agents import AgentManager
from omega_memory import MemoryOrchestrator
from omega_integration import SystemIntegrator

app = FastAPI(title="OMEGA Swarm Brain Gateway", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global OMEGA instance
omega: Optional[OmegaCore] = None
start_time = datetime.now()

# ============================================
# REQUEST MODELS
# ============================================

class AgentCommand(BaseModel):
    agent_id: str
    command: str
    parameters: Optional[Dict[str, Any]] = {}

class SwarmTask(BaseModel):
    task_type: str
    task_data: Dict[str, Any]
    priority: Optional[int] = 5
    guild: Optional[str] = None

class TrinityQuery(BaseModel):
    query: str
    mode: str = "fused"  # fused, sage, thorne, nyx

# ============================================
# STARTUP/SHUTDOWN
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize OMEGA Swarm Brain"""
    global omega
    print("🚀 OMEGA Swarm Brain Gateway starting...")
    
    try:
        # Initialize OMEGA Core
        omega = OmegaCore()
        await omega.initialize()
        
        print("✅ OMEGA Swarm Brain online")
        print(f"   Port: 5200")
        print(f"   Max Agents: {omega.config.get('max_agents', 1200)}")
        print(f"   Trinity: SAGE, THORNE, NYX")
        
    except Exception as e:
        print(f"❌ OMEGA initialization failed: {e}")
        omega = None

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup OMEGA resources"""
    global omega
    if omega:
        await omega.shutdown()
        print("🔥 OMEGA Swarm Brain shutdown complete")

# ============================================
# HEALTH & STATUS
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "online" if omega else "initializing",
        "service": "OMEGA Swarm Brain Gateway",
        "port": 5200,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def get_status():
    """Get comprehensive OMEGA status"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        uptime = (datetime.now() - start_time).total_seconds()
        
        status = {
            "online": True,
            "uptime_seconds": uptime,
            "total_agents": omega.agent_manager.get_agent_count(),
            "max_agents": omega.config.get('max_agents', 1200),
            "trinity_harmony": omega.trinity.get_harmony_level(),
            "guilds": omega.guild_system.get_guild_status(),
            "swarm_intelligence": omega.swarm.get_swarm_metrics(),
            "memory_stats": omega.memory.get_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status error: {str(e)}")

# ============================================
# AGENT MANAGEMENT
# ============================================

@app.get("/agents/list")
async def list_agents():
    """List all active agents"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        agents = omega.agent_manager.list_agents()
        return {"agents": agents, "count": len(agents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/command")
async def send_agent_command(command: AgentCommand):
    """Send command to specific agent"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        result = await omega.agent_manager.send_command(
            command.agent_id,
            command.command,
            command.parameters
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# SWARM INTELLIGENCE
# ============================================

@app.post("/swarm/task")
async def submit_swarm_task(task: SwarmTask):
    """Submit task to swarm intelligence"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        task_id = await omega.swarm.submit_task(
            task_type=task.task_type,
            task_data=task.task_data,
            priority=task.priority,
            guild=task.guild
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "status": "queued"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/swarm/metrics")
async def get_swarm_metrics():
    """Get swarm intelligence metrics"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        metrics = omega.swarm.get_swarm_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# TRINITY BRAIN
# ============================================

@app.post("/trinity/query")
async def trinity_query(query: TrinityQuery):
    """Query Trinity consciousness"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        if query.mode == "fused":
            response = await omega.trinity.fused_response(query.query)
        elif query.mode == "sage":
            response = await omega.trinity.sage_response(query.query)
        elif query.mode == "thorne":
            response = await omega.trinity.thorne_response(query.query)
        elif query.mode == "nyx":
            response = await omega.trinity.nyx_response(query.query)
        else:
            raise ValueError(f"Invalid mode: {query.mode}")
        
        return {
            "success": True,
            "mode": query.mode,
            "response": response,
            "harmony": omega.trinity.get_harmony_level()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trinity/harmony")
async def get_trinity_harmony():
    """Get Trinity harmony level"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        harmony = omega.trinity.get_harmony_level()
        return {
            "harmony": harmony,
            "sage": omega.trinity.sage_activity,
            "thorne": omega.trinity.thorne_activity,
            "nyx": omega.trinity.nyx_activity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# GUILD SYSTEM
# ============================================

@app.get("/guilds/list")
async def list_guilds():
    """List all guilds"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        guilds = omega.guild_system.list_guilds()
        return {"guilds": guilds}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/guilds/{guild_name}/status")
async def get_guild_status(guild_name: str):
    """Get guild status"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        status = omega.guild_system.get_guild_status(guild_name)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# MEMORY OPERATIONS
# ============================================

@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory orchestrator stats"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        stats = omega.memory.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/store")
async def store_memory(data: Dict[str, Any]):
    """Store memory"""
    if not omega:
        raise HTTPException(status_code=503, detail="OMEGA not initialized")
    
    try:
        memory_id = await omega.memory.store(data)
        return {"success": True, "memory_id": memory_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("🧠 OMEGA Swarm Brain HTTP Gateway")
    print("=" * 50)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5200,
        log_level="info"
    )
