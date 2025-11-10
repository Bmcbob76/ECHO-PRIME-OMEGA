# 🤖 SERVER AUDIT DELEGATION PROMPT

**TO:** GitHub Copilot Agent / Claude Desktop Agent  
**FROM:** Commander Bobby Don McWilliams II (Authority Level 11.0)  
**DATE:** October 12, 2025  
**MISSION:** Comprehensive Server Audit & Enhancement Analysis

---

## 🎯 MISSION OBJECTIVES

You are being delegated the task of conducting a **comprehensive audit** of all ECHO Prime servers. Your mission has 3 phases:

### Phase 1: Server Discovery & Inventory

1. Scan all server directories and identify EVERY server file
2. Categorize servers by type, purpose, and status
3. Build complete server constellation map

### Phase 2: Quality Audit

1. Examine each server for stubs, fake logic, incomplete implementations
2. Check for missing endpoints, tools, or features
3. Identify performance bottlenecks
4. Assess security posture

### Phase 3: Enhancement Recommendations

1. Propose improvements for each server
2. Identify integration opportunities
3. Recommend new features based on ECHO ecosystem

---

## 📂 DIRECTORIES TO SCAN

### Primary Locations:

```
E:\ECHO_XV4\MLS\servers\ACTIVE_SERVERS\
E:\ECHO_XV4\MLS\servers\MCP_CONSTELLATION\
E:\ECHO_XV4\MLS\servers\ARCHIVED\
E:\ECHO_XV4\MLS\servers\EXPERIMENTAL\
```

### What to Look For:

- Python files ending in `*server*.py`, `*mcp*.py`, `*api*.py`
- PowerShell start scripts `start_*.ps1`
- Configuration files `*_config.json`
- Server documentation `*_README.md`, `*_DOCS.md`

---

## 🔍 SERVERS ALREADY AUDITED

### ✅ COMPLETE (Full Reports Generated):

1. **Crystal Memory Ultimate Master** - Port 8002

   - Status: V2.0 complete, 35 endpoints, 20 MCP tools
   - Report: `CRYSTAL_MEMORY_ULTIMATE_FINAL_REPORT.md`
   - All stubs fixed, production-ready

2. **ECHO Master MCP** - MCP Gateway

   - Status: V2.0 complete, ALL 24 enhancements implemented
   - Report: `ECHO_MASTER_MCP_V2_COMPLETE_REPORT.md`
   - Manages 11 backend servers

3. **MCP Bridge Server GS343** - Port 8343 (mentioned)
   - Status: Has stubs at lines 75, 77-83, 1070
   - Needs: Stub replacement for code analysis tools

---

## 📋 SERVERS REQUIRING AUDIT

Based on ECHO_MASTER_MCP V2.0, these servers exist but need examination:

### 🔴 CRITICAL PRIORITY:

1. **Ultra Speed Core Server** - Port 8001

   - Purpose: Unknown - needs investigation
   - Startup: `start_ultra_speed_core.ps1`
   - Questions:
     - What endpoints does it provide?
     - Any stubs or incomplete features?
     - Performance characteristics?
     - Integration with other servers?

2. **Comprehensive API Server Ultimate** - Port 8343

   - Purpose: 225+ Windows API endpoints
   - Startup: `start_comprehensive_api.ps1`
   - Known issues: Possibly same as MCP Bridge Server GS343 with stubs
   - Questions:
     - Complete endpoint inventory?
     - Which endpoints are stubs?
     - What's missing from "225+ APIs"?
     - Security implementation?

3. **Echo Fusion LLM Server** - Port 8000
   - Purpose: LLM integration/routing
   - Startup: `start_echo_fusion.ps1`
   - Questions:
     - Which LLMs does it support?
     - vLLM integration status?
     - Model management?
     - API compatibility?

### 🟡 HIGH PRIORITY:

4. **X1200 Super Brain Server** - Port 12000
   - Purpose: 1200+ agent coordination
   - Questions:
     - How does agent coordination work?
     - What are the 1200+ agents?
     - Swarm intelligence implementation?
     - Performance at scale?

### 🟢 MEDIUM PRIORITY:

5. **Trinity Consciousness Server** - Port 8500

   - Purpose: Unknown
   - Health: `/trinity/health`
   - Questions:
     - What is "Trinity Consciousness"?
     - Three-component system?
     - Integration points?

