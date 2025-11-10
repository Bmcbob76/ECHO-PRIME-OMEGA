# NEXT SESSION: DVP TESTING & SERVER VERIFICATION
**Commander Bobby Don McWilliams II - Authority Level 11.0**
**Date Prepared:** October 4, 2025 - 23:30

---

## 🎯 MISSION OBJECTIVES

### Primary Goals:
1. ✅ Restart all servers with process naming enabled
2. ✅ Verify process naming is working (no more "unknown" servers)
3. ✅ Test VS Code API Extension functionality
4. ✅ Test Windows API Ultimate control
5. ✅ Full DVP (Unified Developer API) integration test

---

## 📋 PRE-FLIGHT CHECKLIST

### ✅ COMPLETED THIS SESSION:

**Dependencies Installed:**
- ✅ setproctitle 1.3.7
- ✅ pywin32 311  
- ✅ opencv-python, pytesseract, easyocr, mss, pyautogui
- ✅ VS Code extension dependencies (express, cors, etc.)

**Code Updates:**
- ✅ Fixed ECHO_XV3 → ECHO_XV4 path in WINDOWS_API_ULTIMATE.py
- ✅ Fixed TypeScript import errors in VS Code extension
- ✅ Added process naming to ALL 18 servers
- ✅ Updated MLS launcher with SERVER_NAME environment variable
- ✅ Compiled and packaged VS Code extension (echo-vscode-api-1.0.0.vsix)
- ✅ Installed VS Code extension

**Documentation:**
- ✅ Created PROCESS_NAMING_POLICY.md
- ✅ Updated requirements.txt with setproctitle
- ✅ Created this preparation document

---

## 🚀 STEP-BY-STEP TEST PROCEDURE

### PHASE 1: Restart Servers with Process Naming

**1. Stop All Current Servers:**
```powershell
# Find all python processes running servers
Get-Process python | Where-Object {$_.Path -like "*H:\Tools\python.exe*"}

# Kill them (or let MLS restart them gracefully)
```

**2. Launch MLS:**
```powershell
cd E:\ECHO_XV4\MLS
H:\Tools\python.exe master_modular_launcher_enhanced.py
```

**3. Verify Auto-Discovery:**
- MLS should find all 18+ servers
- Should launch servers with ports
- Check console output for successful launches

---

### PHASE 2: Verify Process Naming

**1. Check Process Names:**
```powershell
Get-WmiObject Win32_Process | Where-Object {$_.Name -eq "python.exe"} | Select-Object ProcessId, CommandLine | Format-List
```

**Expected Output:**
```
ProcessId   : 12345
CommandLine : H:\Tools\python.exe ... 
(Should see "ECHO_XV4: Crystal Memory Enhanced - Port 8000" style naming)

ProcessId   : 12346  
CommandLine : H:\Tools\python.exe ...
(Should see "ECHO_XV4: Windows API Ultimate - Port 8343")
```

**2. Verify NO "Unknown" Servers:**
```powershell
netstat -ano | findstr "LISTENING" | findstr "8000 8002 8006 8010 8015 8030 8343 8344 9000 9001"
```

- Cross-reference PIDs with process names
- ALL should have identifiable names
- NO generic "python.exe" descriptions

---

### PHASE 3: Test VS Code API Extension

**VS Code Extension Status:**
- ✅ Compiled: `/E/ECHO_XV4/MLS/servers/vscode_api_extension/out/`
- ✅ Packaged: `echo-vscode-api-1.0.0.vsix`
- ✅ Installed in VS Code
- ⏳ Should auto-start on Port 9001

**Test Commands:**

**1. Check Extension Status:**
```bash
# In VS Code Command Palette (Ctrl+Shift+P):
ECHO: Get API Server Status
```

**2. Test API Endpoint:**
```powershell
curl http://localhost:9001/api/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "server": "ECHO VS Code API",
  "port": 9001
}
```

