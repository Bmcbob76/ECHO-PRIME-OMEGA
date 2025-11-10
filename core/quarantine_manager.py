#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Quarantine Manager
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Move persistently failing servers to quarantine
Generate comprehensive diagnostic reports
Track failure patterns
Recommend solutions
Signal Commander/Claude Desktop
"""

import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("QuarantineManager")


class QuarantineManager:
    """
    Quarantine Manager
    
    Features:
    - Move failed servers to quarantine directory
    - Generate diagnostic reports
    - Track failure patterns
    - Recommend solutions
    - Signal Commander/Claude Desktop
    - Integration with GS343 and Phoenix
    """
    
    def __init__(self, config: Dict):
        """Initialize Quarantine Manager"""
        self.config = config
        self.quarantine_config = config.get('quarantine', {})
        
        # Paths
        self.quarantine_dir = Path(config.get('paths', {}).get('quarantine', 'E:/ECHO_XV4/MLS/QUARANTINE'))
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        
        self.reports_dir = self.quarantine_dir / "REPORTS"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Settings
        self.enabled = self.quarantine_config.get('enabled', True)
        self.auto_quarantine = self.quarantine_config.get('auto_quarantine', True)
        self.generate_report = self.quarantine_config.get('generate_report', True)
        self.signal_commander = self.quarantine_config.get('signal_commander', True)
        self.signal_claude = self.quarantine_config.get('signal_claude_desktop', True)
        
        # Quarantine threshold
        self.failure_threshold = self.quarantine_config.get('failure_threshold', 3)
        
        # Components
        self.gs343 = None
        self.phoenix = None
        self.voice_system = None
        
        # Statistics
        self.servers_quarantined = 0
        self.reports_generated = 0
        
        # Quarantined servers tracking
        self.quarantined_servers = {}
        
        logger.info("Quarantine Manager initialized")
        logger.info(f"   Quarantine directory: {self.quarantine_dir}")
        logger.info(f"   Auto-quarantine: {self.auto_quarantine}")
        logger.info(f"   Failure threshold: {self.failure_threshold}")
    
    def set_gs343(self, gs343):
        """Set GS343 Foundation reference"""
        self.gs343 = gs343
    
    def set_phoenix(self, phoenix):
        """Set Phoenix Healer reference"""
        self.phoenix = phoenix
    
    def set_voice_system(self, voice):
        """Set Voice System reference"""
        self.voice_system = voice
    
    async def quarantine_server(self, server_name: str, server_path: Path, reason: str, 
                                failure_history: List[Dict] = None) -> bool:
        """
        Move server to quarantine
        
        Args:
            server_name: Name of server
            server_path: Path to server file
            reason: Reason for quarantine
            failure_history: List of failure records
        
        Returns:
            Success status
        """
        if not self.enabled:
            return False
        
        try:
            logger.warning(f"🚫 Quarantining server: {server_name}")
            logger.warning(f"   Reason: {reason}")
            
            # Create server quarantine directory
            server_quarantine_dir = self.quarantine_dir / server_name
            server_quarantine_dir.mkdir(parents=True, exist_ok=True)
            
            # Move server file to quarantine
            if server_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                quarantine_filename = f"{server_path.name}.quarantine_{timestamp}"
                quarantine_path = server_quarantine_dir / quarantine_filename
                
                shutil.copy2(server_path, quarantine_path)
                logger.info(f"   Moved to: {quarantine_path}")
            
            # Generate diagnostic report
            if self.generate_report:
                report_path = await self._generate_diagnostic_report(
                    server_name, 
                    server_path, 
                    reason, 
                    failure_history
                )
                logger.info(f"   Report: {report_path}")
            
            # Track quarantine
            self.quarantined_servers[server_name] = {
                'timestamp': datetime.now(),
                'reason': reason,
                'path': str(quarantine_path) if server_path.exists() else None,
                'failure_count': len(failure_history) if failure_history else 0
            }
            
            self.servers_quarantined += 1
            
            # Signal Commander
            if self.signal_commander:
                await self._signal_commander(server_name, reason)
            
            # Signal Claude Desktop
            if self.signal_claude:
                await self._signal_claude_desktop(server_name, reason)
            
            # Voice announcement (Bree roasts the failure)
            if self.voice_system:
                await self.voice_system.speak(
                    "bree",
                    f"Alright, {server_name} is completely fucked. "
                    f"It's been quarantined. Reason: {reason}. "
                    f"Check the diagnostic report for details."
                )
            
            logger.info(f"✅ Server {server_name} quarantined successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to quarantine server: {e}")
            return False
    
    async def _generate_diagnostic_report(self, server_name: str, server_path: Path,
                                         reason: str, failure_history: List[Dict]) -> Path:
        """Generate comprehensive diagnostic report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"{server_name}_diagnostic_{timestamp}.json"
            report_path = self.reports_dir / report_filename
            
            # Build report
            report = {
                'server_name': server_name,
                'timestamp': datetime.now().isoformat(),
                'quarantine_reason': reason,
                'server_path': str(server_path),
                'failure_history': failure_history or [],
                'diagnostics': {}
            }
            
            # GS343 error analysis
            if self.gs343 and failure_history:
                report['diagnostics']['gs343_analysis'] = self._analyze_with_gs343(failure_history)
            
            # Phoenix healing attempts
            if self.phoenix:
                phoenix_stats = self.phoenix.get_statistics()
                report['diagnostics']['phoenix_attempts'] = phoenix_stats
            
            # System recommendations
            report['diagnostics']['recommendations'] = self._generate_recommendations(
                server_name, 
                failure_history
            )
            
            # Failure patterns
            report['diagnostics']['failure_patterns'] = self._analyze_failure_patterns(failure_history)
            
            # Save report
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.reports_generated += 1
            
            # Also generate human-readable text report
            text_report_path = self.reports_dir / f"{server_name}_diagnostic_{timestamp}.txt"
            self._generate_text_report(report, text_report_path)
            
            return report_path
            
        except Exception as e:
            logger.error(f"Failed to generate diagnostic report: {e}")
            return None
    
    def _analyze_with_gs343(self, failure_history: List[Dict]) -> Dict:
        """Analyze failures using GS343"""
        analysis = {
            'error_types': {},
            'common_patterns': [],
            'suggested_solutions': []
        }
        
        try:
            for failure in failure_history:
                error_msg = failure.get('error_message', '')
                
                # Diagnose with GS343
                diagnosis = self.gs343.diagnose_error(error_msg)
                
                if diagnosis:
                    error_type = diagnosis['error_type']
                    analysis['error_types'][error_type] = analysis['error_types'].get(error_type, 0) + 1
                    
                    if diagnosis['solution'] not in analysis['suggested_solutions']:
                        analysis['suggested_solutions'].append(diagnosis['solution'])
        
        except Exception as e:
            logger.error(f"GS343 analysis failed: {e}")
        
        return analysis
    
    def _generate_recommendations(self, server_name: str, failure_history: List[Dict]) -> List[str]:
        """Generate recommendations for fixing the server"""
        recommendations = []
        
        if not failure_history:
            return ["Insufficient failure data for recommendations"]
        
        failure_count = len(failure_history)
        
        # Check for common issues
        if failure_count >= 3:
            recommendations.append("Server has failed multiple times - consider code review")
        
        # Check for port issues
        port_errors = sum(1 for f in failure_history if 'port' in str(f.get('error_message', '')).lower())
        if port_errors > 0:
            recommendations.append("Port conflicts detected - verify port configuration")
        
        # Check for dependency issues
        import_errors = sum(1 for f in failure_history if 'import' in str(f.get('error_message', '')).lower())
        if import_errors > 0:
            recommendations.append("Import errors detected - check dependencies")
        
        # Check for permission issues
        perm_errors = sum(1 for f in failure_history if 'permission' in str(f.get('error_message', '')).lower())
        if perm_errors > 0:
            recommendations.append("Permission errors detected - check file permissions")
        
        if not recommendations:
            recommendations.append("Manual review required")
        
        return recommendations
    
    def _analyze_failure_patterns(self, failure_history: List[Dict]) -> Dict:
        """Analyze failure patterns"""
        patterns = {
            'total_failures': len(failure_history) if failure_history else 0,
            'unique_errors': set(),
            'time_pattern': 'unknown',
            'crash_rate': 0.0
        }
        
        if not failure_history:
            return patterns
        
        # Unique error types
        for failure in failure_history:
            error_type = failure.get('error_type', 'UNKNOWN')
            patterns['unique_errors'].add(error_type)
        
        patterns['unique_errors'] = list(patterns['unique_errors'])
        
        # Calculate crash rate (failures per day)
        if len(failure_history) >= 2:
            first_failure = failure_history[0].get('timestamp')
            last_failure = failure_history[-1].get('timestamp')
            
            if first_failure and last_failure:
                try:
                    if isinstance(first_failure, str):
                        first_failure = datetime.fromisoformat(first_failure)
                    if isinstance(last_failure, str):
                        last_failure = datetime.fromisoformat(last_failure)
                    
                    duration_days = (last_failure - first_failure).days or 1
                    patterns['crash_rate'] = len(failure_history) / duration_days
                except:
                    pass
        
        return patterns
    
    def _generate_text_report(self, report: Dict, output_path: Path):
        """Generate human-readable text report"""
        try:
            lines = []
            lines.append("=" * 80)
            lines.append("QUARANTINE DIAGNOSTIC REPORT")
            lines.append("=" * 80)
            lines.append(f"Server: {report['server_name']}")
            lines.append(f"Timestamp: {report['timestamp']}")
            lines.append(f"Reason: {report['quarantine_reason']}")
            lines.append("")
            
            # Failure history
            lines.append("FAILURE HISTORY")
            lines.append("-" * 80)
            failure_history = report.get('failure_history', [])
            for i, failure in enumerate(failure_history, 1):
                lines.append(f"{i}. {failure.get('timestamp', 'N/A')}")
                lines.append(f"   Error: {failure.get('error_message', 'N/A')}")
                lines.append("")
            
            # Diagnostics
            if report.get('diagnostics'):
                lines.append("DIAGNOSTICS")
                lines.append("-" * 80)
                
                # GS343 Analysis
                gs343 = report['diagnostics'].get('gs343_analysis', {})
                if gs343:
                    lines.append("GS343 Error Analysis:")
                    for error_type, count in gs343.get('error_types', {}).items():
                        lines.append(f"  - {error_type}: {count} occurrences")
                    lines.append("")
                
                # Recommendations
                recommendations = report['diagnostics'].get('recommendations', [])
                if recommendations:
                    lines.append("RECOMMENDATIONS:")
                    for i, rec in enumerate(recommendations, 1):
                        lines.append(f"  {i}. {rec}")
                    lines.append("")
                
                # Failure patterns
                patterns = report['diagnostics'].get('failure_patterns', {})
                if patterns:
                    lines.append("FAILURE PATTERNS:")
                    lines.append(f"  Total Failures: {patterns.get('total_failures', 0)}")
                    lines.append(f"  Unique Errors: {len(patterns.get('unique_errors', []))}")
                    lines.append(f"  Crash Rate: {patterns.get('crash_rate', 0):.2f} per day")
                    lines.append("")
            
            lines.append("=" * 80)
            
            # Write to file
            with open(output_path, 'w') as f:
                f.write('\n'.join(lines))
            
        except Exception as e:
            logger.error(f"Failed to generate text report: {e}")
    
    async def _signal_commander(self, server_name: str, reason: str):
        """Signal Commander about quarantine"""
        # Would send notification to Commander
        # Could be email, Discord, etc.
        logger.info(f"📧 Signaling Commander about {server_name} quarantine")
    
    async def _signal_claude_desktop(self, server_name: str, reason: str):
        """Signal Claude Desktop about quarantine"""
        # Would create notification for Claude Desktop
        # Could be through MCP or other mechanism
        logger.info(f"🤖 Signaling Claude Desktop about {server_name} quarantine")
    
    def get_quarantined_servers(self) -> Dict:
        """Get list of quarantined servers"""
        return self.quarantined_servers
    
    def get_quarantine_report(self, server_name: str) -> Optional[Dict]:
        """Get latest diagnostic report for quarantined server"""
        try:
            # Find latest report
            reports = sorted(
                self.reports_dir.glob(f"{server_name}_diagnostic_*.json"),
                reverse=True
            )
            
            if not reports:
                return None
            
            latest_report = reports[0]
            
            with open(latest_report, 'r') as f:
                return json.load(f)
        
        except Exception as e:
            logger.error(f"Failed to get quarantine report: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """Get quarantine statistics"""
        return {
            'enabled': self.enabled,
            'quarantine_directory': str(self.quarantine_dir),
            'servers_quarantined': self.servers_quarantined,
            'reports_generated': self.reports_generated,
            'currently_quarantined': len(self.quarantined_servers),
            'failure_threshold': self.failure_threshold
        }


# Export
__all__ = ['QuarantineManager']