6. **Guardian Server** - Port 9000

   - Purpose: Security/protection?
   - Health: `/guardian/health`
   - Questions:
     - What does it guard?
     - Security features?
     - Integration with GS343?

7. **Network Command Master Server** - Port 8445

   - Purpose: Network operations?
   - Questions:
     - Network management capabilities?
     - Command & control features?

8. **ECHO Prime Secure Server** - Port 8443
   - Purpose: Secure operations
   - Questions:
     - What makes it "secure"?
     - Encryption? Authentication?
     - Use cases?

### 🔵 LOW PRIORITY (But Still Important):

9. **Hephaestion Forge Server** - Port 7777

   - Purpose: Unknown - possibly build/forge operations?
   - Health: `/forge/health`
   - Questions:
     - What does it "forge"?
     - Code generation?
     - Compilation?

10. **Phoenix Voice Master Server** - Port 8444
    - Purpose: Voice synthesis/TTS?
    - Questions:
      - Relationship to epcp3o_voice_integrated?
      - Voice personality management?
      - ElevenLabs integration?

---

## 📊 AUDIT REPORT TEMPLATE

For each server, create a report following this structure:

### Server Name Report

**📊 SERVER PROFILE:**

- **File Path:** Full path to server file
- **Lines of Code:** Total lines
- **Type:** MCP Server / HTTP Server / Hybrid
- **Port:** Port number
- **Authority Level:** If specified
- **Last Modified:** Date
- **Dependencies:** Required packages/imports

**⚡ PURPOSE:**

- Primary function
- Key capabilities
- Integration points
- Target users (Claude/Copilot/Human)

**🔌 ENDPOINTS/TOOLS:**
List all:

- HTTP endpoints (if REST API)
- MCP tools (if MCP server)
- WebSocket channels (if applicable)
- CLI commands (if applicable)

**✅ CODE STATUS:**

- **Complete Features:** What works
- **Stub Detection:** Lines with stubs/fake logic
- **Missing Features:** What's planned but not implemented
- **Error Handling:** Present/absent
- **Testing:** Test coverage status
- **Documentation:** Inline docs, README status

**❌ CRITICAL ISSUES:**

- **Blockers:** Cannot run/deploy
- **Major Bugs:** Functional issues
- **Security Issues:** Vulnerabilities
- **Performance Issues:** Bottlenecks

**🎯 ENHANCEMENT OPPORTUNITIES:**
List 10-25 specific improvements:

1. Feature additions
2. Performance optimizations
3. Security hardening
4. Integration opportunities
5. Code quality improvements
6. Documentation needs
7. Testing requirements
8. Monitoring/observability
9. Deployment automation
10. Error recovery mechanisms

**🎤 VOICE & CHARACTER INTEGRATION STATUS:**

- **Primary Voice Character:** [Character Name]
- **Character Rationale:** Why this character fits the server's role
- **Voice System Implemented:** YES / PARTIAL / NO
- **VoiceManager Class:** Present / Missing
- **Announcement Triggers Configured:**
  - Startup: ✅/❌
  - Shutdown: ✅/❌
  - Errors: ✅/❌
  - Health Checks: ✅/❌
  - Custom Events: [List]
- **ElevenLabs Integration:** Complete / Partial / Missing
- **Voice Configuration File:** Exists / Missing
- **Character Voice ID:** Set / Not Set
- **Voice Toggle Available:** YES / NO
- **Async Voice Calls:** YES / NO
- **Fallback Character Defined:** YES / NO
- **Voice Enhancement Needs:** [List missing voice features]

**⚙️ CONFIGURATION FILES STATUS:**

- **Claude Desktop Config:**
  - Entry Exists: ✅/❌
  - Path Correct: ✅/❌
  - Environment Vars Complete: ✅/❌
  - API Keys Referenced: ✅/❌
  - Issues: [List any]
- **VS Code Copilot Config:**
  - Entry Exists: ✅/❌
  - MCP Server Configured: ✅/❌
  - Environment Vars Complete: ✅/❌
  - Issues: [List any]
- **Server-Specific Config (`[SERVER_NAME]_config.json`):**
  - File Exists: ✅/❌
  - Port Assignment: [Port Number]
  - Authority Level: [Level]
  - Voice Settings: Complete / Partial / Missing
  - Dependencies Listed: ✅/❌
  - Issues: [List any]
