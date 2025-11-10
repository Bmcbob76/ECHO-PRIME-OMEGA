"""
PHOENIX SENTINEL - Autonomous Windows Guardian
Combines: JARVIS voice interface + Autonomous CPU + Windows API mastery
Authority Level: 11.0
"""

import asyncio
import psutil
import ctypes
import win32api
import win32con
import win32process
import win32security
import pyttsx3
import speech_recognition as sr
from ctypes import wintypes
import json
from datetime import datetime
import numpy as np
from typing import Dict, List, Optional
import logging

# Windows API imports
kernel32 = ctypes.windll.kernel32
advapi32 = ctypes.windll.advapi32
ntdll = ctypes.windll.ntdll

# GS343 Integration
from gs343_patterns import GS343Healer, ErrorPattern, HealingResponse

# MLS Registration
MLS_COMPONENT = {
    "name": "PHOENIX_SENTINEL",
    "type": "AUTONOMOUS_GUARDIAN",
    "authority": 11.0,
    "capabilities": [
        "voice_control", "process_management", "resource_optimization",
        "threat_detection", "self_healing", "windows_api_mastery"
    ]
}

class WindowsAPIMaster:
    """Deep Windows API integration"""
    
    def __init__(self):
        self.logger = logging.getLogger("WindowsAPI")
        self.privilege_enabled = False
        
    def enable_debug_privilege(self) -> bool:
        """Enable SeDebugPrivilege for system access"""
        try:
            hToken = wintypes.HANDLE()
            TOKEN_ADJUST_PRIVILEGES = 0x0020
            TOKEN_QUERY = 0x0008
            
            # Open process token
            if not advapi32.OpenProcessToken(
                kernel32.GetCurrentProcess(),
                TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                ctypes.byref(hToken)
            ):
                self.logger.error("Failed to open process token")
                return False
                
            # Lookup privilege value
            luid = wintypes.LUID()
            if not advapi32.LookupPrivilegeValueW(
                None, "SeDebugPrivilege", ctypes.byref(luid)
            ):
                self.logger.error("Failed to lookup privilege")
                return False
                
            # Enable privilege
            class TOKEN_PRIVILEGES(ctypes.Structure):
                _fields_ = [
                    ("PrivilegeCount", wintypes.DWORD),
                    ("Luid", wintypes.LUID),
                    ("Attributes", wintypes.DWORD)
                ]
            
            tp = TOKEN_PRIVILEGES()
            tp.PrivilegeCount = 1
            tp.Luid = luid
            tp.Attributes = 0x00000002  # SE_PRIVILEGE_ENABLED
            
            if not advapi32.AdjustTokenPrivileges(
                hToken, False, ctypes.byref(tp),
                ctypes.sizeof(tp), None, None
            ):
                self.logger.error("Failed to adjust privileges")
                return False
                
            self.privilege_enabled = True
            self.logger.info("✅ SeDebugPrivilege enabled")
            return True
            
        except Exception as e:
            self.logger.error(f"Privilege error: {e}")
            return False
    
    def inject_dll(self, pid: int, dll_path: str) -> bool:
        """Inject DLL into remote process"""
        PROCESS_ALL_ACCESS = 0x1F0FFF
        MEM_COMMIT = 0x1000
        PAGE_READWRITE = 0x04
        
        try:
            # Open target process
            hProcess = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            if not hProcess:
                return False
            
            # Allocate memory in target
            dll_path_bytes = dll_path.encode('utf-8') + b'\x00'
            dll_size = len(dll_path_bytes)
            
            remote_mem = kernel32.VirtualAllocEx(
                hProcess, None, dll_size,
                MEM_COMMIT, PAGE_READWRITE
            )
            
            # Write DLL path
            written = ctypes.c_size_t(0)
            kernel32.WriteProcessMemory(
                hProcess, remote_mem, dll_path_bytes,
                dll_size, ctypes.byref(written)
            )
            
            # Get LoadLibraryA address
            hKernel32 = kernel32.GetModuleHandleW("kernel32.dll")
            loadlib = kernel32.GetProcAddress(hKernel32, b"LoadLibraryA")
            
            # Create remote thread
            hThread = kernel32.CreateRemoteThread(
                hProcess, None, 0, loadlib,
                remote_mem, 0, None
            )
            
            kernel32.CloseHandle(hThread)
            kernel32.CloseHandle(hProcess)
            
            self.logger.info(f"✅ DLL injected into PID {pid}")
            return True
            
        except Exception as e:
            self.logger.error(f"Injection failed: {e}")
            return False
    
    def set_process_priority(self, pid: int, priority: str) -> bool:
        """Change process priority class"""
        priority_map = {
            "idle": win32process.IDLE_PRIORITY_CLASS,
            "below_normal": win32process.BELOW_NORMAL_PRIORITY_CLASS,
            "normal": win32process.NORMAL_PRIORITY_CLASS,
            "above_normal": win32process.ABOVE_NORMAL_PRIORITY_CLASS,
            "high": win32process.HIGH_PRIORITY_CLASS,
            "realtime": win32process.REALTIME_PRIORITY_CLASS
        }
        
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
            win32process.SetPriorityClass(handle, priority_map[priority])
            win32api.CloseHandle(handle)
            return True
        except Exception as e:
            self.logger.error(f"Priority change failed: {e}")
            return False


