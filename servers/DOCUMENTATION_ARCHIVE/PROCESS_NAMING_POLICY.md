# ECHO_XV4 PROCESS NAMING POLICY
**Authority Level 11.0 - Commander Bobby Don McWilliams II**

## 📋 MANDATORY POLICY

**ALL ECHO_XV4 servers MUST implement process naming** for identification and monitoring.

---

## 🎯 PURPOSE

Process naming enables:
- **Instant Identification** - Know which Python process is which server
- **Easy Monitoring** - Track server performance in system tools
- **Quick Debugging** - Identify problematic servers immediately
- **Professional Operations** - No more "unknown" Python processes

---

## ⚙️ IMPLEMENTATION

### For All New Servers:

**1. Add Import (After other imports, before main code):**
```python
# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass
```

**2. That's It!**
The `echo_process_naming` module auto-executes on import and:
- Reads `SERVER_NAME` environment variable (set by MLS launcher)
- Calls `setproctitle.setproctitle()` to rename the process
- Falls back to script name + port if environment var missing

---

## 🚀 MLS LAUNCHER INTEGRATION

The Master Modular Launcher automatically:

1. **Sets Environment Variable** before launching each server:
   ```python
   env['SERVER_NAME'] = f"ECHO_XV4: {server['name']} - Port {server['port']}"
   ```

2. **All MLS-launched servers** get named automatically

3. **Manual launches** use fallback naming based on script name

---

## 📊 NAMING FORMAT

**Standard Format:**
```
ECHO_XV4: [Server Name] - Port [Port Number]
```

**Examples:**
- `ECHO_XV4: Crystal Memory Enhanced - Port 8000`
- `ECHO_XV4: Windows API Ultimate - Port 8343`
- `ECHO_XV4: VS Code API Extension - Port 9001`
- `ECHO_XV4: GS343 Auto-Healer - Port 8010`

**Fallback Format** (when SERVER_NAME not set):
```
ECHO_XV4: [Script Name] - Port [Port]
```

---

## ✅ COMPLIANCE STATUS

### All Servers Updated (17 total):

1. ✅ `WINDOWS_API_ULTIMATE.py`
2. ✅ `unified_developer_api.py`
3. ✅ `ultra_speed_core_server_enhanced.py`
4. ✅ `ultra_speed_mcp_server.py`
5. ✅ `gs343_autohealer_server_enhanced.py`
6. ✅ `echo_shield_defense_server.py`
7. ✅ `epcp3_0_c3po_server.py`
8. ✅ `crystal_memory_server_enhanced.py`
9. ✅ `crystal_memory_server_MASTER.py`
10. ✅ `desktop_commander_server.py`
11. ✅ `echo_fusion_server.py`
12. ✅ `ECHO_MASTER_MCP.py`
13. ✅ `echo_prime_service.py`
14. ✅ `ECHO_WINDOWS_API_225.py`
15. ✅ `epcp3_backend.py`
16. ✅ `multi_llm_defense.py`
17. ✅ `network_guardian_integration.py`
18. ✅ `phoenix_voice_guilty_spark.py`

---

## 🔧 DEPENDENCIES

**Required Package:**
```bash
pip install setproctitle --break-system-packages
```

**Added to `requirements.txt`:**
```
setproctitle>=1.3.0  # Process naming for server identification
```

---

## 🪟 PLATFORM NOTES

### Windows:
- Task Manager still shows "python.exe" (Windows limitation)
- PowerShell `Get-Process` shows custom name in some fields
- `Get-WmiObject Win32_Process` shows full command line
- Process Explorer and similar tools show custom name

### Linux/Mac:
- Full process name visible in `ps`, `htop`, `top`
- Process monitoring tools show custom name immediately

---

## 📝 TESTING VERIFICATION

**To verify process naming works:**

```powershell
# After launching servers with MLS:
Get-WmiObject Win32_Process | Where-Object {$_.Name -eq "python.exe"} | Select-Object ProcessId, CommandLine

# Look for "ECHO_XV4: [Server Name] - Port [Port]" in output
```

**Or check individual process:**
```powershell
Get-WmiObject Win32_Process -Filter "ProcessId=[PID]" | Select-Object ProcessId, CommandLine
```

---

## 🎖️ COMPLIANCE REQUIREMENT

**This is MANDATORY for all ECHO_XV4 production servers.**

- New servers must include process naming before deployment
- Existing servers without it should be updated immediately
- Non-compliance identified by "unknown" processes in system tools

---

## 📚 FILES

**Core Implementation:**
- `/E/ECHO_XV4/MLS/servers/echo_process_naming.py` - Auto-naming utility
- `/E/ECHO_XV4/MLS/master_modular_launcher_enhanced.py` - Sets SERVER_NAME env var
- `/E/ECHO_XV4/MLS/requirements.txt` - Includes setproctitle dependency

**Documentation:**
- This file: `PROCESS_NAMING_POLICY.md`

---

**Last Updated:** October 4, 2025  
**Status:** FULLY IMPLEMENTED ACROSS ALL SERVERS