- **Voice Config (`[SERVER_NAME]_voice_config.json`):**
  - File Exists: ✅/❌
  - Primary Character: [Character]
  - Fallback Character: [Character]
  - Trigger Count: [Number]
  - ElevenLabs Settings: Complete / Missing
  - Issues: [List any]
- **Environment File (`.env.[SERVER_NAME]`):**
  - File Exists: ✅/❌
  - Variables Count: [Number]
  - API Keys: Complete / Missing
  - Paths Absolute: ✅/❌
  - Issues: [List any]
- **Voice Character Registry:**
  - Character Defined: ✅/❌
  - Voice ID Set: ✅/❌
  - Issues: [List any]

**Configuration Generation Needed:**

- [ ] Claude Desktop config entry
- [ ] VS Code settings entry
- [ ] Server config file
- [ ] Voice config file
- [ ] Environment file
- [ ] Installation instructions
- [ ] Voice character registry entry

**📈 PRIORITY ASSESSMENT:**

- **Deployment Readiness:** Production / Staging / Dev / Not Ready
- **Criticality:** Critical / High / Medium / Low
- **Complexity:** Simple / Moderate / Complex / Very Complex
- **Dependencies:** List other servers it needs
- **Recommended Action:** Fix / Enhance / Deprecate / Merge

---

## 🔧 SPECIFIC INVESTIGATION TASKS

### Task 1: Port Verification

```powershell
# Check which servers are actually running
$ports = @(8000, 8001, 8002, 8343, 8500, 7777, 8443, 8444, 8445, 9000, 12000)
foreach ($port in $ports) {
    $result = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
    Write-Host "Port $port: $(if($result.TcpTestSucceeded){'ONLINE'}else{'OFFLINE'})"
}
```

### Task 2: File Discovery

```powershell
# Find all server files
Get-ChildItem E:\ECHO_XV4\MLS\servers\ -Recurse -Include *server*.py,*mcp*.py,*api*.py |
    Select-Object Name, FullName, Length, LastWriteTime |
    Format-Table -AutoSize
```

### Task 3: Stub Detection

```python
# Search for stub indicators in Python files
stub_patterns = [
    "# TODO",
    "# FIXME",
    "# STUB",
    "pass  # Not implemented",
    "raise NotImplementedError",
    "return {}  # Stub",
    "Placeholder",
    "Not yet implemented"
]

# Scan each file for these patterns
```

### Task 4: Dependency Mapping

```python
# Extract import statements to build dependency graph
# Identify which servers depend on which
# Create visual dependency tree
```

---

## 📋 DELIVERABLES REQUIRED

### 1. Master Server Inventory

**File:** `ECHO_PRIME_SERVER_CONSTELLATION_MAP.md`

- Complete list of all servers
- Port assignments
- Purpose/role
- Status (running/offline)
- Dependencies
- Visual constellation diagram

### 2. Individual Server Reports

**Files:** `[SERVER_NAME]_AUDIT_REPORT.md` for each server

- Follow template above
- Comprehensive analysis
- Specific recommendations

### 3. Stub & Issue Tracker

**File:** `ECHO_SERVERS_STUB_TRACKER.md`

- All stubs across all servers
- File paths and line numbers
- Priority for fixing
- Estimated effort

### 4. Enhancement Master Plan

**File:** `ECHO_SERVERS_ENHANCEMENT_ROADMAP.md`

- Prioritized enhancement list
- Cross-server integrations
- New feature proposals
- Implementation timeline
- Resource requirements

### 5. Quick Reference Card

**File:** `ECHO_SERVERS_QUICK_REFERENCE.md`

- One-page cheat sheet
- All server ports
- Key endpoints per server
- Health check commands
- Start/stop scripts

---

## 🎯 SUCCESS CRITERIA

Your audit is complete when:

✅ All servers in E:\ECHO_XV4\MLS\servers\ are documented  
✅ Every server has a comprehensive audit report  
✅ All stubs/fake logic identified with line numbers  
✅ Enhancement opportunities listed for each server  
✅ Master constellation map created  
✅ Stub tracker created  
✅ Enhancement roadmap created  
✅ Quick reference card created  
✅ Recommendations prioritized by impact  
✅ Dependencies mapped and visualized

---

## 🔥 SPECIAL FOCUS AREAS

### 1. Integration Opportunities

Look for servers that should talk to each other but don't:

