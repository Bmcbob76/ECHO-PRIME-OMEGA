"""
EPCP3-0 C3PO Server
Flask REST API for C3PO Voice + Personality
MLS Compatible | Port 8030
GS343 Foundation 9.5 Integrated
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
from pathlib import Path
import traceback
from datetime import datetime

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# Add EPCP3-0 to path
sys.path.insert(0, "E:/ECHO_XV4/EPCP3-0")
sys.path.insert(0, "E:/ECHO_XV4")

# === GS343 FOUNDATION INTEGRATION ===
sys.path.insert(0, "E:/GS343/FOUNDATION")
try:
    from GS343Foundation import GS343Foundation
    from PhoenixAutoHeal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    print("⚠️  GS343 Foundation not available - running standalone")
    class GS343Foundation:
        @staticmethod
        def register_module(name, instance): pass
    class PhoenixAutoHeal:
        @staticmethod
        def execute_with_healing(func, *args, **kwargs):
            return func(*args, **kwargs)

# Initialize Flask
app = Flask(__name__)
CORS(app)

# C3PO Integration
c3po_integration = None
server_stats = {
    'start_time': datetime.now(),
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'voice_generations': 0,
    'personality_responses': 0
}

def initialize_c3po():
    """Initialize C3PO integration"""
    global c3po_integration
    
    try:
        from c3po_master import C3POIntegration
        c3po_integration = C3POIntegration()
        
        if c3po_integration.initialize():
            print("✅ C3PO Integration initialized successfully")
            return True
        else:
            print("❌ C3PO Integration failed to initialize")
            return False
    except Exception as e:
        print(f"❌ Error initializing C3PO: {e}")
        traceback.print_exc()
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    uptime = (datetime.now() - server_stats['start_time']).total_seconds()
    
    health_data = {
        "status": "healthy" if c3po_integration else "degraded",
        "service": "EPCP3-0 C3PO Integration",
        "version": "1.0.0",
        "uptime_seconds": uptime,
        "c3po_initialized": c3po_integration is not None,
        "voice_available": c3po_integration.voice is not None if c3po_integration else False,
        "personality_available": c3po_integration.personality is not None if c3po_integration else False,
        "gs343_foundation": GS343_AVAILABLE,
        "statistics": server_stats,
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(health_data)

@app.route('/respond', methods=['POST'])
def respond():
    """
    Get C3PO response with optional voice
    
    POST body:
    {
        "text": "User input text",
        "speak": true/false (optional, default false),
        "context": {...} (optional)
    }
    """
    server_stats['total_requests'] += 1
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            server_stats['failed_requests'] += 1
            return jsonify({
                "error": "Missing 'text' parameter"
            }), 400
        
        user_input = data['text']
        speak = data.get('speak', False)
        context = data.get('context', None)
        
        if not c3po_integration:
            if not initialize_c3po():
                server_stats['failed_requests'] += 1
                return jsonify({
                    "error": "C3PO integration not initialized"
                }), 500
        
        # Generate response
        response = c3po_integration.respond(user_input, speak=speak, context=context)
        
        if response.get('success'):
            server_stats['successful_requests'] += 1
            if response.get('audio'):
                server_stats['voice_generations'] += 1
            server_stats['personality_responses'] += 1
        else:
            server_stats['failed_requests'] += 1
        
        return jsonify(response)
        
    except Exception as e:
        server_stats['failed_requests'] += 1
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/speak', methods=['POST'])
def speak():
    """
    Generate C3PO voice from text
    
    POST body:
    {
        "text": "Text to speak",
        "apply_personality": true/false (optional, default true)
    }
    """
    server_stats['total_requests'] += 1
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            server_stats['failed_requests'] += 1
            return jsonify({
                "error": "Missing 'text' parameter"
            }), 400
        
        text = data['text']
        apply_personality = data.get('apply_personality', True)
        
        if not c3po_integration:
            if not initialize_c3po():
                server_stats['failed_requests'] += 1
                return jsonify({
                    "error": "C3PO integration not initialized"
                }), 500
        
        # Generate voice
        audio_path = c3po_integration.speak(text, apply_personality)
        
        if audio_path:
            server_stats['successful_requests'] += 1
            server_stats['voice_generations'] += 1
            
            return jsonify({
                "success": True,
                "audio_path": audio_path,
                "text": text
            })
        else:
            server_stats['failed_requests'] += 1
            return jsonify({
                "success": False,
                "error": "Voice generation failed"
            }), 500
        
    except Exception as e:
        server_stats['failed_requests'] += 1
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/personality', methods=['POST'])
def personality():
    """
    Apply C3PO personality styling to text
    
    POST body:
    {
        "text": "Input text",
        "context": {...} (optional)
    }
    """
    server_stats['total_requests'] += 1
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            server_stats['failed_requests'] += 1
            return jsonify({
                "error": "Missing 'text' parameter"
            }), 400
        
        text = data['text']
        context = data.get('context', None)
        
        if not c3po_integration:
            if not initialize_c3po():
                server_stats['failed_requests'] += 1
                return jsonify({
                    "error": "C3PO integration not initialized"
                }), 500
        
        # Apply personality
        styled_text = c3po_integration.personality.apply_c3po_style(text, context)
        
        server_stats['successful_requests'] += 1
        server_stats['personality_responses'] += 1
        
        return jsonify({
            "success": True,
            "original": text,
            "styled": styled_text
        })
        
    except Exception as e:
        server_stats['failed_requests'] += 1
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Get comprehensive statistics"""
    try:
        response_data = {
            "server_stats": server_stats,
            "uptime_seconds": (datetime.now() - server_stats['start_time']).total_seconds()
        }
        
        if c3po_integration:
            response_data["c3po_stats"] = c3po_integration.get_stats()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    import sys
    
    # Handle port parameter
    port = 8030  # Default port
    debug = False
    
    for arg in sys.argv[1:]:
        if arg.startswith('--port='):
            port = int(arg.split('=')[1])
        elif arg == '--debug':
            debug = True
    
    print("="*70)
    print("🎖️ EPCP3-0 C3PO SERVER")
    print("="*70)
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"GS343 Foundation: {'ACTIVE' if GS343_AVAILABLE else 'UNAVAILABLE'}")
    print("="*70)
    
    # Initialize C3PO
    print("\nInitializing C3PO Integration...")
    if initialize_c3po():
        print("✅ C3PO Ready\n")
    else:
        print("⚠️  C3PO initialization failed - server will run in degraded mode\n")
    
    print(f"🚀 Starting server on http://localhost:{port}")
    print(f"📡 Health: http://localhost:{port}/health")
    print(f"🤖 Respond: POST http://localhost:{port}/respond")
    print(f"🔊 Speak: POST http://localhost:{port}/speak")
    print(f"💬 Personality: POST http://localhost:{port}/personality")
    print(f"📊 Stats: GET http://localhost:{port}/stats")
    print("="*70 + "\n")
    
    # Register with GS343 Foundation
    if GS343_AVAILABLE:
        GS343Foundation.register_module("EPCP3-0_C3PO_SERVER", app)
    
    # Start server
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )
