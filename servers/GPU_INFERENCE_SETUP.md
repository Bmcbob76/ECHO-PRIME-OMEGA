# 🎖️ GPU INFERENCE NETWORK SETUP
**Commander: Bobby Don McWilliams II**  
**Authority Level: 11.0**  
**System: ECHO_XV4**

Complete setup guide for distributed AI inference using RTX 4070 16GB GPU server.

---

## 📋 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────┐
│  MAIN COMPUTER (ECHO_XV4)              │
│  • Python Client (gpu_inference_client) │
│  • Flask API Server (Port 8070)         │
│  • Desktop Commander / MLS              │
│  • GS343 Foundation + Phoenix           │
└─────────────┬───────────────────────────┘
              │
              │ Local Network (LAN)
              │ IP: 192.168.1.x
              │
┌─────────────▼───────────────────────────┐
│  GPU COMPUTER (RTX 4070 16GB)          │
│  • Ollama Server (Port 11434)           │
│  • Mixtral 8x7B / Qwen 14B / etc.       │
│  • CUDA Support                         │
│  • Automatic Model Management           │
└─────────────────────────────────────────┘
```

---

## 🚀 QUICK START CHECKLIST

### ✅ GPU Machine (RTX 4070)
- [ ] Install Ollama
- [ ] Configure network access
- [ ] Open firewall port 11434
- [ ] Pull AI model (Mixtral/Qwen)
- [ ] Test local connection

### ✅ Main Computer (ECHO_XV4)
- [ ] Update GPU server IP in config
- [ ] Install Python requirements
- [ ] Run connectivity test
- [ ] Start API server (optional)
- [ ] Run full test suite

---

## 🔧 PART 1: GPU MACHINE SETUP (RTX 4070)

### Step 1.1: Install Ollama

**Option A: Download Installer**
1. Download: https://ollama.ai/download
2. Run OllamaSetup.exe
3. Install to default location

**Option B: Direct Link**
```powershell
# Download and run
Invoke-WebRequest -Uri "https://ollama.ai/download/OllamaSetup.exe" -OutFile "$env:TEMP\OllamaSetup.exe"
Start-Process "$env:TEMP\OllamaSetup.exe"
```

### Step 1.2: Configure Network Access

**CRITICAL: Allow external connections**

```powershell
# Open PowerShell as Administrator

# Set environment variable to allow network access
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'Machine')

# Restart Ollama service
Restart-Service Ollama

# Verify service is running
Get-Service Ollama
```

### Step 1.3: Configure Windows Firewall

```powershell
# Open PowerShell as Administrator

# Create firewall rule for Ollama
New-NetFirewallRule `
    -DisplayName "Ollama AI Server" `
    -Direction Inbound `
    -LocalPort 11434 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any

# Verify rule was created
Get-NetFirewallRule -DisplayName "Ollama AI Server"
```

### Step 1.4: Get GPU Machine IP Address

```powershell
# Get IP address
ipconfig

# Look for IPv4 Address under your network adapter
# Example output:
#   IPv4 Address. . . . . . . . . . . : 192.168.1.100
```

**📝 Write down this IP address - you'll need it!**

### Step 1.5: Pull AI Model

**Recommended Models for 16GB VRAM:**

```powershell
# Option 1: Mixtral 8x7B (RECOMMENDED - Best general purpose)
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M

# Option 2: Qwen 2.5 14B (Excellent coding & reasoning)
ollama pull qwen2.5:14b-instruct-q5_K_M

# Option 3: DeepSeek Coder 33B (Code generation specialist)
ollama pull deepseek-coder:33b-instruct-q4_K_M

# Option 4: CodeLlama 34B (Code tasks)
ollama pull codellama:34b-instruct-q4_K_M

# Option 5: Llama 3.2 11B (Fast inference)
ollama pull llama3.2:11b-instruct-q5_K_M
```

**Model Size Guide:**
- **q4_K_M**: 4-bit quantization (smaller, faster, slightly less accurate)
- **q5_K_M**: 5-bit quantization (larger, slower, more accurate)

### Step 1.6: Test Local Connection

```powershell
# Test Ollama is running
ollama list

# Test generation
ollama run mixtral:8x7b-instruct-v0.1-q4_K_M "Say hello"

# Test API endpoint
curl http://localhost:11434/api/tags
```

---

## 💻 PART 2: MAIN COMPUTER SETUP (ECHO_XV4)

### Step 2.1: Update Configuration File

**Edit:** `E:\ECHO_XV4\MLS\servers\gpu_config.env`

```bash
# UPDATE THIS LINE with your GPU machine's IP address!
GPU_SERVER_HOST=192.168.1.100  # ← CHANGE THIS!

# Update model if you pulled a different one
GPU_MODEL=mixtral:8x7b-instruct-v0.1-q4_K_M
```

