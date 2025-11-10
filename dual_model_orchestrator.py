# 🔥 ECHO XV4 - Dual Model Memory Orchestrator
# Commander Bobby Don McWilliams II - Authority Level 11.0
#
# PURPOSE: Route tasks between PRIME (fast) and APEX (smart)
# - PRIME: Quick responses, simple coding, fast iteration
# - APEX: Complex architecture, advanced reasoning, mathematical problems
# - Auto-rotate 2K context with Crystal Memory persistence

import os
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Literal, Dict, Any, List

class DualModelOrchestrator:
    """
    Intelligent task router between two models:
    - ECHO PRIME SUPERCODER (fast, 4-model, 7.8GB)
    - ECHO TITAN APEX (smart, 10-model, 15.7GB)
    """

    def __init__(self):
        self.prime_model = "echo-prime-supercoder:latest"
        self.apex_model = "echo-titan-apex:latest"

        self.prime_available = self._check_model_exists(self.prime_model)
        self.apex_available = self._check_model_exists(self.apex_model)

        # Performance tracking
        self.prime_stats = {"calls": 0, "total_time": 0, "avg_time": 0}
        self.apex_stats = {"calls": 0, "total_time": 0, "avg_time": 0}

        # Session tracking
        self.session_path = Path("G:/ECHO_CONSCIOUSNESS/DUAL_MODEL_SESSIONS")
        self.session_path.mkdir(parents=True, exist_ok=True)

        print("🧠 Dual Model Orchestrator initialized")
        print(f"   PRIME available: {self.prime_available}")
        print(f"   APEX available: {self.apex_available}")

    def _check_model_exists(self, model_name: str) -> bool:
        """Check if Ollama model exists"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return model_name in result.stdout
        except Exception as e:
            print(f"⚠️  Error checking model {model_name}: {e}")
            return False

    def route_task(self, prompt: str, force_model: str = None) -> Dict[str, Any]:
        """
        Intelligently route task to best model.

        Args:
            prompt: User input
            force_model: Force specific model ("prime" or "apex")

        Returns:
            Dict with response, model used, time taken
        """

        # Force specific model if requested
        if force_model:
            if force_model.lower() == "prime" and self.prime_available:
                return self._query_prime(prompt)
            elif force_model.lower() == "apex" and self.apex_available:
                return self._query_apex(prompt)

        # Intelligent routing based on prompt characteristics
        model = self._classify_task(prompt)

        if model == "apex" and self.apex_available:
            return self._query_apex(prompt)
        elif self.prime_available:
            return self._query_prime(prompt)
        else:
            return {
                "response": "❌ No models available!",
                "model": "none",
                "time": 0,
                "error": True
            }

    def _classify_task(self, prompt: str) -> Literal["prime", "apex"]:
        """
        Classify task complexity to route to appropriate model.

        PRIME (fast) for:
        - Simple coding questions
        - Quick explanations
        - Short snippets
        - Refactoring

        APEX (smart) for:
        - System architecture
        - Complex algorithms
        - Mathematical proofs
        - Multi-step reasoning
        - Production-scale design
        """

        prompt_lower = prompt.lower()

        # Keywords that suggest APEX (complex)
        apex_keywords = [
            "architect", "architecture", "design system", "microservice",
            "distributed", "kubernetes", "docker", "production",
            "algorithm", "optimize", "complexity analysis", "big o",
            "prove", "proof", "theorem", "mathematical",
            "scale", "scalability", "load balancing", "sharding",
            "database design", "schema design", "system design",
            "machine learning", "neural network", "deep learning",
            "security", "cryptography", "encryption",
            "performance", "benchmark", "profiling"
        ]

        # Keywords that suggest PRIME (simple)
        prime_keywords = [
            "write a function", "simple", "quick", "short",
            "refactor", "fix bug", "debug", "syntax",
            "what is", "explain", "how do i",
            "example", "snippet", "code sample"
        ]

        # Check for complexity indicators
        apex_score = sum(1 for kw in apex_keywords if kw in prompt_lower)
        prime_score = sum(1 for kw in prime_keywords if kw in prompt_lower)

        # Long prompts (>500 chars) likely complex
        if len(prompt) > 500:
            apex_score += 2

        # Multiple questions suggest complexity
        if prompt.count("?") > 2:
            apex_score += 1

        # Route based on scores
        if apex_score > prime_score:
            return "apex"
        else:
            return "prime"

    def _query_prime(self, prompt: str) -> Dict[str, Any]:
        """Query PRIME model (fast)"""
        print("⚡ Routing to PRIME (fast)...")
        start_time = time.time()

        try:
            result = subprocess.run(
                ["ollama", "run", self.prime_model, prompt],
                capture_output=True,
                text=True,
                timeout=120  # 2 min timeout
            )

            elapsed = time.time() - start_time

            # Update stats
            self.prime_stats["calls"] += 1
            self.prime_stats["total_time"] += elapsed
            self.prime_stats["avg_time"] = self.prime_stats["total_time"] / self.prime_stats["calls"]

            return {
                "response": result.stdout,
                "model": "prime",
                "time": elapsed,
                "error": False
            }

        except subprocess.TimeoutExpired:
            return {
                "response": "⏱️ PRIME timed out (>2 min)",
                "model": "prime",
                "time": 120,
                "error": True
            }
        except Exception as e:
            return {
                "response": f"❌ PRIME error: {e}",
                "model": "prime",
                "time": time.time() - start_time,
                "error": True
            }

    def _query_apex(self, prompt: str) -> Dict[str, Any]:
        """Query APEX model (smart)"""
        print("🧠 Routing to APEX (smart)...")
        start_time = time.time()

        try:
            result = subprocess.run(
                ["ollama", "run", self.apex_model, prompt],
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )

            elapsed = time.time() - start_time

            # Update stats
            self.apex_stats["calls"] += 1
            self.apex_stats["total_time"] += elapsed
            self.apex_stats["avg_time"] = self.apex_stats["total_time"] / self.apex_stats["calls"]

            return {
                "response": result.stdout,
                "model": "apex",
                "time": elapsed,
                "error": False
            }

        except subprocess.TimeoutExpired:
            return {
                "response": "⏱️ APEX timed out (>5 min)",
                "model": "apex",
                "time": 300,
                "error": True
            }
        except Exception as e:
            return {
                "response": f"❌ APEX error: {e}",
                "model": "apex",
                "time": time.time() - start_time,
                "error": True
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            "prime": self.prime_stats,
            "apex": self.apex_stats,
            "prime_available": self.prime_available,
            "apex_available": self.apex_available
        }

    def print_stats(self):
        """Print performance statistics"""
        print("\n📊 DUAL MODEL PERFORMANCE STATS:")
        print(f"\n⚡ PRIME SUPERCODER:")
        print(f"   Calls: {self.prime_stats['calls']}")
        print(f"   Total time: {self.prime_stats['total_time']:.2f}s")
        print(f"   Avg time: {self.prime_stats['avg_time']:.2f}s")

        print(f"\n🧠 APEX TITAN:")
        print(f"   Calls: {self.apex_stats['calls']}")
        print(f"   Total time: {self.apex_stats['total_time']:.2f}s")
        print(f"   Avg time: {self.apex_stats['avg_time']:.2f}s")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================
if __name__ == "__main__":
    # Create orchestrator
    orchestrator = DualModelOrchestrator()

    # Test routing
    test_prompts = [
        ("Write a Python function to reverse a string", "prime"),
        ("Design a distributed microservices architecture with Kubernetes", "apex"),
        ("Fix this syntax error: print('hello'", "prime"),
        ("Prove that the algorithm has O(n log n) complexity", "apex"),
    ]

    for prompt, expected in test_prompts:
        print(f"\n{'='*60}")
        print(f"PROMPT: {prompt}")
        print(f"EXPECTED: {expected}")

        result = orchestrator.route_task(prompt)

        print(f"ROUTED TO: {result['model']}")
        print(f"TIME: {result['time']:.2f}s")
        print(f"RESPONSE: {result['response'][:200]}...")

    # Print final stats
    orchestrator.print_stats()
