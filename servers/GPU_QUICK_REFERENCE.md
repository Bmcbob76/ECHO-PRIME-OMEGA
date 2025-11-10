# 🎖️ GPU INFERENCE - QUICK REFERENCE CARD

**Commander: Bobby Don McWilliams II** | **Authority Level: 11.0**

---

## ⚡ QUICK SETUP (5 MINUTES)

### GPU Machine (RTX 4070):
```powershell
# 1. Install Ollama
https://ollama.ai/download

# 2. Allow network access
[Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'Machine')
Restart-Service Ollama

# 3. Open firewall
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow

# 4. Pull model
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M

# 5. Get IP address
ipconfig  # Note your IPv4 address
```

### Main Computer (ECHO_XV4):
```powershell
# 1. Run automated setup (UPDATE IP!)
cd E:\ECHO_XV4\MLS\servers
.\setup_gpu_inference.ps1 -GPUServerIP "192.168.1.100"

# 2. Done! ✅
```

---

## 🚀 USAGE EXAMPLES

### Python Client:
```python
from gpu_inference_client import GPUInferenceClient, GPUServerConfig

config = GPUServerConfig(host="192.168.1.100")
client = GPUInferenceClient(config)

# Generate
result = client.generate("Explain quantum computing")
print(result['response'])

# Chat
messages = [{"role": "user", "content": "Hi!"}]
result = client.chat(messages)
print(result['message']['content'])

client.shutdown()
```

### REST API:
```powershell
# Start server
H:\Tools\python.exe E:\ECHO_XV4\MLS\servers\gpu_inference_server.py

# Use API
curl -X POST http://localhost:8070/api/generate `
  -H "Content-Type: application/json" `
  -d '{"prompt": "Hello!", "max_tokens": 50}'
```

### From Other Services:
```python
import requests

response = requests.post(
    "http://localhost:8070/api/generate",
    json={"prompt": "Your prompt", "max_tokens": 1000}
)
print(response.json()['response'])
```

---

## 🧪 TESTING

```powershell
# Quick connectivity test
curl http://192.168.1.100:11434/api/tags

# Full test suite
H:\Tools\python.exe E:\ECHO_XV4\MLS\servers\test_gpu_inference.py
```

---

## 📁 FILES

```
E:\ECHO_XV4\MLS\servers\
├── gpu_inference_client.py       # Python client
├── gpu_inference_server.py       # API server (Port 8070)
├── gpu_config.env                # Config
├── test_gpu_inference.py         # Tests
├── setup_gpu_inference.ps1       # Automated setup
├── GPU_INFERENCE_SETUP.md        # Full documentation
└── GPU_QUICK_REFERENCE.md        # This file
```

---

## 🔧 TROUBLESHOOTING

### Cannot connect:
```powershell
# Check GPU machine
ping 192.168.1.100
Test-NetConnection -ComputerName 192.168.1.100 -Port 11434

# Check Ollama service (on GPU machine)
Get-Service Ollama

# Check firewall (on GPU machine)
Get-NetFirewallRule -DisplayName "Ollama*"
```

### Model errors:
```powershell
# List models (on GPU machine)
ollama list

# Pull model (on GPU machine)
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M
```

---

## 📊 RECOMMENDED MODELS (16GB VRAM)

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| mixtral:8x7b-q4_K_M | 5GB | General purpose | Medium |
| qwen2.5:14b-q5_K_M | 10GB | Code & reasoning | Medium |
| deepseek-coder:33b-q4_K_M | 19GB | Code generation | Slow |
| llama3.2:11b-q5_K_M | 11GB | Fast inference | Fast |

---

## 🎯 API ENDPOINTS

**Base URL:** `http://localhost:8070`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/generate` | POST | Generate text |
| `/api/chat` | POST | Multi-turn chat |
| `/api/models` | GET | List models |
| `/api/config` | GET | Get config |

---

## ⚙️ CONFIGURATION

**Location:** `E:\ECHO_XV4\MLS\servers\gpu_config.env`

```bash
GPU_SERVER_HOST=192.168.1.100    # GPU machine IP
GPU_SERVER_PORT=11434            # Ollama port
GPU_MODEL=mixtral:8x7b-instruct-v0.1-q4_K_M
GPU_TIMEOUT=120                  # Request timeout
```

---

## 📈 PERFORMANCE

**Expected speeds (Mixtral 8x7B Q4 on RTX 4070):**
- Short (50 tokens): 2-3 seconds
- Medium (500 tokens): 15-20 seconds
- Long (2000 tokens): 60-80 seconds
- Tokens/sec: ~20-25

---

## 🔐 SECURITY

**Current:** Development mode (LAN only)

**For Production:**
- Add API authentication
- Use HTTPS/TLS
- Implement rate limiting
- Monitor for abuse

**⚠️ DO NOT expose port 11434 to internet without security!**

---

## 🎖️ INTEGRATION

### Add to MLS:
Create `E:\ECHO_XV4\MLS\servers\gpu_inference.json`:
```json
{
    "name": "GPU Inference API",
    "port": 8070,
    "path": "E:\\ECHO_XV4\\MLS\\servers\\gpu_inference_server.py",
    "python": "H:\\Tools\\python.exe",
    "auto_start": true,
    "health_endpoint": "/health"
}
```

---

## 📞 SUPPORT

**Documentation:** `E:\ECHO_XV4\MLS\servers\GPU_INFERENCE_SETUP.md`  
**Tests:** `test_gpu_inference.py`  
**Logs:** `E:\ECHO_XV4\LOGS\`

---

**🎖️ Authority Level: 11.0**  
**Status: ✅ DEPLOYMENT READY**

*"Execute with precision."*
