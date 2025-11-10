"""
Load Balancing System
Distributes server load intelligently across available resources

Authority Level: 11.0
Commander Bobby Don McWilliams II
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import psutil
from collections import defaultdict

logger = logging.getLogger(__name__)

class LoadBalancer:
    """Intelligent load distribution for MLS servers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.strategy = config.get('balancing_strategy', 'round_robin')
        self.max_load_per_server = config.get('max_load_per_server', 80)
        
        # Server load tracking
        self.server_loads = defaultdict(lambda: {
            'cpu': 0,
            'memory': 0,
            'requests': 0,
            'last_assigned': None
        })
        
        # Request tracking
        self.request_counter = 0
        self.last_assigned_index = 0
        
        # Available strategies
        self.strategies = {
            'round_robin': self._round_robin,
            'least_connections': self._least_connections,
            'least_load': self._least_load,
            'weighted': self._weighted,
            'random': self._random
        }
        
        logger.info(f"Load Balancer initialized (strategy: {self.strategy})")
    
    def get_server_load(self, server_name: str) -> Dict[str, Any]:
        """Get current load for a server"""
        return self.server_loads[server_name]
    
    def update_server_load(self, server_name: str, cpu: float, memory: float):
        """Update server load metrics"""
        self.server_loads[server_name]['cpu'] = cpu
        self.server_loads[server_name]['memory'] = memory
        self.server_loads[server_name]['last_update'] = datetime.now()
    
    def _round_robin(self, servers: List[str]) -> str:
        """Round-robin strategy"""
        if not servers:
            return None
        
        self.last_assigned_index = (self.last_assigned_index + 1) % len(servers)
        return servers[self.last_assigned_index]
    
    def _least_connections(self, servers: List[str]) -> str:
        """Assign to server with fewest connections"""
        if not servers:
            return None
        
        server_loads = [(s, self.server_loads[s]['requests']) for s in servers]
        server_loads.sort(key=lambda x: x[1])
        return server_loads[0][0]
    
    def _least_load(self, servers: List[str]) -> str:
        """Assign to server with lowest resource usage"""
        if not servers:
            return None
        
        server_loads = []
        for s in servers:
            load = self.server_loads[s]
            total_load = (load['cpu'] + load['memory']) / 2
            server_loads.append((s, total_load))
        
        server_loads.sort(key=lambda x: x[1])
        return server_loads[0][0]
    
    def _weighted(self, servers: List[str]) -> str:
        """Weighted distribution based on server capacity"""
        # This would use server capacity weights from config
        # For now, fallback to least_load
        return self._least_load(servers)
    
    def _random(self, servers: List[str]) -> str:
        """Random distribution"""
        if not servers:
            return None
        
        import random
        return random.choice(servers)
    
    def assign_server(self, servers: List[str]) -> Optional[str]:
        """Assign a server using the configured strategy"""
        if not servers:
            logger.warning("⚠️ No servers available for assignment")
            return None
        
        # Filter out overloaded servers
        available = []
        for server in servers:
            load = self.server_loads[server]
            if load['cpu'] < self.max_load_per_server and \
               load['memory'] < self.max_load_per_server:
                available.append(server)
        
        if not available:
            logger.warning("⚠️ All servers overloaded, using all servers")
            available = servers
        
        # Use strategy to select server
        strategy_func = self.strategies.get(self.strategy, self._round_robin)
        selected = strategy_func(available)
        
        if selected:
            self.server_loads[selected]['requests'] += 1
            self.server_loads[selected]['last_assigned'] = datetime.now()
            self.request_counter += 1
        
        return selected
    
    def release_server(self, server_name: str):
        """Release server after request completion"""
        if server_name in self.server_loads:
            self.server_loads[server_name]['requests'] = max(
                0,
                self.server_loads[server_name]['requests'] - 1
            )
    
    def get_load_distribution(self) -> Dict[str, Any]:
        """Get current load distribution across servers"""
        distribution = {}
        
        for server, load in self.server_loads.items():
            distribution[server] = {
                'cpu': load['cpu'],
                'memory': load['memory'],
                'requests': load['requests'],
                'last_assigned': load['last_assigned'].isoformat() if load['last_assigned'] else None
            }
        
        return distribution
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get load balancing statistics"""
        stats = {
            'strategy': self.strategy,
            'total_requests': self.request_counter,
            'servers': len(self.server_loads),
            'distribution': self.get_load_distribution(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate average loads
        if self.server_loads:
            total_cpu = sum(s['cpu'] for s in self.server_loads.values())
            total_memory = sum(s['memory'] for s in self.server_loads.values())
            total_requests = sum(s['requests'] for s in self.server_loads.values())
            
            stats['averages'] = {
                'cpu': total_cpu / len(self.server_loads),
                'memory': total_memory / len(self.server_loads),
                'requests': total_requests / len(self.server_loads)
            }
        
        return stats
    
    def rebalance_if_needed(self) -> List[str]:
        """Check if rebalancing is needed and return recommendations"""
        recommendations = []
        
        if not self.server_loads:
            return recommendations
        
        # Calculate load variance
        loads = [(s, (l['cpu'] + l['memory']) / 2) 
                 for s, l in self.server_loads.items()]
        
        if not loads:
            return recommendations
        
        avg_load = sum(l[1] for l in loads) / len(loads)
        
        # Find overloaded and underloaded servers
        for server, load in loads:
            if load > avg_load * 1.5:
                recommendations.append({
                    'type': 'reduce_load',
                    'server': server,
                    'current_load': load,
                    'target_load': avg_load
                })
            elif load < avg_load * 0.5 and avg_load > 20:
                recommendations.append({
                    'type': 'increase_load',
                    'server': server,
                    'current_load': load,
                    'target_load': avg_load
                })
        
        return recommendations
    
    def set_strategy(self, strategy: str) -> bool:
        """Change load balancing strategy"""
        if strategy in self.strategies:
            self.strategy = strategy
            logger.info(f"✅ Load balancing strategy changed to: {strategy}")
            return True
        else:
            logger.warning(f"⚠️ Unknown strategy: {strategy}")
            return False


if __name__ == "__main__":
    # Test load balancer
    config = {
        'balancing_strategy': 'least_load',
        'max_load_per_server': 80
    }
    
    lb = LoadBalancer(config)
    
    # Simulate servers
    servers = ['server1', 'server2', 'server3']
    
    # Update loads
    lb.update_server_load('server1', 50, 60)
    lb.update_server_load('server2', 30, 40)
    lb.update_server_load('server3', 70, 80)
    
    # Assign servers
    for i in range(10):
        selected = lb.assign_server(servers)
        print(f"Request {i+1} assigned to: {selected}")
    
    # Show statistics
    import json
    print("\nLoad Statistics:")
    print(json.dumps(lb.get_statistics(), indent=2))
