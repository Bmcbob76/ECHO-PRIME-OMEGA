#!/usr/bin/env python3
"""
PRODUCTION DEPLOYMENT SYSTEM
Commander Bobby Don McWilliams II - Authority Level 11.0

Handles production launch, monitoring, and maintenance
"""

import sys
import os
import subprocess
import time
import json
import psutil
from pathlib import Path
from datetime import datetime
import logging

PROJECT_ROOT = Path(__file__).parent
PYTHON = "H:\\Tools\\python.exe"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Production")


class ProductionDeployment:
    """Production deployment manager"""
    
    def __init__(self):
        self.root = PROJECT_ROOT
        self.python = PYTHON
        self.process = None
        self.start_time = None
        self.stats = {
            'launches': 0,
            'crashes': 0,
            'uptime': 0,
            'restarts': 0
        }
        self.stats_file = self.root / "production_stats.json"
        self.load_stats()
    
    def load_stats(self):
        """Load production statistics"""
        if self.stats_file.exists():
            with open(self.stats_file) as f:
                self.stats.update(json.load(f))
    
    def save_stats(self):
        """Save production statistics"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def pre_flight_check(self):
        """Pre-flight system check"""
        logger.info("🔍 PRE-FLIGHT CHECK")
        
        checks = []
        
        # Check Python
        if Path(self.python).exists():
            checks.append(("Python", True))
        else:
            checks.append(("Python", False))
        
        # Check required files
        required = ['master_launcher.py', 'config.yaml', 'requirements.txt']
        for file in required:
            exists = (self.root / file).exists()
            checks.append((file, exists))
        
        # Check dependencies
        try:
            result = subprocess.run(
                [self.python, '-c', 'import PyQt6, yaml, psutil'],
                capture_output=True,
                timeout=5
            )
            checks.append(("Dependencies", result.returncode == 0))
        except:
            checks.append(("Dependencies", False))
        
        # Display results
        all_pass = True
        for name, status in checks:
            symbol = "✅" if status else "❌"
            logger.info(f"  {symbol} {name}")
            if not status:
                all_pass = False
        
        return all_pass
    
    def launch_production(self):
        """Launch in production mode"""
        logger.info("\n🚀 LAUNCHING PRODUCTION")
        
        # Pre-flight check
        if not self.pre_flight_check():
            logger.error("❌ Pre-flight check failed")
            return False
        
        # Launch master launcher
        try:
            self.process = subprocess.Popen(
                [self.python, str(self.root / "master_launcher.py")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.root)
            )
            
            self.start_time = datetime.now()
            self.stats['launches'] += 1
            self.save_stats()
            
            logger.info(f"✅ Production launched (PID: {self.process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Launch failed: {e}")
            return False
    
    def monitor_production(self):
        """Monitor production system"""
        logger.info("\n📊 PRODUCTION MONITORING")
        
        if not self.process:
            logger.error("❌ No process running")
            return
        
        try:
            while True:
                # Check if process is alive
                if self.process.poll() is not None:
                    logger.error("❌ Process crashed!")
                    self.stats['crashes'] += 1
                    self.save_stats()
                    
                    # Auto-restart
                    logger.info("🔄 Auto-restarting...")
                    self.stats['restarts'] += 1
                    self.save_stats()
                    self.launch_production()
                    continue
                
                # Get process info
                try:
                    proc = psutil.Process(self.process.pid)
                    cpu = proc.cpu_percent()
                    mem = proc.memory_info().rss / 1024 / 1024  # MB
                    
                    # Calculate uptime
                    uptime = (datetime.now() - self.start_time).total_seconds()
                    self.stats['uptime'] += 60
                    
                    logger.info(f"Status: ✅ Running | CPU: {cpu:.1f}% | Memory: {mem:.0f}MB | Uptime: {int(uptime/60)}m")
                    
                except psutil.NoSuchProcess:
                    logger.error("❌ Process not found")
                    break
                
                # Wait 60 seconds
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("\n⏸️  Monitoring stopped")
            self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("\n🛑 SHUTTING DOWN")
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
                logger.info("✅ Graceful shutdown complete")
            except:
                self.process.kill()
                logger.info("⚠️  Force killed")
        
        self.save_stats()
    
    def show_stats(self):
        """Show production statistics"""
        logger.info("\n📊 PRODUCTION STATISTICS")
        logger.info(f"Total Launches: {self.stats['launches']}")
        logger.info(f"Total Crashes: {self.stats['crashes']}")
        logger.info(f"Total Restarts: {self.stats['restarts']}")
        logger.info(f"Total Uptime: {self.stats['uptime']/3600:.1f}h")
        
        if self.stats['launches'] > 0:
            reliability = (1 - self.stats['crashes']/self.stats['launches']) * 100
            logger.info(f"Reliability: {reliability:.1f}%")


def main():
    """Main production deployment"""
    print("="*80)
    print("🎖️  MASTER LAUNCHER ULTIMATE - PRODUCTION DEPLOYMENT")
    print("Commander Bobby Don McWilliams II - Authority Level 11.0")
    print("="*80)
    
    deployment = ProductionDeployment()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "launch":
            deployment.launch_production()
            deployment.monitor_production()
        
        elif command == "stats":
            deployment.show_stats()
        
        elif command == "check":
            deployment.pre_flight_check()
        
        else:
            print("Commands: launch, stats, check")
    
    else:
        # Default: launch and monitor
        deployment.launch_production()
        deployment.monitor_production()


if __name__ == '__main__':
    main()
