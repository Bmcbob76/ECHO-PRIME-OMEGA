"""
🚀 MCP CONSTELLATION DASHBOARD - Real-time monitoring
Port: 9000
"""

from flask import Flask, jsonify, render_template_string
import socket
import requests

app = Flask(__name__)

SERVERS = {
    "Orchestrator": 8000,
    "Filesystem": 8001,
    "Windows API": 8002,
    "Process Control": 8003,
    "Crystal Memory": 8004,
    "Workflow Engine": 8005,
    "Voice System": 8006,
    "Network Tools": 8007,
    "Healing Protocols": 8008
}

def check_server(port):
    """Check if server is running"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

@app.route('/')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Constellation Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                color: #00ff41;
                padding: 20px;
                margin: 0;
            }
            .header {
                text-align: center;
                border: 2px solid #00ff41;
                padding: 30px;
                margin-bottom: 30px;
                border-radius: 15px;
                background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
                box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
            }
            h1 {
                font-size: 3em;
                margin: 0;
                text-shadow: 0 0 20px #00ff41;
                animation: glow 2s ease-in-out infinite alternate;
            }
            @keyframes glow {
                from { text-shadow: 0 0 10px #00ff41; }
                to { text-shadow: 0 0 30px #00ff41, 0 0 40px #00ff41; }
            }
            .servers {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .server {
                border: 2px solid #00ff41;
                padding: 20px;
                border-radius: 10px;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                transition: all 0.3s;
            }
            .server:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 30px rgba(0, 255, 65, 0.4);
            }
            .server.online {
                border-color: #00ff41;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
            }
            .server.offline {
                border-color: #ff4141;
                box-shadow: 0 0 20px rgba(255, 65, 65, 0.3);
            }
            .status {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 10px;
            }
            .status.online {
                background: #00ff41;
                color: #000;
            }
            .status.offline {
                background: #ff4141;
                color: #fff;
            }
            .port {
                color: #00ccff;
                font-size: 1.2em;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 MCP CONSTELLATION</h1>
            <p>Authority Level 11.0 - Commander Bobby Don McWilliams II</p>
        </div>
        <div class="servers">
            {% for name, port in servers.items() %}
            <div class="server {{ 'online' if status[name] else 'offline' }}">
                <h2>{{ name }}</h2>
                <p class="port">Port: {{ port }}</p>
                <span class="status {{ 'online' if status[name] else 'offline' }}">
                    {{ 'ONLINE ✅' if status[name] else 'OFFLINE ❌' }}
                </span>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    ''', servers=SERVERS, status={name: check_server(port) for name, port in SERVERS.items()})

@app.route('/api/status')
def api_status():
    status = {name: check_server(port) for name, port in SERVERS.items()}
    return jsonify(status)

if __name__ == "__main__":
    print("🚀 MCP Constellation Dashboard starting on port 9000")
    print("📊 Open: http://localhost:9000")
    app.run(host='0.0.0.0', port=9000, debug=False)
