# Master Server Launcher (MLS)

A **modular, dynamic, auto-healing server launcher and manager** for Windows, Linux, and macOS. Drop any server script, executable, or container into the `servers/` directory, and MLS will automatically detect, launch, monitor, and heal them, providing a live web dashboard and robust logging.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Supported Server Types](#supported-server-types)
- [Live Dashboard](#live-dashboard)
- [Health Checks & Auto-Heal](#health-checks--auto-heal)
- [Docker Support](#docker-support)
- [Hot Reload & Auto-Detection](#hot-reload--auto-detection)
- [Logging & Debugging](#logging--debugging)
- [Advanced Options](#advanced-options)
- [Extending MLS](#extending-mls)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [License](#license)

---

## Features

- **Plug-and-play modularity:** Drop servers in the `servers/` directory; MLS auto-detects and launches them.
- **Dynamic port assignment:** Each server is assigned a free port at launch.
- **Auto-healing:** If a server crashes or fails its health check, MLS auto-restarts it.
- **Multiple instances:** Easily configure the number of instances per server.
- **Hot reload:** Adding/removing servers or changing configuration is detected live.
- **Docker support:** Launch servers from Docker images or directories containing a `Dockerfile`.
- **Health checks:** Supports HTTP health endpoints or custom script-based checks.
- **Live dashboard:** Monitor server status, ports, restarts, and metrics in real-time via a web dashboard.
- **Comprehensive logging:** File and console logging with selectable verbosity.
- **Resource limits:** (Optional) Limit server memory and CPU usage.
- **Notification hooks:** (Optional) Trigger webhooks on server crash or restart.
- **Cross-platform:** Runs on Windows, Linux, and macOS.

---

## Quick Start

### 1. Prerequisites

- **Python 3.8+** (https://python.org)
- **pip** (Python package manager)
- **(Optional) Docker Desktop** for Docker support

### 2. Installation

```powershell
# Create the MLS directory
mkdir E:\ECHO_XV4\MLS
cd E:\ECHO_XV4\MLS

# Create subdirectories
mkdir servers, logs, static

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure

Edit `config.yaml` to set options such as how many instances per server, logging level, dashboard port, etc.

### 4. Add Servers

- **Python servers:** Place `.py` files in `servers/`.
- **Docker servers:** Place a directory with a `Dockerfile` in `servers/`.
- **Executables:** Place `.exe` or other runnable files in `servers/`.

### 5. Run MLS

```powershell
python master_launcher.py
```

### 6. View Dashboard

Open your browser to [http://localhost:9000/](http://localhost:9000/) (default).

---

## Directory Structure

```
MLS/
├── config.yaml           # Main configuration file
├── requirements.txt      # Python dependencies
├── master_launcher.py    # Main launcher logic
├── plugin.py             # Plugin detection logic
├── server_manager.py     # Server process manager
├── health.py             # Health check utilities
├── dashboard.py          # Flask dashboard server
├── servers/              # Server scripts/executables/Docker directories
│   ├── my_server.py
│   ├── DockerServer/
│   │   ├── Dockerfile
│   │   └── server.py
├── logs/
│   └── master.log        # Log output
├── static/
│   └── dashboard.html    # Dashboard template
```

---

## Configuration

### `config.yaml` Example

```yaml
servers_dir: "./servers"
log_file: "./logs/master.log"
log_level: "INFO"
num_instances_per_server: 2
extra_args: []
dashboard_port: 9000
health_check_interval: 5
docker_support: true
metrics_enabled: true
restart_backoff: 2
resource_limits:
  memory_mb: 256
  cpu_percent: 50
notification_hooks:
  on_restart: ""
  on_crash: ""
```

- **num_instances_per_server:** Number of processes to launch per server.
- **health_check_interval:** Seconds between health checks.
- **docker_support:** Enable/disable Docker container support.
- **restart_backoff:** Seconds to wait before restarting unhealthy servers.
- **resource_limits:** Optional memory/CPU limits for servers.
- **notification_hooks:** URLs to notify on server events.

---

## How It Works

1. **Plugin detection:** Scans `servers/` for `.py` scripts, Docker directories, or executables.
2. **Dynamic launch:** Starts each server in a separate process on a free port.
3. **Health monitoring:** Periodically checks each server’s health endpoint or custom health logic.
4. **Auto-healing:** Restarts any server that crashes or becomes unhealthy.
5. **Hot reload:** Watches for changes in `servers/` or `config.yaml` and adapts automatically.
6. **Dashboard:** Updates live status, metrics, and restarts count.

---

## Supported Server Types

- **Python:** `.py` scripts with a main entry and optional `/health` HTTP endpoint.
- **Docker:** Directories with a `Dockerfile` and main server script.
- **Executables:** `.exe`/`.sh`/runnable binaries.

### Example Python Server

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, threading, time

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health": self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
        else: self.send_response(404); self.end_headers()

def run_health_server(port): HTTPServer(('0.0.0.0', int(port)), HealthHandler).serve_forever()
if __name__ == "__main__":
    port = sys.argv[1]
    threading.Thread(target=run_health_server, args=(port,), daemon=True).start()
    while True: time.sleep(1)
```

### Example Docker Server

`servers/DockerServer/Dockerfile`
```dockerfile
FROM python:3.9-slim
COPY server.py /server.py
CMD ["python", "/server.py", "8080"]
```

---

## Live Dashboard

- Real-time status of all managed servers
- Shows name, port, status (running/dead), restart count
- Accessible by default at [http://localhost:9000/](http://localhost:9000/)

---

## Health Checks & Auto-Heal

- **HTTP health:** Each server should expose `/health` endpoint that returns `200 OK`.
- **Custom health:** For executables, custom checks can be added via `health.py`.
- **Auto-restart:** If a server fails its health check or crashes, MLS restarts it after a configurable backoff.

---

## Docker Support

- If a subdirectory in `servers/` contains a `Dockerfile`, it is built and run as a Docker container.
- Each container is mapped to its assigned dynamic port.

---

## Hot Reload & Auto-Detection

- **File watcher:** Uses `watchdog` to monitor `servers/` for changes.
- **Config reload:** Changing `config.yaml` or adding/removing servers is detected live—no need to restart MLS.

---

## Logging & Debugging

- **File and console logging** with selectable verbosity (`INFO`, `DEBUG`, etc.).
- **master.log** records all events, restarts, errors, and health failures.

---

## Advanced Options

- **Resource limits:** Apply CPU/memory limits to child servers (may require `psutil` and OS support).
- **Notification hooks:** Trigger webhooks when a server crashes or is restarted.
- **Metrics:** Live metrics available in dashboard and via `/status` API.

---

## Extending MLS

- Add new server types by extending `plugin.py` and `server_manager.py`.
- Integrate with monitoring solutions by consuming dashboard API.
- Customize dashboard via `static/dashboard.html`.

---

## Troubleshooting

- **Server not launching:** Check `master.log` for errors.
- **Dashboard not updating:** Verify dashboard is running on correct port.
- **Health checks failing:** Ensure your server exposes a valid `/health` endpoint.
- **Docker errors:** Make sure Docker Desktop is installed and running.

---

## FAQ

**Q: Can I run different numbers of instances for different servers?**  
A: Currently, `num_instances_per_server` is global. For per-server counts, extend config and logic in `server_manager.py`.

**Q: Can I use non-Python servers?**  
A: Yes! Drop any executable in `servers/` with a health check mechanism.

**Q: What happens if a server is removed from the directory?**  
A: MLS will detect the removal and shut down the associated process.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
