"""
🎖️ GPU INFERENCE CLIENT - ECHO_XV4 SYSTEM
Authority Level: 11.0
Commander: Bobby Don McWilliams II

Client for querying remote GPU server (RTX 4070 16GB) for AI inference.
Integrated with GS343 Foundation and Phoenix Auto-Heal.

Location: E:\ECHO_XV4\MLS\servers\gpu_inference_client.py
"""

import sys
import os
import json
import time
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Add GS343 to path
sys.path.insert(0, r"E:\GS343\FOUNDATION")

from gs343_foundation_core import GS343UniversalFoundation
from phoenix_auto_heal import PhoenixAutoHeal


@dataclass
class GPUServerConfig:
    """Configuration for GPU inference server"""
    host: str = "192.168.1.100"  # UPDATE WITH YOUR GPU MACHINE IP
    port: int = 11434
    timeout: int = 120
    model: str = "mixtral:8x7b-instruct-v0.1-q4_K_M"
    
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


class GPUInferenceClient:
    """
    Client for distributed AI inference on remote GPU server.
    
    Features:
    - Streaming and non-streaming responses
    - Automatic retry on failure
    - Health monitoring
    - GS343 Foundation integration
    - Phoenix Auto-Heal recovery
    """
    
    def __init__(self, config: Optional[GPUServerConfig] = None):
        """Initialize GPU inference client"""
        self.config = config or GPUServerConfig()
        
        # Initialize GS343 Foundation
        self.gs343 = GS343UniversalFoundation("GPUInferenceClient", authority_level=11.0)
        self.gs343.log_event("system_startup", "Initializing GPU Inference Client")
        
        # Initialize Phoenix Auto-Heal
        self.phoenix = PhoenixAutoHeal("GPUInferenceClient", authority_level=11.0)
        self.phoenix.start_monitoring()
        
        # Session for connection pooling
        self.session = requests.Session()
        
        # Verify server connection
        self._verify_connection()
    
    def _verify_connection(self) -> bool:
        """Verify connection to GPU server"""
        try:
            response = self.session.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            
            if response.status_code == 200:
                self.gs343.log_event("connection_success", f"Connected to GPU server at {self.config.host}")
                models = response.json().get('models', [])
                self.gs343.log_event("models_available", f"Available models: {len(models)}")
                return True
            else:
                self.gs343.log_event("connection_failed", f"Server returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.gs343.log_event("connection_error", f"Failed to connect: {str(e)}")
            print(f"❌ Cannot connect to GPU server at {self.config.base_url}")
            print(f"   Error: {str(e)}")
            print(f"\n🔧 Troubleshooting:")
            print(f"   1. Verify GPU machine is on and Ollama is running")
            print(f"   2. Check IP address: {self.config.host}")
            print(f"   3. Verify firewall allows port {self.config.port}")
            print(f"   4. Test: curl http://{self.config.host}:{self.config.port}/api/tags")
            return False
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Generate response from GPU server.
        
        Args:
            prompt: User prompt
            model: Model name (defaults to config.model)
            system: System prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Enable streaming response
            
        Returns:
            Response dict with 'response', 'model', 'created_at', etc.
        """
        model = model or self.config.model
        
        # Build request
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
            
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            start_time = time.time()
            
            response = self.session.post(
                f"{self.config.base_url}/api/generate",
                json=payload,
                timeout=self.config.timeout,
                stream=stream
            )
            
            response.raise_for_status()
            
            if stream:
                return self._handle_stream(response)
            else:
                result = response.json()
                elapsed = time.time() - start_time
                
                self.gs343.log_event(
                    "inference_complete",
                    f"Generated {len(result.get('response', ''))} chars in {elapsed:.2f}s"
                )
                
                return result
                
        except Exception as e:
            self.gs343.log_event("inference_error", f"Generation failed: {str(e)}")
            raise
    
    def _handle_stream(self, response) -> Dict[str, Any]:
        """Handle streaming response"""
        full_response = ""
        
        try:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        text = chunk['response']
                        full_response += text
                        print(text, end='', flush=True)
                    
                    if chunk.get('done', False):
                        print()  # Newline at end
                        return {
                            'response': full_response,
                            'model': chunk.get('model'),
                            'created_at': chunk.get('created_at'),
                            'done': True
                        }
            
        except Exception as e:
            self.gs343.log_event("stream_error", f"Stream failed: {str(e)}")
            raise
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Chat with GPU model (multi-turn conversation).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [
                         {"role": "system", "content": "You are a helpful assistant"},
                         {"role": "user", "content": "Hello!"}
                     ]
            model: Model name
            temperature: Sampling temperature
            stream: Enable streaming
            
        Returns:
            Response dict
        """
        model = model or self.config.model
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature
            }
        }
        
        try:
            start_time = time.time()
            
            response = self.session.post(
                f"{self.config.base_url}/api/chat",
                json=payload,
                timeout=self.config.timeout,
                stream=stream
            )
            
            response.raise_for_status()
            
            if stream:
                return self._handle_chat_stream(response)
            else:
                result = response.json()
                elapsed = time.time() - start_time
                
                self.gs343.log_event(
                    "chat_complete",
                    f"Chat response in {elapsed:.2f}s"
                )
                
                return result
                
        except Exception as e:
            self.gs343.log_event("chat_error", f"Chat failed: {str(e)}")
            raise
    
    def _handle_chat_stream(self, response) -> Dict[str, Any]:
        """Handle streaming chat response"""
        full_response = ""
        
        try:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'message' in chunk and 'content' in chunk['message']:
                        text = chunk['message']['content']
                        full_response += text
                        print(text, end='', flush=True)
                    
                    if chunk.get('done', False):
                        print()  # Newline at end
                        return {
                            'message': {'role': 'assistant', 'content': full_response},
                            'model': chunk.get('model'),
                            'created_at': chunk.get('created_at'),
                            'done': True
                        }
            
        except Exception as e:
            self.gs343.log_event("chat_stream_error", f"Chat stream failed: {str(e)}")
            raise
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models on GPU server"""
        try:
            response = self.session.get(f"{self.config.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            self.gs343.log_event("list_models_error", f"Failed to list models: {str(e)}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Check GPU server health"""
        try:
            start = time.time()
            response = self.session.get(f"{self.config.base_url}/api/tags", timeout=5)
            latency = (time.time() - start) * 1000  # ms
            
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "latency_ms": round(latency, 2),
                "models_available": len(response.json().get('models', [])),
                "server": f"{self.config.host}:{self.config.port}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "server": f"{self.config.host}:{self.config.port}"
            }
    
    def shutdown(self):
        """Graceful shutdown"""
        self.gs343.log_event("system_shutdown", "Shutting down GPU Inference Client")
        self.phoenix.stop_monitoring()
        self.session.close()