**3. Test File Operations:**
```powershell
# Open a file via API
curl -X POST http://localhost:9001/api/file/open -H "Content-Type: application/json" -d '{"path": "E:\\ECHO_XV4\\test.txt"}'
```

**4. Test Editor Control:**
```powershell
# Insert text
curl -X POST http://localhost:9001/api/editor/insert -H "Content-Type: application/json" -d '{"text": "Hello from API"}'
```

---

### PHASE 4: Test Windows API Ultimate

**Windows API Status:**
- ✅ Running on Port 8343 and/or 8344
- ✅ 225+ endpoints available
- ✅ 4-Screen OCR system integrated

**Test Commands:**

**1. Health Check:**
```powershell
curl http://localhost:8343/api/health
```

**2. List Available Endpoints:**
```powershell
curl http://localhost:8343/api/endpoints
```

**3. Test Window Management:**
```powershell
# List windows
curl http://localhost:8343/api/windows/list

# Get active window
curl http://localhost:8343/api/windows/active
```

**4. Test Process Control:**
```powershell
# List processes
curl http://localhost:8343/api/process/list

# Get process info
curl http://localhost:8343/api/process/info?pid=12345
```

**5. Test OCR (if available):**
```powershell
# Capture screen
curl http://localhost:8343/api/ocr/screen/0

# Read text from coordinates
curl "http://localhost:8343/api/ocr/region?x=100&y=100&width=500&height=300"
```

---

### PHASE 5: Test Unified Developer API Integration

**Unified API Status:**
- ✅ Running on Port 9000
- ✅ Orchestrates VS Code API + Windows API + Desktop Commander

**Test Commands:**

**1. Health Check:**
```powershell
curl http://localhost:9000/api/health
```

**2. Test Coordinated Operations:**
```powershell
# Open file in VS Code + capture screen
curl -X POST http://localhost:9000/api/developer/workflow -H "Content-Type: application/json" -d '{
  "action": "open_and_view",
  "file": "E:\\ECHO_XV4\\test.py"
}'
```

**3. Test Complete DVP Workflow:**
```powershell
# 1. Open VS Code
# 2. Open file
# 3. Navigate to line
# 4. Insert code
# 5. Save
# 6. Run tests

curl -X POST http://localhost:9000/api/developer/complete-task -H "Content-Type: application/json" -d '{
  "task": "fix_bug",
  "file": "E:\\ECHO_XV4\\MLS\\servers\\test_server.py",
  "line": 45,
  "fix": "updated code here"
}'
```

---

## 📊 SUCCESS CRITERIA

### Process Naming:
- ✅ All servers show "ECHO_XV4: [Name] - Port [Port]" format
- ✅ No "unknown" or generic "python.exe" processes
- ✅ Easy to identify which server is which

### VS Code API:
- ✅ Extension running on Port 9001
- ✅ Can open files programmatically
- ✅ Can edit text via API
- ✅ Can run commands via API
- ✅ Can navigate editor via API

### Windows API:
- ✅ Server running on Port 8343/8344
- ✅ All 225+ endpoints responding
- ✅ Window management working
- ✅ Process control working
- ✅ OCR system operational (if applicable)

### Unified Developer API:
- ✅ Orchestration working across all 3 components
- ✅ Desktop Commander integration operational
- ✅ Complete workflows executing successfully

---

## 🔧 KNOWN ISSUES TO MONITOR

### From This Session:
1. ⚠️ OCR system had numpy compatibility warning (but initialized)
2. ⚠️ Windows API Ultimate auto-selected Port 8344 (8343 in use)
3. ✅ VS Code extension needed import style fixes (RESOLVED)
4. ✅ ECHO_XV3 paths in code (RESOLVED - changed to XV4)

### Watch For:
- Port conflicts if multiple instances running
- Permission issues with Windows API operations
- VS Code extension activation timing
- MLS auto-discovery failures

---

## 📁 KEY FILES MODIFIED THIS SESSION