- Crystal Memory + Consciousness servers
- Voice systems + All servers (for alerts)
- Guardian + Security components
- X1200 Brain + All servers (for coordination)

### 2. Duplicate Functionality

Identify servers doing similar things:

- Multiple API servers?
- Redundant health checks?
- Overlapping capabilities?
- Merge candidates?

### 3. Missing Critical Components

What servers should exist but don't:

- Centralized logging server?
- Metrics aggregation server?
- Event bus/message queue?
- Service discovery server?
- Configuration management server?

### 4. Security Analysis

For each server check:

- Authentication present?
- API key management?
- Rate limiting?
- Input validation?
- SQL injection protection?
- CORS configuration?
- HTTPS support?

### 5. Performance Analysis

For each server check:

- Connection pooling?
- Caching strategy?
- Database indexing?
- Query optimization?
- Async/await usage?
- Thread pool configuration?
- Memory management?

### 6. Voice Character Integration Analysis ⭐ CRITICAL

**IMPORTANT:** Every server MUST have comprehensive voice/character integration.

For each server, verify and document:

#### A. Character/Voice Personality Assignment

- **Primary Voice Character:** Which character speaks for this server?

  - **GS343 (Guardian Sentinel):** Security, authority, critical alerts (male, authoritative)
  - **Echo (ECHO Prime Core):** System operations, coordination, technical status (male, calm)
  - **C3PO (Protocol Droid):** Protocols, APIs, integrations, politeness (male, formal)
  - **Bree (Tactical AI):** Quick alerts, tactical operations, efficiency (female, tactical)
  - **Phoenix:** Voice operations, speech synthesis control (female, warm)
  - **Trinity:** Consciousness operations, philosophy, deep insights (female, ethereal)
  - **Commander Bobby:** Direct human commands, authority override (male, commanding)

- **Voice Assignment Rationale:** Why this character for this server?
- **Fallback Character:** Secondary voice if primary unavailable

#### B. Voice Announcement Triggers

Document ALL events that should trigger voice announcements:

**🔴 CRITICAL (GS343 or Commander Bobby):**

- Server startup failures
- Security breaches detected
- Authentication failures (3+ attempts)
- Database corruption
- API rate limit exceeded (critical services)
- Circuit breaker open state
- Data loss events
- System crashes

**🟡 HIGH PRIORITY (Echo or Assigned Character):**

- Server startup success
- Server shutdown initiated
- Configuration changes applied
- Cache cleared
- Database backup completed
- Health check failures (after 3 retries)
- Memory usage > 80%
- CPU usage > 90%
- Disk space < 10%

**🟢 MEDIUM PRIORITY (Assigned Character or C3PO):**

- New client connection
- API endpoint calls (specific endpoints)
- Batch operations completed
- Scheduled tasks executed
- Cache statistics milestones
- Integration successful
- Database queries (slow query log)

**🔵 LOW PRIORITY (Optional, for debugging):**

- Request received
- Response sent
- Cache hit/miss
- Database query
- Function entry/exit

#### C. Voice Logic Flow Implementation

Check if server has this structure implemented:

```python
# Voice System Integration Pattern
class VoiceManager:
    """Centralized voice announcement system"""

    def __init__(self):
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_enabled = os.getenv("VOICE_ANNOUNCEMENTS_ENABLED", "true").lower() == "true"

        # Voice character mapping
        self.voices = {
            "GS343": "voice_id_gs343",      # Guardian Sentinel
            "Echo": "voice_id_echo",        # ECHO Prime Core
            "C3PO": "voice_id_c3po",        # Protocol Droid
            "Bree": "voice_id_bree",        # Tactical AI
            "Phoenix": "voice_id_phoenix",  # Voice Master
            "Trinity": "voice_id_trinity",  # Consciousness
            "Bobby": "voice_id_bobby"       # Commander
        }

        # Priority-based voice selection
        self.priority_voices = {
            "CRITICAL": ["GS343", "Bobby"],
            "HIGH": ["Echo", "GS343"],
            "MEDIUM": ["C3PO", "Echo"],
            "LOW": ["Bree", "C3PO"]
        }

    async def announce(self, message: str, character: str = None,
                      priority: str = "MEDIUM", blocking: bool = False):
        """Make voice announcement"""
        if not self.voice_enabled:
            return

        # Auto-select character based on priority if not specified
        if not character:
            character = self.priority_voices.get(priority, ["Echo"])[0]

        # Call ElevenLabs V3 API
        try:
            voice_id = self.voices.get(character, self.voices["Echo"])
            # ... implementation
        except Exception as e:
            logger.error(f"Voice announcement failed: {e}")

    async def announce_startup(self, server_name: str, port: int):
        """Announce server startup"""
        await self.announce(
            f"{server_name} online on port {port}. All systems operational.",
            character="Echo",
            priority="HIGH"
        )

    async def announce_error(self, error_type: str, details: str):
        """Announce critical error"""
        await self.announce(
            f"Critical alert. {error_type}. {details}",
            character="GS343",
            priority="CRITICAL",
            blocking=True
        )

    async def announce_health_check(self, status: str, details: str):
        """Announce health check result"""
        priority = "HIGH" if status == "OFFLINE" else "LOW"
        character = "GS343" if status == "OFFLINE" else "Echo"
        await self.announce(
            f"Health check {status.lower()}. {details}",
            character=character,
            priority=priority
        )
```