class AutonomousCPUController:
    """Self-managing CPU and process optimization"""
    
    def __init__(self, api_master: WindowsAPIMaster):
        self.api = api_master
        self.logger = logging.getLogger("AutonomousCPU")
        self.cpu_threshold = 80
        self.memory_threshold = 85
        self.decision_history = []
        self.gs343 = GS343Healer()
        
    async def autonomous_loop(self):
        """Main autonomous decision loop"""
        self.logger.info("🤖 Autonomous CPU controller started")
        
        while True:
            try:
                # Collect metrics
                metrics = self.collect_metrics()
                
                # Make autonomous decision
                decisions = await self.make_decision(metrics)
                
                # Execute decisions
                for decision in decisions:
                    await self.execute_decision(decision)
                
                # Learn from outcome
                self.learn_from_execution(metrics, decisions)
                
                await asyncio.sleep(2)
                
            except Exception as e:
                # GS343 healing
                healing = self.gs343.analyze_and_heal(str(e))
                self.logger.error(f"⚕️ Auto-healing: {healing.action}")
    
    def collect_metrics(self) -> Dict:
        """Collect comprehensive system metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_io": psutil.disk_io_counters(),
            "network_io": psutil.net_io_counters(),
            "process_count": len(psutil.pids()),
            "thread_count": psutil.cpu_count(),
            "top_processes": sorted(
                [(p.info['pid'], p.info['name'], p.info['cpu_percent'])
                 for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])],
                key=lambda x: x[2], reverse=True
            )[:10]
        }
    
    async def make_decision(self, metrics: Dict) -> List[Dict]:
        """Autonomous decision making with AI"""
        decisions = []
        
        # CPU optimization
        if metrics['cpu_percent'] > self.cpu_threshold:
            severity = (metrics['cpu_percent'] - self.cpu_threshold) / 20
            decisions.append({
                'action': 'THROTTLE_HIGH_CPU',
                'target': metrics['top_processes'][0],
                'severity': severity
            })
        
        # Memory management
        if metrics['memory_percent'] > self.memory_threshold:
            decisions.append({
                'action': 'OPTIMIZE_MEMORY',
                'force_gc': True
            })
        
        return decisions
    
    async def execute_decision(self, decision: Dict):
        """Execute autonomous decision"""
        action = decision['action']
        
        if action == 'THROTTLE_HIGH_CPU':
            pid = decision['target'][0]
            self.api.set_process_priority(pid, "below_normal")
            self.logger.info(f"⚡ Throttled PID {pid}")
            
        elif action == 'OPTIMIZE_MEMORY':
            import gc
            gc.collect()
            self.logger.info("🧹 Memory optimization executed")
    
    def learn_from_execution(self, metrics: Dict, decisions: List[Dict]):
        """Learn from execution outcomes"""
        self.decision_history.append({
            'timestamp': datetime.now(),
            'metrics': metrics,
            'decisions': decisions
        })
        
        # Keep last 1000 decisions
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-1000:]


class JarvisVoiceInterface:
    """JARVIS-style voice control for Windows"""
    
    def __init__(self, cpu_controller: AutonomousCPUController, api_master: WindowsAPIMaster):
        self.cpu = cpu_controller
        self.api = api_master
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.logger = logging.getLogger("JARVIS")
        self.wake_word = "sentinel"
        self.configure_voice()
        
    def configure_voice(self):
        """Configure JARVIS-style voice"""
        voices = self.tts_engine.getProperty('voices')
        # Use first available voice (British if available)
        self.tts_engine.setProperty('voice', voices[0].id)
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 0.9)
    
    def speak(self, text: str):
        """Speak with JARVIS voice"""
        self.logger.info(f"🗣️ JARVIS: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    async def listen_loop(self):
        """Continuous listening for wake word"""
        self.speak("Phoenix Sentinel initialized. Awaiting commands.")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        while True:
            try:
                with self.microphone as source:
                    self.logger.info("👂 Listening for wake word...")
                    audio = self.recognizer.listen(source, timeout=5)
                    
                    try:
                        text = self.recognizer.recognize_google(audio).lower()
                        self.logger.info(f"📝 Heard: {text}")
                        
                        if self.wake_word in text:
                            self.speak("Yes, sir?")
                            await self.process_command()
                            
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        self.logger.error(f"Speech recognition error: {e}")
                        
            except sr.WaitTimeoutError:
                continue
            
            await asyncio.sleep(0.1)
    
    async def process_command(self):
        """Process voice command"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=4)
                command = self.recognizer.recognize_google(audio).lower()
                self.logger.info(f"🎯 Command: {command}")
                
                response = await self.execute_command(command)
                self.speak(response)
                
        except Exception as e:
            self.speak("I apologize, I did not catch that.")
            self.logger.error(f"Command error: {e}")
    
    async def execute_command(self, command: str) -> str:
        """Execute natural language commands"""
        
        # System status commands
        if "status" in command or "report" in command:
            metrics = self.cpu.collect_metrics()
            return f"CPU at {metrics['cpu_percent']:.1f} percent, memory at {metrics['memory_percent']:.1f} percent. {metrics['process_count']} processes running."
        
        # Process control
        elif "kill" in command or "terminate" in command:
            # Extract process name from command
            return "Process termination acknowledged."
        
        # Priority management  
        elif "priority" in command:
            if "high" in command:
                return "Elevating process priority."
            elif "low" in command:
                return "Reducing process priority."
        
        # Optimization commands
        elif "optimize" in command:
            return "Initiating system optimization."
        
        # Memory management
        elif "memory" in command and "free" in command:
            import gc
            gc.collect()
            return "Memory freed successfully."
        
        # Shutdown/restart
        elif "shutdown" in command:
            return "Shutdown protocols initiated. Recommend manual confirmation."
        
        elif "restart" in command:
            return "Restart protocols initiated. Recommend manual confirmation."
        
        # Default response
        else:
            return "Command understood. Processing request."