### Step 2.2: Install Python Requirements

```powershell
# Install Flask and dependencies
H:\Tools\python.exe -m pip install flask flask-cors requests --break-system-packages

# Verify installation
H:\Tools\python.exe -m pip list | findstr flask
```

### Step 2.3: Test Network Connectivity

```powershell
# Test connection to GPU server (use your GPU machine's IP)
curl http://192.168.1.100:11434/api/tags

# Should return JSON with model list
```

**If this fails:**
1. Verify GPU machine is on
2. Check firewall on GPU machine
3. Verify IP address is correct
4. Test ping: `ping 192.168.1.100`

### Step 2.4: Run Test Suite

```powershell
# Load environment and run tests
cd E:\ECHO_XV4\MLS\servers
H:\Tools\python.exe test_gpu_inference.py
```

**Expected Output:**
```
🎖️ GPU INFERENCE SYSTEM - COMPLETE TEST SUITE
=================================================================
🎯 TEST 1: Direct Ollama Connection
✅ SUCCESS - Connected to Ollama server
   Models available: 1
   • mixtral:8x7b-instruct-v0.1-q4_K_M (5.2GB)

🎯 TEST 2: GPU Client Initialization
✅ SUCCESS - GPU client initialized

🎯 TEST 3: Health Check
✅ SUCCESS - Server is healthy

[... more tests ...]

TOTAL: 6/6 tests passed (100%)
🎖️ ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT!
```

---

## 🎯 PART 3: USING THE SYSTEM

### Method 1: Direct Python Client

```python
from gpu_inference_client import GPUInferenceClient, GPUServerConfig

# Initialize client
config = GPUServerConfig(
    host="192.168.1.100",  # Your GPU machine IP
    model="mixtral:8x7b-instruct-v0.1-q4_K_M"
)
client = GPUInferenceClient(config)

# Simple generation
result = client.generate(
    prompt="Explain quantum computing in one sentence.",
    temperature=0.7
)
print(result['response'])

# Chat conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a Python function to sort a list."}
]
result = client.chat(messages)
print(result['message']['content'])

# Cleanup
client.shutdown()
```

### Method 2: Flask API Server

**Start the API server:**
```powershell
cd E:\ECHO_XV4\MLS\servers
H:\Tools\python.exe gpu_inference_server.py
```

**Use the API:**
```powershell
# Generate text
curl -X POST http://localhost:8070/api/generate `
  -H "Content-Type: application/json" `
  -d '{"prompt": "Hello, world!", "max_tokens": 50}'

# Chat
curl -X POST http://localhost:8070/api/chat `
  -H "Content-Type: application/json" `
  -d '{"messages": [{"role": "user", "content": "Hi!"}]}'

# Health check
curl http://localhost:8070/health

# List models
curl http://localhost:8070/api/models
```

### Method 3: From Other ECHO_XV4 Services

```python
import requests

# From any ECHO_XV4 server/script
response = requests.post(
    "http://localhost:8070/api/generate",
    json={
        "prompt": "Your prompt here",
        "temperature": 0.7,
        "max_tokens": 1000
    }
)

result = response.json()
print(result['response'])
```

---

## 📁 FILES CREATED

```
E:\ECHO_XV4\MLS\servers\
├── gpu_inference_client.py      # Python client library
├── gpu_inference_server.py      # Flask API server (Port 8070)
├── gpu_config.env               # Configuration file
├── test_gpu_inference.py        # Complete test suite
└── GPU_INFERENCE_SETUP.md       # This README
```

---

## 🔍 TROUBLESHOOTING

### Problem: Cannot connect to GPU server

**Symptoms:**
```
❌ Cannot connect to GPU server at http://192.168.1.100:11434
   Error: [WinError 10061] No connection could be made
```

**Solutions:**

1. **Verify GPU machine is on**
   ```powershell
   ping 192.168.1.100
   ```

2. **Check Ollama service**
   ```powershell
   # On GPU machine:
   Get-Service Ollama
   # Should show "Running"
   ```

3. **Verify firewall rule**
   ```powershell
   # On GPU machine:
   Get-NetFirewallRule -DisplayName "Ollama AI Server"
   Test-NetConnection -ComputerName 192.168.1.100 -Port 11434
   ```

4. **Check OLLAMA_HOST environment variable**
   ```powershell
   # On GPU machine:
   [Environment]::GetEnvironmentVariable("OLLAMA_HOST", "Machine")
   # Should show: 0.0.0.0:11434
   ```