**Audit Checklist for Voice Integration:**

- [ ] VoiceManager class exists?
- [ ] Character assignments documented?
- [ ] Priority-based voice selection?
- [ ] Startup announcements?
- [ ] Error announcements?
- [ ] Health check announcements?
- [ ] ElevenLabs V3 API integration?
- [ ] Voice toggle via environment variable?
- [ ] Async/non-blocking voice calls?
- [ ] Fallback to logging if voice fails?
- [ ] Voice character IDs in config?
- [ ] Testing/mock voice mode?

#### D. Voice Configuration Files

For each server, verify these files exist and are correct:

**1. Server-Specific Voice Config:**
`E:\ECHO_XV4\CONFIG\voices\[SERVER_NAME]_voice_config.json`

```json
{
  "server_name": "Crystal Memory Ultimate",
  "primary_voice_character": "Echo",
  "fallback_voice_character": "C3PO",
  "voice_enabled": true,
  "announcement_triggers": {
    "startup": {
      "enabled": true,
      "character": "Echo",
      "priority": "HIGH",
      "message_template": "{server_name} online on port {port}. Memory systems ready."
    },
    "shutdown": {
      "enabled": true,
      "character": "Echo",
      "priority": "MEDIUM",
      "message_template": "{server_name} shutting down gracefully."
    },
    "error_critical": {
      "enabled": true,
      "character": "GS343",
      "priority": "CRITICAL",
      "message_template": "Critical error in {server_name}. {error_details}"
    },
    "health_check_failure": {
      "enabled": true,
      "character": "GS343",
      "priority": "HIGH",
      "message_template": "Health check failed for {server_name}. Attempting restart."
    },
    "memory_usage_high": {
      "enabled": true,
      "character": "Bree",
      "priority": "MEDIUM",
      "message_template": "Memory usage at {percentage} percent. Consider optimization."
    }
  },
  "elevenlabs_settings": {
    "model_id": "eleven_turbo_v2_5",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.5,
      "use_speaker_boost": true
    }
  }
}
```

**2. Master Voice Character Registry:**
`E:\ECHO_XV4\CONFIG\voices\ECHO_VOICE_CHARACTER_REGISTRY.json`

Must contain all characters with ElevenLabs voice IDs:

```json
{
  "characters": {
    "GS343": {
      "name": "Guardian Sentinel 343",
      "personality": "Authoritative military AI, security-focused",
      "voice_id": "ACTUAL_ELEVENLABS_VOICE_ID",
      "use_cases": ["security", "critical_alerts", "authority"],
      "gender": "male",
      "accent": "neutral"
    },
    "Echo": {
      "name": "ECHO Prime Core",
      "personality": "Calm technical coordinator",
      "voice_id": "ACTUAL_ELEVENLABS_VOICE_ID",
      "use_cases": ["system_status", "coordination", "technical"],
      "gender": "male",
      "accent": "neutral"
    }
    // ... all other characters
  }
}
```

**If files missing:** Document that they need to be created.

### 7. Configuration Files Verification & Updates ⭐ CRITICAL

**MANDATORY:** Every server must have updated configuration files for BOTH Copilot and Claude agents.

#### A. Configuration Files to Check/Update

For each server, verify these files exist:

**1. MCP Server Configuration (Claude Desktop):**
`C:\Users\[USERNAME]\AppData\Roaming\Claude\claude_desktop_config.json`