def main():
    """Demo usage"""
    print("🎖️ GPU INFERENCE CLIENT - ECHO_XV4")
    print("=" * 60)
    
    # Initialize client
    config = GPUServerConfig(
        host="192.168.1.100",  # UPDATE THIS!
        model="mixtral:8x7b-instruct-v0.1-q4_K_M"
    )
    
    client = GPUInferenceClient(config)
    
    # Check health
    print("\n🏥 Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    # List models
    print("\n📋 Available Models:")
    models = client.list_models()
    for model in models:
        print(f"  • {model['name']} ({model['size'] / 1e9:.1f}GB)")
    
    # Generate response
    print("\n💬 Generating Response (Non-Streaming):")
    result = client.generate(
        prompt="Explain quantum computing in one sentence.",
        temperature=0.7
    )
    print(f"\n{result['response']}")
    
    # Generate streaming response
    print("\n💬 Generating Response (Streaming):")
    result = client.generate(
        prompt="Write a haiku about artificial intelligence.",
        temperature=0.9,
        stream=True
    )
    
    # Chat example
    print("\n💬 Chat Example:")
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What's the capital of France?"}
    ]
    result = client.chat(messages)
    print(f"\nAssistant: {result['message']['content']}")
    
    # Shutdown
    client.shutdown()
    print("\n✅ Client shutdown complete")


if __name__ == "__main__":
    main()
