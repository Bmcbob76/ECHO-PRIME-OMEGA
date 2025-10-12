from flask import Flask, jsonify, render_template
import threading

from pathlib import Path
import sys

# GS343 Foundation Integration - MANDATORY
GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    print("?? WARNING: GS343 Foundation not loaded - Limited functionality")
app = Flask(__name__, template_folder='static')

server_status = []
metrics = {}

@app.route('/')
def index():
    return render_template('dashboard.html', servers=server_status, metrics=metrics)

@app.route('/status')
def status():
    return jsonify({'servers': server_status, 'metrics': metrics})

def run_dashboard(port):
    app.run(port=port, use_reloader=False)

def start_dashboard_thread(port):
    t = threading.Thread(target=run_dashboard, args=(port,), daemon=True)
    t.start()
