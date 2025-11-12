#!/usr/bin/env python3
"""
PRODUCTION MONITORING DASHBOARD
Commander Bobby Don McWilliams II - Authority Level 11.0

Real-time production monitoring and alerting
"""

import sys
import time
import json
import psutil
from pathlib import Path
from datetime import datetime
from collections import deque

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


class ProductionMonitor:
    """Real-time production monitoring"""
    
    def __init__(self):
        self.history_size = 100
        self.cpu_history = deque(maxlen=self.history_size)
        self.mem_history = deque(maxlen=self.history_size)
        self.disk_history = deque(maxlen=self.history_size)
        self.net_history = deque(maxlen=self.history_size)
        
        self.alerts = []
        self.thresholds = {
            'cpu': 80,
            'memory': 85,
            'disk': 90,
            'network': 1000  # MB/s
        }
    
    def collect_metrics(self):
        """Collect system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'network': self.get_network_speed()
        }
        
        # Add to history
        self.cpu_history.append(metrics['cpu'])
        self.mem_history.append(metrics['memory'])
        self.disk_history.append(metrics['disk'])
        self.net_history.append(metrics['network'])
        
        # Check thresholds
        self.check_thresholds(metrics)
        
        return metrics
    
    def get_network_speed(self):
        """Get network speed in MB/s"""
        try:
            net1 = psutil.net_io_counters()
            time.sleep(1)
            net2 = psutil.net_io_counters()
            
            sent = (net2.bytes_sent - net1.bytes_sent) / 1024 / 1024
            recv = (net2.bytes_recv - net1.bytes_recv) / 1024 / 1024
            
            return sent + recv
        except:
            return 0
    
    def check_thresholds(self, metrics):
        """Check alert thresholds"""
        for key, threshold in self.thresholds.items():
            if metrics[key] > threshold:
                alert = {
                    'time': datetime.now().isoformat(),
                    'type': key,
                    'value': metrics[key],
                    'threshold': threshold,
                    'severity': 'critical' if metrics[key] > threshold * 1.1 else 'warning'
                }
                self.alerts.append(alert)
                
                # Keep only last 50 alerts
                if len(self.alerts) > 50:
                    self.alerts = self.alerts[-50:]
    
    def get_status_symbol(self, value, threshold):
        """Get status symbol"""
        if value > threshold * 1.1:
            return "🔴"
        elif value > threshold:
            return "🟡"
        else:
            return "🟢"
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        while True:
            try:
                # Collect metrics
                metrics = self.collect_metrics()
                
                # Clear screen
                print("\033[2J\033[H")
                
                # Header
                print("="*80)
                print("📊 MASTER LAUNCHER ULTIMATE - PRODUCTION DASHBOARD")
                print("Commander Bobby Don McWilliams II - Authority Level 11.0")
                print("="*80)
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                # CPU
                cpu_sym = self.get_status_symbol(metrics['cpu'], self.thresholds['cpu'])
                cpu_bar = self.get_bar(metrics['cpu'], 100)
                print(f"{cpu_sym} CPU:    {cpu_bar} {metrics['cpu']:6.2f}%")
                
                # Memory
                mem_sym = self.get_status_symbol(metrics['memory'], self.thresholds['memory'])
                mem_bar = self.get_bar(metrics['memory'], 100)
                print(f"{mem_sym} Memory: {mem_bar} {metrics['memory']:6.2f}%")
                
                # Disk
                disk_sym = self.get_status_symbol(metrics['disk'], self.thresholds['disk'])
                disk_bar = self.get_bar(metrics['disk'], 100)
                print(f"{disk_sym} Disk:   {disk_bar} {metrics['disk']:6.2f}%")
                
                # Network
                net_sym = self.get_status_symbol(metrics['network'], self.thresholds['network'])
                print(f"{net_sym} Network: {metrics['network']:6.2f} MB/s")
                
                print()
                
                # Process info
                print("PROCESSES:")
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        if 'python' in proc.info['name'].lower():
                            print(f"  PID {proc.info['pid']}: {proc.info['name']} - "
                                  f"CPU {proc.info['cpu_percent']:.1f}% - "
                                  f"MEM {proc.info['memory_percent']:.1f}%")
                    except:
                        pass
                
                print()
                
                # Recent alerts
                if self.alerts:
                    print("RECENT ALERTS:")
                    for alert in self.alerts[-5:]:
                        severity_sym = "🔴" if alert['severity'] == 'critical' else "🟡"
                        print(f"  {severity_sym} {alert['time']}: {alert['type'].upper()} "
                              f"at {alert['value']:.1f}% (threshold: {alert['threshold']}%)")
                
                print()
                print("Press Ctrl+C to exit")
                
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n\n✅ Dashboard closed")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(5)
    
    def get_bar(self, value, max_value):
        """Generate progress bar"""
        bar_length = 20
        filled = int((value / max_value) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        return bar


def main():
    """Main dashboard"""
    monitor = ProductionMonitor()
    monitor.display_dashboard()


if __name__ == '__main__':
    main()