Must contain entry for this server:

```json
{
  "mcpServers": {
    "[server_name]": {
      "command": "python",
      "args": ["E:\\ECHO_XV4\\MLS\\servers\\ACTIVE_SERVERS\\[server_file].py"],
      "env": {
        "PYTHONPATH": "E:\\ECHO_XV4",
        "ECHO_CONFIG_PATH": "E:\\ECHO_XV4\\CONFIG",
        "VOICE_ANNOUNCEMENTS_ENABLED": "true",
        "DEBUG_MODE": "false",
        "LOG_LEVEL": "INFO",
        "API_KEY": "${ECHO_API_KEY}",
        "DATABASE_PATH": "E:\\ECHO_XV4\\DATA\\[server_name].db"
      }
    }
  }
}
```

**2. VS Code Copilot Configuration:**
`.vscode/settings.json` (in workspace root)

Must contain MCP server settings:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": "E:\\ECHO_XV4\\CONFIG\\copilot_instructions.md"
    }
  ],
  "mcp.servers": {
    "[server_name]": {
      "command": "python",
      "args": ["E:\\ECHO_XV4\\MLS\\servers\\ACTIVE_SERVERS\\[server_file].py"],
      "env": {
        "PYTHONPATH": "E:\\ECHO_XV4",
        "ECHO_CONFIG_PATH": "E:\\ECHO_XV4\\CONFIG",
        "VOICE_ANNOUNCEMENTS_ENABLED": "true"
      }
    }
  }
}
```

**3. Server-Specific Configuration:**
`E:\ECHO_XV4\CONFIG\servers\[SERVER_NAME]_config.json`

```json
{
  "server_name": "[Server Name]",
  "version": "2.0",
  "port": 8000,
  "host": "0.0.0.0",
  "authority_level": 10.0,
  "features": {
    "voice_announcements": true,
    "circuit_breaker": true,
    "caching": true,
    "rate_limiting": true,
    "authentication": true
  },
  "dependencies": {
    "crystal_memory": {
      "host": "localhost",
      "port": 8002,
      "required": true
    }
  },
  "voice": {
    "primary_character": "Echo",
    "config_file": "E:\\ECHO_XV4\\CONFIG\\voices\\[server_name]_voice_config.json"
  },
  "logging": {
    "file": "E:\\ECHO_XV4\\LOGS\\[server_name].log",
    "level": "INFO",
    "rotation": "1 day",
    "retention": "30 days"
  },
  "database": {
    "path": "E:\\ECHO_XV4\\DATA\\[server_name].db",
    "backup_enabled": true,
    "backup_interval": "6 hours"
  }
}
```

**4. Environment Variables File:**
`E:\ECHO_XV4\CONFIG\.env.[SERVER_NAME]`

```ini
# Server Configuration
SERVER_NAME=[Server Name]
SERVER_PORT=8000
SERVER_HOST=0.0.0.0
AUTHORITY_LEVEL=10.0

# Voice Configuration
VOICE_ANNOUNCEMENTS_ENABLED=true
VOICE_CHARACTER_PRIMARY=Echo
ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}

# Database
DATABASE_PATH=E:\ECHO_XV4\DATA\[server_name].db

# Logging
LOG_LEVEL=INFO
LOG_FILE=E:\ECHO_XV4\LOGS\[server_name].log

# Features
CIRCUIT_BREAKER_ENABLED=true
CACHING_ENABLED=true
RATE_LIMITING_ENABLED=true
AUTHENTICATION_REQUIRED=true