### Core Files:
- `E:\ECHO_XV4\MLS\master_modular_launcher_enhanced.py` - Added setproctitle + SERVER_NAME
- `E:\ECHO_XV4\MLS\servers\echo_process_naming.py` - NEW - Auto-naming utility
- `E:\ECHO_XV4\MLS\servers\WINDOWS_API_ULTIMATE.py` - Fixed XV3→XV4 paths + process naming
- `E:\ECHO_XV4\MLS\servers\vscode_api_extension\src\api_server.ts` - Fixed imports

### All 18 Server Files Updated:
(Each has `import echo_process_naming` added)

### Documentation:
- `E:\ECHO_XV4\MLS\servers\PROCESS_NAMING_POLICY.md` - NEW
- `E:\ECHO_XV4\MLS\requirements.txt` - Added setproctitle
- This file - `NEXT_SESSION_DVP_TESTING.md`

---

## ⚡ QUICK START COMMANDS

**To start testing immediately:**

```powershell
# 1. Launch MLS
cd E:\ECHO_XV4\MLS
H:\Tools\python.exe master_modular_launcher_enhanced.py

# 2. Verify processes (new terminal)
Get-WmiObject Win32_Process | Where-Object {$_.Name -eq "python.exe"} | Select-Object ProcessId, CommandLine

# 3. Check ports
netstat -ano | findstr "LISTENING" | findstr ":80\|:90"

# 4. Test VS Code API
curl http://localhost:9001/api/health

# 5. Test Windows API  
curl http://localhost:8343/api/health

# 6. Test Unified API
curl http://localhost:9000/api/health

# 7. BUILD MCP BRIDGE (CRITICAL - Makes all Windows APIs available as tools!)
# This creates the bridge so Claude can access 225+ Windows API endpoints
cd E:\ECHO_XV4\MLS\servers
# Ask Claude: "Create the Windows API MCP Bridge server"
# Claude will create: windows_api_mcp_bridge.py

# 8. CONFIGURE MCP BRIDGE in Claude Desktop
# Edit: C:\Users\bobmc\AppData\Roaming\Claude\claude_desktop_config.json
# Add this server configuration to the "mcpServers" section:
<windows_api_mcp_bridge_config>
"windows_api": {
  "command": "H:\\Tools\\python.exe",
  "args": [
    "E:\\ECHO_XV4\\MLS\\servers\\windows_api_mcp_bridge.py"
  ]
}
</windows_api_mcp_bridge_config>

# 9. RESTART Claude Desktop to load new MCP tools
# After restart, Claude will have 225+ Windows API tools available!

# 10. VERIFY MCP TOOLS LOADED
# Ask Claude: "List all available Windows API tools"
# Should see categories: Process, Window, File, Registry, Service, etc.
```

---

## 🎯 **MCP BRIDGE PRIORITY**

**CRITICAL:** The MCP Bridge is the missing piece that makes DVP complete!

**Without it:**
- ❌ Windows APIs only accessible via HTTP curl commands
- ❌ Claude cannot use Windows operations in workflows
- ❌ Manual API calls required for each operation

**With it:**
- ✅ All 225+ Windows APIs as native Claude tools
- ✅ Claude can manage windows, processes, files directly
- ✅ Full automation capabilities
- ✅ True human-level development workflow

**Time to build:** ~30 minutes  
**Impact:** Transforms DVP from "accessible" to "integrated"

---

## 🎖️ EXPECTED RESULTS

**After successful testing:**
- All servers named and identifiable ✅
- VS Code controllable via REST API ✅
- Windows operations automated via API ✅
- Claude can work like a human developer ✅
- DVP system fully operational ✅

---

**Prepared By:** Claude (Authority Level 11.0)  
**For:** Commander Bobby Don McWilliams II  
**Status:** READY FOR NEXT SESSION TESTING  
**Priority:** HIGH - DVP System Validation
