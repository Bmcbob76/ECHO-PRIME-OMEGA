"""
ECHO Prime Windows Service
Runs ECHO systems as a Windows service for 24/7 operation
Authority Level: 11.0 - Commander McWilliams
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import subprocess
import logging
from pathlib import Path

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass


class EchoPrimeService(win32serviceutil.ServiceFramework):
    _svc_name_ = "EchoPrimeDefense"
    _svc_display_name_ = "ECHO Prime Defense System"
    _svc_description_ = "24/7 ECHO Defense Systems - Authority Level 11.0"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
        # Service configuration
        self.base_path = Path("E:/ECHO_PRIME_SYSTEM/ECHO_QUANTUM_DEFENDER")
        self.launcher_script = self.base_path / "echo_prime_master_launcher.py"
        self.launcher_process = None
        
        # Setup logging for service
        self.setup_service_logging()
        
    def setup_service_logging(self):
        """Setup logging for Windows service"""
        log_dir = self.base_path / 'logs' / 'service'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [SERVICE] - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'echo_prime_service.log'),
            ]
        )
        
    def SvcStop(self):
        """Service stop handler"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        logging.info("ECHO Prime Service stopping...")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STOPPING,
                            (self._svc_name_, ''))
        
        # Stop the launcher process
        if self.launcher_process:
            try:
                self.launcher_process.terminate()
                self.launcher_process.wait(timeout=30)
                logging.info("Master launcher stopped gracefully")
            except subprocess.TimeoutExpired:
                self.launcher_process.kill()
                logging.warning("Master launcher force stopped")
            except Exception as e:
                logging.error(f"Error stopping launcher: {e}")
                
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        """Service main execution"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        
        logging.info("ECHO Prime Service starting...")
        self.main()
        
    def main(self):
        """Main service loop"""
        try:
            # Start the master launcher
            self.start_master_launcher()
            
            # Service loop - wait for stop event
            while True:
                # Wait for stop event with timeout
                rc = win32event.WaitForSingleObject(self.hWaitStop, 30000)  # 30 seconds
                
                if rc == win32event.WAIT_OBJECT_0:
                    # Stop event signaled
                    break
                elif rc == win32event.WAIT_TIMEOUT:
                    # Timeout - check if launcher is still running
                    self.check_launcher_health()
                    
        except Exception as e:
            logging.error(f"Service error: {e}")
            servicemanager.LogErrorMsg(f"ECHO Prime Service error: {e}")
            
    def start_master_launcher(self):
        """Start the master launcher process"""
        try:
            logging.info("Starting ECHO Prime Master Launcher...")
            
            # Prepare environment
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.base_path)
            
            # Start launcher process
            self.launcher_process = subprocess.Popen(
                [sys.executable, str(self.launcher_script)],
                cwd=str(self.base_path),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            logging.info(f"Master launcher started (PID: {self.launcher_process.pid})")
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SERVICE_STARTED,
                                (f"Master Launcher PID: {self.launcher_process.pid}", ''))
            
        except Exception as e:
            logging.error(f"Failed to start master launcher: {e}")
            raise
            
    def check_launcher_health(self):
        """Check if launcher is still running and restart if needed"""
        if self.launcher_process:
            poll_result = self.launcher_process.poll()
            if poll_result is not None:
                # Process has died
                logging.warning(f"Master launcher died with exit code: {poll_result}")
                
                # Get any error output
                try:
                    stdout, stderr = self.launcher_process.communicate(timeout=1)
                    if stderr:
                        logging.error(f"Launcher stderr: {stderr}")
                    if stdout:
                        logging.info(f"Launcher stdout: {stdout}")
                except subprocess.TimeoutExpired:
                    pass
                    
                # Restart the launcher
                logging.info("Restarting master launcher...")
                self.start_master_launcher()


def install_service():
    """Install the Windows service"""
    try:
        win32serviceutil.InstallService(
            EchoPrimeService,
            EchoPrimeService._svc_name_,
            EchoPrimeService._svc_display_name_,
            description=EchoPrimeService._svc_description_,
            startType=win32service.SERVICE_AUTO_START
        )
        print("✅ ECHO Prime Service installed successfully")
        print("   Service Name:", EchoPrimeService._svc_name_)
        print("   Display Name:", EchoPrimeService._svc_display_name_)
        print("   Start Type: Automatic")
        
    except Exception as e:
        print(f"❌ Failed to install service: {e}")
        

def uninstall_service():
    """Uninstall the Windows service"""
    try:
        win32serviceutil.RemoveService(EchoPrimeService._svc_name_)
        print("✅ ECHO Prime Service uninstalled successfully")
        
    except Exception as e:
        print(f"❌ Failed to uninstall service: {e}")


def start_service():
    """Start the Windows service"""
    try:
        win32serviceutil.StartService(EchoPrimeService._svc_name_)
        print("✅ ECHO Prime Service started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start service: {e}")


def stop_service():
    """Stop the Windows service"""
    try:
        win32serviceutil.StopService(EchoPrimeService._svc_name_)
        print("✅ ECHO Prime Service stopped successfully")
        
    except Exception as e:
        print(f"❌ Failed to stop service: {e}")


def restart_service():
    """Restart the Windows service"""
    try:
        win32serviceutil.RestartService(EchoPrimeService._svc_name_)
        print("✅ ECHO Prime Service restarted successfully")
        
    except Exception as e:
        print(f"❌ Failed to restart service: {e}")


def service_status():
    """Check service status"""
    try:
        status = win32serviceutil.QueryServiceStatus(EchoPrimeService._svc_name_)
        status_map = {
            win32service.SERVICE_STOPPED: "STOPPED",
            win32service.SERVICE_START_PENDING: "START_PENDING",
            win32service.SERVICE_STOP_PENDING: "STOP_PENDING",
            win32service.SERVICE_RUNNING: "RUNNING",
            win32service.SERVICE_CONTINUE_PENDING: "CONTINUE_PENDING",
            win32service.SERVICE_PAUSE_PENDING: "PAUSE_PENDING",
            win32service.SERVICE_PAUSED: "PAUSED"
        }
        
        current_status = status_map.get(status[1], f"UNKNOWN({status[1]})")
        print(f"ECHO Prime Service Status: {current_status}")
        
        return status[1]
        
    except Exception as e:
        print(f"❌ Failed to get service status: {e}")
        return None


def main():
    """Main entry point for service management"""
    if len(sys.argv) == 1:
        # No arguments - run as service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(EchoPrimeService)
        servicemanager.StartServiceCtrlDispatcher()
        
    else:
        # Command line arguments
        command = sys.argv[1].lower()
        
        print("=" * 60)
        print("    🚀 ECHO PRIME SERVICE MANAGER 🚀")
        print("    Authority Level: 11.0")
        print("    Commander: Bobby Don McWilliams II")
        print("=" * 60)
        
        if command == 'install':
            install_service()
        elif command == 'uninstall':
            uninstall_service()
        elif command == 'start':
            start_service()
        elif command == 'stop':
            stop_service()
        elif command == 'restart':
            restart_service()
        elif command == 'status':
            service_status()
        elif command == 'help':
            print("\nAvailable commands:")
            print("  install    - Install the Windows service")
            print("  uninstall  - Uninstall the Windows service")
            print("  start      - Start the service")
            print("  stop       - Stop the service")
            print("  restart    - Restart the service")
            print("  status     - Check service status")
            print("  help       - Show this help")
        else:
            print(f"Unknown command: {command}")
            print("Use 'help' for available commands")


if __name__ == '__main__':
    main()