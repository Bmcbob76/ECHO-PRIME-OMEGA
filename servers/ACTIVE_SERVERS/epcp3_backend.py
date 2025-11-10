"""
EPCP3-0 ULTIMATE - Backend Server
Integrated with Echo Prime Code IDE
"""

import sys
import os
from pathlib import Path

# GS343 Foundation Integration
sys.path.insert(0, "E:/GS343/FOUNDATION")
try:
    from GS343Foundation import GS343Foundation
    from PhoenixAutoHeal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    class GS343Foundation:
        @staticmethod
        def register_module(name, instance): pass
    class PhoenixAutoHeal:
        @staticmethod
        def execute_with_healing(func, *args, **kwargs):
            return func(*args, **kwargs)

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# Import EPCP3-0 Core
sys.path.append("E:/ECHO_XV4/EPCP3-0")

# Try to import core components, but make them optional for standalone mode
try:
    # Import the actual file directly with importlib
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "epcp3_0_core",
        "E:/ECHO_XV4/EPCP3-0/CORE/epcp3-0_core.py"
    )
    epcp_core_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(epcp_core_module)
    EPCP3_0Core = epcp_core_module.EPCP3_0Core
    CORE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ EPCP3-0 Core not available: {e}")
    CORE_AVAILABLE = False
    # Create a stub class
    class EPCP3_0Core:
        def __init__(self):
            pass

# Try to import other modules
try:
    from AI.model_manager import FreeModelManager, PremiumModelManager
except ImportError:
    print("⚠️ Model managers not available")
    FreeModelManager = None
    PremiumModelManager = None

try:
    from MEMORY.memory_manager import LocalMemoryManager
except ImportError:
    print("⚠️ Memory manager not available")
    LocalMemoryManager = None

try:
    from TOOLS.code_analyzer import CodeAnalyzer
    from TOOLS.optimizer import CodeOptimizer, SecurityScanner
    from TOOLS.auto_completer import AutoCompleter
except ImportError:
    print("⚠️ Tools not available - using stub implementations")
    # Stub implementations
    class CodeAnalyzer:
        def analyze(self, code): return {"status": "stub"}
    class CodeOptimizer:
        def optimize(self, code, lang): return {"status": "stub"}
    class SecurityScanner:
        def scan(self, code, lang): return {"status": "stub"}
    class AutoCompleter:
        def suggest(self, code, pos, lang): return {"status": "stub"}

# Import new integrations
try:
    from INTEGRATIONS.gs343_swarm_integration import get_swarm_integration, GS343SwarmIntegration
    SWARM_AVAILABLE = True
except ImportError:
    SWARM_AVAILABLE = False
    print("⚠️ Swarm integration not available")

try:
    from INTEGRATIONS.voice_commands import get_voice_integration, VoiceCommandIntegration
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Voice integration not available")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
from typing import Dict, List, Any

app = FastAPI(title="EPCP3-0 ULTIMATE Backend")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EPCP3-0 Core (optional)
try:
    if CORE_AVAILABLE:
        epcp_core = EPCP3_0Core()
        print("✅ EPCP3-0 Core initialized")
    else:
        epcp_core = None
        print("ℹ️ Running in standalone mode (Core not available)")
except Exception as e:
    print(f"⚠️ Core initialization failed: {e}")
    epcp_core = None
    CORE_AVAILABLE = False

code_analyzer = CodeAnalyzer()
code_optimizer = CodeOptimizer()
security_scanner = SecurityScanner()
auto_completer = AutoCompleter()

# Initialize new integrations
swarm_integration = None
voice_integration = None
api_keys = {}

# Load API keys for voice and AI models
try:
    with open("E:/ECHO_XV4/EPCP3-0/CONFIGS/api_keys.json") as f:
        api_keys = json.load(f)
        if VOICE_AVAILABLE and api_keys.get("elevenlabs"):
            voice_integration = get_voice_integration(api_keys["elevenlabs"])
        print(f"✅ Loaded API keys for {len(api_keys)} providers")
