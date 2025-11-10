#!/usr/bin/env python3
"""
Windows API MCP Bridge - Verification Test
Tests backend connectivity and basic functionality
"""

import requests
import json
from datetime import datetime

def test_backend():
    """Test Windows API Ultimate backend connection"""
    print("=" * 60)
    print("WINDOWS API MCP BRIDGE - VERIFICATION TEST")
    print("=" * 60)
    print()
    
    url = "http://localhost:8343"
    
    print(f"[TEST 1] Backend Connection Test")
    print(f"URL: {url}")
    print()
    
    try:
        # Test health endpoint
        response = requests.get(f"{url}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is ONLINE")
            print(f"   Server: {data.get('server', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            print(f"   Port: {data.get('port', 'Unknown')}")
            print()
            
            # Test system info endpoint
            print("[TEST 2] System Info Test")
            response = requests.get(f"{url}/system/info", timeout=5)
            if response.status_code == 200:
                info = response.json()
                print("✅ System info retrieved")
                print(f"   OS: {info.get('os', {}).get('platform', 'Unknown')}")
                print(f"   CPU Cores: {info.get('cpu', {}).get('cores', 'Unknown')}")
                print(f"   Memory: {info.get('memory', {}).get('total', 'Unknown')}")
                print()
            else:
                print(f"❌ System info failed: HTTP {response.status_code}")
                print()
            
            # Test performance endpoint
            print("[TEST 3] Performance Test")
            response = requests.get(f"{url}/performance", timeout=5)
            if response.status_code == 200:
                perf = response.json()
                print("✅ Performance metrics retrieved")
                print(f"   CPU: {perf.get('cpu', {}).get('percent', 'Unknown')}%")
                print(f"   Memory: {perf.get('memory', {}).get('percent', 'Unknown')}%")
                print()
            else:
                print(f"❌ Performance test failed: HTTP {response.status_code}")
                print()
            
            print("=" * 60)
            print("✅ ALL TESTS PASSED - Backend is fully operational")
            print("=" * 60)
            print()
            print("Next steps:")
            print("1. Update Claude Desktop config:")
            print("   %APPDATA%\\Claude\\claude_desktop_config.json")
            print()
            print("2. Copy configuration from:")
            print("   E:\\ECHO_XV4\\MLS\\servers\\claude_desktop_config.json")
            print()
            print("3. Restart Claude Desktop")
            print()
            
        else:
            print(f"❌ Backend returned HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            print()
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION FAILED")
        print()
        print("Windows API Ultimate backend is NOT running!")
        print()
        print("Start backend first:")
        print("   E:\\ECHO_XV4\\MLS\\servers\\START_WINDOWS_API_ULTIMATE.bat")
        print()
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT")
        print("   Backend is not responding (timeout after 5s)")
        print()
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()

if __name__ == "__main__":
    test_backend()
    input("Press Enter to exit...")
