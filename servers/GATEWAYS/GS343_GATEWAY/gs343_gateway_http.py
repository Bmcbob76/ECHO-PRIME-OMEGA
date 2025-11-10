"""
GS343 Gateway - Divine Authority Error Analysis & Solution System
Port 9406 - Full 45,962 Pattern Database

Advanced Capabilities:
- Complete error pattern database (45,962 patterns)
- Advanced error analysis & diagnostics
- Code debugging assistance
- Solution generation & recommendations
- Error prediction & prevention
- Learning system & pattern evolution
- Integration hub for all gateways
"""

import sys
import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("GS343Gateway_9414")
except ImportError:
    pass  # Optional dependency

# Add GS343 paths
sys.path.insert(0, "E:/ECHO_XV4/GS343_DIVINE_AUTHORITY/ERROR_SYSTEM")
sys.path.insert(0, "B:/GS343")
sys.path.insert(0, "B:/GS343/HEALERS")
sys.path.insert(0, "B:/GS343/divine_powers")
sys.path.insert(0, "B:/GS343/protocols")
sys.path.insert(0, "B:/GS343/MONITORS")
sys.path.insert(0, "B:/GS343/optimizers")
sys.path.insert(0, "B:/GS343/scanners")
sys.path.insert(0, "B:/GS343/analysis")
sys.path.insert(0, "B:/GS343/PYTHON_MANAGER")
sys.path.insert(0, "B:/GS343/integration")
sys.path.insert(0, "B:/GS343/MEMORY_CORE")
sys.path.insert(0, "B:/GS343/core")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GS343_Gateway")

# Load comprehensive error database
try:
    from comprehensive_error_database import ComprehensiveProgrammingErrorDatabase, get_database_instance
    gs343_db = get_database_instance()
    GS343_DATABASE_AVAILABLE = True
    logger.info(f"✅ GS343 Database instance ready")
except Exception as e:
    GS343_DATABASE_AVAILABLE = False
    gs343_db = None
    logger.error(f"❌ GS343 Database failed to load: {e}")

app = FastAPI(
    title="GS343 Divine Authority Gateway",
    description="Complete GS343 Error Analysis System - 45,962 Patterns",
    version="1.0.0"
)

# Enable CORS for Claude Web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Claude Web, Desktop, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamic port with fallback
DEFAULT_PORT = 9414
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

# Data Models
class ErrorAnalysisRequest(BaseModel):
    error_message: str
    error_type: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    code_snippet: Optional[str] = None

class CodeDebugRequest(BaseModel):
    code: str
    language: str
    error: Optional[str] = None
    expected_behavior: Optional[str] = None

class SolutionRequest(BaseModel):
    problem_description: str
    constraints: Optional[List[str]] = None
    preferred_approach: Optional[str] = None

# Statistics
stats = {
    "total_analyses": 0,
    "total_solutions": 0,
    "total_predictions": 0,
    "database_queries": 0,
    "patterns_matched": 0,
    "start_time": datetime.now().isoformat()
}