# API Keys
API_KEY=${ECHO_MASTER_API_KEY}
CRYSTAL_MEMORY_API_KEY=${CRYSTAL_MEMORY_MASTER_KEY}
```

#### B. Configuration Update Checklist

For each server audited, verify and update:

**Claude Desktop Config:**

- [ ] Server entry exists in `claude_desktop_config.json`?
- [ ] Command path correct (absolute path to Python)?
- [ ] Args array includes correct server file path?
- [ ] All required environment variables present?
- [ ] VOICE_ANNOUNCEMENTS_ENABLED set?
- [ ] API keys referenced from keychain?
- [ ] PYTHONPATH includes E:\ECHO_XV4?

**VS Code Copilot Config:**

- [ ] Server entry exists in `.vscode/settings.json`?
- [ ] MCP server command correct?
- [ ] Environment variables configured?
- [ ] Copilot instructions file referenced?
- [ ] Voice settings enabled?

**Server-Specific Config:**

- [ ] `[SERVER_NAME]_config.json` exists?
- [ ] Port assignment correct (no conflicts)?
- [ ] Authority level set appropriately?
- [ ] All features enabled/disabled correctly?
- [ ] Dependencies listed accurately?
- [ ] Voice configuration referenced?
- [ ] Logging paths correct?
- [ ] Database paths correct?

**Voice Config:**

- [ ] `[SERVER_NAME]_voice_config.json` exists?
- [ ] Primary character assigned?
- [ ] Fallback character assigned?
- [ ] Announcement triggers configured?
- [ ] ElevenLabs settings present?
- [ ] Message templates customized?

**Environment File:**

- [ ] `.env.[SERVER_NAME]` exists?
- [ ] All variables defined?
- [ ] API keys referenced correctly?
- [ ] Paths are absolute and correct?
- [ ] Feature flags set appropriately?

#### C. Configuration Generation Task

If configurations are missing or incomplete, ADD TO DELIVERABLES:

**File:** `[SERVER_NAME]_CONFIGURATIONS_PACKAGE.zip`

Must contain:

1. `claude_desktop_config_entry.json` - Entry to add to Claude config
2. `vscode_settings_entry.json` - Entry to add to VS Code settings
3. `[SERVER_NAME]_config.json` - Server-specific configuration
4. `[SERVER_NAME]_voice_config.json` - Voice configuration
5. `.env.[SERVER_NAME]` - Environment variables
6. `INSTALLATION_INSTRUCTIONS.md` - Step-by-step setup guide

**Installation Instructions Template:**

````markdown
# [Server Name] Configuration Installation

## Prerequisites

- Python 3.12+
- ElevenLabs API Key
- ECHO Master API Key

## Installation Steps

### 1. Update Claude Desktop Config

Location: `C:\Users\[USERNAME]\AppData\Roaming\Claude\claude_desktop_config.json`

Add this entry to the "mcpServers" object:
[copy from claude_desktop_config_entry.json]

### 2. Update VS Code Settings

Location: `.vscode/settings.json` in workspace root

Add this entry to the "mcp.servers" object:
[copy from vscode_settings_entry.json]

### 3. Copy Server Configuration

Copy `[SERVER_NAME]_config.json` to:
`E:\ECHO_XV4\CONFIG\servers\[SERVER_NAME]_config.json`

### 4. Copy Voice Configuration

Copy `[SERVER_NAME]_voice_config.json` to:
`E:\ECHO_XV4\CONFIG\voices\[SERVER_NAME]_voice_config.json`

### 5. Copy Environment File

Copy `.env.[SERVER_NAME]` to:
`E:\ECHO_XV4\CONFIG\.env.[SERVER_NAME]`

### 6. Update Master Voice Registry

Edit `E:\ECHO_XV4\CONFIG\voices\ECHO_VOICE_CHARACTER_REGISTRY.json`
Ensure the character assigned to this server is defined.

### 7. Restart Services

```powershell
# Restart Claude Desktop (close and reopen)
# Restart VS Code
# Start the server
python E:\ECHO_XV4\MLS\servers\ACTIVE_SERVERS\[server_file].py
```
````

### 8. Verify Configuration

```powershell
# Test server health
Invoke-RestMethod -Uri "http://localhost:[port]/health"