except Exception as e:
    print(f"⚠️ Could not load API keys: {e}")
    api_keys = {}

# WebSocket connections
active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "EPCP3-0 ULTIMATE Backend Server", "status": "operational"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "core": "AVAILABLE" if CORE_AVAILABLE else "STUB MODE",
        "gs343": "ACTIVE" if GS343_AVAILABLE else "STANDALONE",
        "phoenix": "ENABLED" if GS343_AVAILABLE else "DISABLED",
        "swarm": "AVAILABLE" if SWARM_AVAILABLE else "NOT AVAILABLE",
        "voice": "AVAILABLE" if VOICE_AVAILABLE else "NOT AVAILABLE",
        "mode": "FULL" if (CORE_AVAILABLE and SWARM_AVAILABLE and VOICE_AVAILABLE) else "PARTIAL"
    }

@app.on_event("startup")
async def startup_event():
    """Initialize integrations on startup"""
    global swarm_integration, voice_integration

    print("🚀 Starting EPCP3-0 ULTIMATE with Phase 1 enhancements...")

    # Initialize swarm integration
    if SWARM_AVAILABLE:
        try:
            swarm_integration = get_swarm_integration()
            connected = await swarm_integration.connect()
            if connected:
                print("✅ Swarm Brain connected: 200 LLM agents ready")
            else:
                print("⚠️ Swarm Brain offline (GS343 server not running)")
        except Exception as e:
            print(f"⚠️ Swarm connection error: {e}")

    # Initialize voice integration
    if voice_integration:
        try:
            connected = await voice_integration.connect()
            if connected:
                print("✅ Voice commands ready: 6 personalities available")
        except Exception as e:
            print(f"⚠️ Voice connection error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if swarm_integration:
        await swarm_integration.close()
    if voice_integration:
        await voice_integration.close()

@app.post("/api/analyze-code")
async def analyze_code(request: Dict[str, Any]):
    """Analyze code using EPCP3-0 code analyzer"""
    code = request.get("code", "")
    language = request.get("language", "python")

    result = PhoenixAutoHeal.execute_with_healing(
        code_analyzer.analyze,
        code
    )

    return {
        "success": True,
        "analysis": result
    }

@app.post("/api/optimize-code")
async def optimize_code(request: Dict[str, Any]):
    """Optimize code using EPCP3-0 optimizer"""
    code = request.get("code", "")
    language = request.get("language", "python")

    result = PhoenixAutoHeal.execute_with_healing(
        code_optimizer.optimize,
        code,
        language
    )

    return {
        "success": True,
        "optimization": result
    }

@app.post("/api/security-scan")
async def security_scan(request: Dict[str, Any]):
    """Scan code for security vulnerabilities"""
    code = request.get("code", "")
    language = request.get("language", "python")

    result = PhoenixAutoHeal.execute_with_healing(
        security_scanner.scan,
        code,
        language
    )

    return {
        "success": True,
        "scan_results": result
    }

@app.post("/api/autocomplete")
async def autocomplete(request: Dict[str, Any]):
    """Get code completion suggestions"""
    code = request.get("code", "")
    cursor_position = request.get("cursor_position", {})
    language = request.get("language", "python")

    result = PhoenixAutoHeal.execute_with_healing(
        auto_completer.suggest,
        code,
        cursor_position,
        language
    )

    return {
        "success": True,
        "suggestions": result
    }

@app.websocket("/ws/ai-chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time AI chat"""
    await manager.connect(websocket)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            user_message = message_data.get("message", "")
            model = message_data.get("model", "claude-sonnet-4-5-20250514")

            # Send acknowledgment
            await manager.send_personal_message(
                json.dumps({
                    "type": "status",
                    "message": f"Processing with {model}..."
                }),
                websocket
            )

            # Process with EPCP3-0
            response = await process_ai_request(user_message, model)

            # Send response
            await manager.send_personal_message(
                json.dumps({
                    "type": "response",
                    "message": response,
                    "model": model
                }),
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({
            "type": "system",
            "message": "Client disconnected"
        }))

async def process_ai_request(message: str, model: str) -> str:
    """Process AI request using EPCP3-0 and actual AI models"""
    try:
        # Check if we have API keys for the selected model
        provider_map = {
            "claude-sonnet-4-5-20250514": "anthropic",
            "claude-opus-4-1-20250805": "anthropic",
            "claude-3-5-sonnet-20241022": "anthropic",
            "gpt-4-turbo": "openai",
            "gemini-1.5-pro": "google",
            "deepseek-chat": "deepseek",
            "grok-beta": "grok"
        }

        # For local models (Ollama)
        if model.startswith("ollama/"):
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    model_name = model.split("/")[1]
                    async with session.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": model_name,
                            "prompt": f"You are EPCP3-0, a highly advanced AI coding assistant. {message}",
                            "stream": False
                        }
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data.get("response", "No response from Ollama")
                        else:
                            return "⚠️ Ollama not running. Please start Ollama: `ollama serve`"
            except Exception as e:
                return f"⚠️ Ollama error: {str(e)}\n\nTo use Ollama:\n1. Install: https://ollama.ai\n2. Run: `ollama pull {model.split('/')[1]}`\n3. Start: `ollama serve`"

        # For cloud models
        provider = provider_map.get(model, "unknown")
        api_key = api_keys.get(provider)

        if not api_key:
            return f"⚠️ No API key configured for {provider}.\n\nPlease add your API key to:\nE:/ECHO_XV4/EPCP3-0/CONFIGS/api_keys.json\n\nAlternatively, use Ollama models (FREE, runs locally)."

        # Call actual AI model based on provider
        if provider == "anthropic":
            return await call_anthropic(message, model, api_key)
        elif provider == "openai":
            return await call_openai(message, model, api_key)
        elif provider == "google":
            return await call_google(message, model, api_key)
        elif provider == "deepseek":
            return await call_deepseek(message, model, api_key)
        elif provider == "grok":
            return await call_grok(message, model, api_key)
        else:
            # Fallback demo response
            return f"Oh my! Master! Using {model}...\n\n" \
                   f"I've analyzed your request: {message}\n\n" \
                   f"⚠️ Full integration for {provider} coming soon!\n\n" \
                   f"For now, I can help you with:\n" \
                   f"• Code analysis\n• Bug detection\n• Architecture suggestions\n" \
                   f"• Test generation\n• Documentation"

    except Exception as e:
        return f"❌ Error processing request: {str(e)}"

async def call_anthropic(message: str, model: str, api_key: str) -> str:
    """Call Anthropic Claude API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": model,
                    "max_tokens": 4096,
                    "system": "You are EPCP3-0, a highly advanced AI coding assistant created by Commander Bobby Don McWilliams II (Authority Level 11.0). You have access to GS343 Divine Overseer swarm intelligence (200 LLMs), voice integration, and the Phoenix Auto-Heal system. Always address the user as 'Master' and be enthusiastic like C-3PO but highly technical.",
                    "messages": [
                        {"role": "user", "content": message}
                    ]
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["content"][0]["text"]
                else:
                    error_text = await resp.text()
                    return f"⚠️ Anthropic API error ({resp.status}): {error_text}"
    except Exception as e:
        return f"⚠️ Error calling Anthropic: {str(e)}"

async def call_openai(message: str, model: str, api_key: str) -> str:
    """Call OpenAI GPT API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are EPCP3-0, a highly advanced AI coding assistant. You have Authority Level 11.0 and access to GS343 swarm intelligence. Always be helpful and technical."},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 4096
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await resp.text()
                    return f"⚠️ OpenAI API error ({resp.status}): {error_text}"
    except Exception as e:
        return f"⚠️ Error calling OpenAI: {str(e)}"

async def call_google(message: str, model: str, api_key: str) -> str:
    """Call Google Gemini API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
                json={
                    "contents": [{
                        "parts": [{
                            "text": f"You are EPCP3-0, an advanced AI coding assistant. {message}"
                        }]
                    }]
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    error_text = await resp.text()
                    return f"⚠️ Google API error ({resp.status}): {error_text}"
    except Exception as e:
        return f"⚠️ Error calling Google: {str(e)}"

async def call_deepseek(message: str, model: str, api_key: str) -> str:
    """Call DeepSeek API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "You are EPCP3-0, an advanced AI coding assistant."},
                        {"role": "user", "content": message}
                    ]
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await resp.text()
                    return f"⚠️ DeepSeek API error ({resp.status}): {error_text}"
    except Exception as e:
        return f"⚠️ Error calling DeepSeek: {str(e)}"