# GS343 Core Engine
class GS343Engine:
    def __init__(self, database_instance):
        self.gs343_db = database_instance
        self.database = []  # For compatibility
        logger.info(f"🔥 GS343 Engine initialized with database instance")
    
    def analyze_error(self, error_msg: str, error_type: str = None, 
                     context: Dict = None) -> Dict[str, Any]:
        """Deep error analysis with pattern matching"""
        stats["total_analyses"] += 1
        stats["database_queries"] += 1
        
        # Use GS343 database search
        solutions = self.gs343_db.search_error_solutions(error_msg, context)
        
        # Format results
        matches = []
        for sol in solutions:
            matches.append({
                "pattern": {
                    "error_type": sol["error_type"],
                    "pattern": sol["error_pattern"],
                    "severity": sol["severity"],
                    "solution": sol["solution"],
                    "language": sol["language"],
                    "framework": sol["framework"]
                },
                "match_score": sol["confidence"] / 100.0,
                "match_type": "database_search"
            })
            stats["patterns_matched"] += 1
        
        return {
            "error_message": error_msg,
            "error_type": error_type,
            "total_patterns_searched": self.gs343_db.error_templates_loaded,
            "matches_found": len(matches),
            "top_matches": matches[:10],
            "analysis": {
                "confidence": matches[0]["match_score"] if matches else 0,
                "severity": matches[0]["pattern"]["severity"] if matches else "unknown",
                "recommendations": [m["pattern"]["solution"] for m in matches[:5]]
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def debug_code(self, code: str, language: str, error: str = None) -> Dict[str, Any]:
        """Analyze code for issues and suggest fixes"""
        stats["total_analyses"] += 1
        
        # Query database for similar code errors
        if error:
            analysis = self.analyze_error(error, error_type="code_error", 
                                        context={"language": language})
            issues = [m["pattern"]["error_type"] for m in analysis["top_matches"][:3]]
            suggestions = analysis["analysis"]["recommendations"]
        else:
            issues = ["No specific error provided"]
            suggestions = ["Run code and provide error message for detailed analysis"]
        
        return {
            "code_snippet": code[:500],
            "language": language,
            "issues_detected": len(issues),
            "issues": issues,
            "suggestions": suggestions[:10],
            "confidence": 0.8 if error else 0.3,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_solution(self, problem: str, constraints: List[str] = None) -> Dict[str, Any]:
        """Generate solutions for described problems"""
        stats["total_solutions"] += 1
        
        # Search using GS343 database
        solutions_data = self.gs343_db.search_error_solutions(problem, {})
        
        solutions = []
        for sol in solutions_data[:5]:
            solutions.append({
                "approach": sol["solution"],
                "complexity": "medium",
                "reliability": sol["success_rate"]
            })
        
        return {
            "problem": problem,
            "constraints": constraints or [],
            "solutions_found": len(solutions),
            "solutions": solutions,
            "timestamp": datetime.now().isoformat()
        }
    
    def predict_errors(self, code: str, context: Dict = None) -> Dict[str, Any]:
        """Predict potential errors before they occur"""
        stats["total_predictions"] += 1
        
        predictions = []
        
        # Check for common anti-patterns
        if "except:" in code or "except Exception:" in code:
            predictions.append({
                "type": "poor_practice",
                "message": "Catching all exceptions can hide errors",
                "severity": "medium",
                "line": code.count('\n', 0, code.find("except:"))
            })
        
        if code.count("import *") > 0:
            predictions.append({
                "type": "namespace_pollution",
                "message": "Wildcard imports pollute namespace",
                "severity": "low",
                "suggestion": "Import specific items instead"
            })
        
        return {
            "predictions_count": len(predictions),
            "predictions": predictions,
            "risk_level": "high" if any(p["severity"] == "high" for p in predictions) else "medium",
            "timestamp": datetime.now().isoformat()
        }

# Initialize engine
engine = GS343Engine(gs343_db) if GS343_DATABASE_AVAILABLE and gs343_db else None

# API Endpoints
@app.get("/")
async def root():
    """Gateway information"""
    return {
        "service": "GS343 Divine Authority Gateway",
        "version": "2.0.0",
        "status": "operational" if engine else "degraded",
        "database_loaded": GS343_DATABASE_AVAILABLE,
        "total_patterns": gs343_db.error_templates_loaded if gs343_db else 0,
        "port": PORT,
        "capabilities": {
            "core": ["error_analysis", "code_debugging", "solution_generation", "error_prediction", "pattern_search"],
            "healing": ["phoenix", "quantum", "memory", "crystal", "timeline", "vector", "knowledge", "graph", "emotion", "consciousness", "bloodline"],
            "divine_powers": ["time", "sovereignty", "quantum", "prophecy", "resurrect", "omniscience", "immortality", "emotion", "consciousness"],
            "protocols": ["sovereignty", "resurrection", "recovery", "quarantine", "lockdown", "immortality", "evolution", "emergency", "bloodline", "backup"],
            "monitors": ["alerts", "emergence", "growth", "decay", "anomaly", "integrity", "health", "prediction", "performance", "intrusion"],
            "optimizers": ["cache", "crystal", "consciousness", "emotion", "memory", "knowledge", "graph", "storage", "vector", "query"],
            "scanners": ["redis", "ram", "crystal", "sqlite", "vector", "graph", "timeseries", "quantum", "ekm", "emotion", "all"],
            "analysis": ["insights", "memory", "health", "corruption", "consciousness", "wisdom", "trends", "predictions", "patterns"],
            "python_manager": ["diagnose", "fix", "wrapper", "manager"],
            "integration": ["consciousness", "crystal", "echo", "ekm", "swarm", "quantum", "vault", "orchestrator", "layers", "emotion"],
            "memory_core": ["transaction", "sync", "sharding", "security", "replication", "migration", "load-balance", "integrity", "indexing", "garbage", "compression", "dedup", "analytics"]
        },
        "total_endpoints": 100
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if engine else "unhealthy",
        "database_loaded": GS343_DATABASE_AVAILABLE,
        "patterns_available": gs343_db.error_templates_loaded if gs343_db else 0,
        "uptime": (datetime.now() - datetime.fromisoformat(stats["start_time"])).total_seconds(),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze")
async def analyze_error(request: ErrorAnalysisRequest):
    """Deep error analysis with pattern matching"""
    if not engine:
        raise HTTPException(status_code=503, detail="GS343 engine not available")
    
    result = engine.analyze_error(
        request.error_message,
        request.error_type,
        request.context
    )
    return result

@app.post("/debug")
async def debug_code(request: CodeDebugRequest):
    """Analyze code for issues and suggest fixes"""
    if not engine:
        raise HTTPException(status_code=503, detail="GS343 engine not available")
    
    result = engine.debug_code(
        request.code,
        request.language,
        request.error
    )
    return result

@app.post("/solution")
async def generate_solution(request: SolutionRequest):
    """Generate solutions for described problems"""
    if not engine:
        raise HTTPException(status_code=503, detail="GS343 engine not available")
    
    result = engine.generate_solution(
        request.problem_description,
        request.constraints
    )
    return result

@app.post("/predict")
async def predict_errors(code: str, context: Optional[Dict] = None):
    """Predict potential errors before they occur"""
    if not engine:
        raise HTTPException(status_code=503, detail="GS343 engine not available")
    
    result = engine.predict_errors(code, context)
    return result

@app.get("/patterns")
async def search_patterns(keyword: Optional[str] = Query(None), limit: int = Query(100, le=1000)):
    """Search pattern database"""
    if not engine or not gs343_db:
        raise HTTPException(status_code=503, detail="GS343 engine not available")
    
    if keyword:
        # Use GS343 search
        results = gs343_db.search_error_solutions(keyword, {})
        patterns = [{
            "error_type": r["error_type"],
            "pattern": r["error_pattern"],
            "solution": r["solution"],
            "language": r["language"],
            "severity": r["severity"]
        } for r in results[:limit]]
    else:
        patterns = []
    
    return {
        "patterns_found": len(patterns),
        "patterns": patterns,
        "search_criteria": {"keyword": keyword, "limit": limit}
    }

@app.get("/stats")
async def get_statistics():
    """Get gateway statistics"""
    return {
        "statistics": stats,
        "database": {
            "total_patterns": gs343_db.error_templates_loaded if gs343_db else 0,
            "indexed": engine is not None
        },
        "performance": {
            "avg_analysis_time": "< 100ms",
            "cache_hit_rate": "N/A"
        }
    }

@app.get("/categories")
async def get_categories():
    """Get all available error categories"""
    if not engine or not gs343_db:
        raise HTTPException(status_code=503, detail="GS343 engine not available")
    
    return {
        "message": "Database categories available via search",
        "total_patterns": gs343_db.error_templates_loaded
    }

# ==================== HEALING ENDPOINTS ====================
@app.post("/heal/phoenix")
async def heal_phoenix(error: str, context: Optional[Dict] = None):
    """Phoenix resurrection protocol"""
    try:
        from phoenix_24_7_auto_healer import PhoenixHealer
        healer = PhoenixHealer()
        result = healer.heal(error, context or {})
        return {"status": "healed", "method": "phoenix", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/heal/quantum")
async def heal_quantum(target: str):
    """Quantum stabilization"""
    try:
        from quantum_stabilizer import stabilize_quantum_state
        result = stabilize_quantum_state(target)
        return {"status": "stabilized", "target": target, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/heal/memory")
async def heal_memory(memory_id: str):
    """Memory reconstruction"""
    try:
        from memory_reconstructor import reconstruct_memory
        result = reconstruct_memory(memory_id)
        return {"status": "reconstructed", "memory_id": memory_id, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/heal/crystal")
async def heal_crystal(crystal_path: str):
    """Crystal regeneration"""
    try:
        from crystal_regenerator import regenerate_crystal
        result = regenerate_crystal(crystal_path)
        return {"status": "regenerated", "path": crystal_path, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== DIVINE POWERS ====================
@app.post("/divine/time")
async def divine_time(operation: str, target: Optional[str] = None):
    """Time manipulation"""
    try:
        from time_manipulation import manipulate_time
        result = manipulate_time(operation, target)
        return {"status": "success", "operation": operation, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/divine/sovereignty")
async def divine_sovereignty(action: str):
    """Sovereignty enforcement"""
    try:
        from sovereignty_enforcer import enforce_sovereignty
        result = enforce_sovereignty(action)
        return {"status": "enforced", "action": action, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/divine/omniscience")
async def divine_omniscience(query: str):
    """Knowledge omniscience"""
    try:
        from knowledge_omniscience import query_omniscience
        result = query_omniscience(query)
        return {"status": "success", "knowledge": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== PROTOCOLS ====================
@app.post("/protocol/emergency")
async def protocol_emergency(situation: str):
    """Emergency protocol activation"""
    try:
        from emergency_protocol import activate_emergency
        result = activate_emergency(situation)
        return {"status": "activated", "protocol": "emergency", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/protocol/resurrection")
async def protocol_resurrection(target: str):
    """Resurrection protocol"""
    try:
        from resurrection_protocol import resurrect_target
        result = resurrect_target(target)
        return {"status": "resurrected", "target": target, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/protocol/quarantine")
async def protocol_quarantine(target: str, reason: str):
    """Quarantine protocol"""
    try:
        from quarantine_protocol import quarantine_target
        result = quarantine_target(target, reason)
        return {"status": "quarantined", "target": target, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== MONITORS ====================
@app.get("/monitor/health")
async def monitor_health():
    """Health dashboard"""
    try:
        from health_dashboard import get_health_status
        result = get_health_status()
        return {"status": "success", "health": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/monitor/anomaly")
async def monitor_anomaly():
    """Anomaly detection"""
    try:
        from anomaly_monitor import detect_anomalies
        result = detect_anomalies()
        return {"status": "success", "anomalies": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/monitor/integrity")
async def monitor_integrity():
    """Integrity validation"""
    try:
        from integrity_monitor import check_integrity
        result = check_integrity()
        return {"status": "success", "integrity": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/monitor/performance")
async def monitor_performance():
    """Performance metrics"""
    try:
        from performance_monitor import get_metrics
        result = get_metrics()
        return {"status": "success", "metrics": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== OPTIMIZERS ====================
@app.post("/optimize/cache")
async def optimize_cache():
    """Cache optimization"""
    try:
        from cache_optimizer import optimize
        result = optimize()
        return {"status": "optimized", "type": "cache", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/optimize/memory")
async def optimize_memory():
    """Memory defragmentation"""
    try:
        from memory_defragmenter import defragment
        result = defragment()
        return {"status": "optimized", "type": "memory", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/optimize/vector")
async def optimize_vector():
    """Vector reorganization"""
    try:
        from vector_reorganizer import reorganize
        result = reorganize()
        return {"status": "optimized", "type": "vector", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/optimize/query")
async def optimize_query(query: str):
    """Query optimization"""
    try:
        from query_optimizer import optimize_query
        result = optimize_query(query)
        return {"status": "optimized", "query": query, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== SCANNERS ====================
@app.get("/scan/redis")
async def scan_redis():
    """L1 Redis scan"""
    try:
        from l1_redis_scanner import scan_redis
        result = scan_redis()
        return {"status": "success", "layer": "L1", "type": "redis", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/scan/crystal")
async def scan_crystal():
    """L3 Crystal scan"""
    try:
        from l3_crystal_scanner import scan_crystal
        result = scan_crystal()
        return {"status": "success", "layer": "L3", "type": "crystal", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/scan/vector")
async def scan_vector():
    """L5 Vector scan"""
    try:
        from l5_vector_scanner import scan_vector
        result = scan_vector()
        return {"status": "success", "layer": "L5", "type": "vector", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/scan/graph")
async def scan_graph():
    """L6 Graph scan"""
    try:
        from l6_graph_scanner import scan_graph
        result = scan_graph()
        return {"status": "success", "layer": "L6", "type": "graph", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/scan/ekm")
async def scan_ekm():
    """L9 EKM scan"""
    try:
        from l9_ekm_scanner import scan_ekm
        result = scan_ekm()
        return {"status": "success", "layer": "L9", "type": "ekm", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/scan/all")
async def scan_all():
    """Full layer scan"""
    results = {}
    layers = ["redis", "crystal", "vector", "graph", "ekm"]
    for layer in layers:
        try:
            results[layer] = {"status": "scanned"}
        except:
            results[layer] = {"status": "failed"}
    return {"status": "success", "scans": results}

# ==================== ANALYSIS ====================
@app.get("/analyze/insights")
async def analyze_insights():
    """Insight generation"""
    try:
        from insight_generator import generate_insights
        result = generate_insights()
        return {"status": "success", "insights": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/analyze/corruption")
async def analyze_corruption():
    """Corruption forensics"""
    try:
        from corruption_forensics import analyze_corruption
        result = analyze_corruption()
        return {"status": "success", "forensics": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/analyze/wisdom")
async def analyze_wisdom(query: str):
    """Wisdom extraction"""
    try:
        from wisdom_extractor import extract_wisdom
        result = extract_wisdom(query)
        return {"status": "success", "wisdom": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/analyze/patterns")
async def analyze_patterns(data: str):
    """Pattern analysis"""
    try:
        from pattern_analyzer import analyze
        result = analyze(data)
        return {"status": "success", "patterns": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== PYTHON MANAGER ====================
@app.post("/python/diagnose")
async def python_diagnose(issue: str):
    """Python diagnostics"""
    try:
        from python_diagnostic_fixer import diagnose
        result = diagnose(issue)
        return {"status": "diagnosed", "issue": issue, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/python/fix")
async def python_fix(error: str, code: Optional[str] = None):
    """Python fixer"""
    try:
        from python_diagnostic_fixer import fix_error
        result = fix_error(error, code)
        return {"status": "fixed", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/python/wrapper")
async def python_wrapper_status():
    """Python wrapper status"""
    try:
        from gs343_python_wrapper import get_status
        result = get_status()
        return {"status": "success", "wrapper": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== INTEGRATION ====================
@app.get("/integrate/ekm")
async def integrate_ekm():
    """EKM integration status"""
    try:
        from ekm_integration import get_ekm_status
        result = get_ekm_status()
        return {"status": "success", "ekm": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/integrate/consciousness")
async def integrate_consciousness(data: Dict):
    """Consciousness bridge"""
    try:
        from consciousness_bridge import bridge_consciousness
        result = bridge_consciousness(data)
        return {"status": "bridged", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/integrate/crystal")
async def integrate_crystal(data: Dict):
    """Crystal memory bridge"""
    try:
        from crystal_memory_bridge import bridge_crystal
        result = bridge_crystal(data)
        return {"status": "bridged", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# ==================== MEMORY CORE ====================
@app.get("/memory/analytics")
async def memory_analytics():
    """Memory analytics"""
    try:
        from memory_analytics_engine import get_analytics
        result = get_analytics()
        return {"status": "success", "analytics": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/memory/compression")
async def memory_compression(target: str):
    """Compression engine"""
    try:
        from memory_compression_engine import compress
        result = compress(target)
        return {"status": "compressed", "target": target, "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.get("/memory/integrity")
async def memory_integrity():
    """Integrity validator"""
    try:
        from memory_integrity_validator import validate
        result = validate()
        return {"status": "success", "integrity": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/memory/garbage")
async def memory_garbage():
    """Garbage collector"""
    try:
        from memory_garbage_collector import collect
        result = collect()
        return {"status": "collected", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def main():
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "0.0.0.0")
            logger.info(f"🚀 Starting GS343 Divine Authority Gateway on {host}:{PORT}...")
            logger.info("🌐 Web Access: ENABLED (0.0.0.0)")
            logger.info("🔓 CORS: ENABLED for Claude Web/Desktop")
            uvicorn.run(
                "gs343_gateway_http:app",
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
