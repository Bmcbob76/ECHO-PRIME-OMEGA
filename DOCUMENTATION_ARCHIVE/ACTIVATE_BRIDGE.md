# 🚀 WINDOWS API BRIDGE - INSTANT ACTIVATION GUIDE

**BRIDGE STATUS:** ✅ FIXED & VALIDATED  
**TIME TO ACTIVATE:** 30 seconds

---

## ⚡ ACTIVATION (3 STEPS)

### **1. VERIFY BACKEND IS RUNNING**
```powershell
curl http://localhost:8343/health
```
**Expected:** `{"success": true, "status": "operational"}`

**If not running, start it:**
```powershell
cd E:\ECHO_XV4\MLS\servers
H:\Tools\python.exe WINDOWS_API_ULTIMATE.py
```

---

### **2. RESTART CLAUDE DESKTOP**
- Close Claude Desktop (exit from system tray)
- Wait 3 seconds
- Reopen Claude Desktop

---

### **3. TEST IT**
Ask Claude: *"List all Windows API tools you have available"*

**Expected:** Claude shows 13 Windows API tools

---

## 🧪 QUICK TESTS

**Health Check:**
```
"Check Windows API server health"
```

**System Info:**
```
"Show my system information"
```

**Live Performance:**
```
"What's my current CPU and RAM usage?"
```

**Process List:**
```
"What are the top 5 processes by memory?"
```

---

## 🎖️ 13 AVAILABLE TOOLS

1. windows_health
2. windows_system_info
3. windows_performance
4. windows_live_performance
5. windows_process_list
6. windows_process_info
7. windows_process_kill
8. windows_memory_stats
9. windows_network_connections
10. windows_service_list
11. windows_service_status
12. windows_ocr_screens_all
13. windows_ocr_screen

---

## 🔧 IF TOOLS DON'T APPEAR

**Check bridge log:**
```powershell
type E:\ECHO_XV4\MLS\logs\windows_api_bridge.log
```

**Test bridge manually:**
```powershell
H:\Tools\python.exe E:\ECHO_XV4\MLS\servers\windows_api_mcp_bridge.py
```

---

**That's it! 30 seconds to full Windows integration.** ✅