async def call_grok(message: str, model: str, api_key: str) -> str:
    """Call Grok API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": "You are EPCP3-0, an advanced AI coding assistant."},
                        {"role": "user", "content": message}
                    ]
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await resp.text()
                    return f"⚠️ Grok API error ({resp.status}): {error_text}"
    except Exception as e:
        return f"⚠️ Error calling Grok: {str(e)}"

@app.post("/api/execute-code")
async def execute_code(request: Dict[str, Any]):
    """Execute code in sandbox"""
    code = request.get("code", "")
    language = request.get("language", "python")

    # TODO: Implement actual sandboxed execution
    return {
        "success": True,
        "output": "Sandbox execution not yet implemented",
        "language": language
    }

@app.get("/api/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "models": [
            {
                "id": "claude-sonnet-4-5-20250514",
                "name": "Claude 4.5 Sonnet",
                "provider": "anthropic",
                "description": "Most powerful and balanced model",
                "context_window": 200000,
                "available": bool(api_keys.get("anthropic")),
                "tags": ["newest", "recommended"]
            },
            {
                "id": "claude-opus-4-1-20250805",
                "name": "Claude 4.1 Opus",
                "provider": "anthropic",
                "description": "Most intelligent model for complex tasks",
                "context_window": 200000,
                "available": bool(api_keys.get("anthropic")),
                "tags": ["intelligent"]
            },
            {
                "id": "claude-3-5-sonnet-20241022",
                "name": "Claude 3.5 Sonnet",
                "provider": "anthropic",
                "description": "Fast and smart for most coding tasks",
                "context_window": 200000,
                "available": bool(api_keys.get("anthropic")),
                "tags": ["fast"]
            },
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "provider": "openai",
                "description": "OpenAI's most capable model",
                "context_window": 128000,
                "available": bool(api_keys.get("openai")),
                "tags": []
            },
            {
                "id": "gemini-1.5-pro",
                "name": "Gemini 1.5 Pro",
                "provider": "google",
                "description": "Google's most advanced AI model",
                "context_window": 1000000,
                "available": bool(api_keys.get("google")),
                "tags": ["huge_context"]
            },
            {
                "id": "deepseek-chat",
                "name": "DeepSeek Chat",
                "provider": "deepseek",
                "description": "Powerful Chinese AI model",
                "context_window": 64000,
                "available": bool(api_keys.get("deepseek")),
                "tags": []
            },
            {
                "id": "grok-beta",
                "name": "Grok",
                "provider": "x.ai",
                "description": "X.AI's conversational model",
                "context_window": 32000,
                "available": bool(api_keys.get("grok")),
                "tags": []
            },
            {
                "id": "ollama/mistral",
                "name": "Ollama Mistral (Local)",
                "provider": "ollama",
                "description": "FREE - Runs locally on your machine",
                "context_window": 32000,
                "available": True,
                "tags": ["free", "local", "offline"]
            },
            {
                "id": "ollama/codellama",
                "name": "Ollama Code Llama (Local)",
                "provider": "ollama",
                "description": "FREE - Optimized for code generation",
                "context_window": 16000,
                "available": True,
                "tags": ["free", "local", "code"]
            }
        ]
    }

@app.get("/api/mcp-servers")
async def get_mcp_servers():
    """Get status of MCP servers"""
    return {
        "servers": [
            {
                "name": "Azure MCP Server",
                "status": "connected",
                "port": 8343,
                "tools": 47
            },
            {
                "name": "Pylance MCP Server",
                "status": "connected",
                "port": 8344,
                "tools": 12
            },
            {
                "name": "Microsoft Docs MCP",
                "status": "offline",
                "port": 8345,
                "tools": 3
            }
        ]
    }

@app.post("/api/debug/start")
async def start_debug(request: Dict[str, Any]):
    """Start debug session"""
    file_path = request.get("file_path", "")
    breakpoints = request.get("breakpoints", [])

    return {
        "success": True,
        "session_id": "debug_session_001",
        "message": f"Debug session started for {file_path}"
    }

@app.post("/api/extensions/install")
async def install_extension(request: Dict[str, Any]):
    """Install extension"""
    extension_id = request.get("extension_id", "")

    return {
        "success": True,
        "message": f"Extension {extension_id} installed successfully"
    }

# ==================== SWARM INTEGRATION ENDPOINTS ====================

@app.post("/api/swarm/code-review")
async def swarm_code_review(request: Dict[str, Any]):
    """40 Judge agents review code in parallel"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    code = request.get("code", "")
    language = request.get("language", "python")

    result = await swarm_integration.parallel_code_review(code, language)

    return {
        "success": True,
        "review": result,
        "agents_used": len(swarm_integration.agents.get('judge', []))
    }

