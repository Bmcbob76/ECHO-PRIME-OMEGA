"""
🎖️ HYBRID LLM ROUTER - AUTHORITY 11.0
Route queries between local CPU (conversational) and OMEN-40L (complex coding)

Architecture:
- LOCAL CPU: Fast conversational responses, simple queries
- OMEN-40L (192.168.1.187): Qwen2.5-Coder for complex coding tasks

Author: Commander Bobby Don McWilliams II
Location: E:\ECHO_XV4\MLS\servers\ACTIVE_SERVERS\hybrid_llm_router.py
"""

import asyncio
import aiohttp
import re
from typing import Dict, Optional, Tuple
from enum import Enum
import json
import time

# =============================================================================
# CONFIGURATION
# =============================================================================

OMEN_HOST = "192.168.1.187"
OMEN_PORT = 11434
OMEN_MODEL = "qwen2.5-coder:32b-instruct-q5_K_M"

LOCAL_CPU_MODEL = "llama3.2:3b-instruct-q4_K_M"  # Fast local model
LOCAL_HOST = "localhost"
LOCAL_PORT = 11434

TIMEOUT = 120  # seconds

# =============================================================================
# QUERY CLASSIFICATION
# =============================================================================

class QueryType(Enum):
    """Query classification for routing"""
    CONVERSATIONAL = "conversational"  # Local CPU
    SIMPLE_CODE = "simple_code"        # Local CPU
    COMPLEX_CODE = "complex_code"      # OMEN-40L
    ARCHITECTURE = "architecture"       # OMEN-40L
    DEBUGGING = "debugging"             # OMEN-40L
    
class HybridRouter:
    """Routes queries between local CPU and OMEN-40L"""
    
    def __init__(self):
        self.omen_url = f"http://{OMEN_HOST}:{OMEN_PORT}"
        self.local_url = f"http://{LOCAL_HOST}:{LOCAL_PORT}"
        
        # Complex coding keywords
        self.complex_keywords = [
            "refactor", "optimize", "architect", "design pattern",
            "algorithm", "data structure", "performance", "scalability",
            "async", "concurrent", "parallel", "threading",
            "database", "sql", "orm", "migration",
            "api design", "rest", "graphql", "microservice",
            "security", "authentication", "authorization",
            "testing", "unit test", "integration test",
            "debug complex", "trace", "profile",
            "large codebase", "enterprise", "production"
        ]
        
        # Simple conversational keywords
        self.conversational_keywords = [
            "hello", "hi", "how are you", "thanks", "thank you",
            "help", "explain", "what is", "tell me about",
            "can you", "please", "show me"
        ]
        
    def classify_query(self, query: str) -> QueryType:
        """Classify query type for routing"""
        query_lower = query.lower()
        
        # Check for complex coding patterns
        if any(keyword in query_lower for keyword in self.complex_keywords):
            return QueryType.COMPLEX_CODE
            
        # Check for code-related patterns
        code_patterns = [
            r"```",  # Code blocks
            r"class\s+\w+",  # Class definitions
            r"def\s+\w+",  # Function definitions
            r"async\s+def",  # Async functions
            r"import\s+\w+",  # Imports
        ]
        
        if any(re.search(pattern, query) for pattern in code_patterns):
            # Long code blocks → OMEN-40L
            if len(query) > 500 or query.count('\n') > 20:
                return QueryType.COMPLEX_CODE
            else:
                return QueryType.SIMPLE_CODE
                
        # Architecture/design questions
        architecture_keywords = ["architecture", "design", "structure", "organize"]
        if any(kw in query_lower for kw in architecture_keywords):
            return QueryType.ARCHITECTURE
            
        # Default to conversational for short queries
        if len(query) < 200:
            return QueryType.CONVERSATIONAL
            
        # Medium queries with no code → conversational
        return QueryType.CONVERSATIONAL
        
    def should_use_omen(self, query_type: QueryType) -> bool:
        """Determine if query should route to OMEN-40L"""
        return query_type in [
            QueryType.COMPLEX_CODE,
            QueryType.ARCHITECTURE,
            QueryType.DEBUGGING
        ]
        
    async def query_llm(
        self,
        prompt: str,
        use_omen: bool = False,
        stream: bool = False
    ) -> Dict:
        """Query either local CPU or OMEN-40L"""
        
        url = self.omen_url if use_omen else self.local_url
        model = OMEN_MODEL if use_omen else LOCAL_CPU_MODEL
        target = "OMEN-40L" if use_omen else "LOCAL CPU"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=TIMEOUT)
                ) as response:
                    
                    if response.status == 200:
                        if stream:
                            # Handle streaming response
                            full_response = ""
                            async for line in response.content:
                                if line:
                                    try:
                                        data = json.loads(line)
                                        if "response" in data:
                                            full_response += data["response"]
                                            yield {
                                                "chunk": data["response"],
                                                "done": data.get("done", False)
                                            }
                                    except json.JSONDecodeError:
                                        continue
                            
                            elapsed = time.time() - start_time
                            yield {
                                "full_response": full_response,
                                "target": target,
                                "model": model,
                                "elapsed": elapsed,
                                "done": True
                            }
                        else:
                            data = await response.json()
                            elapsed = time.time() - start_time
                            
                            return {
                                "response": data.get("response", ""),
                                "target": target,
                                "model": model,
                                "elapsed": elapsed,
                                "success": True
                            }
                    else:
                        return {
                            "error": f"HTTP {response.status}",
                            "target": target,
                            "success": False
                        }
                        
        except asyncio.TimeoutError:
            return {
                "error": f"Timeout after {TIMEOUT}s",
                "target": target,
                "success": False
            }
        except Exception as e:
            return {
                "error": str(e),
                "target": target,
                "success": False
            }
            
    async def route_query(
        self,
        query: str,
        force_omen: bool = False,
        stream: bool = False
    ) -> Dict:
        """
        Main routing function
        
        Args:
            query: User query
            force_omen: Force routing to OMEN-40L
            stream: Enable streaming response
            
        Returns:
            Response dict with routing info
        """
        
        # Classify query
        query_type = self.classify_query(query)
        use_omen = force_omen or self.should_use_omen(query_type)
        
        # Route to appropriate LLM
        if stream:
            async for chunk in self.query_llm(query, use_omen, stream=True):
                chunk["query_type"] = query_type.value
                yield chunk
        else:
            result = await self.query_llm(query, use_omen, stream=False)
            result["query_type"] = query_type.value
            return result
            
    async def health_check(self) -> Dict:
        """Check health of both LLMs"""
        
        async def check_endpoint(url: str, name: str) -> Tuple[str, bool, Optional[str]]:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{url}/api/tags",
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as response:
                        if response.status == 200:
                            return name, True, None
                        else:
                            return name, False, f"HTTP {response.status}"
            except Exception as e:
                return name, False, str(e)
                
        # Check both endpoints
        local_check, omen_check = await asyncio.gather(
            check_endpoint(self.local_url, "LOCAL CPU"),
            check_endpoint(self.omen_url, "OMEN-40L")
        )
        
        return {
            "local": {
                "name": local_check[0],
                "healthy": local_check[1],
                "error": local_check[2],
                "model": LOCAL_CPU_MODEL
            },
            "omen": {
                "name": omen_check[0],
                "healthy": omen_check[1],
                "error": omen_check[2],
                "model": OMEN_MODEL
            }
        }

