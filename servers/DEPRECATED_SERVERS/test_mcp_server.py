import sys
from pathlib import Path

print("="*80)
print("EPCP30 XV4 MCP SERVER TEST SUITE".center(80))
print("="*80)

passed = 0
failed = 0

# Test 1: Python version
print("\n[1/8] Python version...", end=" ")
if sys.version_info >= (3, 10):
    print("✓ PASS")
    passed += 1
else:
    print("✗ FAIL - Need Python 3.10+")
    failed += 1

# Test 2: Directories
print("[2/8] Directories...", end=" ")
paths = [
    Path("E:/ECHO_XV4/MLS/servers"),
    Path("E:/ECHO_XV4/EPCP30/LOGS"),
    Path("E:/ECHO_XV4/MLS/logs")
]
if all(p.exists() for p in paths):
    print("✓ PASS")
    passed += 1
else:
    print("✗ FAIL")
    failed += 1
    for p in paths:
        if not p.exists():
            print(f"  Missing: {p}")

# Test 3: Dependencies
print("[3/8] Dependencies...", end=" ")
try:
    import mcp, psutil, fastapi, uvicorn
    print("✓ PASS")
    passed += 1
except ImportError as e:
    print(f"✗ FAIL - {e}")
    failed += 1

# Test 4: MCP server file
print("[4/8] MCP server file...", end=" ")
server_file = Path("E:/ECHO_XV4/EPCP30/MCP_SERVER/desktop_commander_server.py")
if server_file.exists():
    print("✓ PASS")
    passed += 1
else:
    print("✗ FAIL")
    failed += 1

# Test 5: MLS registry
print("[5/8] MLS registry...", end=" ")
registry = Path("E:/ECHO_XV4/MLS/server_registry.json")
if registry.exists():
    print("✓ PASS")
    passed += 1
else:
    print("✗ FAIL")
    failed += 1

# Test 6: File creation
print("[6/8] File operations...", end=" ")
try:
    test_path = Path("E:/ECHO_XV4/EPCP30/test.txt")
    test_path.write_text("EPCP30 XV4 Test")
    if test_path.read_text() == "EPCP30 XV4 Test":
        test_path.unlink()
        print("✓ PASS")
        passed += 1
    else:
        print("✗ FAIL")
        failed += 1
except Exception as e:
    print(f"✗ FAIL - {e}")
    failed += 1

# Test 7: Port check
print("[7/8] Socket operations...", end=" ")
try:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to any available port
        port = s.getsockname()[1]
    print(f"✓ PASS (tested port {port})")
    passed += 1
except Exception as e:
    print(f"✗ FAIL - {e}")
    failed += 1

# Test 8: MCP server syntax
print("[8/8] MCP server syntax...", end=" ")
try:
    import ast
    server_code = server_file.read_text()
    ast.parse(server_code)
    print("✓ PASS")
    passed += 1
except Exception as e:
    print(f"✗ FAIL - {e}")
    failed += 1

print("\n" + "="*80)
print(f"Results: {passed} PASSED, {failed} FAILED".center(80))
print("="*80)

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! Server ready for mobile control!".center(80))
    print("\nNext Steps:")
    print("  1. Run: START_MCP_SERVER.bat")
    print("  2. Open Claude on mobile")
    print("  3. Say: 'Create a test server on my desktop'")
else:
    print("\n⚠️ SOME TESTS FAILED - Check errors above".center(80))
    sys.exit(1)