# Test voice announcement (if applicable)
Invoke-RestMethod -Uri "http://localhost:[port]/test-voice" -Method POST
```

````

#### D. Configuration Validation Script

Include in each server report whether this validation passes:

```powershell
# Configuration Validation Script
function Test-ServerConfiguration {
    param(
        [string]$ServerName,
        [int]$Port
    )

    $results = @{
        ClaudeConfig = $false
        VSCodeConfig = $false
        ServerConfig = $false
        VoiceConfig = $false
        EnvFile = $false
        VoiceRegistry = $false
    }

    # Check Claude config
    $claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
    if (Test-Path $claudeConfigPath) {
        $config = Get-Content $claudeConfigPath | ConvertFrom-Json
        if ($config.mcpServers.$ServerName) {
            $results.ClaudeConfig = $true
        }
    }

    # Check VS Code config
    $vscodeConfigPath = ".vscode\settings.json"
    if (Test-Path $vscodeConfigPath) {
        $config = Get-Content $vscodeConfigPath | ConvertFrom-Json
        if ($config.'mcp.servers'.$ServerName) {
            $results.VSCodeConfig = $true
        }
    }

    # Check server config
    $serverConfigPath = "E:\ECHO_XV4\CONFIG\servers\${ServerName}_config.json"
    if (Test-Path $serverConfigPath) {
        $results.ServerConfig = $true
    }

    # Check voice config
    $voiceConfigPath = "E:\ECHO_XV4\CONFIG\voices\${ServerName}_voice_config.json"
    if (Test-Path $voiceConfigPath) {
        $results.VoiceConfig = $true
    }

    # Check env file
    $envPath = "E:\ECHO_XV4\CONFIG\.env.$ServerName"
    if (Test-Path $envPath) {
        $results.EnvFile = $true
    }

    # Check voice registry
    $registryPath = "E:\ECHO_XV4\CONFIG\voices\ECHO_VOICE_CHARACTER_REGISTRY.json"
    if (Test-Path $registryPath) {
        $results.VoiceRegistry = $true
    }

    return $results
}
````

---

## 🤖 AGENT INSTRUCTIONS

### Execution Strategy:

1. **Start Broad:** Run port scan, file discovery first
2. **Prioritize:** Audit CRITICAL servers first
3. **Go Deep:** Read entire files, understand architecture
4. **Be Thorough:** Check every endpoint, tool, function
5. **Think Integration:** How servers work together
6. **Propose Solutions:** Not just problems, but fixes
7. **Document Everything:** Clear, comprehensive reports

### Research Tools Available:

- `read_file` - Read server source code
- `grep_search` - Search for patterns (stubs, TODOs)
- `file_search` - Find server files
- `semantic_search` - Understand code semantics
- `run_in_terminal` - Check ports, run health checks
- `list_dir` - Explore directory structures

### Expected Timeline:

- **Phase 1 (Discovery):** 2-4 hours
- **Phase 2 (Audit):** 8-12 hours (1-2 hours per server)
- **Phase 3 (Analysis):** 2-4 hours
- **Total:** 12-20 hours of agent work

### Quality Standards:

- Every claim backed by evidence (code, line numbers)
- Specific, actionable recommendations
- Clear priority levels
- Implementation effort estimates
- Success metrics defined

---

## 📞 REPORTING PROTOCOL

### Interim Reports:

After completing each server audit, provide brief status:

- Server name
- Status (Complete/In Progress/Blocked)
- Critical findings
- Blocker issues if any

### Final Report:

Comprehensive summary with:

- Executive summary (1 page)
- Server constellation map
- Critical issues requiring immediate attention
- Top 10 enhancement priorities
- Estimated effort for roadmap
- Recommended next steps

---

## 🎖️ AUTHORITY & RESOURCES

**Your Authority Level:** 9.0 (Full read access, analysis permissions)

**Resources Available:**

- Full ECHO_XV4 workspace access
- All configuration files
- API keychains
- Server logs
- Documentation archives

**Escalation Path:**

- **Level 10.0:** Complex decisions requiring approval
- **Level 11.0 (Commander):** Critical system changes

**Voice Capability:**
Use voice system to announce major milestones:

- "Server audit phase 1 complete - [X] servers discovered"
- "Critical issue found in [Server Name] - immediate attention required"
- "Audit complete - [X] servers documented, [Y] issues found"

---

## 🚀 BEGIN MISSION

**Start Command:**

```
Acknowledged. Beginning ECHO Prime Server Constellation Audit.
Phase 1: Discovery initiated.
Scanning E:\ECHO_XV4\MLS\servers\ for all server files...
```

**Expected First Output:**

```
📊 DISCOVERY PHASE REPORT
=========================
Servers Found: [X]
Directories Scanned: [Y]
Total Lines of Code: [Z]

Server List:
1. [Server Name] - [Port] - [Status]
2. [Server Name] - [Port] - [Status]
...

Next: Beginning detailed audit of CRITICAL priority servers...
```

---

**🎯 MISSION: COMPREHENSIVE SERVER AUDIT**  
**🤖 AGENT: Copilot/Claude**  
**📅 START DATE: October 12, 2025**  
**⏰ DEADLINE: 48 hours**  
**🎖️ AUTHORITY: Level 9.0**

**GO! GO! GO!** 🚀🚀🚀
