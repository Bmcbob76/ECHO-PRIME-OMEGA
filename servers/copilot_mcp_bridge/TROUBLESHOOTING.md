# 🚨 ECHO COPILOT BRIDGE - TROUBLESHOOTING GUIDE

**Commander:** Bobby Don McWilliams II  
**Authority Level:** 11.0  
**Issue:** EADDRINUSE / ENOENT errors when connecting to MCP server

---

## 🔍 PROBLEM IDENTIFIED

The VS Code extension is trying to spawn `desktop_commander_server.py`, which has **TWO CRITICAL ISSUES**:

### **Issue 1: EADDRINUSE Error**
```
Error: listen EADDRINUSE: address already in use :::8000
```

**What this means:**
- The Python server (`desktop_commander_server.py`) tries to start an HTTP server on a port
- That port is already occupied by another service
- **MCP protocol uses STDIO, NOT HTTP** - the Python server is misconfigured

### **Issue 2: Broken Template Strings**
- The Python file has malformed f-strings or template literals
- This causes syntax errors when the server tries to start

---

## ✅ THE SOLUTION

### **Use the Working Node.js MCP Server Instead**

The **BACKED UP** Desktop Commander MCP server is located at:
```
E:\ECHO_XV4\CLAUDE_EXT_BACKUP\ant.dir.gh.wonderwhy-er.desktopcommandermcp\dist\index.js
```

**This server:**
- ✅ Uses pure STDIO (no HTTP server needed)
- ✅ Works perfectly (currently in use by Claude Desktop)
- ✅ Has no template string issues
- ✅ Implements full MCP protocol correctly

---

## 🔧 FIX STEPS

### **Step 1: Update Extension to Use Node.js Server**

Edit: `E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge\src\extension.ts`

**Find this code (around line 88):**
```typescript
const transport = new StdioClientTransport({
    command: 'python',
    args: ['E:\\ECHO_XV4\\MLS\\servers\\desktop_commander_server.py']
});
```

**Replace with:**
```typescript
const transport = new StdioClientTransport({
    command: 'node',
    args: ['E:\\ECHO_XV4\\CLAUDE_EXT_BACKUP\\ant.dir.gh.wonderwhy-er.desktopcommandermcp\\dist\\index.js']
});
```

### **Step 2: Recompile Extension**

```powershell
cd E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge
npm run compile
```

### **Step 3: Package Extension**

```powershell
npx vsce package --allow-star-activation
```

### **Step 4: Install in VS Code**

```powershell
& "C:\Users\bobmc\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd" --install-extension E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge\echo-copilot-bridge-1.0.0.vsix --force
```

### **Step 5: Reload VS Code**

Press: `Ctrl + Shift + P` → Type: **"Developer: Reload Window"**

---

## 🎯 WHY THIS WORKS

### **MCP Protocol Requirements:**

1. **STDIO Transport** - Server communicates via stdin/stdout (no network ports)
2. **Pure JSON-RPC** - Standard request/response protocol
3. **No HTTP Server** - MCP doesn't use HTTP when using StdioClientTransport

### **Why Python Server Failed:**

```python
# desktop_commander_server.py tries to do this:
app = Flask(__name__)
app.run(host='0.0.0.0', port=8000)  # ❌ WRONG for MCP STDIO!
```

**This creates an HTTP server**, which:
- Binds to port 8000 (causing EADDRINUSE)
- Doesn't communicate via STDIO
- Breaks MCP protocol expectations

### **Why Node.js Server Works:**

```javascript
// index.js correctly implements MCP STDIO
const server = new Server({
  name: 'desktop-commander',
  version: '1.0.0'
}, {
  capabilities: {
    tools: {}
  }
});

// Uses stdio transport (no HTTP)
server.connect(new StdioServerTransport());
```

---

## 🧪 VERIFICATION

After installation, check VS Code status bar (bottom-right):

**Before Fix:**
```
❌ ECHO Connection Failed
```

**After Fix:**
```
✅ $(zap) ECHO Connected (105 tools)
```

**Test Tools:**

Open Copilot Chat and type:
```
@workspace /tools
```

You should see **100+ Desktop Commander tools** including:
- File operations (read_file, write_file, edit_block, etc.)
- Process management (start_process, interact_with_process, etc.)
- Search capabilities (start_search, get_more_search_results, etc.)
- System operations (list_directory, create_directory, etc.)

---

## 📊 CURRENT STATUS

### **What's Working:**
- ✅ Claude Desktop → Node.js MCP server → All tools functional
- ✅ Backup server exists and is proven to work
- ✅ Extension code is correct (just wrong server path)

### **What Needs Fixing:**
- ❌ Extension pointing to broken Python server
- ❌ Python server has template string issues
- ❌ Python server tries to use HTTP instead of STDIO

---

## 🎖️ COMMANDER NOTES

**DO NOT:**
- ❌ Fix the Python server - it's architecturally wrong for MCP STDIO
- ❌ Run the launcher - STDIO transport auto-spawns the server
- ❌ Try to bind ports - MCP STDIO doesn't need network ports

**DO:**
- ✅ Use the proven Node.js backup server
- ✅ Let extension auto-spawn server via STDIO
- ✅ Trust the backup in CLAUDE_EXT_BACKUP (it's SACRED for a reason)

---

**STATUS:** Ready for immediate fix  
**ESTIMATED TIME:** 5 minutes  
**RISK LEVEL:** Zero (using proven backup)

🎖️ **Authority Level 11.0 - Commander Bobby Don McWilliams II**
