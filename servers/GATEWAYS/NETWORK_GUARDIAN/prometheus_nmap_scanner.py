#!/usr/bin/env python3
"""
PROMETHEUS NMAP SCANNER - Real Port Scanning Module
Authority: 11.0 | Commander Bobby Don McWilliams II
Port Scanning, OS Detection, Service Enumeration, NSE Scripts
"""

import asyncio
import logging
import json
import subprocess
import re
import socket
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PrometheusNmapScanner")

class ScanType(Enum):
    """Nmap scan types"""
    QUICK = "quick"          # Top 100 ports
    FAST = "fast"            # Top 1000 ports
    FULL = "full"            # All 65535 ports
    STEALTH = "stealth"      # SYN scan (stealthy)
    VERSION = "version"      # Service version detection
    OS_DETECT = "os_detect"  # Operating system detection
    SCRIPT = "script"        # NSE script scan
    UDP = "udp"              # UDP port scan

@dataclass
class ScanResult:
    """Nmap scan result"""
    success: bool
    target: str
    scan_type: str
    timestamp: str
    ports_found: List[Dict[str, Any]]
    total_ports: int
    os_detection: Optional[Dict[str, Any]] = None
    services: Optional[Dict[str, Any]] = None
    vulnerabilities: Optional[List[Dict[str, Any]]] = None
    raw_output: str = ""
    duration: float = 0.0
    error: str = ""

