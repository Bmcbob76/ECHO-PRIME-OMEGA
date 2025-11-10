#!/usr/bin/env python3
"""
PROMETHEUS PRIME - COMPREHENSIVE TEST SUITE
Authority: 11.0 | Commander Bobby Don McWilliams II
Tests all Prometheus modules with real scanning capabilities
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add NETWORK_GUARDIAN to path
sys.path.insert(0, str(Path(__file__).parent))

from prometheus_nmap_scanner import PrometheusNmapScanner, ScanType
from prometheus_smb_analyzer import PrometheusSMBAnalyzer
from prometheus_vulnerability_scanner import PrometheusVulnerabilityScanner
from prometheus_integration import PrometheusIntegration

def print_header(title: str):
    """Print test section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_result(label: str, value: any):
    """Print test result"""
    print(f"  {label}: {value}")

async def test_nmap_scanner(target: str = "127.0.0.1"):
    """Test Nmap scanner module"""
    print_header("🔱 TEST 1: NMAP PORT SCANNER")
    
    scanner = PrometheusNmapScanner()
    
    # Test quick scan
    print(f"\n📡 Quick scan of {target}...")
    result = await scanner.quick_port_scan(target)
    
    print_result("Success", result.success)
    print_result("Target", result.target)
    print_result("Scan Type", result.scan_type)
    print_result("Total Ports", result.total_ports)
    print_result("Duration", f"{result.duration:.2f}s")
    
    if result.ports_found:
        print(f"\n  📋 Open Ports (top 5):")
        for port in result.ports_found[:5]:
            print(f"    • {port['port']}/{port['protocol']} - {port['service']}")
    
    if result.error:
        print(f"  ❌ Error: {result.error}")
    
    return result.success

async def test_smb_analyzer(target: str = "127.0.0.1"):
    """Test SMB analyzer module"""
    print_header("🔱 TEST 2: SMB/NETBIOS ANALYZER")
    
    analyzer = PrometheusSMBAnalyzer()
    
    # Test anonymous scan
    print(f"\n🔍 Anonymous SMB scan of {target}...")
    result = await analyzer.quick_smb_scan(target)
    
    print_result("Success", result.success)
    print_result("Target", result.target)
    print_result("Total Shares", result.total_shares)
    print_result("Admin Shares", len(result.administrative_shares))
    print_result("Anonymous Access", len(result.anonymous_accessible))
    print_result("Duration", f"{result.duration:.2f}s")
    
    if result.administrative_shares:
        print(f"\n  ⚠️ CRITICAL - Administrative Shares:")
        for share in result.administrative_shares:
            print(f"    • {share}")
    
    if result.shares_found:
        print(f"\n  📋 Discovered Shares (top 5):")
        for share in result.shares_found[:5]:
            risk_icon = "🔴" if share.risk_level == "CRITICAL" else "🟡"
            print(f"    {risk_icon} {share.name} - {share.risk_level} - Accessible: {share.accessible}")
    
    if result.os_info:
        print(f"\n  💻 OS Information:")
        print(f"    Type: {result.os_info.get('os_type', 'Unknown')}")
        print(f"    Computer: {result.os_info.get('computer_name', 'Unknown')}")
    
    if result.error:
        print(f"  ❌ Error: {result.error}")
    
    return result.success

