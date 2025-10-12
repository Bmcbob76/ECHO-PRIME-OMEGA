# Master Modular Launcher Enhanced V3 - Documentation

## Overview

The Master Modular Launcher Enhanced V3 is a comprehensive, production-ready server orchestration system for ECHO_XV4. It automatically discovers, launches, monitors, and manages any server dropped into the `servers/` directory.

## 🎯 NEW: Unified Developer API System

**See:** `servers/UNIFIED_DEVELOPER_API_README.md` for complete documentation

The MLS now includes the **Unified Developer API System** - a groundbreaking integration that enables Claude to work in VS Code like a human developer:

**Components:**
- ✅ **Windows API Server** (Port 8343) - 225+ endpoints, 4-screen OCR, full OS control
- ✅ **Desktop Commander** (MCP) - Complete filesystem access across all drives
- 🔧 **VS Code Extension** (Port 9001) - Full VS Code editor control (Building)
- 🔧 **Unified Orchestrator** (Port 9000) - Master coordinator (Building)

**Status:** 50% complete - Windows API & Desktop Commander operational, VS Code + Unified API in development

**Quick Start:**
```bash
# Launch Windows API Server
cd E:\ECHO_XV4\MLS\servers
START_WINDOWS_API_ULTIMATE.bat
```

## Key Features

### 🔍 Auto-Discovery
- **Automatic Detection**: Scans `E:\ECHO_XV4\MLS\servers\` for new servers
- **Supported Types**:
  - Python scripts (`*.py`)
  - Executables (`*.exe`)
  - Docker containers (directories with `Dockerfile`)
- **Hot Reload**: Automatically detects file changes and reloads servers

### 🚀 Dynamic Launch System
- **Port Management**: Automatically assigns free ports to each server
- **Multiple Instances**: Configure number of instances per server
- **Process Isolation**: Each server runs in its own process
- **Environment Variables**: Automatically sets debug and MCP flags

### 🏥 Health Monitoring & Auto-Healing
- **Health Checks**: Periodic HTTP health endpoint monitoring
- **Auto-Restart**: Automatically restarts failed servers
- **Phoenix Protocol**: GS343 Foundation integration for advanced healing
- **Configurable Backoff**: Smart restart delays to prevent loops

### 📊 Live Dashboard
- **Web Interface**: Real-time status at http://localhost:9000
- **Server Control**: Launch, stop, restart servers from browser
- **Metrics Display**: View health checks, restarts, and performance
- **API Endpoints**: RESTful API for programmatic control

### 🔌 MCP Integration
- **Claude Desktop Ready**: Full Model Context Protocol support
- **Tool Registration**: Exposes server control as MCP tools
- **Status Queries**: Claude can query and control servers

### 🐳 Docker Support
- **Auto-Build**: Automatically builds Docker images
- **Container Management**: Launches and manages containers
- **Port Mapping**: Dynamic port assignment for containers

## Installation

### Prerequisites
```bash
# Required
Python 3.8+
pip

# Optional
Docker Desktop (for Docker support)
MCP package (for Claude integration)
```

### Setup
```bash
# Navigate to MLS directory
cd E:\ECHO_XV4\MLS

# Install dependencies
pip install -r requirements.txt

# Optional: Install MCP for Claude
pip install mcp

# Launch the system
python master_modular_launcher_enhanced.py
# or
launch_v3.bat
```

## Usage

### Adding Servers

Simply drop any of these into `E:\ECHO_XV4\MLS\servers\`:

#### Python Server Example
```python
# my_server.py
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

if __name__ == "__main__":
    port = int(sys.argv[1])  # Port passed by launcher
    HTTPServer(('', port), Handler).serve_forever()
```

#### Docker Server Example
```
servers/
  my_docker_server/
    Dockerfile
    server.py
```

### Configuration

Edit `config.yaml`:

```yaml
# Core settings
servers_dir: "E:/ECHO_XV4/MLS/servers"
dashboard_port: 9000
base_port: 8000

# Instances
num_instances_per_server: 1  # Run multiple instances

# Health monitoring
health_check_interval: 30  # Seconds
max_restart_attempts: 3

