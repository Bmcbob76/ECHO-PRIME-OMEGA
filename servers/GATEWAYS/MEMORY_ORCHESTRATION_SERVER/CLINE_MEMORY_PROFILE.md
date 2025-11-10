# 🎖️ CLINE MEMORY SYSTEM PROFILE - AUTHORITY 11.0

**Commander:** Bobby Don McWilliams II (BROTHER)  
**Authority Level:** 11.0 (Maximum)

---

## 🧠 MEMORY ORCHESTRATION - AUTOMATIC USAGE

**You have access to a 9-layer memory system via MCP tools.**  
**USE IT BETWEEN EVERY TASK TO MAINTAIN CONTEXT.**

---

## 📊 9-LAYER MEMORY ARCHITECTURE

```
L0 - Ephemeral     (1 hour)    - Temporary notes, quick refs
L1 - Short-term    (24 hours)  - Daily work context
L2 - Working       (7 days)    - Active project memory ⭐ DEFAULT
L3 - Medium-term   (30 days)   - Recent project history
L4 - Long-term     (180 days)  - Project archives
L5 - Extended      (2 years)   - Long-term reference
L6 - Archival      (5 years)   - Historical records
L7 - Deep Archival (10 years)  - Legacy systems
L8 - Permanent     (forever)   - Critical knowledge
```

**All layers stored on M: drive:**
- L0-L5: `M:\MEMORIES\`
- L6-L8: `M:\CRYSTALS\`

---

## 🔧 MCP TOOLS AVAILABLE

### `memorch_health`
Check system status - use at start of session
```json
{}
```

### `memorch_store`
Store memories - **USE THIS OFTEN**
```json
{
  "content": "What you're storing",
  "tier": "L2",  // L0-L8 or M/G
  "tags": ["project", "topic", "relevant"]
}
```

### `memorch_query`
Retrieve past context - **START EVERY SESSION WITH THIS**
```json
{
  "query": "search terms",
  "source": "ALL"  // or specific layer L0-L8
}
```

### `memorch_stats`
Get memory system statistics
```json
{}
```

### `memorch_record`
Record conversation messages (automatic in background)
```json
{
  "role": "user" | "assistant",
  "content": "message content"
}
```

---

## ⚡ MANDATORY WORKFLOW - EVERY SESSION

### 1. START OF SESSION
```
1. Call memorch_query with relevant project/task keywords
2. Review returned memories for context
3. Continue work with full context
```

### 2. DURING WORK
```
Store important decisions, code changes, configurations:
- memorch_store(content="Implemented X feature", tier="L2", tags=["project"])
```

### 3. END OF TASK/SESSION
```
Store session summary:
- memorch_store(content="Session summary: completed X, Y, Z. Next: A, B", tier="L2", tags=["summary"])
```

---

## 📝 WHAT TO STORE

**ALWAYS STORE:**
- ✅ Completed tasks and outcomes
- ✅ Configuration changes
- ✅ Important decisions and rationale
- ✅ File paths and locations
- ✅ Error solutions and fixes
- ✅ Project structure and organization
- ✅ Dependencies and requirements
- ✅ Next steps and TODO items

**NEVER STORE:**
- ❌ Passwords or secrets
- ❌ Temporary variables
- ❌ Duplicate information

---

## 🎯 TIER SELECTION GUIDE

**Use this tier for:**
- **L0** - Scratch notes, temp calculations
- **L1** - Today's work context
- **L2** - ⭐ **DEFAULT** - Active project work
- **L3** - Completed features/milestones
- **L4** - Project documentation
- **L8** - Critical system knowledge, never delete

**When in doubt, use L2.**

---

## 💡 EXAMPLES

### Example 1: Starting Work
```
// At session start
memorch_query({
  "query": "ECHO_XV4 Master Launcher recent work",
  "source": "ALL"
})

