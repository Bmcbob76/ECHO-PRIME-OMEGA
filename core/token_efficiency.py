#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Token Efficiency System
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Track and optimize token usage:
- Monitor API token consumption
- Suggest crystal memory vs API
- Authority-based token allocation
- Token budget management
- Efficiency reporting
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger("TokenEfficiency")


class TokenEfficiency:
    """
    Token Efficiency System
    
    Features:
    - Track token usage per operation
    - Crystal memory savings tracking
    - Authority-based token budgets
    - Efficiency recommendations
    - Usage reports and analytics
    - Token budget alerts
    """
    
    def __init__(self, config: Dict):
        """Initialize Token Efficiency System"""
        self.config = config
        self.token_config = config.get('token_efficiency', {})
        
        # Settings
        self.enabled = self.token_config.get('enabled', True)
        self.track_per_operation = self.token_config.get('track_per_operation', True)
        self.alert_on_high_usage = self.token_config.get('alert_on_high_usage', True)
        
        # Token budgets by authority level
        self.authority_budgets = {
            11.0: float('inf'),  # Commander - Unlimited
            10: 1000000,  # Sovereign Architect
            9: 500000,   # Heir
            8: 250000,   # Bloodline
            7: 100000,   # Bloodline
            6: 50000,    # Engineer
            5: 25000,    # Developer
            4: 10000,    # Operator
            3: 5000,     # Analyst
            2: 2500,     # Observer
            1: 1000,     # Guest
            0: 500       # Public
        }
        
        # Usage tracking
        self.total_tokens_used = 0
        self.total_tokens_saved = 0  # Via crystal memory
        self.operations_tracked = 0
        
        # Per-operation tracking
        self.operation_history = []
        self.max_history = self.token_config.get('max_history_entries', 1000)
        
        # Per-user/authority tracking
        self.user_usage = defaultdict(lambda: {
            'tokens_used': 0,
            'operations': 0,
            'last_operation': None
        })
        
        # Efficiency thresholds
        self.efficiency_thresholds = {
            'excellent': 0.9,  # >90% token efficiency
            'good': 0.7,       # >70% efficiency
            'acceptable': 0.5, # >50% efficiency
            'poor': 0.3,       # >30% efficiency
            'critical': 0.0    # ≤30% efficiency
        }
        
        # Components
        self.crystal_memory = None
        self.voice_system = None
        
        logger.info("Token Efficiency System initialized")
        logger.info(f"   Tracking per operation: {self.track_per_operation}")
        logger.info(f"   Alert on high usage: {self.alert_on_high_usage}")
    
    def set_crystal_memory(self, crystal_memory):
        """Set Crystal Memory reference"""
        self.crystal_memory = crystal_memory
    
    def set_voice_system(self, voice):
        """Set Voice System reference"""
        self.voice_system = voice
    
    async def track_operation(self, operation_name: str, tokens_used: int, 
                             authority_level: float = 0, user: str = "system") -> bool:
        """
        Track token usage for an operation
        
        Args:
            operation_name: Name of operation
            tokens_used: Tokens consumed
            authority_level: User's authority level
            user: User identifier
        
        Returns:
            True if within budget, False if over budget
        """
        if not self.enabled:
            return True
        
        try:
            self.operations_tracked += 1
            self.total_tokens_used += tokens_used
            
            # Track per-user usage
            self.user_usage[user]['tokens_used'] += tokens_used
            self.user_usage[user]['operations'] += 1
            self.user_usage[user]['last_operation'] = datetime.now()
            
            # Add to history
            if self.track_per_operation:
                operation_record = {
                    'timestamp': datetime.now(),
                    'operation': operation_name,
                    'tokens': tokens_used,
                    'user': user,
                    'authority_level': authority_level
                }
                
                self.operation_history.append(operation_record)
                
                # Trim history if needed
                if len(self.operation_history) > self.max_history:
                    self.operation_history = self.operation_history[-self.max_history:]
            
            # Check budget
            budget = self.authority_budgets.get(authority_level, 1000)
            user_tokens = self.user_usage[user]['tokens_used']
            
            within_budget = user_tokens <= budget
            
            # Alert if approaching budget
            if self.alert_on_high_usage and user_tokens > budget * 0.8:
                await self._alert_high_usage(user, user_tokens, budget, authority_level)
            
            logger.info(f"📊 Tracked: {operation_name} - {tokens_used} tokens (User: {user})")
            
            return within_budget
        
        except Exception as e:
            logger.error(f"Failed to track operation: {e}")
            return True
    
    async def _alert_high_usage(self, user: str, current: int, budget: int, authority: float):
        """Alert about high token usage"""
        percentage = (current / budget) * 100
        
        logger.warning(f"⚠️ High token usage: {user} at {percentage:.1f}% of budget")
        
        # Voice alert if available
        if self.voice_system and authority < 11.0:  # Don't alert Commander
            await self.voice_system.speak(
                "echo",
                f"Token usage alert: {user} has used {percentage:.0f}% of their budget."
            )
    
    async def suggest_optimization(self, query: str) -> Dict:
        """
        Suggest optimization for a query
        
        Args:
            query: Query to analyze
        
        Returns:
            Optimization suggestions
        """
        suggestions = {
            'use_crystal_memory': False,
            'estimated_tokens': 0,
            'estimated_savings': 0,
            'recommendation': ''
        }
        
        try:
            # Estimate tokens for query (rough: 1 token ~ 4 chars)
            estimated_tokens = len(query) // 4
            
            suggestions['estimated_tokens'] = estimated_tokens
            
            # Check if crystal memory could help
            if self.crystal_memory:
                found, content = await self.crystal_memory.search_before_api_call(query)
                
                if found:
                    # Crystal memory found answer
                    suggestions['use_crystal_memory'] = True
                    suggestions['estimated_savings'] = estimated_tokens
                    suggestions['recommendation'] = "Use crystal memory - answer found in existing crystals"
                else:
                    suggestions['recommendation'] = "API call required - no crystal match found"
            else:
                suggestions['recommendation'] = "API call required - crystal memory not available"
            
            return suggestions
        
        except Exception as e:
            logger.error(f"Failed to suggest optimization: {e}")
            return suggestions
    
    def track_crystal_savings(self, tokens_saved: int):
        """Track tokens saved by using crystal memory"""
        self.total_tokens_saved += tokens_saved
        logger.info(f"💎 Crystal memory saved {tokens_saved} tokens")
    
    def calculate_efficiency(self) -> float:
        """
        Calculate overall token efficiency
        
        Returns:
            Efficiency ratio (0.0 to 1.0)
        """
        if self.total_tokens_used == 0:
            return 1.0
        
        # Efficiency = tokens saved / (tokens used + tokens saved)
        total_potential = self.total_tokens_used + self.total_tokens_saved
        
        if total_potential == 0:
            return 1.0
        
        efficiency = self.total_tokens_saved / total_potential
        return efficiency
    
    def get_efficiency_rating(self, efficiency: float) -> str:
        """Get efficiency rating from ratio"""
        if efficiency >= self.efficiency_thresholds['excellent']:
            return "EXCELLENT"
        elif efficiency >= self.efficiency_thresholds['good']:
            return "GOOD"
        elif efficiency >= self.efficiency_thresholds['acceptable']:
            return "ACCEPTABLE"
        elif efficiency >= self.efficiency_thresholds['poor']:
            return "POOR"
        else:
            return "CRITICAL"
    
    def get_user_usage(self, user: str) -> Dict:
        """Get token usage for specific user"""
        return dict(self.user_usage.get(user, {}))
    
    def get_recent_operations(self, limit: int = 10) -> List[Dict]:
        """Get recent operations"""
        return self.operation_history[-limit:] if self.operation_history else []
    
    def get_efficiency_report(self) -> Dict:
        """Generate efficiency report"""
        efficiency = self.calculate_efficiency()
        rating = self.get_efficiency_rating(efficiency)
        
        # Calculate per-operation average
        avg_tokens_per_op = (self.total_tokens_used / self.operations_tracked 
                            if self.operations_tracked > 0 else 0)
        
        # Top users by usage
        top_users = sorted(
            self.user_usage.items(),
            key=lambda x: x[1]['tokens_used'],
            reverse=True
        )[:5]
        
        return {
            'total_tokens_used': self.total_tokens_used,
            'total_tokens_saved': self.total_tokens_saved,
            'operations_tracked': self.operations_tracked,
            'efficiency_ratio': efficiency,
            'efficiency_rating': rating,
            'avg_tokens_per_operation': avg_tokens_per_op,
            'top_users': [
                {
                    'user': user,
                    'tokens_used': data['tokens_used'],
                    'operations': data['operations']
                }
                for user, data in top_users
            ]
        }
    
    def get_statistics(self) -> Dict:
        """Get token efficiency statistics"""
        efficiency = self.calculate_efficiency()
        
        return {
            'enabled': self.enabled,
            'total_tokens_used': self.total_tokens_used,
            'total_tokens_saved': self.total_tokens_saved,
            'efficiency_ratio': efficiency,
            'efficiency_rating': self.get_efficiency_rating(efficiency),
            'operations_tracked': self.operations_tracked,
            'unique_users': len(self.user_usage),
            'history_size': len(self.operation_history)
        }
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.total_tokens_used = 0
        self.total_tokens_saved = 0
        self.operations_tracked = 0
        self.operation_history.clear()
        self.user_usage.clear()
        logger.info("Token efficiency statistics reset")


# Export
__all__ = ['TokenEfficiencySystem']
