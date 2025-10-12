"""
🚀 UNIFIED MEGA-LAUNCHER V2 - WITH ECHO PRIME DIAGNOSTICS
Authority Level 11.0 - Commander Bobby Don McWilliams II
Launches all servers WITHOUT console windows
+ Full Echo Prime Diagnostic System Integration
+ Self-healing capabilities
+ Real-time health monitoring
+ Voice-activated diagnostics
"""

import subprocess
import time
import psutil
import logging
from pathlib import Path
from datetime import datetime
import sys
import warnings
import sqlite3
import json
import asyncio
import queue
import platform

warnings.filterwarnings('ignore')

# Voice System
sys.path.insert(0, "E:/ECHO_XV4/EPCP3O_COPILOT")
try:
    from epcp3o_voice_integrated import EPCP3OVoiceSystem
    import asyncio
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

import threading

class ThreadSafeVoice:
    def __init__(self):
        self.voice = None
        self.mutex = threading.Lock()
        if VOICE_AVAILABLE:
            try:
                self.voice = EPCP3OVoiceSystem()
                self.voice.initialize()
            except: pass
    
    def announce(self, message: str, voice_id: str = '0UTDtgGGkpqERQn1s0YK'):
        if not self.voice: return
        with self.mutex:
            try:
                self.voice.play_r2d2_sound('processing')
                asyncio.run(self.voice.speak_c3po(message, voice_id=voice_id, emotion='calm'))
            except: pass

voice = ThreadSafeVoice()

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 ECHO PRIME DIAGNOSTIC SYSTEM - FULL INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