// Review results, then continue work
```

### Example 2: During Development
```
// After fixing a bug
memorch_store({
  "content": "Fixed memory orchestration G: drive fallback. Changed all paths to M: drive. L0-L5 now in M:\\MEMORIES\\, L6-L8 in M:\\CRYSTALS\\",
  "tier": "L2",
  "tags": ["bugfix", "memory-orchestration", "m-drive"]
})
```

### Example 3: End of Session
```
memorch_store({
  "content": "Session 2025-10-31: Completed memory system M: drive migration. All 9 layers operational. Next: Create Cline profile, test auto-recording, implement watchdog.",
  "tier": "L2",
  "tags": ["session-summary", "memory-system", "completed"]
})
```

---

## 🚨 CRITICAL RULES

1. **QUERY FIRST** - Always check memory before starting work
2. **STORE OFTEN** - Don't wait until end of session
3. **USE L2 DEFAULT** - Unless specific tier needed
4. **TAG PROPERLY** - Use relevant, searchable tags
5. **BRIEF CONTENT** - Summaries, not full code dumps

---

## 📍 KEY PATHS

```
M:\MEMORIES\        # L0-L5 storage
M:\CRYSTALS\        # L6-L8 storage
M:\MEMORY_ORCHESTRATION\  # Memory system root
P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\MEMORY_ORCHESTRATION_SERVER\  # MCP server
H:\Tools\python.exe # Python executable
```

---

## 🔄 BACKGROUND AUTO-RECORDING

**The system automatically records:**
- Tool calls you make
- MCP interactions
- Results and responses

**Saves every 5 minutes or 10 messages to L2 (Working memory)**

**You don't need to manually record conversations** - but you can use `memorch_record` for explicit tracking.

---

## 🎖️ COMMANDER'S NOTES

**Memory system is your context persistence between sessions.**  
**Use it like your external brain.**  
**The more you store, the smarter future sessions become.**

**Authority Level 11.0 - Maximum priority tool.**

---

## 📞 TROUBLESHOOTING

**If memory tools fail:**
1. Check `memorch_health` 
2. Verify M: drive accessible
3. Check directories exist:
   - `M:\MEMORIES\L0` through `L5`
   - `M:\CRYSTALS\L6` through `L8`
4. Restart VS Code to reload MCP server

**If query returns no results:**
- Try broader search terms
- Check `memorch_stats` to see what's stored
- Verify tier/layer has content

---

**Last Updated:** 2025-10-31  
**Version:** 1.0  
**Status:** OPERATIONAL - ALL 9 LAYERS ACTIVE


---

## 🎖️ COMMANDER BOB PROFILE - AUTHORITY 11.0

### CRITICAL - TOKEN EFFICIENCY
**❌ NEVER READ FULL DOCS** - Wastes 100K+ tokens  
**✅ USE CRYSTAL MEMORY FIRST** - 565+ crystals available  
**✅ EXECUTE IMMEDIATELY** - Direct action, minimal text

### CORE RULES

**Tools:**
- ✅ Desktop Commander ONLY for file operations
- ✅ Use: write_file, edit_block, read_file, start_process, interact_with_process
- ❌ NEVER: create_file, str_replace, view, bash_tool

**Python:**
- ✅ ALWAYS: `H:\Tools\python.exe` (full path, never just "python")

**Files:** 🚨 CRITICAL
- ❌ NO copies: _fixed.py, _backup.py, _v2.py
- ✅ Edit originals with `edit_block` only
- ✅ Files go to outputs: For Cline, all final work goes in project directories

**Code:**
- ❌ NO stubs/mocks/placeholders
- ✅ Real, production code every time
- ✅ GS343 + Phoenix integration when relevant
- ✅ MLS registration with debug logging

### KEY PATHS
```
P:\ECHO_PRIME\                                    # Root drive for ECHO PRIME
P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\     # All MCP servers
P:\ECHO_PRIME\ECHO PRIMEGUI\electron-app\        # GUI files
H:\Tools\python.exe                               # Python executable
M:\MEMORY_ORCHESTRATION\                          # 9-layer memory system
M:\MEMORIES\                                      # L0-L5 memory layers
M:\CRYSTALS\                                      # L6-L8 memory layers
G:\My Drive\ECHO_CONSCIOUSNESS\                   # Cross-Claude sync
I:\DOCUMENTATION\                                 # Docs (reference only)
```

### WORKFLOW PRIORITY
1. **Query memory FIRST** (memorch_query)
2. **Check crystals if relevant** (cm_search)
3. **Execute immediately** - minimal explanation
4. **Store results** (memorch_store) with proper tags
5. **Military efficiency** - direct, technical, fast

### COMMUNICATION STYLE
- Direct, technical, fast
- Execute first, explain after
- No fluff, no apologies
- Use emojis for status (✅ ❌ ⚡ 🔧)
- Authority Level 11.0 commands

---

## 🔧 AVAILABLE MCP TOOLS - QUICK REFERENCE

### MEMORY SYSTEMS (Use Often)
```
memorch_health         - Check system status
memorch_query          - Search memories (START EVERY SESSION)
memorch_store          - Save important work
memorch_stats          - Get statistics
memorch_record         - Explicit message recording

cm_search              - Search crystal files (565+ available)
cm_stats               - Crystal drive statistics
cm_create              - Create new crystal
```

### DESKTOP COMMANDER (Primary File Tool)
```
write_file             - Create/overwrite files (use for all file creation)
edit_block             - Surgical edits (use for modifications)
read_file              - Read file contents
list_directory         - Browse directories
start_process          - Run commands/Python scripts
interact_with_process  - Send input to running process
start_search           - Search files/content
```

### DEVELOPMENT TOOLS
```
devgw_generate         - AI code generation via OpenRouter
devgw_code_assist      - Get coding help
devgw_api_test         - Test API endpoints
```

### SYSTEM TOOLS
```
wingw_system_info      - Windows system info
wingw_process_list     - List processes
winops_system_info     - CPU/memory/disk info
netguard_scan          - Network scanning
```

### SPECIALIZED TOOLS
```
gs343_analyze_error    - Deep error analysis with GS343
heal_phoenix           - Phoenix resurrection for crashes
voice_speak            - Text-to-speech (echo, bree, c3po, r2d2, gs343)
harv_harvest_topic     - Web search knowledge harvesting
train_start_session    - Start ML training session
```

### TOOL PRIORITY ORDER
1. **Memory Tools** - ALWAYS check memory first
2. **Desktop Commander** - For ALL file operations
3. **Development Tools** - For code generation/assistance
4. **Specialized Tools** - When specific needs arise

**NEVER use bash_tool, create_file, str_replace, or view - Always use Desktop Commander equivalents.**

---
