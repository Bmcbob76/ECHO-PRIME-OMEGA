# EPCP3-0 Backend Server

**Location:** `E:\ECHO_XV4\MLS\servers\epcp3_backend.py`
**Auto-Launch:** Managed by MLS launcher system
**Port:** 7331
**Status:** Production Ready

---

## 🎯 Server Details

**Server Type:** FastAPI + WebSocket
**Purpose:** EPCP3-0 IDE Backend with AI Integration
**Authority Level:** 11.0
**Commander:** Bobby Don McWilliams II

---

## 🌐 Endpoints

### Main IDE

```
http://localhost:7331/epcp-code
```

Full VS Code-like IDE with:

- Monaco Editor
- File explorer with folder opening
- AI chat with 9 models
- Extensions with enable/disable
- Integrated terminal

### API Documentation

```
http://localhost:7331/docs
```

Interactive Swagger UI for testing all endpoints

### WebSocket

```
ws://localhost:7331/ws/ai-chat
```

Real-time AI chat communication

### Health Check

```
http://localhost:7331/health
```

Returns server status and configuration

---

## 🤖 AI Models Supported

1. **Claude 4.5 Sonnet** ⚡ (NEWEST)
2. **Claude 4.1 Opus** (Most Intelligent)
3. **Claude 3.5 Sonnet** (Fast & Smart)
4. **GPT-4 Turbo** (OpenAI)
5. **Gemini 1.5 Pro** (Google)
6. **DeepSeek Chat**
7. **Grok Beta** (X.AI)
8. **Ollama Mistral** (FREE - Local)
9. **Ollama Code Llama** (FREE - Local)

---

## 🔑 API Keys

**Location:** `E:\ECHO_XV4\EPCP3-0\CONFIGS\api_keys.json`

**Loaded Providers:**

- Anthropic (Claude models)
- OpenAI (GPT models)
- Google (Gemini)
- DeepSeek
- Grok
- ElevenLabs (Voice)
- And 8 more...

---

## 📋 Features

### ✅ Core Features

- Real AI responses (not placeholders)
- WebSocket communication
- File system operations
- Extension management
- Voice integration (ElevenLabs)
- 6 personality voices

### ✅ Advanced Features

- GS343 Swarm integration ready
- Phoenix Auto-Heal system
- Memory management
- Code analysis
- Multi-model support

---

## 🚀 Auto-Launch

This server is automatically managed by the MLS launcher system:

- **Auto-starts** on system boot
- **Stays running** in background
- **Auto-restarts** on crash
- **Health monitoring** enabled

**No manual intervention needed!**

---

## 🔧 Manual Operations

### Check if Running

```powershell
netstat -ano | findstr :7331
```

### Manual Start (if needed)

```powershell
python E:\ECHO_XV4\MLS\servers\epcp3_backend.py
```

### View Logs

Server outputs to console with colored status messages:

- ✅ Green: Success
- ⚠️ Yellow: Warning
- ❌ Red: Error

---

## 📊 Three Critical Fixes Applied

### Fix 1: Folder Opening

- File tree now renders properly
- Nested folder structure
- Click to open files
- File type icons

### Fix 2: Real AI Responses

- Backend properly configured
- API keys loaded
- WebSocket active
- All 9 models working

### Fix 3: Extension Enable/Disable

- Two-button system
- Enable/disable toggle
- Uninstall option
- State management

---

## 📁 Related Files

**HTML IDE:**

```
E:\ECHO_XV4\MLS\servers\epcp_code.html
```

**Original Location (backup):**

```
E:\ECHO_XV4\ECHO_PRIME_SYSTEM\ECHO_GUI\electron-app\TABS\EPCP3-0\
```

**Documentation:**

- `FINAL_THREE_FIXES_COMPLETE.md` - Technical fix details
- `QUICK_ACCESS_GUIDE.md` - User guide
- `OPEN_IDE.bat` - Quick launcher
- `OPEN_API_DOCS.bat` - API docs launcher

---

## ⚙️ Configuration

**Server runs in STANDALONE mode:**

- GS343 Foundation: Optional (connects if available)
- Voice Commands: ENABLED
- API Keys: Auto-loaded
- WebSocket: Always active

**Performance:**

- Port: 7331 (configurable)
- Max connections: Unlimited
- Timeout: 60 seconds
- Auto-reconnect: Enabled

---

## 🎯 Integration Status

| Component       | Status       | Notes                    |
| --------------- | ------------ | ------------------------ |
| Backend Server  | ✅ DEPLOYED  | In MLS servers directory |
| WebSocket       | ✅ ACTIVE    | Port 7331                |
| AI Models       | ✅ READY     | 9 models configured      |
| API Keys        | ✅ LOADED    | 14 providers             |
| Voice           | ✅ CONNECTED | ElevenLabs               |
| GS343 Swarm     | ⚠️ OPTIONAL  | Connects if available    |
| File Operations | ✅ WORKING   | Folder opening fixed     |
| Extensions      | ✅ WORKING   | Enable/disable added     |

---

## 🔥 Quick Start

**The MLS launcher automatically manages this server!**

**To use the IDE:**

1. Open browser to `http://localhost:7331/epcp-code`
2. OR double-click `OPEN_IDE.bat`
3. Start coding!

**Server should already be running in background.**

---

**Commander Bobby Don McWilliams II - Authority Level 11.0**
**GS343 Divine Overseer Foundation: ACTIVE**
**October 3, 2025**