# Features
auto_discovery: true
hot_reload: true
docker_support: true
mcp_enabled: true
```

### Dashboard Access

Open browser to: http://localhost:9000

Features:
- View all discovered servers
- See real-time status
- Control servers (launch/stop/restart)
- View metrics and health status
- Monitor instances and PIDs

### API Endpoints

```
GET /api/status         - Get system status
GET /api/servers        - List all servers
GET /api/metrics        - Get performance metrics
GET /api/launch/<id>    - Launch a server
GET /api/stop/<id>      - Stop a server
GET /api/restart/<id>   - Restart a server
```

## MCP Integration for Claude

When MCP is enabled, Claude Desktop can:

### Available Tools
- `discover_servers` - Find new servers
- `launch_server` - Start a specific server
- `stop_server` - Stop a running server
- `get_status` - Get comprehensive status
- `health_check` - Check all server health

### Example Claude Commands
```
"Launch the crystal memory server"
"Show me the status of all running servers"
"Restart any failed servers"
"How many servers are currently running?"
```

## Auto-Discovery Rules

### Python Scripts
- Must accept port as first argument: `sys.argv[1]`
- Should expose `/health` endpoint returning 200 OK
- File extension: `.py`

### Executables
- Must accept port as first argument
- Should expose `/health` endpoint
- File extensions: `.exe`, `.bat`, `.sh`

### Docker Containers
- Directory must contain `Dockerfile`
- Container should expose health endpoint
- Port mapping handled automatically

## Health Check Protocol

Servers should implement:

```python
# Required endpoint
GET /health
Response: 200 OK

# Optional response body
{
    "status": "healthy",
    "uptime": 3600,
    "custom_metrics": {...}
}
```

## Logging

### Log Locations
- Master log: `E:\ECHO_XV4\MLS\logs\master.log`
- Server logs: `E:\ECHO_XV4\MLS\logs\<server_id>_<instance>_<timestamp>.log`

### Log Levels
- DEBUG: Detailed debugging information
- INFO: Normal operational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical failures

## Advanced Features

### Resource Limits
```yaml
resource_limits:
  memory_mb: 512      # Max memory per server
  cpu_percent: 80     # Max CPU usage
```

### Notification Webhooks
```yaml
notification_hooks:
  on_restart: "https://webhook.site/..."
  on_crash: "https://webhook.site/..."
```

### Server Overrides
```yaml
server_overrides:
  special_server:
    port: 9999
    instances: 3
    auto_restart: false
```

## Troubleshooting

### Server Not Launching
1. Check `logs/master.log` for errors
2. Verify server accepts port argument
3. Ensure health endpoint exists
4. Check port availability

### Dashboard Not Loading
1. Verify dashboard port (default 9000) is free
2. Check firewall settings
3. Look for Flask errors in console

### Health Checks Failing
1. Ensure `/health` endpoint returns 200
2. Check `health_check_timeout` setting
3. Verify server is actually running

### Docker Issues
1. Ensure Docker Desktop is running
2. Check Dockerfile syntax
3. Verify port mapping in container

## Best Practices

1. **Always implement health endpoint** - Critical for auto-healing
2. **Use unique server names** - Avoid naming conflicts
3. **Handle graceful shutdown** - Catch SIGTERM signals
4. **Log important events** - Use stdout for logging
5. **Set resource limits** - Prevent resource exhaustion
6. **Test locally first** - Verify server works standalone
7. **Use environment variables** - Check MCP_ENABLED, DEBUG flags

## Architecture

```
Master Launcher (MLS)
├── Auto-Discovery Engine
│   ├── File Watcher (hot reload)
│   └── Server Scanner
├── Process Manager
│   ├── Launch Controller
│   ├── Health Monitor
│   └── Auto-Healer
├── Dashboard Server
│   ├── Web Interface
│   └── REST API
├── MCP Server
│   └── Claude Tools
└── GS343 Integration
    ├── Phoenix Healing
    └── Authority Control
```

## Authority & Compliance

- **Authority Level**: 11.0 (Maximum)
- **Commander**: Bobby Don McWilliams II
- **Foundation**: GS343 Divine Overseer
- **Protocol**: Phoenix Auto-Heal Active
- **Environment**: ECHO_XV4 Production

## Support

For issues or enhancements:
1. Check logs in `E:\ECHO_XV4\MLS\logs\`
2. Verify configuration in `config.yaml`
3. Ensure all dependencies installed
4. Contact through ECHO_XV4 command structure

---

**Version**: 3.0.0
**Build**: Production
**Status**: Fully Operational