async def test_vulnerability_scanner():
    """Test vulnerability scanner module"""
    print_header("🔱 TEST 3: VULNERABILITY SCANNER")
    
    scanner = PrometheusVulnerabilityScanner()
    
    # Test with common services
    print(f"\n🔎 Scanning for known vulnerabilities...")
    services = {
        "445": "SMB",
        "5985": "WinRM",
        "135": "RPC"
    }
    
    result = await scanner.scan_target("192.168.1.200", services)
    
    print_result("Success", result.success)
    print_result("Target", result.target)
    print_result("Total Vulnerabilities", result.total_vulnerabilities)
    print_result("Critical", result.critical_count)
    print_result("High", result.high_count)
    print_result("Medium", result.medium_count)
    print_result("Low", result.low_count)
    print_result("Risk Score", f"{result.risk_score}/100")
    print_result("Duration", f"{result.duration:.2f}s")
    
    if result.vulnerabilities_found:
        print(f"\n  🚨 Top Vulnerabilities (max 3):")
        for vuln in result.vulnerabilities_found[:3]:
            severity_icon = "🔴" if vuln.severity == "CRITICAL" else "🟠"
            print(f"\n    {severity_icon} {vuln.cve_id} - {vuln.title}")
            print(f"       Severity: {vuln.severity} (CVSS: {vuln.cvss_score})")
            print(f"       Exploit: {vuln.exploit_status}")
            if vuln.metasploit_modules:
                print(f"       Metasploit: {vuln.metasploit_modules[0]}")
    
    # Test CVE lookup
    print(f"\n  🔍 Testing CVE lookup...")
    eternalblue = await scanner.check_cve("CVE-2017-0143")
    if eternalblue:
        print(f"    ✅ Found: {eternalblue.title}")
        print(f"       CVSS: {eternalblue.cvss_score}")
    
    if result.error:
        print(f"  ❌ Error: {result.error}")
    
    return result.success

async def test_integration(target: str = "127.0.0.1"):
    """Test comprehensive integration module"""
    print_header("🔱 TEST 4: COMPREHENSIVE INTEGRATION")
    
    integration = PrometheusIntegration()
    
    # Comprehensive scan
    print(f"\n🎯 Comprehensive security scan of {target}...")
    print("   (This may take 30-60 seconds...)")
    
    result = await integration.comprehensive_scan(target)
    
    print(f"\n  📊 SCAN RESULTS:")
    print_result("Success", result.success)
    print_result("Target", result.target)
    print_result("Duration", f"{result.scan_duration:.2f}s")
    
    print(f"\n  🎯 THREAT ASSESSMENT:")
    threat_color = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }.get(result.threat_level, "⚪")
    
    print_result(f"  {threat_color} Threat Level", result.threat_level)
    print_result("  Risk Score", f"{result.risk_score}/100")
    print_result("  Open Ports", result.total_ports)
    print_result("  Critical Vulns", result.critical_vulns)
    print_result("  High Vulns", result.high_vulns)
    print_result("  Admin Shares", "EXPOSED" if result.administrative_shares_exposed else "Secure")
    
    if result.attack_vectors:
        print(f"\n  🚨 ATTACK VECTORS:")
        for i, vector in enumerate(result.attack_vectors, 1):
            print(f"    {i}. {vector}")
    
    if result.recommendations:
        print(f"\n  🛡️ TOP RECOMMENDATIONS:")
        for rec in result.recommendations[:5]:
            print(f"    {rec}")
    
    if result.error:
        print(f"  ❌ Error: {result.error}")
    
    return result.success

async def run_all_tests(target: str = "127.0.0.1"):
    """Run complete test suite"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║  🔱 PROMETHEUS PRIME - COMPREHENSIVE TEST SUITE                    ║")
    print("║  Authority: 11.0 | Commander Bobby Don McWilliams II              ║")
    print("╚" + "="*68 + "╝")
    
    start_time = datetime.now()
    
    print(f"\n📍 Test Target: {target}")
    print(f"⏰ Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    try:
        # Run all tests
        results["nmap"] = await test_nmap_scanner(target)
        results["smb"] = await test_smb_analyzer(target)
        results["vuln"] = await test_vulnerability_scanner()
        results["integration"] = await test_integration(target)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        return
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        return
    
    # Summary
    duration = (datetime.now() - start_time).total_seconds()
    
    print_header("📊 TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n  Tests Passed: {passed}/{total}")
    print(f"  Duration: {duration:.2f}s")
    
    print(f"\n  Test Results:")
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"    {status} - {test_name.upper()}")
    
    if passed == total:
        print(f"\n  🎉 ALL TESTS PASSED - PROMETHEUS FULLY OPERATIONAL")
    else:
        print(f"\n  ⚠️ SOME TESTS FAILED - CHECK LOGS ABOVE")
    
    print("\n" + "="*70)
    print("  ✅ TESTING COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    # Get target from command line or use localhost
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    
    # Run tests
    asyncio.run(run_all_tests(target))