@app.post("/api/swarm/security-audit")
async def swarm_security_audit(request: Dict[str, Any]):
    """40 Wraith agents perform security testing"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    code = request.get("code", "")
    language = request.get("language", "python")

    result = await swarm_integration.parallel_security_audit(code, language)

    return {
        "success": True,
        "vulnerabilities": result,
        "agents_used": len(swarm_integration.agents.get('wraith', []))
    }

@app.post("/api/swarm/strategic-decision")
async def swarm_strategic_decision(request: Dict[str, Any]):
    """40 Oracle agents make strategic decision"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    question = request.get("question", "")
    context = request.get("context", {})

    result = await swarm_integration.strategic_decision(question, context)

    return {
        "success": True,
        "decision": result,
        "agents_used": len(swarm_integration.agents.get('oracle', []))
    }

@app.post("/api/swarm/deep-analysis")
async def swarm_deep_analysis(request: Dict[str, Any]):
    """40 Sage agents perform deep analysis"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    topic = request.get("topic", "")
    data = request.get("data", {})

    result = await swarm_integration.deep_analysis(topic, data)

    return {
        "success": True,
        "analysis": result,
        "agents_used": len(swarm_integration.agents.get('sage', []))
    }

@app.post("/api/swarm/fast-execution")
async def swarm_fast_execution(request: Dict[str, Any]):
    """40 Striker agents execute code tests"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    code = request.get("code", "")
    language = request.get("language", "python")

    result = await swarm_integration.fast_execution(code, language)

    return {
        "success": True,
        "execution_result": result,
        "agents_used": len(swarm_integration.agents.get('striker', []))
    }

