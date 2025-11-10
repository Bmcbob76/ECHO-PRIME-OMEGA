"""
🎖️ GPU INFERENCE API SERVER - ECHO_XV4 SYSTEM
Authority Level: 11.0
Commander: Bobby Don McWilliams II

Flask API server that exposes GPU inference capabilities to ECHO_XV4 ecosystem.
Wraps gpu_inference_client.py with REST API endpoints.

Location: E:\ECHO_XV4\MLS\servers\gpu_inference_server.py
Port: 8070
"""

import sys
import os
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import time

# Add to path
sys.path.insert(0, r"E:\GS343\FOUNDATION")
sys.path.insert(0, r"E:\ECHO_XV4\MLS\servers")

from gs343_foundation_core import GS343UniversalFoundation
from phoenix_auto_heal import PhoenixAutoHeal
from gpu_inference_client import GPUInferenceClient, GPUServerConfig


# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize GS343 & Phoenix
gs343 = GS343UniversalFoundation("GPUInferenceServer", authority_level=11.0)
phoenix = PhoenixAutoHeal("GPUInferenceServer", authority_level=11.0)

# Initialize GPU client (will be set on first request)
gpu_client = None


def get_gpu_client():
    """Get or initialize GPU client"""
    global gpu_client
    if gpu_client is None:
        config = GPUServerConfig(
            host=os.environ.get("GPU_SERVER_HOST", "192.168.1.100"),
            port=int(os.environ.get("GPU_SERVER_PORT", "11434")),
            model=os.environ.get("GPU_MODEL", "mixtral:8x7b-instruct-v0.1-q4_K_M")
        )
        gpu_client = GPUInferenceClient(config)
    return gpu_client


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        client = get_gpu_client()
        gpu_health = client.health_check()
        
        return jsonify({
            "status": "healthy",
            "service": "GPU Inference API Server",
            "port": 8070,
            "gpu_server": gpu_health,
            "timestamp": time.time()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }), 500


@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Generate text from prompt
    
    POST /api/generate
    {
        "prompt": "Your prompt here",
        "model": "mixtral:8x7b-instruct-v0.1-q4_K_M",  // optional
        "system": "System prompt",  // optional
        "temperature": 0.7,  // optional
        "max_tokens": 2000,  // optional
        "stream": false  // optional
    }
    """
    try:
        data = request.json
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        client = get_gpu_client()
        
        if data.get('stream', False):
            def generate_stream():
                # This is a simplified streaming approach
                # For full streaming, you'd need to modify the client
                result = client.generate(
                    prompt=data['prompt'],
                    model=data.get('model'),
                    system=data.get('system'),
                    temperature=data.get('temperature', 0.7),
                    max_tokens=data.get('max_tokens'),
                    stream=False  # Handle streaming differently
                )
                yield json.dumps(result)
            
            return Response(
                stream_with_context(generate_stream()),
                mimetype='application/json'
            )
        else:
            result = client.generate(
                prompt=data['prompt'],
                model=data.get('model'),
                system=data.get('system'),
                temperature=data.get('temperature', 0.7),
                max_tokens=data.get('max_tokens'),
                stream=False
            )
            
            gs343.log_event("generation_success", f"Generated {len(result.get('response', ''))} chars")
            return jsonify(result)
            
    except Exception as e:
        gs343.log_event("generation_error", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint (multi-turn conversation)
    
    POST /api/chat
    {
        "messages": [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "Hello!"}
        ],
        "model": "mixtral:8x7b-instruct-v0.1-q4_K_M",  // optional
        "temperature": 0.7,  // optional
        "stream": false  // optional
    }
    """
    try:
        data = request.json
        
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing 'messages' in request"}), 400
        
        client = get_gpu_client()
        
        result = client.chat(
            messages=data['messages'],
            model=data.get('model'),
            temperature=data.get('temperature', 0.7),
            stream=data.get('stream', False)
        )
        
        gs343.log_event("chat_success", "Chat completed")
        return jsonify(result)
        
    except Exception as e:
        gs343.log_event("chat_error", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/models', methods=['GET'])
def list_models():
    """List available models"""
    try:
        client = get_gpu_client()
        models = client.list_models()
        
        return jsonify({
            "models": models,
            "count": len(models)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current server configuration"""
    try:
        client = get_gpu_client()
        config = client.config
        
        return jsonify({
            "host": config.host,
            "port": config.port,
            "model": config.model,
            "timeout": config.timeout,
            "base_url": config.base_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🎖️ GPU INFERENCE API SERVER - ECHO_XV4")
    print("=" * 60)
    print(f"Authority Level: 11.0")
    print(f"Port: 8070")
    print(f"GPU Server: {os.environ.get('GPU_SERVER_HOST', '192.168.1.100')}")
    print("=" * 60)
    
    # Start Phoenix monitoring
    phoenix.start_monitoring()
    
    try:
        # Run server
        app.run(
            host='0.0.0.0',
            port=8070,
            debug=True,
            use_reloader=False
        )
    finally:
        # Cleanup
        if gpu_client:
            gpu_client.shutdown()
        phoenix.stop_monitoring()
        print("\n✅ Server shutdown complete")