5. **Verify Ollama is listening**
   ```powershell
   # On GPU machine:
   Get-NetTCPConnection -LocalPort 11434
   # Should show LISTENING state
   ```

### Problem: Model generation is slow

**Causes & Solutions:**

1. **First generation is always slow** (model loading)
   - Solution: Run a warmup query first

2. **Model too large for VRAM**
   - Check: `ollama ps` on GPU machine
   - Solution: Use smaller quantization (q4 instead of q5)

3. **Other GPU processes**
   - Check: Task Manager → GPU usage
   - Solution: Close other GPU-intensive apps

### Problem: "Model not found" error

**Solution:**
```powershell
# On GPU machine, list available models
ollama list

# Pull the model if missing
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M

# Update config file to match available model
```

### Problem: API server won't start

**Check:**
1. Port 8070 is available: `netstat -an | findstr 8070`
2. Python can be found: `H:\Tools\python.exe --version`
3. Flask is installed: `H:\Tools\python.exe -m pip list | findstr flask`
4. GS343 Foundation is accessible: `dir E:\GS343\FOUNDATION`

---

## ⚡ PERFORMANCE OPTIMIZATION

### GPU Machine Optimization

1. **Disable Windows features you don't need**
   - Windows Defender (if safe)
   - Background apps
   - Windows Update (temporarily)

2. **Set GPU for performance**
   - NVIDIA Control Panel → Manage 3D Settings
   - Power Management Mode → Prefer Maximum Performance

3. **Use faster quantization**
   - q4_K_M for speed
   - q5_K_M for accuracy

### Network Optimization

1. **Use wired connection** (not WiFi)
2. **Gigabit ethernet** if available
3. **Minimize network hops** (direct connection best)

### Client Optimization

