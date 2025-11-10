#!/usr/bin/env python3
"""
PROMETHEUS PRIME INTEGRATION - Real Scanning Integration
Authority: 11.0 | Commander Bobby Don McWilliams II
Replaces mock data with real nmap/SMB/vulnerability scans
"""

import asyncio
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

# Import Prometheus modules
from prometheus_nmap_scanner import PrometheusNmapScanner, ScanType
from prometheus_smb_analyzer import PrometheusSMBAnalyzer
from prometheus_vulnerability_scanner import PrometheusVulnerabilityScanner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PrometheusIntegration")

@dataclass
class ComprehensiveScanResult:
    """Complete scan result from all modules"""
    success: bool
    target: str
    timestamp: str
    
    # Port scan results
    ports_open: List[Dict[str, Any]]
    total_ports: int
    
    # SMB analysis
    smb_shares: List[Dict[str, Any]]
    smb_vulnerabilities: List[str]
    administrative_shares_exposed: bool
    
    # Vulnerability assessment
    vulnerabilities: List[Dict[str, Any]]
    critical_vulns: int
    high_vulns: int
    risk_score: float
    
    # Overall assessment
    threat_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    attack_vectors: List[str]
    recommendations: List[str]
    
    # Timing
    scan_duration: float
    
    error: str = ""

