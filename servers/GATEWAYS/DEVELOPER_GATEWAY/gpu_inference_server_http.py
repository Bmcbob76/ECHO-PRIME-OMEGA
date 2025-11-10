#!/usr/bin/env python3
"""
GPU INFERENCE SERVER - HTTP Wrapper (GATEWAYS)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Expose the GPU Inference Flask server under the consolidated GATEWAYS tree
- Provide a stable PORT constant for Master Launcher discovery
- Initialize the Ollama MCP Bridge before starting the Flask app (parity with __main__)
- Start Phoenix monitoring and ensure graceful cleanup on shutdown

Discovery Hints:
- Type: HTTP (Flask)
- Port: 8070 (overridable via env PORT)

Endpoints (proxied from underlying server):
- GET  /health
- POST /api/generate
- POST /api/chat
- GET  /api/models
- GET  /api/mcp/tools
- POST /api/generate_with_mcp
"""

import os
import sys
import asyncio
import logging
import time

# Ensure the main servers directory is importable
SERVERS_ROOT = r"E:\ECHO_XV4\MASTER_LAUNCHER_ULTIMATE\servers"
if SERVERS_ROOT not in sys.path:
    sys.path.insert(0, SERVERS_ROOT)

# Stable constant for discovery (ServerDiscovery scans for 'port = (\d+)' or 'PORT = (\d+)')
PORT = 9401  # default listening port for GPU Inference Server

# Import underlying server module
import gpu_inference_server as gpu  # provides app, phoenix, gpu_client, mcp_bridge variable
# initialize_bridge is imported inside gpu_inference_server, but import explicitly for clarity
from ollama_mcp_bridge import initialize_bridge

logger = logging.getLogger("GPUInferenceGatewayWrapper")
logging.basicConfig(level=logging.INFO)


def main() -> None:
    while True:
        try:
            host = os.environ.get("HOST", "0.0.0.0")
            # Allow env override but retain a literal constant for discovery
            port = int(os.environ.get("PORT", PORT))

            logger.info("Starting GPU Inference Server (GATEWAYS wrapper)")
            logger.info(f"Host: {host}  Port: {port}")
            
            # Ensure downstream GPU client sees correct target host/port even if shell env didn't propagate
            # Priority: existing GPU_SERVER_* env -> WRAPPER_GPU_* env -> sane defaults
            desired_host = os.environ.get("GPU_SERVER_HOST") or os.environ.get("WRAPPER_GPU_SERVER_HOST") or "192.168.1.187"
            desired_port = os.environ.get("GPU_SERVER_PORT") or os.environ.get("WRAPPER_GPU_SERVER_PORT") or "11434"
            os.environ["GPU_SERVER_HOST"] = str(desired_host)
            os.environ["GPU_SERVER_PORT"] = str(desired_port)
            logger.info(f"GPU backend target set to http://{os.environ['GPU_SERVER_HOST']}:{os.environ['GPU_SERVER_PORT']}")
            
            loop = None

            # Initialize MCP bridge (guarded; continue even if MCP fails)
            # Default: skip MCP initialization unless explicitly enabled
            skip_mcp = os.environ.get("ENABLE_MCP_INIT", "0") != "1"
            if skip_mcp:
                logger.info("MCP initialization disabled (default). Set ENABLE_MCP_INIT=1 to enable.")
                gpu.mcp_bridge = None
            else:
                logger.info("Initializing MCP Bridge (via wrapper)...")
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        # Guard with timeout so a non-conforming MCP server doesn't block startup
                        gpu.mcp_bridge = loop.run_until_complete(asyncio.wait_for(initialize_bridge(), timeout=3.0))
                        logger.info("MCP Bridge ready with %d tools", len(getattr(gpu.mcp_bridge, "available_tools", [])))
                    except asyncio.TimeoutError:
                        gpu.mcp_bridge = None
                        logger.warning("MCP Bridge initialization timed out; continuing without MCP tools.")
                except Exception as e:
                    gpu.mcp_bridge = None
                    logger.warning(f"MCP Bridge initialization failed: {e}. Continuing without MCP tools.")

            # Start Phoenix monitoring if available
            try:
                if getattr(gpu, "phoenix", None):
                    gpu.phoenix.start_monitoring()
            except Exception as e:
                logger.debug(f"Phoenix monitor start skipped: {e}")

            try:
                # Run the Flask app with the same options as the original __main__
                gpu.app.run(
                    host=host,
                    port=port,
                    debug=True,
                    use_reloader=False
                )
            finally:
                # Cleanup on shutdown
                logger.info("Shutting down GPU Inference Server (wrapper cleanup)...")
                try:
                    if getattr(gpu, "gpu_client", None):
                        gpu.gpu_client.shutdown()
                except Exception as e:
                    logger.debug(f"gpu_client shutdown skipped: {e}")
                try:
                    if getattr(gpu, "mcp_bridge", None) and loop:
                        loop.run_until_complete(gpu.mcp_bridge.shutdown())
                except Exception as e:
                    logger.debug(f"MCP bridge shutdown skipped: {e}")
                try:
                    if loop:
                        loop.close()
                except Exception:
                    pass
                try:
                    if getattr(gpu, "phoenix", None):
                        gpu.phoenix.stop_monitoring()
                except Exception as e:
                    logger.debug(f"Phoenix monitor stop skipped: {e}")
                logger.info("GPU Inference wrapper shutdown complete")
        except Exception as e:
            logger.error(f"Server crashed: {e}. Restarting in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    main()
