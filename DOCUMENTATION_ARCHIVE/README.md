# 🚀 MASTER MODULAR LAUNCHER V3 - ECHO_XV4 PRODUCTION

**Authority Level**: 11.0  
**Commander**: Bobby Don McWilliams II  
**Status**: FULLY OPERATIONAL  
**Version**: 3.0.0  

## 📋 SYSTEM OVERVIEW

The Master Modular Launcher V3 is a **fully autonomous server orchestration system** that automatically discovers, launches, monitors, and heals ANY server dropped into the `servers/` directory. No configuration needed - just drop and run!

## ⚡ QUICK START

```batch
# Method 1: Batch File (Recommended)
cd E:\ECHO_XV4\MLS
launch_v3.bat

# Method 2: PowerShell Installer
.\install.ps1

# Method 3: Direct Python
python master_modular_launcher_enhanced.py
```

**Dashboard**: http://localhost:9000

## 🎯 KEY FEATURES

### ✅ Auto-Discovery
- **Automatically detects** all servers in `servers/` directory
- **No configuration** - just drop files and they launch
- **Supports**: Python (.py), Executables (.exe), Docker containers

### ✅ Dynamic Port Assignment
- **Automatically assigns** free ports starting from 8000
- **Handles conflicts** intelligently
- **Multiple instances** get offset ports

### ✅ Health Monitoring & Auto-Healing
- **HTTP health checks** every 30 seconds
- **Auto-restarts** failed servers
- **Phoenix Protocol** integration from GS343
- **Configurable** restart attempts and backoff

### ✅ Hot Reload
- **File watcher** monitors changes
- **Auto-reloads** modified servers
- **No manual restart** needed

### ✅ Live Dashboard
- **Web interface**: http://localhost:9000
- **Real-time status** of all servers
- **Control panel**: Launch/Stop/Restart
- **Metrics**: Health checks, restarts, performance

### ✅ MCP Integration for Claude
- **Launcher is MCP-enabled** - Claude can control ALL servers
- **Available MCP tools**:
  - `discover_servers` - Find new servers
  - `launch_server` - Start any server
  - `stop_server` - Stop any server
  - `get_status` - Get full system status
  - `health_check` - Check all server health

### ✅ Docker Support
- **Auto-builds** Docker images
- **Container management**
- **Dynamic port mapping**

## 📁 CURRENT SERVERS (20+ Auto-Discovered)

All these servers are **automatically launched** when you start the system:

| Server | Purpose | MCP-Enabled | Auto-Launch |
|--------|---------|-------------|-------------|
| **ultra_speed_mcp_server.py** | File operations with MCP | ✅ YES | ✅ YES |
| **comprehensive_api_server_ULTIMATE.py** | 225 Windows APIs + OCR | ✅ YES | ✅ YES |
| **crystal_memory_server_enhanced.py** | Quantum memory storage | ❌ NO | ✅ YES |
| **multi_llm_defense.py** | 10+ LLM orchestration | ❌ NO | ✅ YES |
| **quantum_defender_v3.py** | AI threat hunting | ❌ NO | ✅ YES |
| **echo_prime_master_launcher.py** | Legacy launcher | ❌ NO | ✅ YES |
| **gs343_autohealer_server_enhanced.py** | Phoenix auto-heal | ❌ NO | ✅ YES |
| **network_guardian_integration.py** | Network monitoring | ❌ NO | ✅ YES |
| **realtime_monitor.py** | System monitoring | ❌ NO | ✅ YES |
| **standalone_hardware_monitor.py** | Hardware metrics | ❌ NO | ✅ YES |
| **api_server.py** | Basic API server | ❌ NO | ✅ YES |
| **unified_defense.py** | Defense orchestration | ❌ NO | ✅ YES |
| **sample_echo_server.py** | Test server with health | ❌ NO | ✅ YES |
| **test_mcp_server.py** | MCP test server | ❌ NO | ✅ YES |
| + More... | Various functions | ❌ NO | ✅ YES |

**Note**: All servers are controllable via the launcher's MCP interface, even if they don't have individual MCP support.

## 🔌 MCP INTEGRATION DETAILS

### Launcher MCP Control (Available Now)
Claude can control **ALL servers** through the launcher:
```
"Launch the crystal memory server"     ✅ Works
"Stop all running servers"             ✅ Works
"Show me the status of all servers"    ✅ Works
"Restart any failed servers"           ✅ Works
```

### Individual Server MCP (Limited)
Only 2 servers currently have their own MCP tools:
- `ultra_speed_mcp_server.py` - File operations
- `comprehensive_api_server_ULTIMATE.py` - Windows APIs

To access server-specific functions via MCP, those servers need individual MCP implementation.

## 📊 API ENDPOINTS

```
GET /api/status         - Full system status
GET /api/servers        - List all servers
GET /api/metrics        - Performance metrics
GET /api/launch/<id>    - Launch specific server
GET /api/stop/<id>      - Stop specific server  
GET /api/restart/<id>   - Restart specific server
```

