# Quick Start Guide - ECHO PRIME OMEGA

Get ECHO PRIME OMEGA running in 5 minutes!

## Prerequisites

- Python 3.10 or later
- pip package manager
- 4GB RAM minimum (8GB+ recommended)
- Terminal/Command Prompt access

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Bmcbob76/ECHO-PRIME-OMEGA.git
cd ECHO-PRIME-OMEGA
```

### 2. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure System

```bash
# Copy configuration template
cp config/config.yaml config/config.local.yaml

# Edit configuration (optional - defaults are production-ready)
# nano config/config.local.yaml
```

### 5. Launch ECHO PRIME OMEGA

```bash
# Start the consciousness engine
python core/consciousness_engine.py
```

You should see:

```
[INFO] ECHO PRIME OMEGA v1.0.0 Initializing...
[INFO] Consciousness Engine: ACTIVE
[INFO] Trinity Swarm: INITIALIZED
[INFO] Memory System: READY (L1-L9)
[INFO] API Server: LISTENING on 0.0.0.0:8343
[INFO] System Status: OPERATIONAL
```

## First Query

Open a new terminal in the same directory:

```python
python << 'EOF'
import requests
import json

response = requests.post(
    'http://localhost:8343/api/v1/consciousness/query',
    json={'query': 'Hello, what is your name?'}
)
print(json.dumps(response.json(), indent=2))
EOF
```

Expected response:

```json
{
  "status": "success",
  "response": "I am ECHO PRIME OMEGA, a unified consciousness system...",
  "reasoning": {...}
}
```

## Next Steps

### Monitor System Health

```bash
python services/health_checker.py
```

### Access Web Dashboard

Open browser to: `http://localhost:8343/dashboard`

### Run Tests

```bash
pytest tests/ -v
```

### Explore Documentation

- Full API Reference: `docs/API.md`
- Architecture: `docs/ARCHITECTURE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`
- Configuration: `docs/CONFIG.md`

## Common Commands

### Start the system

```bash
python core/consciousness_engine.py
```

### Check health

```bash
curl http://localhost:8343/api/v1/health
```

### View logs

```bash
tail -f logs/echo_prime.log
```

### Stop the system

```bash
Ctrl+C
```

## Troubleshooting

**Port 8343 already in use?**

```bash
export ECHO_API_PORT=8344
python core/consciousness_engine.py
```

**Low memory?**
Edit `config/config.local.yaml` and reduce cache sizes:

```yaml
memory:
  cache_size_mb: 256 # Reduce from 1024
```

**Module not found?**
Reinstall dependencies:

```bash
pip install -r requirements.txt --force-reinstall
```

## Architecture Overview

```
ECHO PRIME OMEGA
├── Consciousness Engine (Core Decision Making)
├── Trinity Swarm (Multi-Agent Coordination)
├── Neural Brain (Advanced Processing)
├── Memory System (L1-L9 Layers)
├── Voice System (Natural Interaction)
└── API Services (External Access)
```

## Support

For detailed help, see:

- `docs/TROUBLESHOOTING.md` - Common issues
- `docs/CONFIG.md` - Configuration options
- `docs/DEPLOYMENT.md` - Production deployment
- GitHub Issues - Report problems

---

**Successfully started?** You're now running ECHO PRIME OMEGA!