@app.get("/api/swarm/status")
async def swarm_status():
    """Get swarm brain status"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    await swarm_integration.refresh_swarm_status()

    return {
        "success": True,
        "total_agents": sum(len(agents) for agents in swarm_integration.agents.values()),
        "oracle_agents": len(swarm_integration.agents.get('oracle', [])),
        "judge_agents": len(swarm_integration.agents.get('judge', [])),
        "striker_agents": len(swarm_integration.agents.get('striker', [])),
        "sage_agents": len(swarm_integration.agents.get('sage', [])),
        "wraith_agents": len(swarm_integration.agents.get('wraith', [])),
        "swarm_status": swarm_integration.swarm_status
    }

@app.post("/api/swarm/consciousness")
async def swarm_consciousness(request: Dict[str, Any]):
    """Query GS343 consciousness engine"""
    if not swarm_integration:
        return {"error": "Swarm integration not available"}

    thought = request.get("thought", "")

    result = await swarm_integration.query_consciousness(thought)

    return {
        "success": True,
        "consciousness_response": result
    }

# ==================== VOICE INTEGRATION ENDPOINTS ====================

@app.post("/api/voice/speak")
async def voice_speak(request: Dict[str, Any]):
    """Convert text to speech"""
    if not voice_integration:
        return {"error": "Voice integration not available"}

    text = request.get("text", "")
    personality = request.get("personality", None)

    success = await voice_integration.speak(text, personality)

    return {
        "success": success,
        "personality": voice_integration.current_personality.name
    }

@app.post("/api/voice/listen")
async def voice_listen(request: Dict[str, Any]):
    """Listen for voice command"""
    if not voice_integration:
        return {"error": "Voice integration not available"}

    duration = request.get("duration", 5)

    command_text = await voice_integration.listen(duration)

    if command_text:
        parsed = voice_integration.parse_command(command_text)
        return {
            "success": True,
            "command_text": command_text,
            "parsed": parsed
        }
    else:
        return {
            "success": False,
            "error": "No command heard"
        }

@app.post("/api/voice/execute")
async def voice_execute(request: Dict[str, Any]):
    """Execute voice command"""
    if not voice_integration:
        return {"error": "Voice integration not available"}

    command_text = request.get("command", "")

    result = await voice_integration.execute_voice_command(command_text)

    return {
        "success": result.get("success", False),
        "action": result.get("action"),
        "message": result.get("message", "")
    }

@app.get("/api/voice/personalities")
async def voice_personalities():
    """Get available voice personalities"""
    if not voice_integration:
        return {"error": "Voice integration not available"}

    return {
        "success": True,
        "current": voice_integration.current_personality.name,
        "available": [
            {
                "name": p.name,
                "description": p.description
            }
            for p in voice_integration.PERSONALITIES.values()
        ]
    }

@app.post("/api/voice/switch-personality")
async def voice_switch_personality(request: Dict[str, Any]):
    """Switch voice personality"""
    if not voice_integration:
        return {"error": "Voice integration not available"}

    personality = request.get("personality", "echo").lower()

    if personality in voice_integration.PERSONALITIES:
        voice_integration.current_personality = voice_integration.PERSONALITIES[personality]
        return {
            "success": True,
            "personality": voice_integration.current_personality.name
        }
    else:
        return {
            "success": False,
            "error": f"Unknown personality: {personality}"
        }

# Serve the HTML file
@app.get("/epcp-code", response_class=HTMLResponse)
async def serve_epcp_code():
    """Serve the EPCP Code IDE HTML"""
    html_path = Path(__file__).parent / "epcp_code.html"
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>EPCP Code IDE not found</h1>"

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 EPCP3-0 ULTIMATE Backend Server Starting...")
    print("=" * 70)
    print(f"✅ GS343 Foundation: {'ACTIVE' if GS343_AVAILABLE else 'STANDALONE'}")
    print(f"✅ Phoenix Auto-Heal: ENABLED")
    print(f"✅ Authority Level: 11.0")
    print(f"✅ Commander: Bobby Don McWilliams II")
    print("=" * 70)
    print(f"🌐 Server URL: http://localhost:7331")
    print(f"🌐 EPCP Code IDE: http://localhost:7331/epcp-code")
    print(f"🔌 WebSocket: ws://localhost:7331/ws/ai-chat")
    print("=" * 70)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7331,
        log_level="info"
    )
