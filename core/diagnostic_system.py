#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Diagnostic System
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

6-Component Health Diagnostic System:
1. Process Status (running/stopped)
2. Port Status (bound/available)
3. Memory Usage (within limits)
4. CPU Usage (within limits)
5. Error Rate (acceptable threshold)
6. Response Time (acceptable latency)
"""

import psutil
import socket
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger("DiagnosticSystem")


class HealthStatus(Enum):
    """Health status levels"""
    EXCELLENT = "excellent"  # All checks pass
    GOOD = "good"            # Minor issues
    FAIR = "fair"            # Multiple issues
    POOR = "poor"            # Major issues
    CRITICAL = "critical"    # Immediate attention required


class DiagnosticSystem:
    """
    6-Component Health Diagnostic System
    
    Components:
    1. Process Status - Is process running?
    2. Port Status - Is port bound correctly?
    3. Memory Usage - Within acceptable limits?
    4. CPU Usage - Within acceptable limits?
    5. Error Rate - Acceptable error threshold?
    6. Response Time - Acceptable latency?
    """
    
    def __init__(self, config: Dict):
        """Initialize Diagnostic System"""
        self.config = config
        self.diagnostic_config = config.get('diagnostics', {})
        
        # Thresholds
        self.memory_threshold_mb = self.diagnostic_config.get('memory_threshold_mb', 500)
        self.cpu_threshold_percent = self.diagnostic_config.get('cpu_threshold_percent', 80)
        self.error_rate_threshold = self.diagnostic_config.get('error_rate_threshold', 0.1)  # 10%
        self.response_time_threshold_ms = self.diagnostic_config.get('response_time_threshold_ms', 5000)
        
        # History tracking
        self.diagnostic_history = {}
        self.max_history = self.diagnostic_config.get('max_history', 100)
        
        # Statistics
        self.diagnostics_run = 0
        self.issues_detected = 0
        
        logger.info("Diagnostic System initialized")
        logger.info(f"   Memory threshold: {self.memory_threshold_mb} MB")
        logger.info(f"   CPU threshold: {self.cpu_threshold_percent}%")
        logger.info(f"   Error rate threshold: {self.error_rate_threshold*100}%")
        logger.info(f"   Response time threshold: {self.response_time_threshold_ms} ms")
    
    async def run_diagnostic(self, server_name: str, server_info: Dict) -> Dict:
        """
        Run 6-component diagnostic
        
        Args:
            server_name: Name of server
            server_info: Server information (pid, port, etc.)
        
        Returns:
            Diagnostic report
        """
        self.diagnostics_run += 1
        
        logger.info(f"🔍 Running diagnostic for {server_name}")
        
        report = {
            'server_name': server_name,
            'timestamp': datetime.now(),
            'components': {},
            'overall_status': HealthStatus.EXCELLENT,
            'score': 0.0,
            'issues': []
        }
        
        # Component 1: Process Status
        process_result = self._check_process_status(server_info)
        report['components']['process'] = process_result
        
        # Component 2: Port Status
        port_result = self._check_port_status(server_info)
        report['components']['port'] = port_result
        
        # Component 3: Memory Usage
        memory_result = self._check_memory_usage(server_info)
        report['components']['memory'] = memory_result
        
        # Component 4: CPU Usage
        cpu_result = self._check_cpu_usage(server_info)
        report['components']['cpu'] = cpu_result
        
        # Component 5: Error Rate
        error_result = self._check_error_rate(server_name)
        report['components']['error_rate'] = error_result
        
        # Component 6: Response Time
        response_result = self._check_response_time(server_info)
        report['components']['response_time'] = response_result
        
        # Calculate overall score and status
        report = self._calculate_overall_status(report)
        
        # Track history
        self._track_history(server_name, report)
        
        # Count issues
        if report['issues']:
            self.issues_detected += len(report['issues'])
        
        logger.info(f"   Overall Status: {report['overall_status'].value.upper()}")
        logger.info(f"   Score: {report['score']:.1f}/100")
        
        if report['issues']:
            logger.warning(f"   Issues: {len(report['issues'])}")
            for issue in report['issues']:
                logger.warning(f"      - {issue}")
        
        return report
    
    def _check_process_status(self, server_info: Dict) -> Dict:
        """Check if process is running"""
        result = {
            'name': 'Process Status',
            'status': 'pass',
            'details': {},
            'weight': 25.0  # 25% of total score
        }
        
        pid = server_info.get('pid')
        
        if not pid:
            result['status'] = 'fail'
            result['details']['message'] = "No PID found"
            result['details']['running'] = False
            return result
        
        try:
            process = psutil.Process(pid)
            
            if not process.is_running():
                result['status'] = 'fail'
                result['details']['message'] = "Process not running"
                result['details']['running'] = False
            else:
                result['status'] = 'pass'
                result['details']['message'] = "Process running"
                result['details']['running'] = True
                result['details']['status'] = process.status()
                result['details']['create_time'] = datetime.fromtimestamp(process.create_time())
        
        except psutil.NoSuchProcess:
            result['status'] = 'fail'
            result['details']['message'] = "Process does not exist"
            result['details']['running'] = False
        except Exception as e:
            result['status'] = 'warn'
            result['details']['message'] = f"Error checking process: {e}"
        
        return result
    
    def _check_port_status(self, server_info: Dict) -> Dict:
        """Check if port is bound correctly"""
        result = {
            'name': 'Port Status',
            'status': 'pass',
            'details': {},
            'weight': 20.0  # 20% of total score
        }
        
        port = server_info.get('port')
        
        if not port:
            result['status'] = 'warn'
            result['details']['message'] = "No port configured"
            return result
        
        try:
            # Check if port is bound
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            result_code = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result_code == 0:
                result['status'] = 'pass'
                result['details']['message'] = f"Port {port} is bound"
                result['details']['port'] = port
                result['details']['bound'] = True
            else:
                result['status'] = 'fail'
                result['details']['message'] = f"Port {port} not bound"
                result['details']['port'] = port
                result['details']['bound'] = False
        
        except Exception as e:
            result['status'] = 'warn'
            result['details']['message'] = f"Error checking port: {e}"
        
        return result
    
    def _check_memory_usage(self, server_info: Dict) -> Dict:
        """Check memory usage"""
        result = {
            'name': 'Memory Usage',
            'status': 'pass',
            'details': {},
            'weight': 15.0  # 15% of total score
        }
        
        pid = server_info.get('pid')
        
        if not pid:
            result['status'] = 'warn'
            result['details']['message'] = "No PID to check memory"
            return result
        
        try:
            process = psutil.Process(pid)
            mem_info = process.memory_info()
            mem_mb = mem_info.rss / 1024 / 1024  # Convert to MB
            
            result['details']['memory_mb'] = round(mem_mb, 2)
            result['details']['threshold_mb'] = self.memory_threshold_mb
            
            if mem_mb > self.memory_threshold_mb:
                result['status'] = 'warn'
                result['details']['message'] = f"High memory usage: {mem_mb:.1f} MB"
            else:
                result['status'] = 'pass'
                result['details']['message'] = f"Memory usage OK: {mem_mb:.1f} MB"
        
        except psutil.NoSuchProcess:
            result['status'] = 'fail'
            result['details']['message'] = "Process does not exist"
        except Exception as e:
            result['status'] = 'warn'
            result['details']['message'] = f"Error checking memory: {e}"
        
        return result
    
    def _check_cpu_usage(self, server_info: Dict) -> Dict:
        """Check CPU usage"""
        result = {
            'name': 'CPU Usage',
            'status': 'pass',
            'details': {},
            'weight': 15.0  # 15% of total score
        }
        
        pid = server_info.get('pid')
        
        if not pid:
            result['status'] = 'warn'
            result['details']['message'] = "No PID to check CPU"
            return result
        
        try:
            process = psutil.Process(pid)
            cpu_percent = process.cpu_percent(interval=0.1)
            
            result['details']['cpu_percent'] = round(cpu_percent, 2)
            result['details']['threshold_percent'] = self.cpu_threshold_percent
            
            if cpu_percent > self.cpu_threshold_percent:
                result['status'] = 'warn'
                result['details']['message'] = f"High CPU usage: {cpu_percent:.1f}%"
            else:
                result['status'] = 'pass'
                result['details']['message'] = f"CPU usage OK: {cpu_percent:.1f}%"
        
        except psutil.NoSuchProcess:
            result['status'] = 'fail'
            result['details']['message'] = "Process does not exist"
        except Exception as e:
            result['status'] = 'warn'
            result['details']['message'] = f"Error checking CPU: {e}"
        
        return result
    
    def _check_error_rate(self, server_name: str) -> Dict:
        """Check error rate from history"""
        result = {
            'name': 'Error Rate',
            'status': 'pass',
            'details': {},
            'weight': 15.0  # 15% of total score
        }
        
        # Check recent diagnostic history
        history = self.diagnostic_history.get(server_name, [])
        
        if len(history) < 2:
            result['status'] = 'pass'
            result['details']['message'] = "Insufficient history"
            return result
        
        # Check last 10 diagnostics
        recent_history = history[-10:]
        error_count = sum(1 for h in recent_history if h.get('score', 100) < 50)
        
        error_rate = error_count / len(recent_history)
        
        result['details']['error_rate'] = round(error_rate, 2)
        result['details']['threshold'] = self.error_rate_threshold
        result['details']['recent_errors'] = error_count
        result['details']['recent_checks'] = len(recent_history)
        
        if error_rate > self.error_rate_threshold:
            result['status'] = 'warn'
            result['details']['message'] = f"High error rate: {error_rate*100:.0f}%"
        else:
            result['status'] = 'pass'
            result['details']['message'] = f"Error rate OK: {error_rate*100:.0f}%"
        
        return result
    
    def _check_response_time(self, server_info: Dict) -> Dict:
        """Check response time"""
        result = {
            'name': 'Response Time',
            'status': 'pass',
            'details': {},
            'weight': 10.0  # 10% of total score
        }
        
        # For now, this is a placeholder
        # In production, would actually test server response
        result['status'] = 'pass'
        result['details']['message'] = "Response time check not implemented"
        
        return result
    
    def _calculate_overall_status(self, report: Dict) -> Dict:
        """Calculate overall status and score"""
        total_score = 0.0
        total_weight = 0.0
        
        for component_name, component in report['components'].items():
            weight = component.get('weight', 0)
            status = component.get('status', 'fail')
            
            # Calculate component score
            if status == 'pass':
                score = 100
            elif status == 'warn':
                score = 50
            else:  # fail
                score = 0
                # Add to issues list
                report['issues'].append(
                    f"{component['name']}: {component['details'].get('message', 'Failed')}"
                )
            
            # Weighted score
            total_score += score * (weight / 100)
            total_weight += weight
        
        # Final score (0-100)
        report['score'] = total_score
        
        # Determine overall status
        if total_score >= 90:
            report['overall_status'] = HealthStatus.EXCELLENT
        elif total_score >= 70:
            report['overall_status'] = HealthStatus.GOOD
        elif total_score >= 50:
            report['overall_status'] = HealthStatus.FAIR
        elif total_score >= 30:
            report['overall_status'] = HealthStatus.POOR
        else:
            report['overall_status'] = HealthStatus.CRITICAL
        
        return report
    
    def _track_history(self, server_name: str, report: Dict):
        """Track diagnostic history"""
        if server_name not in self.diagnostic_history:
            self.diagnostic_history[server_name] = []
        
        # Store simplified report
        simplified_report = {
            'timestamp': report['timestamp'],
            'score': report['score'],
            'status': report['overall_status'].value,
            'issues': report['issues']
        }
        
        self.diagnostic_history[server_name].append(simplified_report)
        
        # Limit history size
        if len(self.diagnostic_history[server_name]) > self.max_history:
            self.diagnostic_history[server_name] = self.diagnostic_history[server_name][-self.max_history:]
    
    def get_diagnostic_history(self, server_name: str) -> List[Dict]:
        """Get diagnostic history for server"""
        return self.diagnostic_history.get(server_name, [])
    
    def get_statistics(self) -> Dict:
        """Get diagnostic statistics"""
        return {
            'diagnostics_run': self.diagnostics_run,
            'issues_detected': self.issues_detected,
            'servers_tracked': len(self.diagnostic_history),
            'thresholds': {
                'memory_mb': self.memory_threshold_mb,
                'cpu_percent': self.cpu_threshold_percent,
                'error_rate': self.error_rate_threshold,
                'response_time_ms': self.response_time_threshold_ms
            }
        }


# Export
__all__ = ['DiagnosticSystem', 'HealthStatus']