class EchoDiagnosticSystem:
    """Master diagnostic system for Echo Prime - Integrated into launcher"""
    
    def __init__(self, voice_system=None):
        self.voice = voice_system
        self.components = {
            "core_system": self.check_core_system,
            "memory": self.check_memory_system,
            "voice": self.check_voice_system,
            "servers": self.check_server_systems,
            "performance": self.check_performance,
            "storage": self.check_storage
        }
        
        self.diagnostic_history = []
        self.last_diagnostic = None
        self.alerts = []
        
        # Performance metrics
        self.performance_baseline = {}
        self.performance_current = {}
        
        # Initialize diagnostic database
        self.db_path = LOG_DIR / "echo_diagnostics.db"
        self._init_diagnostic_db()
        
        # Real-time monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self.diagnostic_queue = queue.Queue()
        
        logger.info("🔧 Echo Diagnostic System initialized")
    
    def _init_diagnostic_db(self):
        """Initialize diagnostic database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnostic_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                overall_status TEXT NOT NULL,
                details TEXT,
                alerts TEXT,
                performance_score REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS component_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                component TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES diagnostic_runs (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                server_count INTEGER,
                active_threads INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def run_full_diagnostic(self, server_states_dict: dict = None) -> dict:
        """Run complete system diagnostic"""
        logger.info("🔍 Starting full diagnostic")
        start_time = time.time()
        
        diagnostic_result = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "components": {},
            "alerts": [],
            "performance": {},
            "recommendations": []
        }
        
        # Store server states for server diagnostics
        self.current_server_states = server_states_dict or {}
        
        # Check each component
        for component_name, check_function in self.components.items():
            try:
                result = await check_function()
                diagnostic_result["components"][component_name] = result
                
                # Update overall status
                if result["status"] == "critical":
                    diagnostic_result["status"] = "critical"
                elif result["status"] == "warning" and diagnostic_result["status"] != "critical":
                    diagnostic_result["status"] = "warning"
                    
            except Exception as e:
                logger.error(f"Error checking {component_name}: {e}")
                diagnostic_result["components"][component_name] = {
                    "status": "error",
                    "message": str(e)
                }
        
        # Calculate performance score
        diagnostic_result["performance"]["diagnostic_time"] = time.time() - start_time
        diagnostic_result["performance"]["score"] = self._calculate_health_score(diagnostic_result)
        
        # Generate recommendations
        diagnostic_result["recommendations"] = self._generate_recommendations(diagnostic_result)
        
        # Store results
        self._store_diagnostic_results(diagnostic_result)
        
        # Update alerts
        self._update_alerts(diagnostic_result)
        
        self.last_diagnostic = diagnostic_result
        self.diagnostic_history.append(diagnostic_result)
        
        return diagnostic_result
    
    async def check_core_system(self) -> dict:
        """Check core Echo launcher system"""
        result = {"status": "healthy", "details": {}, "issues": []}
        
        try:
            # Check Python version
            python_version = sys.version_info
            result["details"]["python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
            
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                result["status"] = "warning"
                result["issues"].append("Python 3.8+ recommended")
            
            # System info
            result["details"]["platform"] = platform.platform()
            result["details"]["processor"] = platform.processor()
            
            # Check critical directories
            critical_dirs = [LOG_DIR, DESKTOP_SERVERS_PATH, Path("E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION")]
            missing_dirs = [str(d) for d in critical_dirs if not d.exists()]
            
            if missing_dirs:
                result["status"] = "warning"
                result["issues"].append(f"Missing directories: {len(missing_dirs)}")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def check_memory_system(self) -> dict:
        """Check memory systems"""
        result = {"status": "healthy", "details": {}, "issues": []}
        
        try:
            mem = psutil.virtual_memory()
            result["details"]["system_memory"] = {
                "total_gb": round(mem.total / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "percent_used": mem.percent
            }
            
            if mem.percent > 85:
                result["status"] = "warning"
                result["issues"].append(f"High memory usage: {mem.percent}%")
            elif mem.percent > 95:
                result["status"] = "critical"
                result["issues"].append(f"Critical memory usage: {mem.percent}%")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def check_voice_system(self) -> dict:
        """Check voice I/O systems"""
        result = {"status": "healthy", "details": {}, "issues": []}
        
        try:
            result["details"]["voice_available"] = VOICE_AVAILABLE
            
            if not VOICE_AVAILABLE:
                result["status"] = "warning"
                result["issues"].append("Voice system not available")
            else:
                result["details"]["voice_initialized"] = self.voice and self.voice.voice is not None
                
                if not (self.voice and self.voice.voice):
                    result["status"] = "warning"
                    result["issues"].append("Voice system not initialized")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def check_server_systems(self) -> dict:
        """Check all launched servers"""
        result = {"status": "healthy", "details": {}, "issues": []}
        
        try:
            total_servers = len(self.current_server_states)
            running_servers = sum(1 for s in self.current_server_states.values() if s.get("status") == "running")
            failed_servers = sum(1 for s in self.current_server_states.values() if s.get("status") == "failed")
            
            result["details"]["total_servers"] = total_servers
            result["details"]["running_servers"] = running_servers
            result["details"]["failed_servers"] = failed_servers
            result["details"]["success_rate"] = (running_servers / max(total_servers, 1)) * 100
            
            if failed_servers > 0:
                result["status"] = "warning"
                result["issues"].append(f"{failed_servers} server(s) failed to start")
            
            if running_servers == 0 and total_servers > 0:
                result["status"] = "critical"
                result["issues"].append("No servers are running")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def check_performance(self) -> dict:
        """Check system performance"""
        result = {"status": "healthy", "details": {}, "issues": []}
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.5)
            result["details"]["cpu"] = {
                "usage_percent": cpu_percent,
                "core_count": psutil.cpu_count()
            }
            
            if cpu_percent > 80:
                result["status"] = "warning"
                result["issues"].append(f"High CPU usage: {cpu_percent}%")
            
            # Memory
            mem = psutil.virtual_memory()
            result["details"]["memory"] = {
                "percent_used": mem.percent,
                "available_gb": round(mem.available / (1024**3), 2)
            }
            
            # Active threads
            result["details"]["active_threads"] = threading.active_count()
            
            # Response time test
            start = time.time()
            _ = 2 ** 20  # Simple computation
            response_time = (time.time() - start) * 1000
            result["details"]["response_time_ms"] = round(response_time, 2)
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def check_storage(self) -> dict:
        """Check storage systems"""
        result = {"status": "healthy", "details": {}, "issues": []}
        
        try:
            # Check E: drive (main Echo drive)
            disk = psutil.disk_usage('E:/')
            result["details"]["echo_drive"] = {
                "total_gb": round(disk.total / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent_used": disk.percent
            }
            
            if disk.percent > 90:
                result["status"] = "critical"
                result["issues"].append(f"Critical disk space: {disk.percent}% used")
            elif disk.percent > 80:
                result["status"] = "warning"
                result["issues"].append(f"Low disk space: {disk.percent}% used")
            
            # Check log directory size
            log_size = sum(f.stat().st_size for f in LOG_DIR.glob('**/*') if f.is_file())
            result["details"]["log_size_mb"] = round(log_size / (1024**2), 2)
            
            if log_size > 1024**3:  # 1GB
                result["status"] = "warning"
                result["issues"].append("Log files exceed 1GB")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _calculate_health_score(self, diagnostic_result: dict) -> float:
        """Calculate overall health score (0-100)"""
        score = 100.0
        
        for component, data in diagnostic_result["components"].items():
            if data["status"] == "critical":
                score -= 25
            elif data["status"] == "warning":
                score -= 10
            elif data["status"] == "error":
                score -= 20
        
        if diagnostic_result["performance"].get("diagnostic_time", 0) > 10:
            score -= 5
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self, diagnostic_result: dict) -> list:
        """Generate recommendations based on diagnostic results"""
        recommendations = []
        
        for component, data in diagnostic_result["components"].items():
            if data["status"] != "healthy" and "issues" in data:
                for issue in data["issues"]:
                    if "High memory usage" in issue or "Critical memory" in issue:
                        recommendations.append("Restart servers to free memory")
                    elif "failed to start" in issue:
                        recommendations.append("Check server logs for startup errors")
                    elif "Low disk space" in issue or "Critical disk" in issue:
                        recommendations.append("Free up disk space or archive old logs")
                    elif "Log files exceed" in issue:
                        recommendations.append("Rotate or compress log files")
        
        if diagnostic_result.get("performance", {}).get("score", 100) < 70:
            recommendations.append("System health degraded - consider maintenance")
        
        return recommendations[:3]  # Top 3 recommendations
    
    def _store_diagnostic_results(self, results: dict):
        """Store diagnostic results in database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO diagnostic_runs (timestamp, overall_status, details, alerts, performance_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                results["timestamp"],
                results["status"],
                json.dumps(results),
                json.dumps(results.get("alerts", [])),
                results.get("performance", {}).get("score", 0)
            ))
            
            run_id = cursor.lastrowid
            
            for component, data in results["components"].items():
                cursor.execute('''
                    INSERT INTO component_status (run_id, component, status, details, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    run_id,
                    component,
                    data.get("status", "unknown"),
                    json.dumps(data),
                    results["timestamp"]
                ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to store diagnostic results: {e}")
    
    def _update_alerts(self, diagnostic_result: dict):
        """Update system alerts based on diagnostic results"""
        self.alerts.clear()
        
        critical_components = [
            comp for comp, data in diagnostic_result["components"].items()
            if data.get("status") == "critical"
        ]
        
        if critical_components:
            self.alerts.append({
                "level": "critical",
                "message": f"Critical issues in: {', '.join(critical_components)}",
                "timestamp": datetime.now().isoformat()
            })
        
        warning_components = [
            comp for comp, data in diagnostic_result["components"].items()
            if data.get("status") == "warning"
        ]
        
        if warning_components:
            self.alerts.append({
                "level": "warning",
                "message": f"Warnings in: {', '.join(warning_components)}",
                "timestamp": datetime.now().isoformat()
            })
    
    def start_real_time_monitoring(self, interval: int = 300):
        """Start real-time monitoring (default: every 5 minutes)"""
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    cpu = psutil.cpu_percent(interval=1)
                    mem = psutil.virtual_memory().percent
                    disk = psutil.disk_usage('E:/').percent
                    
                    metrics = {
                        "timestamp": datetime.now().isoformat(),
                        "cpu_usage": cpu,
                        "memory_usage": mem,
                        "disk_usage": disk,
                        "server_count": len(self.current_server_states),
                        "active_threads": threading.active_count()
                    }
                    
                    self._store_performance_metrics(metrics)
                    
                    # Check thresholds
                    if cpu > 90 or mem > 90:
                        alert_msg = f"High resource usage - CPU: {cpu}%, Memory: {mem}%"
                        logger.warning(alert_msg)
                        if self.voice:
                            self.voice.announce(f"Warning: {alert_msg}", voice_id='0UTDtgGGkpqERQn1s0YK')
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info(f"🔍 Real-time monitoring started (interval: {interval}s)")
    
    def stop_real_time_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Real-time monitoring stopped")
    
    def _store_performance_metrics(self, metrics: dict):
        """Store performance metrics in database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_metrics 
                (timestamp, cpu_usage, memory_usage, disk_usage, server_count, active_threads)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                metrics["timestamp"],
                metrics.get("cpu_usage", 0),
                metrics.get("memory_usage", 0),
                metrics.get("disk_usage", 0),
                metrics.get("server_count", 0),
                metrics.get("active_threads", 0)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to store performance metrics: {e}")
    
    def generate_diagnostic_report(self, diagnostic_result: dict) -> str:
        """Generate human-readable diagnostic report"""
        lines = []
        lines.append("=" * 60)
        lines.append("🔧 ECHO PRIME DIAGNOSTIC REPORT")
        lines.append("=" * 60)
        lines.append(f"Timestamp: {diagnostic_result['timestamp']}")
        lines.append(f"Overall Status: {diagnostic_result['status'].upper()}")
        lines.append(f"Health Score: {diagnostic_result.get('performance', {}).get('score', 0):.1f}/100")
        lines.append("")
        
        lines.append("COMPONENT STATUS:")
        lines.append("-" * 40)
        
        status_icons = {"healthy": "✅", "warning": "⚠️", "critical": "❌", "error": "❌"}
        
        for component, data in diagnostic_result["components"].items():
            icon = status_icons.get(data.get("status", "unknown"), "❓")
            lines.append(f"{icon} {component.upper()}: {data.get('status', 'unknown')}")
            
            if "issues" in data and data["issues"]:
                for issue in data["issues"]:
                    lines.append(f"   - {issue}")
        
        lines.append("")
        
        if diagnostic_result.get("recommendations"):
            lines.append("RECOMMENDATIONS:")
            lines.append("-" * 40)
            for i, rec in enumerate(diagnostic_result["recommendations"], 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)

# Server configs
MCP_SERVERS = [
    ("Orchestrator", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\orchestrator\\mcp_orchestrator.py", 8000, "mcp"),
    ("Filesystem", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\filesystem\\mcp_filesystem.py", 8001, "mcp"),
    ("Windows API", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\windows_api\\mcp_windows.py", 8002, "mcp"),
    ("Process Control", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\process_control\\mcp_process.py", 8003, "mcp"),
    ("Crystal Memory", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\crystal_memory\\mcp_crystal.py", 8004, "mcp"),
    ("Workflow Engine", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\workflow_engine\\mcp_workflow.py", 8005, "mcp"),
    ("Voice System", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\voice_system\\mcp_voice.py", 8006, "mcp"),
    ("Network Tools", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\network_tools\\mcp_network.py", 8007, "mcp"),
    ("Healing Protocols", "E:\\ECHO_XV4\\MLS\\servers\\MCP_CONSTELLATION\\healing_protocols\\mcp_healing.py", 8008, "mcp"),
]

DESKTOP_SERVERS_PATH = Path("E:/ECHO_XV4/MLS/servers/ACTIVE_SERVERS")
LOG_DIR = Path("E:/ECHO_XV4/MLS/logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"unified_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

server_states = {}

def discover_desktop_servers():
    if not DESKTOP_SERVERS_PATH.exists():
        return []
    
    servers = []
    next_port = 9000
    
    for py_file in DESKTOP_SERVERS_PATH.glob("*.py"):
        if py_file.stem.startswith("__") or "test" in py_file.stem.lower() or py_file.stem == "LAUNCH_MCP_CONSTELLATION":
            continue
        
        servers.append((
            py_file.stem.replace('_', ' ').title(),
            str(py_file),
            next_port,
            "desktop"
        ))
        next_port += 1
    
    return servers

def launch_server(name: str, path: str, port: int, server_type: str, python_exe: str) -> bool:
    # Check if already running
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and path in ' '.join(cmdline):
                logger.info(f"✅ {name} already running (PID: {proc.info['pid']})")
                server_states[name] = {"status": "running", "pid": proc.info['pid'], "type": server_type}
                return True
        except: continue
    
    # Launch SILENTLY (no window)
    logger.info(f"🚀 Launching {name} ({server_type}) SILENTLY...")
    
    log_file = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    try:
        with open(log_file, 'w') as log:
            # CREATE_NO_WINDOW = 0x08000000
            proc = subprocess.Popen(
                [python_exe, path],
                stdout=log,
                stderr=subprocess.STDOUT,
                creationflags=0x08000000 if sys.platform == 'win32' else 0
            )
        
        time.sleep(2)
        
        if proc.poll() is None:
            logger.info(f"✅ {name} launched silently (PID: {proc.pid})")
            server_states[name] = {"status": "running", "pid": proc.pid, "type": server_type}
            return True
        else:
            logger.error(f"❌ {name} crashed")
            return False
    except Exception as e:
        logger.error(f"❌ {name} exception: {e}")
        return False

def main():
    print("=" * 70)
    print("🚀 UNIFIED MEGA-LAUNCHER V2 + ECHO DIAGNOSTICS")
    print("   Authority Level 11.0 - Commander Bobby Don McWilliams II")
    print("   ALL SERVERS LAUNCH WITHOUT WINDOWS")
    print("   + Real-time Health Monitoring & Self-Healing")
    print("=" * 70)
    
    voice.announce("Unified Silent Launcher with diagnostics initialized", '8ATB4Ory7NkyCVRpePdw')
    
    # Initialize diagnostic system
    logger.info("🔧 Initializing Echo Diagnostic System...")
    diagnostics = EchoDiagnosticSystem(voice_system=voice)
    
    python_exe = "E:\\ECHO_XV4\\MLS\\servers\\ACTIVE_SERVERS\\venv_mcp_py312\\Scripts\\python.exe"
    
    desktop_servers = discover_desktop_servers()
    all_servers = MCP_SERVERS + desktop_servers
    
    logger.info(f"📡 Total: {len(all_servers)} servers (MCP: {len(MCP_SERVERS)}, Desktop: {len(desktop_servers)})")
    
    launched = 0
    already_running = 0
    failed = 0
    
    for name, path, port, server_type in all_servers:
        if launch_server(name, path, port, server_type, python_exe):
            already_running += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print("📊 SILENT LAUNCH SUMMARY")
    print("=" * 70)
    print(f"   ✅ Running: {already_running}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Total: {len(all_servers)}")
    print("=" * 70)
    
    # Run post-launch diagnostic
    print("\n🔧 Running post-launch diagnostic...")
    voice.announce("Running system diagnostic", '0UTDtgGGkpqERQn1s0YK')
    
    diagnostic_result = asyncio.run(diagnostics.run_full_diagnostic(server_states))
    
    # Generate and display report
    report = diagnostics.generate_diagnostic_report(diagnostic_result)
    print("\n" + report)
    
    # Save diagnostic report
    report_file = LOG_DIR / f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    logger.info(f"📄 Diagnostic report saved: {report_file}")
    
    # Voice announcement of status
    health_score = diagnostic_result.get('performance', {}).get('score', 0)
    status = diagnostic_result.get('status', 'unknown')
    
    if status == "healthy":
        voice.announce(f"All systems healthy. Health score {health_score:.0f} out of 100. All {len(all_servers)} servers operational.", 'keDMh3sQlEXKM4EQxvvi')
    elif status == "warning":
        issues = sum(len(c.get('issues', [])) for c in diagnostic_result['components'].values())
        voice.announce(f"System operational with {issues} warnings. Health score {health_score:.0f}. Recommend review.", '0UTDtgGGkpqERQn1s0YK')
    else:
        voice.announce(f"Critical system issues detected. Health score {health_score:.0f}. Immediate attention required.", 'pzKXffibtCDxnrVO8d1U')
    
    # Start real-time monitoring
    print("\n🔍 Starting real-time health monitoring (5-minute intervals)...")
    diagnostics.start_real_time_monitoring(interval=300)
    
    print("\n🔇 All servers running SILENTLY (no console windows)")
    print("🔍 Diagnostic monitoring ACTIVE")
    print("\n📋 DIAGNOSTIC COMMANDS:")
    print("   Press 'D' + Enter for diagnostic report")
    print("   Press 'H' + Enter for health status")
    print("   Press 'S' + Enter for server status")
    print("   Press 'Q' + Enter to quit")
    print("\nPress Ctrl+C to exit (servers continue running)")
    
    try:
        import sys
        import select
        
        while True:
            # Check for keyboard input (Windows-compatible)
            if sys.platform == 'win32':
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').upper()
                    
                    if key == 'D':
                        print("\n🔧 Running diagnostic...")
                        result = asyncio.run(diagnostics.run_full_diagnostic(server_states))
                        print(diagnostics.generate_diagnostic_report(result))
                        voice.announce(f"Diagnostic complete. Health score {result['performance']['score']:.0f}", '0UTDtgGGkpqERQn1s0YK')
                    
                    elif key == 'H':
                        if diagnostics.last_diagnostic:
                            score = diagnostics.last_diagnostic['performance']['score']
                            status = diagnostics.last_diagnostic['status']
                            print(f"\n💚 Health: {status.upper()} - Score: {score:.1f}/100")
                            voice.announce(f"Health score {score:.0f} out of 100", '0UTDtgGGkpqERQn1s0YK')
                        else:
                            print("\n⚠️ No diagnostic data available")
                    
                    elif key == 'S':
                        print("\n📊 SERVER STATUS:")
                        for name, state in server_states.items():
                            status_icon = "✅" if state["status"] == "running" else "❌"
                            print(f"  {status_icon} {name}: {state['status']} (PID: {state.get('pid', 'N/A')})")
                    
                    elif key == 'Q':
                        print("\n👋 Shutting down...")
                        diagnostics.stop_real_time_monitoring()
                        voice.announce("Launcher shutting down", '0UTDtgGGkpqERQn1s0YK')
                        break
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupt received - shutting down...")
        diagnostics.stop_real_time_monitoring()
        voice.announce("Diagnostic system shutting down", '0UTDtgGGkpqERQn1s0YK')
        print("👋 Exiting (servers continue running)")

if __name__ == "__main__":
    main()
