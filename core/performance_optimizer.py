"""
Performance Optimization System
Monitors and optimizes Master Launcher performance

Authority Level: 11.0
Commander Bobby Don McWilliams II
"""

import logging
import time
import psutil
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict
import functools

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Monitor and optimize system performance"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.optimization_enabled = config.get('optimization_enabled', True)
        
        # Performance tracking
        self.function_stats = defaultdict(lambda: {
            'calls': 0,
            'total_time': 0,
            'avg_time': 0,
            'min_time': float('inf'),
            'max_time': 0
        })
        
        self.optimization_history = []
        
        logger.info("Performance Optimizer initialized")
    
    def track_performance(self, func: Callable) -> Callable:
        """Decorator to track function performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.time() - start_time
                self._record_performance(func.__name__, elapsed)
        
        return wrapper
    
    def _record_performance(self, func_name: str, elapsed: float):
        """Record function performance metrics"""
        stats = self.function_stats[func_name]
        stats['calls'] += 1
        stats['total_time'] += elapsed
        stats['avg_time'] = stats['total_time'] / stats['calls']
        stats['min_time'] = min(stats['min_time'], elapsed)
        stats['max_time'] = max(stats['max_time'], elapsed)
    
    def get_slow_functions(self, threshold_ms: float = 100) -> List[Dict[str, Any]]:
        """Identify functions slower than threshold"""
        slow_functions = []
        
        for func_name, stats in self.function_stats.items():
            if stats['avg_time'] * 1000 > threshold_ms:
                slow_functions.append({
                    'function': func_name,
                    'avg_time_ms': stats['avg_time'] * 1000,
                    'calls': stats['calls'],
                    'total_time_s': stats['total_time']
                })
        
        return sorted(slow_functions, key=lambda x: x['avg_time_ms'], reverse=True)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_functions': len(self.function_stats),
            'total_calls': sum(s['calls'] for s in self.function_stats.values()),
            'slowest_functions': self.get_slow_functions(),
            'optimizations_applied': len(self.optimization_history)
        }
        
        return report
    
    def optimize_cache_size(self, current_size: int, hit_rate: float) -> int:
        """Calculate optimal cache size"""
        if hit_rate < 0.5:
            # Low hit rate, increase cache
            return int(current_size * 1.5)
        elif hit_rate > 0.9 and current_size > 100:
            # High hit rate, can reduce cache
            return int(current_size * 0.8)
        
        return current_size
    
    def recommend_optimizations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Check for slow functions
        slow_funcs = self.get_slow_functions(threshold_ms=50)
        for func in slow_funcs[:5]:  # Top 5
            recommendations.append({
                'type': 'slow_function',
                'priority': 'high',
                'target': func['function'],
                'issue': f"Average execution time: {func['avg_time_ms']:.2f}ms",
                'suggestions': [
                    'Add caching if function is deterministic',
                    'Profile to identify bottlenecks',
                    'Consider async execution'
                ]
            })
        
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        if cpu_percent > 80:
            recommendations.append({
                'type': 'high_cpu',
                'priority': 'high',
                'target': 'system',
                'issue': f"CPU usage at {cpu_percent}%",
                'suggestions': [
                    'Reduce concurrent operations',
                    'Optimize CPU-intensive functions',
                    'Consider load balancing'
                ]
            })
        
        if memory_percent > 80:
            recommendations.append({
                'type': 'high_memory',
                'priority': 'high',
                'target': 'system',
                'issue': f"Memory usage at {memory_percent}%",
                'suggestions': [
                    'Clear caches',
                    'Check for memory leaks',
                    'Reduce data retention'
                ]
            })
        
        return recommendations
    
    def auto_optimize(self) -> List[str]:
        """Automatically apply safe optimizations"""
        if not self.optimization_enabled:
            return []
        
        optimizations_applied = []
        
        # Get recommendations
        recommendations = self.recommend_optimizations()
        
        for rec in recommendations:
            if rec['type'] == 'high_memory' and rec['priority'] == 'high':
                # Safe optimization: trigger garbage collection
                import gc
                gc.collect()
                optimizations_applied.append("Triggered garbage collection")
                
                self.optimization_history.append({
                    'timestamp': datetime.now(),
                    'type': 'memory_cleanup',
                    'details': 'Garbage collection'
                })
        
        return optimizations_applied
    
    def benchmark_function(self, func: Callable, *args, iterations: int = 100, **kwargs) -> Dict[str, Any]:
        """Benchmark a function"""
        times = []
        
        for _ in range(iterations):
            start = time.time()
            func(*args, **kwargs)
            elapsed = time.time() - start
            times.append(elapsed)
        
        return {
            'function': func.__name__,
            'iterations': iterations,
            'avg_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
    
    def compare_implementations(self, implementations: Dict[str, Callable], 
                               *args, **kwargs) -> Dict[str, Any]:
        """Compare different implementations of same functionality"""
        results = {}
        
        for name, func in implementations.items():
            benchmark = self.benchmark_function(func, *args, iterations=50, **kwargs)
            results[name] = benchmark
        
        # Find fastest
        fastest = min(results.items(), key=lambda x: x[1]['avg_time'])
        
        return {
            'results': results,
            'fastest': fastest[0],
            'speedup': {
                name: results[fastest[0]]['avg_time'] / data['avg_time']
                for name, data in results.items()
                if name != fastest[0]
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed performance statistics"""
        stats = {
            'tracked_functions': len(self.function_stats),
            'total_calls': sum(s['calls'] for s in self.function_stats.values()),
            'total_time': sum(s['total_time'] for s in self.function_stats.values()),
            'top_time_consumers': [],
            'optimization_history': len(self.optimization_history)
        }
        
        # Get top time consumers
        sorted_funcs = sorted(
            self.function_stats.items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )
        
        for func_name, func_stats in sorted_funcs[:10]:
            stats['top_time_consumers'].append({
                'function': func_name,
                'total_time_s': func_stats['total_time'],
                'calls': func_stats['calls'],
                'avg_time_ms': func_stats['avg_time'] * 1000
            })
        
        return stats
    
    async def monitor_loop(self, interval: int = 300):
        """Continuous performance monitoring"""
        import asyncio
        
        logger.info("🔍 Performance monitoring started")
        
        while True:
            try:
                # Auto-optimize if enabled
                optimizations = self.auto_optimize()
                if optimizations:
                    for opt in optimizations:
                        logger.info(f"⚡ Applied optimization: {opt}")
                
                # Check for performance issues
                recommendations = self.recommend_optimizations()
                if recommendations:
                    logger.warning(f"⚠️ {len(recommendations)} performance issues detected")
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"❌ Performance monitoring error: {e}")
                await asyncio.sleep(interval)


if __name__ == "__main__":
    # Test performance optimizer
    import json
    
    config = {'optimization_enabled': True}
    optimizer = PerformanceOptimizer(config)
    
    # Track some sample functions
    @optimizer.track_performance
    def sample_function():
        time.sleep(0.1)
    
    # Run function multiple times
    for _ in range(10):
        sample_function()
    
    # Get report
    report = optimizer.get_performance_report()
    print(json.dumps(report, indent=2, default=str))
    
    # Get recommendations
    recommendations = optimizer.recommend_optimizations()
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec['type']}: {rec['issue']}")