1. **Batch requests** when possible
2. **Reuse client connection** (don't recreate)
3. **Use appropriate timeouts** (longer for large generations)

---

## 📊 EXPECTED PERFORMANCE

**RTX 4070 16GB with Mixtral 8x7B Q4:**

| Task | Speed | Notes |
|------|-------|-------|
| Model Loading | 5-10s | First request only |
| Short Generation (50 tokens) | 2-3s | ~20 tokens/sec |
| Medium Generation (500 tokens) | 15-20s | ~25 tokens/sec |
| Long Generation (2000 tokens) | 60-80s | ~25 tokens/sec |
| Network Latency | <10ms | On same LAN |

**Factors Affecting Speed:**
- Model size (larger = slower)
- Quantization level (q4 faster than q5)
- Prompt length (longer = slower start)
- Network speed (LAN vs WiFi)
- Other GPU processes

---

## 🎯 INTEGRATION WITH ECHO_XV4

### Add to MLS (Master Launcher System)

**Create MLS server config:**

`E:\ECHO_XV4\MLS\servers\gpu_inference.json`
```json
{
    "name": "GPU Inference API",
    "port": 8070,
    "path": "E:\\ECHO_XV4\\MLS\\servers\\gpu_inference_server.py",
    "python": "H:\\Tools\\python.exe",
    "auto_start": true,
    "health_endpoint": "/health",
    "restart_on_failure": true,
    "gs343_enabled": true,
    "phoenix_enabled": true,
    "description": "Distributed GPU inference API for RTX 4070"
}
```

### Use from Other Servers

```python
# From any ECHO_XV4 server
import requests

def query_gpu(prompt: str, max_tokens: int = 1000) -> str:
    """Query GPU inference server"""
    try:
        response = requests.post(
            "http://localhost:8070/api/generate",
            json={
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": 0.7
            },
            timeout=120
        )
        return response.json()['response']
    except Exception as e:
        print(f"GPU query failed: {e}")
        return None
```

---

## 🔐 SECURITY CONSIDERATIONS

### Current Setup (Development)
- ✅ LAN only (not exposed to internet)
- ✅ No authentication required
- ✅ Firewall configured for specific port

### For Production Use
- ⚠️ Add API authentication
- ⚠️ Use HTTPS/TLS
- ⚠️ Implement rate limiting
- ⚠️ Add request logging
- ⚠️ Monitor for abuse

**DO NOT expose port 11434 to the internet without security!**

---

## 📚 API REFERENCE

### Client API (gpu_inference_client.py)

#### `GPUInferenceClient(config: GPUServerConfig)`

**Methods:**
- `generate(prompt, model, system, temperature, max_tokens, stream)` - Generate text
- `chat(messages, model, temperature, stream)` - Multi-turn chat
- `list_models()` - List available models
- `health_check()` - Check server health
- `shutdown()` - Graceful cleanup

### REST API (gpu_inference_server.py)

**Port:** 8070

**Endpoints:**

#### `GET /health`
Health check
```json
Response: {
  "status": "healthy",
  "service": "GPU Inference API Server",
  "gpu_server": {...},
  "timestamp": 1234567890
}
```

#### `POST /api/generate`
Generate text from prompt
```json
Request: {
  "prompt": "Your prompt",
  "model": "mixtral:8x7b-instruct-v0.1-q4_K_M",
  "system": "System prompt (optional)",
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": false
}

Response: {
  "response": "Generated text...",
  "model": "mixtral:8x7b-instruct-v0.1-q4_K_M",
  "created_at": "2025-10-09T...",
  "done": true
}
```

#### `POST /api/chat`
Multi-turn chat
```json
Request: {
  "messages": [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello!"}
  ],
  "model": "mixtral:8x7b-instruct-v0.1-q4_K_M",
  "temperature": 0.7,
  "stream": false
}

Response: {
  "message": {
    "role": "assistant",
    "content": "Hello! How can I help?"
  },
  "model": "...",
  "created_at": "...",
  "done": true
}
```

#### `GET /api/models`
List available models
```json
Response: {
  "models": [...],
  "count": 1
}
```

#### `GET /api/config`
Get server configuration
```json
Response: {
  "host": "192.168.1.100",
  "port": 11434,
  "model": "mixtral:8x7b-instruct-v0.1-q4_K_M",
  "timeout": 120,
  "base_url": "http://192.168.1.100:11434"
}
```

---

## 🎓 USAGE EXAMPLES

### Example 1: Code Generation

```python
from gpu_inference_client import GPUInferenceClient, GPUServerConfig

config = GPUServerConfig(host="192.168.1.100")
client = GPUInferenceClient(config)

prompt = """
Write a Python function that:
1. Takes a list of numbers
2. Returns the average
3. Includes error handling
"""

result = client.generate(prompt, max_tokens=500, temperature=0.3)
print(result['response'])

client.shutdown()
```

### Example 2: Interactive Chat

```python
from gpu_inference_client import GPUInferenceClient, GPUServerConfig

config = GPUServerConfig(host="192.168.1.100")
client = GPUInferenceClient(config)

# Build conversation
messages = []

# System prompt
messages.append({
    "role": "system",
    "content": "You are a helpful coding assistant."
})

# User asks question
messages.append({
    "role": "user",
    "content": "How do I read a CSV file in Python?"
})

# Get response
result = client.chat(messages)
assistant_msg = result['message']['content']
print(f"Assistant: {assistant_msg}")

# Continue conversation
messages.append({
    "role": "assistant",
    "content": assistant_msg
})

messages.append({
    "role": "user",
    "content": "Show me an example with pandas."
})

result = client.chat(messages)
print(f"Assistant: {result['message']['content']}")

client.shutdown()
```

### Example 3: Streaming Response

```python
from gpu_inference_client import GPUInferenceClient, GPUServerConfig

config = GPUServerConfig(host="192.168.1.100")
client = GPUInferenceClient(config)

print("Generating story (streaming)...")

result = client.generate(
    prompt="Write a short sci-fi story about AI.",
    temperature=0.9,
    stream=True  # Enable streaming
)

# Text will print as it generates
# result will contain full response when done

client.shutdown()
```

---

## 🎖️ SYSTEM STATUS

**✅ Files Created:**
- gpu_inference_client.py (376 lines)
- gpu_inference_server.py (232 lines)
- gpu_config.env (58 lines)
- test_gpu_inference.py (297 lines)
- GPU_INFERENCE_SETUP.md (this file)

**✅ Features:**
- Direct GPU client library
- REST API server wrapper
- Complete test suite
- GS343 Foundation integration
- Phoenix Auto-Heal recovery
- Health monitoring
- Model management
- Configuration system

**✅ Integration:**
- ECHO_XV4 ecosystem
- MLS compatible
- Desktop Commander ready
- Authority Level 11.0

---

## 📞 SUPPORT & TROUBLESHOOTING

**Common Issues:**
1. Connection failures → Check firewall & IP
2. Model errors → Verify model is pulled
3. Slow performance → Check VRAM usage
4. API errors → Check Flask installation

**Logs:**
- GS343: `E:\ECHO_XV4\LOGS\`
- Ollama: `%USERPROFILE%\.ollama\logs\`

**Testing:**
```powershell
# Quick connectivity test
curl http://192.168.1.100:11434/api/tags

# Full test suite
H:\Tools\python.exe E:\ECHO_XV4\MLS\servers\test_gpu_inference.py
```

---

**🎖️ END OF SETUP GUIDE**

**Commander: Bobby Don McWilliams II**  
**Authority Level: 11.0**  
**Status: ✅ DEPLOYMENT READY**

*"Execute with precision. Build with excellence."*
