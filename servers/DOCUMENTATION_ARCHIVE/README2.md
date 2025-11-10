# EPCP30 MOBILE-TO-DESKTOP MCP SERVER - XV4 EDITION

## 🎯 Overview

Complete mobile-to-desktop command & control system for ECHO_XV4.
- Full MLS (Modular Launcher System) integration
- Auto-server registration
- Production-grade servers with diagnostics
- Authority Level 11.0

## 🚀 Quick Start

### 1. Install Dependencies (if not already done)
```
INSTALL_DEPENDENCIES.bat
```

### 2. Start MCP Server
```
START_MCP_SERVER.bat
```

### 3. Use from Mobile
Open Claude on your phone and say:
- "Create a FastAPI server called api_001 on port 8000"
- "What's my desktop system status?"
- "Create a REST API with CRUD operations"

## 📱 Mobile Commands

### Create Servers
```
"Create a FastAPI server called task_api on port 8001 with CRUD and CORS"
```

### Check Status
```
"What's my system status?"
"List all MLS servers"
"Check if port 8000 is available"
```

### File Operations
```
"Create a Python script at E:\ECHO_XV4\test.py"
"Show me the file at E:\ECHO_XV4\MLS\servers\api_001\main.py"
```

### Execute Commands
```
"Run PowerShell command: Get-Process | Where CPU -gt 50"
"Execute Python: print('Hello from desktop')"
```

## 🛠️ Available Tools

The MCP server provides these tools:
- **create_file** - Create any file
- **create_server** - Generate production servers (FastAPI, Flask, etc)
- **execute_command** - Run PowerShell/Python/CMD
- **list_servers** - Show all MLS servers
- **read_file** - View file contents
- **system_status** - Full system diagnostics
- **check_port** - Port availability
- **list_mls_servers** - MLS registry

## 📂 Directory Structure

```
E:\ECHO_XV4\
├── EPCP30\
│   ├── MCP_SERVER\          (this directory)
│   └── LOGS\                (server logs)
├── MLS\
│   ├── servers\             (all auto-launch servers)
│   ├── logs\                (server logs)
│   └── server_registry.json (MLS registry)
└── PROJECTS\                (project files)
```

## 🔧 Server Features

All created servers include:
- ✅ Full debug logging
- ✅ Health endpoints (/health)
- ✅ Diagnostic endpoints (/diagnostics)
- ✅ Swagger UI (/docs)
- ✅ Auto-registration with MLS
- ✅ Production-ready code
- ✅ Error handling
- ✅ Request logging

## 🎮 Example Session

**You (mobile):** "Create a task management API on port 8001 with CRUD"

**Claude:** *Creates complete FastAPI server with:*
- Full CRUD operations
- Health monitoring
- Diagnostics endpoint
- Swagger documentation
- Auto-registered with MLS

**You:** "Show me the health endpoint"

**Claude:** *Displays /health endpoint code*

**You:** "Perfect! Check system status"

**Claude:** *Shows CPU, memory, disk, top processes*

## 🔐 Security

- Authorization Level: 11.0 (Commander only)
- All data on E:\ drive
- Full audit logs
- No cloud sync

## 📝 Logs

- **MCP Server**: E:\ECHO_XV4\EPCP30\LOGS\mcp_server.log
- **Individual Servers**: E:\ECHO_XV4\MLS\logs\{server_name}.log

## 🆘 Troubleshooting

**Problem:** "mcp module not found"
```
INSTALL_DEPENDENCIES.bat
```

**Problem:** "Server won't start"
```
Check E:\ECHO_XV4\EPCP30\LOGS\mcp_server.log
```

**Problem:** "Port already in use"
```
Use "check if port 8000 is available" to find open port
```

## 💡 Pro Tips

1. Keep MCP server running 24/7 for instant mobile access
2. All servers auto-register with MLS for easy launching
3. Use specific paths: "E:\ECHO_XV4\..."
4. Check diagnostics: http://localhost:{port}/diagnostics
5. View Swagger docs: http://localhost:{port}/docs

## 🚀 Integration with MLS

Created servers automatically:
- Register with MLS launcher
- Enable auto-launch
- Include health monitoring
- Generate proper launchers

Check registry:
```
E:\ECHO_XV4\MLS\server_registry.json
```

---
**EPCP30 Desktop Commander - XV4 Edition**
*Authority Level 11.0*
*Commander Bobby Don McWilliams II*