class PrometheusNmapScanner:
    """Real Nmap integration for Prometheus Prime"""
    
    def __init__(self, nmap_path: str = None):
        """
        Initialize Nmap scanner
        
        Args:
            nmap_path: Path to nmap.exe (auto-detects if None)
        """
        self.nmap_path = nmap_path or self._find_nmap()
        self.logger = logger
        self.logger.info(f"🔱 PROMETHEUS NMAP SCANNER - Authority 11.0")
        self.logger.info(f"📍 Nmap path: {self.nmap_path}")
    
    def _find_nmap(self) -> str:
        """Auto-detect nmap installation"""
        # Common Windows locations
        possible_paths = [
            r"H:\Tools\network\nmap\nmap.exe",
            r"C:\Program Files (x86)\Nmap\nmap.exe",
            r"C:\Program Files\Nmap\nmap.exe",
            r"C:\Windows\System32\nmap.exe",
            "nmap"  # PATH environment
        ]
        
        for path in possible_paths:
            if Path(path).exists() or path == "nmap":
                try:
                    result = subprocess.run(
                        [path, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        self.logger.info(f"✅ Found nmap at: {path}")
                        return path
                except:
                    continue
        
        self.logger.warning("⚠️ Nmap not found - install via: choco install nmap")
        return "nmap"  # Hope it's in PATH
    
    async def scan_target(
        self,
        target: str,
        scan_type: ScanType = ScanType.FAST,
        ports: Optional[str] = None,
        timeout: int = 300
    ) -> ScanResult:
        """
        Scan target with nmap
        
        Args:
            target: IP address or hostname
            scan_type: Type of scan to perform
            ports: Port specification (e.g., "1-1000" or "80,443,8080")
            timeout: Scan timeout in seconds
            
        Returns:
            ScanResult with scan data
        """
        start_time = datetime.now()
        self.logger.info(f"🎯 Scanning {target} - Type: {scan_type.value}")
        
        # Build nmap command
        cmd = self._build_nmap_command(target, scan_type, ports)
        
        try:
            # Execute nmap
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                result.communicate(),
                timeout=timeout
            )
            
            raw_output = stdout.decode('utf-8', errors='ignore')
            
            # Parse results
            ports_found = self._parse_ports(raw_output)
            os_detection = self._parse_os_detection(raw_output) if scan_type == ScanType.OS_DETECT else None
            services = self._parse_services(raw_output) if scan_type == ScanType.VERSION else None
            vulnerabilities = self._parse_vulnerabilities(raw_output) if scan_type == ScanType.SCRIPT else None
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return ScanResult(
                success=True,
                target=target,
                scan_type=scan_type.value,
                timestamp=start_time.isoformat(),
                ports_found=ports_found,
                total_ports=len(ports_found),
                os_detection=os_detection,
                services=services,
                vulnerabilities=vulnerabilities,
                raw_output=raw_output,
                duration=duration
            )
            
        except asyncio.TimeoutError:
            return ScanResult(
                success=False,
                target=target,
                scan_type=scan_type.value,
                timestamp=start_time.isoformat(),
                ports_found=[],
                total_ports=0,
                error=f"Scan timeout after {timeout}s"
            )
        except Exception as e:
            self.logger.error(f"❌ Scan error: {e}")
            return ScanResult(
                success=False,
                target=target,
                scan_type=scan_type.value,
                timestamp=start_time.isoformat(),
                ports_found=[],
                total_ports=0,
                error=str(e)
            )
    
    def _build_nmap_command(
        self,
        target: str,
        scan_type: ScanType,
        ports: Optional[str]
    ) -> List[str]:
        """Build nmap command arguments"""
        cmd = [self.nmap_path]
        
        # Scan type specific args
        if scan_type == ScanType.QUICK:
            cmd.extend(["-F"])  # Fast scan (top 100 ports)
        elif scan_type == ScanType.FAST:
            cmd.extend(["-T4"])  # Aggressive timing
        elif scan_type == ScanType.FULL:
            cmd.extend(["-p-"])  # All 65535 ports
        elif scan_type == ScanType.STEALTH:
            cmd.extend(["-sS"])  # SYN stealth scan
        elif scan_type == ScanType.VERSION:
            cmd.extend(["-sV"])  # Service version detection
        elif scan_type == ScanType.OS_DETECT:
            cmd.extend(["-O"])  # OS detection
        elif scan_type == ScanType.SCRIPT:
            cmd.extend(["-sC", "-sV"])  # Default NSE scripts + version
        elif scan_type == ScanType.UDP:
            cmd.extend(["-sU"])  # UDP scan
        
        # Port specification
        if ports:
            cmd.extend(["-p", ports])
        
        # Output format
        cmd.extend(["-oN", "-"])  # Normal output to stdout
        
        # Target
        cmd.append(target)
        
        self.logger.debug(f"Command: {' '.join(cmd)}")
        return cmd
    
    def _parse_ports(self, output: str) -> List[Dict[str, Any]]:
        """Parse open ports from nmap output"""
        ports = []
        
        # Pattern: 80/tcp   open  http
        port_pattern = r'(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+(\S+)'
        
        for match in re.finditer(port_pattern, output):
            port_num, protocol, state, service = match.groups()
            
            if state == "open":
                ports.append({
                    "port": int(port_num),
                    "protocol": protocol,
                    "state": state,
                    "service": service
                })
        
        self.logger.info(f"✅ Found {len(ports)} open ports")
        return ports
    
    def _parse_os_detection(self, output: str) -> Optional[Dict[str, Any]]:
        """Parse OS detection from nmap output"""
        os_info = {
            "detected": False,
            "os_matches": [],
            "accuracy": 0
        }
        
        # Pattern: Running: Microsoft Windows
        running_pattern = r'Running:\s+(.+?)(?:\n|$)'
        match = re.search(running_pattern, output)
        if match:
            os_info["detected"] = True
            os_info["os_matches"].append(match.group(1).strip())
        
        # Pattern: OS details: Microsoft Windows 10
        details_pattern = r'OS details:\s+(.+?)(?:\n|$)'
        match = re.search(details_pattern, output)
        if match:
            os_info["detected"] = True
            os_info["os_matches"].append(match.group(1).strip())
        
        # Extract accuracy percentage
        accuracy_pattern = r'Aggressive OS guesses:.+?\((\d+)%\)'
        match = re.search(accuracy_pattern, output)
        if match:
            os_info["accuracy"] = int(match.group(1))
        
        return os_info if os_info["detected"] else None
    
    def _parse_services(self, output: str) -> Dict[str, Any]:
        """Parse service versions from nmap output"""
        services = {}
        
        # Pattern: 80/tcp open http Apache httpd 2.4.41
        service_pattern = r'(\d+)/(tcp|udp)\s+open\s+(\S+)\s+(.+?)(?:\n|$)'
        
        for match in re.finditer(service_pattern, output):
            port_num, protocol, service, version = match.groups()
            services[f"{port_num}/{protocol}"] = {
                "service": service,
                "version": version.strip()
            }
        
        return services
    
    def _parse_vulnerabilities(self, output: str) -> List[Dict[str, Any]]:
        """Parse NSE script vulnerabilities"""
        vulns = []
        
        # Pattern: |   CVE-2021-34527  (CRITICAL)
        vuln_pattern = r'\|\s+(CVE-\d{4}-\d+)\s+\((\w+)\)'
        
        for match in re.finditer(vuln_pattern, output):
            cve_id, severity = match.groups()
            vulns.append({
                "cve_id": cve_id,
                "severity": severity,
                "source": "nmap_nse"
            })
        
        return vulns
    
    async def quick_port_scan(self, target: str) -> ScanResult:
        """Quick scan of common ports"""
        return await self.scan_target(target, ScanType.QUICK)
    
    async def full_port_scan(self, target: str) -> ScanResult:
        """Full scan of all 65535 ports"""
        return await self.scan_target(target, ScanType.FULL)
    
    async def service_version_scan(self, target: str, ports: str) -> ScanResult:
        """Scan specific ports with version detection"""
        return await self.scan_target(target, ScanType.VERSION, ports=ports)
    
    async def vulnerability_scan(self, target: str) -> ScanResult:
        """Scan with NSE vulnerability scripts"""
        return await self.scan_target(target, ScanType.SCRIPT)
    
    async def os_detection_scan(self, target: str) -> ScanResult:
        """Scan with OS detection"""
        return await self.scan_target(target, ScanType.OS_DETECT)

# ============================================================================
# CLI TEST INTERFACE
# ============================================================================

async def test_scanner():
    """Test scanner on localhost"""
    scanner = PrometheusNmapScanner()
    
    print("🔱 PROMETHEUS NMAP SCANNER - TESTING")
    print("="*60)
    
    # Test 1: Quick scan
    print("\n[TEST 1] Quick scan of localhost...")
    result = await scanner.quick_port_scan("127.0.0.1")
    print(f"Success: {result.success}")
    print(f"Ports found: {result.total_ports}")
    for port in result.ports_found[:5]:
        print(f"  - {port['port']}/{port['protocol']}: {port['service']}")
    
    # Test 2: Specific ports with version detection
    print("\n[TEST 2] Version detection on common ports...")
    result = await scanner.service_version_scan("127.0.0.1", "135,445,5985")
    print(f"Success: {result.success}")
    print(f"Services detected: {len(result.services or {})}")
    if result.services:
        for port, info in list(result.services.items())[:3]:
            print(f"  - {port}: {info['version']}")
    
    print("\n✅ TESTING COMPLETE")

if __name__ == "__main__":
    asyncio.run(test_scanner())
