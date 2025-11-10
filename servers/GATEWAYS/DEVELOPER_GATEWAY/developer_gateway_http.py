#!/usr/bin/env python3
"""
DEVELOPER GATEWAY - HTTP Wrapper (GATEWAYS)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Expose the Developer Gateway (FastAPI) under the consolidated GATEWAYS tree
- Provide a stable PORT constant for Master Launcher discovery
- Run with uvicorn and proxy requests to GPU Inference Server
- Dynamic port finding with launcher assignment

Discovery Hints:
- Type: HTTP (FastAPI/uvicorn)
- Port: Dynamic via GATEWAY_PORT env (default 9407)

Endpoints:
- GET  /health
- POST /api/generate_with_mcp
"""

import os
import sys
import logging
import time

# Process naming
try:
    from setproctitle import setproctitle
    setproctitle("DeveloperGateway_9407")
except ImportError:
    pass  # Optional dependency

# Dynamic port from launcher or fallback default
DEFAULT_PORT = 9407
PORT = int(os.getenv("GATEWAY_PORT", os.getenv("PORT", DEFAULT_PORT)))

import uvicorn  # Triggers HTTP server type detection in discovery
from developer_gateway import app as dev_app  # Reuse FastAPI app defined in GATEWAYS/developer_gateway.py

logger = logging.getLogger("DeveloperGatewayWrapper")
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Main entry with auto-restart on crash"""
    while True:
        try:
            host = os.getenv("HOST", "127.0.0.1")
            
            logger.info("🚀 Starting Developer Gateway (GATEWAYS wrapper)")
            logger.info(f"Host: {host}  Port: {PORT}")
            logger.info("Proxy target: GPU_INFER_URL env in developer_gateway.py (default http://127.0.0.1:8070)")

            # Run uvicorn using the imported FastAPI app
            uvicorn.run(
                "developer_gateway_http:app",
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