class PrometheusIntegration:
    """Integrate all Prometheus scanners for comprehensive security assessment"""
    
    def __init__(self):
        """Initialize all scanners"""
        self.logger = logger
        self.logger.info("🔱 PROMETHEUS PRIME INTEGRATION - Authority 11.0")
        
        # Initialize scanners
        self.nmap_scanner = PrometheusNmapScanner()
        self.smb_analyzer = PrometheusSMBAnalyzer()
        self.vuln_scanner = PrometheusVulnerabilityScanner()
        
        self.logger.info("✅ All scanners initialized")
    
    async def comprehensive_scan(
        self,
        target: str,
        scan_smb: bool = True,
        scan_vulnerabilities: bool = True,
        timeout: int = 600
    ) -> ComprehensiveScanResult:
        """
        Perform comprehensive security scan
        
        Args:
            target: IP address or hostname
            scan_smb: Include SMB analysis
            scan_vulnerabilities: Include vulnerability assessment
            timeout: Total scan timeout
            
        Returns:
            ComprehensiveScanResult with complete assessment
        """
        start_time = datetime.now()
        self.logger.info(f"🎯 COMPREHENSIVE SCAN: {target}")
        
        try:
            # PHASE 1: Port scanning with nmap
            self.logger.info("PHASE 1: Port scanning...")
            nmap_result = await self.nmap_scanner.scan_target(
                target,
                ScanType.FAST  # Top 1000 ports
            )
            
            if not nmap_result.success:
                return self._create_error_result(
                    target, start_time, f"Port scan failed: {nmap_result.error}"
                )
            
            self.logger.info(f"✅ Found {nmap_result.total_ports} open ports")
            
            # PHASE 2: SMB analysis (if enabled and port 445 open)
            smb_shares = []
            smb_vulns = []
            admin_shares_exposed = False
            
            if scan_smb:
                port_445_open = any(p["port"] == 445 for p in nmap_result.ports_found)
                
                if port_445_open:
                    self.logger.info("PHASE 2: SMB analysis...")
                    smb_result = await self.smb_analyzer.analyze_target(target)
                    
                    if smb_result.success:
                        smb_shares = [asdict(s) for s in smb_result.shares_found]
                        admin_shares_exposed = len(smb_result.administrative_shares) > 0
                        
                        self.logger.info(f"✅ Found {len(smb_shares)} SMB shares")
                        
                        if admin_shares_exposed:
                            self.logger.warning(f"⚠️ CRITICAL: Administrative shares exposed!")
            
            # PHASE 3: Vulnerability assessment
            vulnerabilities = []
            critical_count = 0
            high_count = 0
            risk_score = 0.0
            
            if scan_vulnerabilities:
                self.logger.info("PHASE 3: Vulnerability assessment...")
                
                # Build services dict from nmap results
                services = {
                    str(p["port"]): p["service"]
                    for p in nmap_result.ports_found
                }
                
                vuln_result = await self.vuln_scanner.scan_target(target, services)
                
                if vuln_result.success:
                    vulnerabilities = [asdict(v) for v in vuln_result.vulnerabilities_found]
                    critical_count = vuln_result.critical_count
                    high_count = vuln_result.high_count
                    risk_score = vuln_result.risk_score
                    
                    self.logger.info(f"✅ Found {len(vulnerabilities)} vulnerabilities")
                    self.logger.info(f"   🔴 Critical: {critical_count}")
                    self.logger.info(f"   🟠 High: {high_count}")
            
            # PHASE 4: Threat assessment and recommendations
            threat_level = self._assess_threat_level(
                nmap_result.total_ports,
                admin_shares_exposed,
                critical_count,
                high_count,
                risk_score
            )
            
            attack_vectors = self._identify_attack_vectors(
                nmap_result.ports_found,
                smb_shares,
                vulnerabilities
            )
            
            recommendations = self._generate_recommendations(
                threat_level,
                attack_vectors,
                admin_shares_exposed,
                critical_count
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"✅ COMPREHENSIVE SCAN COMPLETE")
            self.logger.info(f"   Threat Level: {threat_level}")
            self.logger.info(f"   Risk Score: {risk_score}/100")
            self.logger.info(f"   Duration: {duration:.2f}s")
            
            return ComprehensiveScanResult(
                success=True,
                target=target,
                timestamp=start_time.isoformat(),
                ports_open=nmap_result.ports_found,
                total_ports=nmap_result.total_ports,
                smb_shares=smb_shares,
                smb_vulnerabilities=smb_vulns,
                administrative_shares_exposed=admin_shares_exposed,
                vulnerabilities=vulnerabilities,
                critical_vulns=critical_count,
                high_vulns=high_count,
                risk_score=risk_score,
                threat_level=threat_level,
                attack_vectors=attack_vectors,
                recommendations=recommendations,
                scan_duration=duration
            )
            
        except Exception as e:
            self.logger.error(f"❌ Comprehensive scan error: {e}")
            return self._create_error_result(target, start_time, str(e))
    
    def _assess_threat_level(
        self,
        open_ports: int,
        admin_shares: bool,
        critical_vulns: int,
        high_vulns: int,
        risk_score: float
    ) -> str:
        """Assess overall threat level"""
        
        # CRITICAL conditions
        if admin_shares:
            return "CRITICAL"
        
        if critical_vulns > 0:
            return "CRITICAL"
        
        if risk_score >= 75:
            return "CRITICAL"
        
        # HIGH conditions
        if high_vulns >= 2:
            return "HIGH"
        
        if risk_score >= 50:
            return "HIGH"
        
        if open_ports >= 10:
            return "HIGH"
        
        # MEDIUM conditions
        if high_vulns > 0:
            return "MEDIUM"
        
        if open_ports >= 5:
            return "MEDIUM"
        
        # LOW
        return "LOW"
    
    def _identify_attack_vectors(
        self,
        ports: List[Dict[str, Any]],
        smb_shares: List[Dict[str, Any]],
        vulns: List[Dict[str, Any]]
    ) -> List[str]:
        """Identify potential attack vectors"""
        vectors = []
        
        # Port-based vectors
        port_map = {p["port"]: p["service"] for p in ports}
        
        if 445 in port_map:
            vectors.append("SMB file sharing (port 445) - Direct file access")
        
        if 5985 in port_map or 47001 in port_map:
            vectors.append("WinRM (port 5985/47001) - Remote PowerShell execution")
        
        if 135 in port_map:
            vectors.append("RPC (port 135) - Lateral movement enabler")
        
        if 3389 in port_map:
            vectors.append("RDP (port 3389) - Remote desktop access")
        
        # SMB-based vectors
        if smb_shares:
            if any(s.get("name") in ["C$", "P$", "D$", "ADMIN$"] for s in smb_shares):
                vectors.append("Administrative shares exposed - Full drive access")
            
            if any(s.get("anonymous_access") for s in smb_shares):
                vectors.append("Anonymous SMB access - No authentication required")
        
        # Vulnerability-based vectors
        if any("EternalBlue" in v.get("title", "") for v in vulns):
            vectors.append("EternalBlue exploit - Critical RCE")
        
        if any("PrintNightmare" in v.get("title", "") for v in vulns):
            vectors.append("PrintNightmare exploit - Print Spooler RCE")
        
        return vectors
    
    def _generate_recommendations(
        self,
        threat_level: str,
        attack_vectors: List[str],
        admin_shares: bool,
        critical_vulns: int
    ) -> List[str]:
        """Generate security recommendations"""
        recs = []
        
        if threat_level == "CRITICAL":
            recs.append("🚨 IMMEDIATE ACTION REQUIRED - Critical vulnerabilities detected")
        
        if admin_shares:
            recs.append("🔴 PRIORITY 1: Disable administrative shares (C$, P$, ADMIN$)")
            recs.append("   Command: net share C$ /delete")
        
        if critical_vulns > 0:
            recs.append("🔴 PRIORITY 1: Apply security patches for critical CVEs")
            recs.append("   Run Windows Update immediately")
        
        if "SMB" in str(attack_vectors):
            recs.append("🟠 PRIORITY 2: Restrict SMB access to internal network only")
            recs.append("   Configure firewall rules for port 445")
        
        if "WinRM" in str(attack_vectors):
            recs.append("🟠 PRIORITY 2: Disable WinRM if not required")
            recs.append("   Command: Stop-Service WinRM; Set-Service WinRM -StartupType Disabled")
        
        recs.append("🟡 PRIORITY 3: Enable Windows Firewall with strict rules")
        recs.append("🟡 PRIORITY 3: Implement network segmentation (VLAN)")
        recs.append("🟢 ONGOING: Regular security audits and monitoring")
        
        return recs
    
    def _create_error_result(
        self,
        target: str,
        start_time: datetime,
        error: str
    ) -> ComprehensiveScanResult:
        """Create error result"""
        return ComprehensiveScanResult(
            success=False,
            target=target,
            timestamp=start_time.isoformat(),
            ports_open=[],
            total_ports=0,
            smb_shares=[],
            smb_vulnerabilities=[],
            administrative_shares_exposed=False,
            vulnerabilities=[],
            critical_vulns=0,
            high_vulns=0,
            risk_score=0.0,
            threat_level="UNKNOWN",
            attack_vectors=[],
            recommendations=[],
            scan_duration=0.0,
            error=error
        )
    
    async def quick_security_assessment(self, target: str) -> Dict[str, Any]:
        """Quick security assessment (fast scan only)"""
        result = await self.comprehensive_scan(
            target,
            scan_smb=False,
            scan_vulnerabilities=False,
            timeout=60
        )
        
        return {
            "target": result.target,
            "threat_level": result.threat_level,
            "open_ports": result.total_ports,
            "duration": result.scan_duration
        }

