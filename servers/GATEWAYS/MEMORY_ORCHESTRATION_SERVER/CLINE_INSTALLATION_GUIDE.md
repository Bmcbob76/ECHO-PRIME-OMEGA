# 🎖️ CLINE MEMORY SYSTEM - INSTALLATION GUIDE

**Authority Level:** 11.0  
**Target:** VS Code + Cline Extension

---

## ⚡ QUICK INSTALL (3 STEPS)

### STEP 1: Open Cline Settings

**In VS Code:**
1. Press `Ctrl+Shift+P` (Command Palette)
2. Type: `Preferences: Open User Settings (JSON)`
3. Press Enter

OR

1. Click gear icon (bottom left)
2. Select "Settings"
3. Click `{}` icon (top right) for JSON mode

---

### STEP 2: Add Custom Instructions

**Copy this block into your settings.json:**

```json
{
  "cline.customInstructions": "READ P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\GATEWAYS\\MEMORY_ORCHESTRATION_SERVER\\CLINE_MEMORY_PROFILE.md\n\n🎖️ COMMANDER BOB - AUTHORITY 11.0\n\nMEMORY SYSTEM MANDATORY:\n1. START: memorch_query for context\n2. WORK: Store important changes\n3. END: Store session summary\n\nUse L2 tier by default. Tag everything. Never lose context.",
  
  "cline.alwaysAllowReadOnly": true
}
```

**If you already have Cline settings, add the `customInstructions` line to existing config.**

---

### STEP 3: Verify MCP Server Connection

**Check your MCP settings are correct:**

1. Open: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

2. Verify `memory-orchestration` entry exists:

```json
{
  "mcpServers": {
    "memory-orchestration": {
      "command": "H:\\Tools\\python.exe",
      "args": ["-u", "P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\GATEWAYS\\MEMORY_ORCHESTRATION_SERVER\\memory_orchestration_mcp.py"],
      "disabled": false
    }
  }
}
```

---

## ✅ TEST INSTALLATION

### Test 1: Restart VS Code
```
Close VS Code completely
Reopen VS Code
Open Cline
```

### Test 2: Ask Cline

```
"Check your memory system"
```

**Expected Response:**
- Cline should call `memorch_health`
- Should report 9 layers active
- Should show operational status

### Test 3: Query Test
```
"Query memory for recent work"
```

**Expected Response:**
- Cline should call `memorch_query`
- Should search for relevant context
- Should show any stored memories

### Test 4: Store Test
```
"Store a test memory: Installation verified"
```

**Expected Response:**
- Cline should call `memorch_store`
- Should confirm storage success
- Should show M: drive path

---

## 🔧 TROUBLESHOOTING

### Issue: Cline doesn't use memory tools

**Fix 1: Check Custom Instructions**
- Verify `cline.customInstructions` is in settings.json
- Restart VS Code

**Fix 2: Remind Cline**
```
"You have memory orchestration MCP tools. Use memorch_query to check for context."
```

**Fix 3: Explicit Command**
```
"Use the memorch_health tool to check memory system"
```

### Issue: MCP server not loading

**Fix: Check MCP Settings**
1. Open: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
2. Verify `memory-orchestration` exists and `disabled: false`
3. Restart VS Code

### Issue: Memory tools timeout or fail

**Fix: Verify M: Drive**
```powershell
# Check directories exist
dir M:\MEMORIES
dir M:\CRYSTALS

# If missing, create:
mkdir M:\MEMORIES\L0, M:\MEMORIES\L1, M:\MEMORIES\L2, M:\MEMORIES\L3, M:\MEMORIES\L4, M:\MEMORIES\L5
mkdir M:\CRYSTALS\L6, M:\CRYSTALS\L7, M:\CRYSTALS\L8
```

---

## 📊 VERIFICATION CHECKLIST

- [ ] Custom instructions added to VS Code settings
- [ ] MCP server configured in Cline settings
- [ ] VS Code restarted
- [ ] `memorch_health` returns operational
- [ ] `memorch_query` runs successfully
- [ ] `memorch_store` creates files in M: drive
- [ ] Cline uses memory tools automatically

---

## 🎯 EXPECTED BEHAVIOR

**After installation, Cline should:**

1. **Start of every conversation:**
   - Call `memorch_query` to check for relevant context
   - Review past work before starting new tasks

2. **During work:**
   - Store important decisions and changes
   - Use L2 tier by default

3. **End of tasks:**
   - Store session summaries
   - Tag appropriately for future retrieval

**This creates persistent context across all Cline sessions.**

---

## 📁 FILE LOCATIONS

```
Profile:      P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\MEMORY_ORCHESTRATION_SERVER\CLINE_MEMORY_PROFILE.md
MCP Server:   P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\MEMORY_ORCHESTRATION_SERVER\memory_orchestration_mcp.py
VS Settings:  %APPDATA%\Code\User\settings.json
MCP Settings: %APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
Memory Store: M:\MEMORIES\ (L0-L5), M:\CRYSTALS\ (L6-L8)
```

---

## 🎖️ NEXT STEPS

1. ✅ Follow installation steps above
2. ✅ Restart VS Code
3. ✅ Test with Cline
4. ✅ Start using memory system automatically

**The system will maintain context across all your sessions with Cline.**

---

**Commander:** Bobby Don McWilliams II  
**Authority:** 11.0  
**Status:** Ready for deployment
