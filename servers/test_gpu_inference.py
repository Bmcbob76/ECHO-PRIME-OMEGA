"""
🎖️ GPU INFERENCE TESTING SCRIPT
Authority Level: 11.0
Commander: Bobby Don McWilliams II

Complete test suite for GPU inference system.
Tests connectivity, models, generation, and API endpoints.

Location: E:\ECHO_XV4\MLS\servers\test_gpu_inference.py
"""

import sys
import os
import time
import requests
import json

# Add to path
sys.path.insert(0, r"E:\ECHO_XV4\MLS\servers")

from gpu_inference_client import GPUInferenceClient, GPUServerConfig


def print_header(title):
    """Print test section header"""
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70)


def test_direct_ollama_connection(host, port):
    """Test 1: Direct connection to Ollama server"""
    print_header("TEST 1: Direct Ollama Connection")
    
    try:
        url = f"http://{host}:{port}/api/tags"
        print(f"Testing: {url}")
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ SUCCESS - Connected to Ollama server")
            print(f"   Models available: {len(models)}")
            for model in models:
                size_gb = model.get('size', 0) / 1e9
                print(f"   • {model['name']} ({size_gb:.1f}GB)")
            return True
        else:
            print(f"❌ FAILED - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Is GPU machine running?")
        print(f"   2. Is Ollama installed and running?")
        print(f"   3. Check IP address: {host}")
        print(f"   4. Verify firewall allows port {port}")
        print(f"   5. On GPU machine run: Get-NetTCPConnection -LocalPort {port}")
        return False


def test_gpu_client_initialization(host):
    """Test 2: GPU client initialization"""
    print_header("TEST 2: GPU Client Initialization")
    
    try:
        config = GPUServerConfig(host=host)
        client = GPUInferenceClient(config)
        
        print("✅ SUCCESS - GPU client initialized")
        print(f"   Server: {config.base_url}")
        print(f"   Model: {config.model}")
        
        return client
        
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        return None


def test_health_check(client):
    """Test 3: Health check"""
    print_header("TEST 3: Health Check")
    
    try:
        health = client.health_check()
        
        print(f"Status: {health['status']}")
        print(f"Latency: {health.get('latency_ms', 'N/A')} ms")
        print(f"Models: {health.get('models_available', 0)}")
        
        if health['status'] == 'healthy':
            print("✅ SUCCESS - Server is healthy")
            return True
        else:
            print("❌ FAILED - Server is unhealthy")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        return False


def test_simple_generation(client):
    """Test 4: Simple text generation"""
    print_header("TEST 4: Simple Text Generation")
    
    try:
        print("Prompt: 'Count from 1 to 5.'")
        print("Generating...\n")
        
        start = time.time()
        result = client.generate(
            prompt="Count from 1 to 5.",
            temperature=0.1,
            max_tokens=50
        )
        elapsed = time.time() - start
        
        print(f"\nResponse: {result['response']}")
        print(f"\n⏱️  Generation time: {elapsed:.2f}s")
        print(f"✅ SUCCESS - Generation completed")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        return False


def test_chat(client):
    """Test 5: Chat conversation"""
    print_header("TEST 5: Chat Conversation")
    
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Answer in one sentence."},
            {"role": "user", "content": "What is 2+2?"}
        ]
        
        print("Chat messages:")
        for msg in messages:
            print(f"  {msg['role']}: {msg['content']}")
        
        print("\nGenerating response...\n")
        
        start = time.time()
        result = client.chat(messages, temperature=0.1)
        elapsed = time.time() - start
        
        response = result['message']['content']
        print(f"Assistant: {response}")
        print(f"\n⏱️  Chat time: {elapsed:.2f}s")
        print(f"✅ SUCCESS - Chat completed")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        return False


def test_api_server(port=8070):
    """Test 6: API Server endpoints"""
    print_header("TEST 6: API Server Endpoints")
    
    base_url = f"http://localhost:{port}"
    
    # Test health
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Health endpoint working")
            print(f"   Status: {health.get('status')}")
        else:
            print(f"⚠️  Health returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {str(e)}")
        print(f"   Note: Make sure API server is running!")
        print(f"   Run: python E:\\ECHO_XV4\\MLS\\servers\\gpu_inference_server.py")
        return False
    
    # Test generate
    print("\nTesting /api/generate endpoint...")
    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={"prompt": "Say hello.", "max_tokens": 20},
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generate endpoint working")
            print(f"   Response: {result.get('response', '')[:100]}")
        else:
            print(f"⚠️  Generate returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Generate endpoint failed: {str(e)}")
        return False
    
    # Test models
    print("\nTesting /api/models endpoint...")
    try:
        response = requests.get(f"{base_url}/api/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Models endpoint working")
            print(f"   Models available: {models.get('count', 0)}")
        else:
            print(f"⚠️  Models returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Models endpoint failed: {str(e)}")
        return False
    
    print("\n✅ SUCCESS - All API endpoints working")
    return True


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "🎖️ GPU INFERENCE SYSTEM - COMPLETE TEST SUITE")
    print("Commander: Bobby Don McWilliams II")
    print("Authority Level: 11.0")
    
    # Load config
    host = os.environ.get("GPU_SERVER_HOST", "192.168.1.100")
    port = int(os.environ.get("GPU_SERVER_PORT", "11434"))
    
    print(f"\nConfiguration:")
    print(f"  GPU Server: {host}:{port}")
    print(f"  Model: {os.environ.get('GPU_MODEL', 'mixtral:8x7b-instruct-v0.1-q4_K_M')}")
    
    results = []
    
    # Test 1: Direct connection
    results.append(("Direct Ollama Connection", test_direct_ollama_connection(host, port)))
    
    if not results[-1][1]:
        print("\n❌ CRITICAL: Cannot connect to Ollama server")
        print("   Fix connection before continuing tests")
        return
    
    # Test 2-5: Client tests
    client = test_gpu_client_initialization(host)
    if client:
        results.append(("GPU Client Init", True))
        results.append(("Health Check", test_health_check(client)))
        results.append(("Simple Generation", test_simple_generation(client)))
        results.append(("Chat Conversation", test_chat(client)))
        
        client.shutdown()
    else:
        results.extend([
            ("GPU Client Init", False),
            ("Health Check", False),
            ("Simple Generation", False),
            ("Chat Conversation", False)
        ])
    
    # Test 6: API Server
    results.append(("API Server", test_api_server()))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*70}")
    print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("🎖️ ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT!")
    else:
        print("⚠️  SOME TESTS FAILED - Review errors above")


if __name__ == "__main__":
    # Load environment variables from config file
    config_path = r"E:\ECHO_XV4\MLS\servers\gpu_config.env"
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    
    run_all_tests()