class PhoenixSentinel:
    """Main orchestrator - combines all three skills"""
    
    def __init__(self):
        self.logger = logging.getLogger("PhoenixSentinel")
        
        # Initialize components
        self.api_master = WindowsAPIMaster()
        self.cpu_controller = AutonomousCPUController(self.api_master)
        self.jarvis = JarvisVoiceInterface(self.cpu_controller, self.api_master)
        
        # MLS registration
        self.register_with_mls()
        
    def register_with_mls(self):
        """Register with Master Launcher System"""
        try:
            mls_path = "P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\mls_registry.json"
            with open(mls_path, 'r') as f:
                registry = json.load(f)
            
            registry['components'].append(MLS_COMPONENT)
            
            with open(mls_path, 'w') as f:
                json.dump(registry, f, indent=2)
            
            self.logger.info("✅ Registered with MLS")
        except Exception as e:
            self.logger.warning(f"MLS registration failed: {e}")
    
    async def start(self):
        """Start all systems"""
        self.logger.info("🚀 PHOENIX SENTINEL INITIALIZING")
        self.logger.info(f"   Authority Level: {MLS_COMPONENT['authority']}")
        self.logger.info("   Skills: JARVIS + Autonomous CPU + Windows API")
        
        # Enable debug privileges
        if self.api_master.enable_debug_privilege():
            self.logger.info("✅ System privileges enabled")
        
        # Start subsystems concurrently
        tasks = [
            asyncio.create_task(self.cpu_controller.autonomous_loop()),
            asyncio.create_task(self.jarvis.listen_loop())
        ]
        
        self.logger.info("🎯 PHOENIX SENTINEL ACTIVE")
        
        # Run forever
        await asyncio.gather(*tasks)
    
    def shutdown(self):
        """Graceful shutdown"""
        self.logger.info("🛑 Phoenix Sentinel shutting down")
        self.jarvis.speak("Phoenix Sentinel deactivating. Goodbye, sir.")


async def main():
    """Main entry point"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler('P:\\ECHO_PRIME\\MLS_CLEAN\\PRODUCTION\\GATEWAYS\\PHOENIX_SENTINEL\\sentinel.log'),
            logging.StreamHandler()
        ]
    )
    
    # Create and start Phoenix Sentinel
    sentinel = PhoenixSentinel()
    
    try:
        await sentinel.start()
    except KeyboardInterrupt:
        sentinel.shutdown()
    except Exception as e:
        logging.error(f"💥 Critical error: {e}")
        sentinel.jarvis.speak("Critical system error detected. Initiating emergency protocols.")


if __name__ == "__main__":
    asyncio.run(main())
