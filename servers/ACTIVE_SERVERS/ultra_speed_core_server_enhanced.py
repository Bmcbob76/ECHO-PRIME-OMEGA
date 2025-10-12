""" 
⚡ ULTRA SPEED CORE SERVER - Built on GS343 Foundation
GS343 Divine Overseer Integration - Authority Level 9.5
Phoenix Auto-Heal Protocol - 24/7 Recovery
Commander Bobby Don McWilliams II - Bloodline Authority Level 11.0

ECHO_XV4 Production Server - Ultra High Performance Core
"""

import sys
import asyncio
import time
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    print("⚠️ WARNING: GS343 Foundation not loaded - Limited functionality")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        pass

class UltraSpeedCoreServer:
    def __init__(self, port: int = 8000):
        self.port = port
        self.log_path = Path("E:/ECHO_XV4/LOGS")
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        # CRITICAL: Setup logger FIRST before anything else
        self.logger = self._setup_logging()
        
        self.server_running = False
        self.executor = ThreadPoolExecutor(max_workers=10)

        if GS343_AVAILABLE:
            self.gs343 = GS343UniversalFoundation("UltraSpeedCoreServer", authority_level=9.5)
            self.phoenix = PhoenixAutoHeal("UltraSpeedCoreServer", authority_level=9.5)
            self.phoenix.start_monitoring()
            self.logger.info("⚡ UltraSpeedCoreServer registered with GS343 Foundation")
        else:
            self.gs343 = None
            self.phoenix = None

        self.logger.info(f"⚡ Ultra Speed Core Server initialized on port {self.port}")

    def _setup_logging(self):
        log_file = self.log_path / "ultra_speed_core_server.log"
        logger = logging.getLogger(f"UltraSpeedCoreServer:{self.port}")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('⚡ %(asctime)s - UltraSpeed[%(name)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    def start_health_server(self):
        def run():
            server = HTTPServer(('0.0.0.0', self.port), HealthHandler)
            server.serve_forever()
        threading.Thread(target=run, daemon=True).start()

    async def run_server(self):
        self.server_running = True
        self.logger.info("⚡ Ultra Speed Core Server running with GS343 Foundation")
        self.logger.info(f"⚡ Phoenix Auto-Heal: {'Active' if self.phoenix else 'Inactive'}")
        self.logger.info(f"⚡ Authority Level: 9.5")
        self.logger.info(f"⚡ Listening on port: {self.port}")
        self.start_health_server()
        try:
            while self.server_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("⚡ Shutting down Ultra Speed Core Server...")
            self.server_running = False
        except Exception as e:
            self.logger.error(f"⚡ Server error: {e}")
            if self.phoenix:
                self.phoenix.heal_error(e, "server_main_loop")
        finally:
            await self.shutdown()

    async def shutdown(self):
        self.server_running = False
        self.executor.shutdown(wait=True)
        if self.phoenix:
            self.phoenix.stop_monitoring()
        if GS343_AVAILABLE and self.gs343:
            self.gs343.shutdown_foundation()
        self.logger.info("⚡ Ultra Speed Core Server shutdown complete")

async def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"⚡ ECHO_XV4 Ultra Speed Core Server - GS343 Foundation\n⚡ Listening on port {port}")
    server = UltraSpeedCoreServer(port=port)
    try:
        await server.run_server()
    except Exception as e:
        print(f"⚡ ❌ Server startup failed: {e}")
        if hasattr(server, 'phoenix') and server.phoenix:
            server.phoenix.heal_error(e, "main_server_startup")

if __name__ == "__main__":
    asyncio.run(main())
