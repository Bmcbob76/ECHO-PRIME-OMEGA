# 🧪 ECHO COPILOT BRIDGE - VERIFICATION TESTS

**Date:** 2025-10-06  
**Authority Level:** 11.0  
**Status:** Testing installation

---

## ✅ STEP 1: VERIFY EXTENSION LOADED

### In VS Code:
1. **Open Extensions panel** (Ctrl+Shift+X)
2. **Search:** "ECHO Copilot Bridge"
3. **Expected:** ✅ Green checkmark "Enabled"

### Check Output Panel:
1. **Open Output** (Ctrl+Shift+U or View → Output)
2. **Select dropdown:** "ECHO Bridge Debug"
3. **Expected logs:**
   ```
   ✓ ECHO Bridge activated
   ✓ Loading MCP client...
   ✓ Connecting to Desktop Commander...
   ✓ Tools registered: 105+ tools
   ```

---

## ✅ STEP 2: TEST EXTENSION COMMANDS

### Command 1: Connection Status
```
Press: Ctrl+Shift+P
Type: "ECHO: Show Connection Status"
Expected: Shows server URLs, connection state, tool count
```

### Command 2: List Tools
```
Press: Ctrl+Shift+P
Type: "ECHO: List Available Tools"
Expected: Lists all 105+ tools with descriptions
```

### Command 3: Manual Connect (if needed)
```
Press: Ctrl+Shift+P
Type: "ECHO: Connect to ECHO Servers"
Expected: "✓ Connected to ECHO servers"
```

---

## ✅ STEP 3: VERIFY MCP SERVER RUNNING

### Check Desktop Commander MCP:
The extension needs Desktop Commander MCP server running.

**Location:** Should be at one of these:
- `E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge\desktop_commander_stdio.py`
- Or wherever Desktop Commander MCP is installed

**Auto-start:** Extension should auto-start the MCP server via stdio transport.

**Manual test:**
```powershell
# Check if process is running
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*desktop*"}
```

---

## ✅ STEP 4: TEST WITH GITHUB COPILOT

### Verify Copilot Can See ECHO Tools:

**In VS Code, open Copilot Chat:**
```
Press: Ctrl+Alt+I (or click Copilot icon)
```

### Test 1: File Reading
```
Ask Copilot: "Use ECHO tools to read the file at E:\ECHO_XV4\test.txt"
Expected: Copilot should use echo.file.read tool
```

### Test 2: Directory Listing
```
Ask Copilot: "List all files in E:\ECHO_XV4\MLS directory"
Expected: Copilot should use echo.file.list tool
```

### Test 3: OCR Screens
```
Ask Copilot: "OCR all my screens and tell me what text you see"
Expected: Copilot should use echo.ocr.all_screens tool
```

### Test 4: Windows Info
```
Ask Copilot: "What processes are running on my system?"
Expected: Copilot should use echo.windows.list_processes tool
```

---

## 🔍 TROUBLESHOOTING

### ❌ Issue: Extension not showing in Extensions panel
**Fix:**
```powershell
# Reinstall extension
code --install-extension E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge\echo-copilot-bridge-1.0.0.vsix --force
```

### ❌ Issue: No output in "ECHO Bridge Debug" channel
**Fix:**
1. Restart VS Code
2. Check extension activation: Should auto-activate on startup
3. Manually trigger: Run "ECHO: Connect to ECHO Servers"

### ❌ Issue: "Failed to connect to MCP server"
**Possible causes:**
1. Desktop Commander path incorrect in settings
2. Python not found at expected location
3. MCP server file missing

**Fix:**
1. Open VS Code Settings (Ctrl+,)
2. Search: "echo.servers"
3. Verify paths are correct
4. Check extension settings for MCP server path

### ❌ Issue: Copilot doesn't see ECHO tools
**Possible causes:**
1. Extension not connected to MCP server
2. Tools not registered with Copilot API
3. Copilot extension not enabled

**Fix:**
1. Run "ECHO: Show Connection Status" - should show 105+ tools
2. Restart Copilot extension
3. Restart VS Code
4. Check Output → "ECHO Bridge Debug" for errors

---

## 📊 EXPECTED SUCCESS STATE

### ✅ Extension Status:
```
Name: ECHO Copilot Bridge
Version: 1.0.0
Status: ✅ Enabled
Auto-activate: ✅ On startup
```

### ✅ Connection Status:
```
MCP Server: ✅ Connected
Tool Count: 105+ tools registered
Transport: stdio
Status: Active
```

### ✅ Available Tools (Sample):
```
echo.file.read - Read file contents
echo.file.write - Write to file
echo.file.list - List directory
echo.file.search - Search files
echo.ocr.all_screens - OCR all monitors
echo.windows.list_processes - List processes
echo.windows.focus_window - Focus window
... (100+ more tools)
```

### ✅ Copilot Integration:
```
Copilot can invoke ECHO tools via:
- @echo read file ...
- @echo list directory ...
- @echo OCR screens ...
```

---

## 🎯 PERFORMANCE VERIFICATION

### Check Response Times:
Look in Output → "ECHO Bridge Debug" for:
```
Tool execution time: <50ms (filesystem)
Tool execution time: <500ms (OCR)
Tool execution time: <10ms (Windows API)
```

### Check for Errors:
```
No errors should appear in:
- Output → "ECHO Bridge Debug"
- Output → "Extension Host"
- Developer Console (Help → Toggle Developer Tools)
```

---

## 📝 VERIFICATION CHECKLIST

**After installation, verify:**
- [ ] Extension appears in Extensions panel
- [ ] "ECHO Bridge Debug" output channel exists
- [ ] Connection status shows "Connected"
- [ ] Tool count shows 105+ tools
- [ ] "ECHO: List Available Tools" command works
- [ ] Copilot chat can invoke ECHO tools
- [ ] File operations work (read, write, list)
- [ ] OCR works (if you test it)
- [ ] Windows operations work (if you test them)
- [ ] No errors in Output panels

---

## 🚀 NEXT ACTIONS AFTER VERIFICATION

### If All Tests Pass: ✅
1. **Document success** - Update project status
2. **Add to MLS** - Register in Master Launcher
3. **Enable auto-start** - Configure MLS to keep extension active
4. **Test workflows** - Try complex multi-step operations
5. **Monitor performance** - Check for any slowdowns

### If Tests Fail: ❌
1. **Check Output logs** - Look for specific errors
2. **Verify paths** - Ensure all file paths are correct
3. **Test MCP server standalone** - Verify it works outside extension
4. **Restart VS Code** - Sometimes helps with loading issues
5. **Reinstall if needed** - Use --force flag

---

## 💬 REPORT RESULTS

**After testing, report status:**
```
Commander: "Extension status: [WORKING/ISSUES]"
- Tool count: [number]
- Connection: [ACTIVE/FAILED]
- Copilot integration: [YES/NO]
- Issues found: [list any problems]
```

---

**Authority Level:** 11.0  
**Test Phase:** ACTIVE  
**Expected Result:** ✅ 105+ tools available to Copilot

🎖️ **End of Verification Guide**