# ============================================================================
# CLI TEST INTERFACE
# ============================================================================

async def test_integration():
    """Test comprehensive scanning"""
    integration = PrometheusIntegration()
    
    print("🔱 PROMETHEUS PRIME INTEGRATION - TESTING")
    print("="*60)
    
    # Test: Comprehensive scan of localhost
    print("\n[TEST] Comprehensive scan...")
    result = await integration.comprehensive_scan("127.0.0.1")
    
    print(f"\nSuccess: {result.success}")
    print(f"Target: {result.target}")
    print(f"Duration: {result.scan_duration:.2f}s")
    print(f"\n🎯 THREAT ASSESSMENT:")
    print(f"  Threat Level: {result.threat_level}")
    print(f"  Risk Score: {result.risk_score}/100")
    print(f"  Open Ports: {result.total_ports}")
    print(f"  Critical Vulnerabilities: {result.critical_vulns}")
    print(f"  High Vulnerabilities: {result.high_vulns}")
    print(f"  Admin Shares Exposed: {result.administrative_shares_exposed}")
    
    if result.attack_vectors:
        print(f"\n🚨 ATTACK VECTORS:")
        for vector in result.attack_vectors:
            print(f"  - {vector}")
    
    if result.recommendations:
        print(f"\n🛡️ RECOMMENDATIONS:")
        for rec in result.recommendations[:5]:
            print(f"  {rec}")
    
    print("\n✅ TESTING COMPLETE")

if __name__ == "__main__":
    asyncio.run(test_integration())
