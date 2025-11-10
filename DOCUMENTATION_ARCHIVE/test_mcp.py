import sys
try:
    import mcp
    print("MCP SDK is installed")
    print(f"MCP version: {mcp.__version__}")
except ImportError:
    print("MCP SDK not installed")
    print("Install with: pip install mcp")
    sys.exit(1)