# =============================================================================
# CLI INTERFACE
# =============================================================================

async def main():
    """Test the hybrid router"""
    router = HybridRouter()
    
    print("🎖️ HYBRID LLM ROUTER - AUTHORITY 11.0")
    print("=" * 80)
    
    # Health check
    print("\n⚡ CHECKING LLM HEALTH...")
    health = await router.health_check()
    
    print(f"\nLOCAL CPU: {'✅' if health['local']['healthy'] else '❌'} {health['local']['model']}")
    if not health['local']['healthy']:
        print(f"  Error: {health['local']['error']}")
        
    print(f"OMEN-40L:  {'✅' if health['omen']['healthy'] else '❌'} {health['omen']['model']}")
    if not health['omen']['healthy']:
        print(f"  Error: {health['omen']['error']}")
        
    print("\n" + "=" * 80)
    
    # Test queries
    test_queries = [
        ("Hello, how are you?", False),
        ("Explain async/await in Python", False),
        ("Refactor this 500-line class for better performance and maintainability", True),
        ("Design a microservices architecture for e-commerce", True)
    ]
    
    for query, expected_omen in test_queries:
        print(f"\n📝 QUERY: {query[:50]}...")
        query_type = router.classify_query(query)
        will_use_omen = router.should_use_omen(query_type)
        
        print(f"   Type: {query_type.value}")
        print(f"   Route: {'OMEN-40L' if will_use_omen else 'LOCAL CPU'}")
        print(f"   Expected: {'OMEN-40L' if expected_omen else 'LOCAL CPU'}")
        print(f"   Match: {'✅' if will_use_omen == expected_omen else '❌'}")
        
    print("\n" + "=" * 80)
    print("✅ HYBRID ROUTER READY")

if __name__ == "__main__":
    asyncio.run(main())