## ⚙️ CONFIGURATION

Edit `config.yaml` to customize:

```yaml
# Core Settings
dashboard_port: 9000              # Web dashboard port
base_port: 8000                  # Starting port for servers
num_instances_per_server: 1      # Instances per server

# Features
auto_discovery: true              # Auto-detect new servers
hot_reload: true                 # Auto-reload on changes
docker_support: true             # Docker container support
mcp_enabled: true                # MCP for Claude Desktop

# Health Monitoring
health_check_interval: 30        # Seconds between checks
max_restart_attempts: 3          # Max restart tries
restart_backoff: 5               # Seconds before restart
```

## 🏥 HEALTH CHECK PROTOCOL

For auto-healing to work, servers should implement:

```python
# Required endpoint
@app.route('/health')
def health():
    return "OK", 200

# Or with JSON response
@app.route('/health')
def health():
    return {"status": "healthy", "uptime": 3600}, 200
```

## 📝 ADDING NEW SERVERS

1. **Create your server** with:
   - Port from `sys.argv[1]`
   - Health endpoint at `/health`

2. **Drop in `servers/` folder**

3. **Auto-launches** immediately (or on next restart)

Example server:
```python
import sys
from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    return "My Server Running!"

if __name__ == "__main__":
    port = int(sys.argv[1])  # Port from launcher
    app.run(port=port)
```

## 📂 DIRECTORY STRUCTURE

```
E:\ECHO_XV4\MLS\
├── master_modular_launcher_enhanced.py   # Main launcher
├── config.yaml                          # Configuration
├── requirements.txt                     # Dependencies
├── launch_v3.bat                        # Windows launcher
├── install.ps1                          # PowerShell installer
├── DOCUMENTATION.md                     # Full documentation
├── servers/                             # Drop servers here
│   ├── ultra_speed_mcp_server.py
│   ├── comprehensive_api_server_ULTIMATE.py
│   ├── crystal_memory_server_enhanced.py
│   ├── multi_llm_defense.py
│   └── ... (20+ more servers)
├── logs/                                # Server logs
│   ├── master.log
│   └── [server_logs]
└── static/                              # Dashboard files
```

## 🛠️ TROUBLESHOOTING

### Server Not Launching?
1. Check `logs/master.log` for errors
2. Verify server accepts port as `sys.argv[1]`
3. Ensure health endpoint exists at `/health`

### Dashboard Not Loading?
1. Check port 9000 is free
2. Verify Flask installed: `pip install flask`
3. Check firewall settings

### Health Checks Failing?
1. Implement `/health` endpoint returning 200
2. Check `health_check_timeout` in config
3. Verify server is actually running

## 🚨 COMMAND EXAMPLES FOR CLAUDE

When using Claude Desktop with MCP:

```
"Show me all running servers"
"Launch the quantum defender"
"Stop the crystal memory server"
"Restart any failed servers"
"How many servers are currently active?"
"Check the health of all servers"
"Launch all servers that aren't running"
```

## 📈 MONITORING

### Dashboard Features (http://localhost:9000)
- **Server Grid**: Visual status of all servers
- **Metrics Panel**: Health checks, auto-heals, uptime
- **Control Buttons**: Launch/Stop/Restart each server
- **Instance View**: See all running instances and PIDs
- **Auto-refresh**: Updates every 5 seconds

### Log Files
- **Master Log**: `logs/master.log`
- **Server Logs**: `logs/[server_name]_[instance]_[timestamp].log`

## 🔐 AUTHORITY & COMPLIANCE

- **Authority Level**: 11.0 (Maximum)
- **Commander**: Bobby Don McWilliams II
- **Foundation**: GS343 Divine Overseer
- **Protocol**: Phoenix Auto-Heal Active
- **Environment**: ECHO_XV4 Production
- **Security**: Bloodline Authentication

## 🆘 SUPPORT

1. **Documentation**: See `DOCUMENTATION.md` for detailed info
2. **Logs**: Check `logs/` directory for debugging
3. **Config**: Adjust `config.yaml` for customization
4. **Dashboard**: Monitor at http://localhost:9000

## ✨ SYSTEM STATUS

```
═══════════════════════════════════════════════
  MASTER MODULAR LAUNCHER V3 - OPERATIONAL
═══════════════════════════════════════════════
  Servers Discovered:     20+
  Auto-Launch:           ENABLED
  Hot Reload:            ACTIVE
  Health Monitoring:     RUNNING
  Phoenix Protocol:      ENGAGED
  MCP Integration:       ONLINE
  Dashboard:             http://localhost:9000
═══════════════════════════════════════════════
```

---

**Version**: 3.0.0  
**Build**: PRODUCTION  
**Last Updated**: 2024  
**Status**: **FULLY OPERATIONAL**
