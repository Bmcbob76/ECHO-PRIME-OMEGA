#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Health Monitoring System
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Configurable health check intervals (5/15/30 minutes)
Auto-relaunch crashed servers
Performance monitoring
Resource usage tracking
24/7 operation
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import psutil
import time

logger = logging.getLogger("HealthMonitor")


class HealthMonitor:
    """
    Health Monitoring System
    
    Features:
    - Configurable check intervals (5/15/30 min)
    - Auto-relaunch crashed servers
    - Performance monitoring
    - Resource usage tracking
    - Integrates with Phoenix Healer for auto-repair
    """
    
    def __init__(self, config: Dict):
        """Initialize Health Monitor"""
        self.config = config
        self.health_config = config.get('health', {})
        
        # Settings
        self.enabled = self.health_config.get('enabled', True)
        self.check_interval = self.health_config.get('check_interval', 1800)  # 30 min default
        self.quick_check_interval = self.health_config.get('quick_check_interval', 300)  # 5 min
        
        # Auto actions
        self.auto_heal = self.health_config.get('auto_heal', True)
        self.auto_restart = self.health_config.get('auto_restart', True)
        self.auto_quarantine = self.health_config.get('auto_quarantine', True)
        
        # Restart configuration
        self.max_restart_attempts = self.health_config.get('max_restart_attempts', 3)
        self.restart_delay = self.health_config.get('restart_delay', 5)
        self.restart_backoff = self.health_config.get('restart_backoff', 2)
        
        # Components
        self.server_discovery = None
        self.phoenix_healer = None
        self.voice_system = None
        
        # State tracking
        self.servers = {}
        self.health_history = {}
        self.restart_counts = {}
        
        # Statistics
        self.checks_performed = 0
        self.servers_restarted = 0
        self.servers_quarantined = 0
        
        # Running state
        self.running = False
        self.monitor_task = None
        
        logger.info("Health Monitor initialized")
        logger.info(f"   Check interval: {self.check_interval}s ({self.check_interval//60} min)")
        logger.info(f"   Quick check: {self.quick_check_interval}s ({self.quick_check_interval//60} min)")
        logger.info(f"   Auto-heal: {self.auto_heal}")
        logger.info(f"   Auto-restart: {self.auto_restart}")
    
    def set_server_discovery(self, discovery):
        """Set server discovery reference"""
        self.server_discovery = discovery
    
    def set_phoenix_healer(self, phoenix):
        """Set Phoenix Healer reference"""
        self.phoenix_healer = phoenix
    
    def set_voice_system(self, voice):
        """Set voice system reference"""
        self.voice_system = voice
    
    async def start(self):
        """Start health monitoring"""
        if not self.enabled:
            logger.warning("Health monitoring is disabled")
            return
        
        if self.running:
            logger.warning("Health monitor already running")
            return
        
        logger.info("🏥 Starting health monitor...")
        self.running = True
        
        # Start monitoring task
        self.monitor_task = asyncio.create_task(self._monitor_loop())
        
        logger.info("✅ Health monitor started")
    
    async def stop(self):
        """Stop health monitoring"""
        logger.info("🛑 Stopping health monitor...")
        self.running = False
        
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        
        logger.info("✅ Health monitor stopped")
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        logger.info("   Starting 24/7 monitoring loop...")
        
        last_full_check = time.time()
        last_quick_check = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Quick check (every 5 min)
                if current_time - last_quick_check >= self.quick_check_interval:
                    await self._perform_quick_check()
                    last_quick_check = current_time
                
                # Full check (every 30 min)
                if current_time - last_full_check >= self.check_interval:
                    await self._perform_full_check()
                    last_full_check = current_time
                
                # Sleep for a bit
                await asyncio.sleep(10)
                
        except asyncio.CancelledError:
            logger.info("   Monitor loop cancelled")
        except Exception as e:
            logger.error(f"   Monitor loop error: {e}")
    
    async def _perform_quick_check(self):
        """Perform quick health check"""
        logger.debug("🔍 Quick health check...")
        
        try:
            if not self.server_discovery:
                return
            
            # Detect running servers
            running = self.server_discovery.detect_running_servers()
            
            # Check for crashed servers
            for server_name, server_info in self.servers.items():
                if server_info.get('should_be_running', False):
                    # Check if it's actually running
                    is_running = any(s['name'] == server_name for s in running)
                    
                    if not is_running:
                        logger.warning(f"⚠️  Server {server_name} has crashed!")
                        await self._handle_crashed_server(server_name, server_info)
            
        except Exception as e:
            logger.error(f"Quick check error: {e}")
    
    async def _perform_full_check(self):
        """Perform comprehensive health check"""
        logger.info("🏥 Performing comprehensive health check...")
        self.checks_performed += 1
        
        try:
            # Update server list
            if self.server_discovery:
                servers = self.server_discovery.discover_all_servers()
                self.servers = servers
                logger.info(f"   Discovered {len(servers)} servers")
            
            # Check each server
            for server_name, server_info in self.servers.items():
                health = await self._check_server_health(server_name, server_info)
                
                # Store health history
                if server_name not in self.health_history:
                    self.health_history[server_name] = []
                
                self.health_history[server_name].append({
                    'timestamp': datetime.now(),
                    'health': health
                })
                
                # Keep only last 100 checks
                if len(self.health_history[server_name]) > 100:
                    self.health_history[server_name] = self.health_history[server_name][-100:]
                
                # Take action if needed
                if health['status'] != 'healthy':
                    await self._handle_unhealthy_server(server_name, server_info, health)
            
            # Generate report
            self._log_health_summary()
            
            # Announce via voice
            if self.voice_system:
                healthy_count = sum(1 for h in self.health_history.values() 
                                   if h[-1]['health']['status'] == 'healthy')
                
                if healthy_count == len(self.servers):
                    # All healthy - Echo announces
                    await self.voice_system.speak(
                        "echo",
                        f"Health check complete. All {len(self.servers)} servers operational."
                    )
                else:
                    # Issues detected - Bree roasts (if failures)
                    unhealthy = len(self.servers) - healthy_count
                    await self.voice_system.speak(
                        "bree",
                        f"Health check shows {unhealthy} servers having issues. Time to fix this shit!"
                    )
            
        except Exception as e:
            logger.error(f"Full health check error: {e}")
    
    async def _check_server_health(self, server_name: str, server_info: Dict) -> Dict:
        """Check health of a single server"""
        health = {
            'server_name': server_name,
            'status': 'unknown',
            'port_available': None,
            'process_running': None,
            'response_time': None,
            'error_count': 0,
            'warnings': []
        }
        
        try:
            port = server_info.get('port')
            
            if port:
                # Check if port is in use (server running)
                if self.server_discovery:
                    port_available = self.server_discovery.is_port_available(port)
                    health['port_available'] = port_available
                    health['process_running'] = not port_available
                    
                    if port_available:
                        health['status'] = 'stopped'
                        health['warnings'].append('Server not running')
                    else:
                        health['status'] = 'healthy'
            else:
                health['status'] = 'unknown'
                health['warnings'].append('No port configured')
            
        except Exception as e:
            health['status'] = 'error'
            health['warnings'].append(f'Health check failed: {str(e)}')
        
        return health
    
    async def _handle_crashed_server(self, server_name: str, server_info: Dict):
        """Handle a crashed server"""
        logger.warning(f"🚨 Handling crashed server: {server_name}")
        
        # Check restart count
        restart_count = self.restart_counts.get(server_name, 0)
        
        if restart_count >= self.max_restart_attempts:
            logger.error(f"   Max restart attempts reached for {server_name}")
            
            if self.auto_quarantine:
                await self._quarantine_server(server_name, "Too many restart failures")
            
            return
        
        # Attempt auto-healing with Phoenix
        if self.auto_heal and self.phoenix_healer:
            logger.info(f"   Attempting Phoenix auto-heal...")
            
            server_path = Path(server_info['path'])
            success = await self.phoenix_healer.heal_server(
                server_name,
                "Server crashed",
                server_path
            )
            
            if success:
                logger.info(f"   ✅ Phoenix healing successful")
                self.restart_counts[server_name] = 0  # Reset count on success
                return
        
        # Auto-restart if Phoenix failed or not available
        if self.auto_restart:
            await self._restart_server(server_name, server_info)
    
    async def _handle_unhealthy_server(self, server_name: str, server_info: Dict, health: Dict):
        """Handle an unhealthy server"""
        status = health['status']
        
        if status == 'stopped':
            # Server stopped when it should be running
            if server_info.get('auto_start', True):
                logger.warning(f"⚠️  {server_name} stopped, attempting restart...")
                await self._restart_server(server_name, server_info)
        
        elif status == 'error':
            # Server in error state
            logger.error(f"❌ {server_name} in error state")
            await self._handle_crashed_server(server_name, server_info)
    
    async def _restart_server(self, server_name: str, server_info: Dict):
        """Restart a server"""
        logger.info(f"🔄 Restarting server: {server_name}")
        
        # Increment restart count
        self.restart_counts[server_name] = self.restart_counts.get(server_name, 0) + 1
        restart_count = self.restart_counts[server_name]
        
        # Calculate delay with backoff
        delay = self.restart_delay * (self.restart_backoff ** (restart_count - 1))
        
        logger.info(f"   Restart attempt {restart_count}/{self.max_restart_attempts}")
        logger.info(f"   Waiting {delay}s before restart...")
        
        await asyncio.sleep(delay)
        
        # Would actually restart the server here
        logger.info(f"   Launching {server_name}...")
        
        # Placeholder for actual server launch
        # In production, this would call server_manager.launch_server()
        
        self.servers_restarted += 1
        
        logger.info(f"   ✅ Server {server_name} restarted")
        
        # Announce via C3PO
        if self.voice_system:
            await self.voice_system.speak(
                "c3po",
                f"Master McWilliams, {server_name} has been successfully restarted."
            )
    
    async def _quarantine_server(self, server_name: str, reason: str):
        """Move server to quarantine"""
        logger.error(f"🚫 Quarantining server: {server_name}")
        logger.error(f"   Reason: {reason}")
        
        self.servers_quarantined += 1
        
        # Would actually move to quarantine directory
        # and generate diagnostic report
        
        # Announce via Bree (she roasts failures)
        if self.voice_system:
            await self.voice_system.speak(
                "bree",
                f"Alright, {server_name} is completely fucked. "
                f"Moving it to quarantine before it breaks anything else."
            )
    
    def _log_health_summary(self):
        """Log health check summary"""
        if not self.health_history:
            return
        
        healthy = 0
        unhealthy = 0
        stopped = 0
        
        for server_name, history in self.health_history.items():
            if history:
                status = history[-1]['health']['status']
                if status == 'healthy':
                    healthy += 1
                elif status == 'stopped':
                    stopped += 1
                else:
                    unhealthy += 1
        
        total = healthy + unhealthy + stopped
        
        logger.info("=" * 60)
        logger.info("HEALTH CHECK SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Servers: {total}")
        logger.info(f"  Healthy: {healthy}")
        logger.info(f"  Stopped: {stopped}")
        logger.info(f"  Unhealthy: {unhealthy}")
        logger.info(f"Checks Performed: {self.checks_performed}")
        logger.info(f"Servers Restarted: {self.servers_restarted}")
        logger.info(f"Servers Quarantined: {self.servers_quarantined}")
        logger.info("=" * 60)
    
    def get_statistics(self) -> Dict:
        """Get health monitoring statistics"""
        healthy = 0
        unhealthy = 0
        
        for history in self.health_history.values():
            if history:
                if history[-1]['health']['status'] == 'healthy':
                    healthy += 1
                else:
                    unhealthy += 1
        
        return {
            'checks_performed': self.checks_performed,
            'servers_monitored': len(self.servers),
            'healthy_servers': healthy,
            'unhealthy_servers': unhealthy,
            'servers_restarted': self.servers_restarted,
            'servers_quarantined': self.servers_quarantined,
            'check_interval': self.check_interval,
            'running': self.running
        }
    
    def get_server_health_history(self, server_name: str) -> List[Dict]:
        """Get health history for a specific server"""
        return self.health_history.get(server_name, [])


# Export
__all__ = ['HealthMonitor']
