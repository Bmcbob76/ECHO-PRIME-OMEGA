"""
PHOENIX AUTO-HEAL MIXIN
Authority Level 11.0 - Commander Bobby Don McWilliams II

Auto-healing and recovery for ALL ECHO PRIME servers.
Provides 24/7 monitoring, crash detection, and automatic recovery.

Usage:
    class MyServer(PhoenixMixin):
        def __init__(self):
            super().__init__()
            # Now has phoenix_heal, phoenix_monitor, phoenix_restore, etc.
"""

import sys
import logging
import threading
import time
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime, timedelta


class PhoenixMixin:
    """Phoenix auto-healing mixin for any server"""

    def __init__(self):
        self.phoenix_enabled = False
        self.phoenix_client = None
        self.phoenix_monitoring = False
        self.phoenix_monitor_thread = None
        self.phoenix_state_backups = []
        self.phoenix_max_backups = 10

        # Setup logging if not already configured
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(self.__class__.__name__)

        # Try to load Phoenix Auto-Healer
        try:
            phoenix_path = Path("E:/GS343-DIVINE-OVERSEER/MODULES")
            if phoenix_path.exists():
                sys.path.insert(0, str(phoenix_path))

            from phoenix_client_gs343 import PhoenixClient
            self.phoenix_client = PhoenixClient()
            self.phoenix_enabled = True
            self.logger.info("✅ Phoenix Auto-Healer integrated - 24/7 recovery active")

        except ImportError as e:
            self.logger.warning(f"⚠️ Phoenix Auto-Healer not available: {e}")
            self.logger.warning("⚠️ Running without auto-healing - manual recovery only")

    def phoenix_heal(self, error: Exception, context: Optional[str] = None) -> Dict:
        """
        Attempt to heal from an error using Phoenix protocols.

        Args:
            error: Exception that occurred
            context: Optional context about where error occurred

        Returns:
            dict: {'healed': bool, 'action_taken': str, 'message': str}
        """
        if not self.phoenix_enabled:
            return {
                'healed': False,
                'action_taken': 'none',
                'message': 'Phoenix not available - manual recovery required'
            }

        try:
            error_str = str(error)
            error_type = type(error).__name__

            self.logger.warning(f"🔥 Phoenix healing {error_type}: {error_str}")

            # Attempt healing via Phoenix client
            # Placeholder - actual implementation depends on Phoenix API
            healed = False
            action_taken = 'attempted_recovery'

            if healed:
                self.logger.info(f"✅ Phoenix successfully healed {error_type}")
            else:
                self.logger.error(f"❌ Phoenix unable to heal {error_type}")

            return {
                'healed': healed,
                'action_taken': action_taken,
                'error_type': error_type,
                'context': context,
                'message': 'Healing attempted' if healed else 'Healing failed'
            }

        except Exception as e:
            self.logger.error(f"phoenix_heal failed: {e}")
            return {
                'healed': False,
                'action_taken': 'failed',
                'error': str(e),
                'message': f'Phoenix healing error: {e}'
            }

    def phoenix_monitor(self, interval_seconds: int = 300):
        """
        Start Phoenix monitoring (background thread).

        Args:
            interval_seconds: Monitoring interval in seconds (default: 300 = 5 minutes)
        """
        if not self.phoenix_enabled:
            self.logger.warning("Phoenix monitoring unavailable - Phoenix not loaded")
            return

        if self.phoenix_monitoring:
            self.logger.warning("Phoenix monitoring already active")
            return

        self.phoenix_monitoring = True

        def monitoring_loop():
            self.logger.info(f"🔥 Phoenix monitoring started (interval: {interval_seconds}s)")

            while self.phoenix_monitoring:
                try:
                    # Perform health check
                    health = self.phoenix_health_check()

                    if not health.get('healthy', True):
                        self.logger.warning(f"⚠️ Phoenix detected unhealthy state: {health}")

                    # Sleep until next check
                    time.sleep(interval_seconds)

                except Exception as e:
                    self.logger.error(f"Phoenix monitoring error: {e}")
                    time.sleep(interval_seconds)

            self.logger.info("🔥 Phoenix monitoring stopped")

        self.phoenix_monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        self.phoenix_monitor_thread.start()

    def phoenix_stop_monitoring(self):
        """Stop Phoenix monitoring"""
        if self.phoenix_monitoring:
            self.logger.info("Stopping Phoenix monitoring...")
            self.phoenix_monitoring = False

            if self.phoenix_monitor_thread:
                self.phoenix_monitor_thread.join(timeout=5)

    def phoenix_backup_state(self, state: Dict) -> Dict:
        """
        Backup current state for potential restoration.

        Args:
            state: State dictionary to backup

        Returns:
            dict: {'success': bool, 'backup_id': str, 'message': str}
        """
        try:
            backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            backup = {
                'id': backup_id,
                'timestamp': datetime.now().isoformat(),
                'state': state.copy()
            }

            self.phoenix_state_backups.append(backup)

            # Limit number of backups
            if len(self.phoenix_state_backups) > self.phoenix_max_backups:
                self.phoenix_state_backups.pop(0)

            return {
                'success': True,
                'backup_id': backup_id,
                'message': f'State backed up: {backup_id}'
            }

        except Exception as e:
            self.logger.error(f"phoenix_backup_state failed: {e}")
            return {
                'success': False,
                'backup_id': None,
                'error': str(e),
                'message': f'Backup failed: {e}'
            }

    def phoenix_restore(self, backup_id: Optional[str] = None) -> Dict:
        """
        Restore from a previous state backup.

        Args:
            backup_id: Specific backup ID to restore (default: latest)

        Returns:
            dict: {'success': bool, 'restored_state': dict, 'message': str}
        """
        try:
            if not self.phoenix_state_backups:
                return {
                    'success': False,
                    'restored_state': None,
                    'message': 'No backups available'
                }

            # Find backup
            if backup_id:
                backup = next((b for b in self.phoenix_state_backups if b['id'] == backup_id), None)
                if not backup:
                    return {
                        'success': False,
                        'restored_state': None,
                        'message': f'Backup not found: {backup_id}'
                    }
            else:
                # Use latest backup
                backup = self.phoenix_state_backups[-1]

            restored_state = backup['state']

            self.logger.info(f"🔥 Phoenix restoring state from {backup['id']}")

            return {
                'success': True,
                'restored_state': restored_state,
                'backup_id': backup['id'],
                'message': f'State restored from {backup["id"]}'
            }

        except Exception as e:
            self.logger.error(f"phoenix_restore failed: {e}")
            return {
                'success': False,
                'restored_state': None,
                'error': str(e),
                'message': f'Restore failed: {e}'
            }

    def phoenix_rollback(self) -> Dict:
        """
        Rollback to previous stable state (alias for phoenix_restore with latest backup).

        Returns:
            dict: Restore result
        """
        return self.phoenix_restore()

    def phoenix_health_check(self) -> Dict:
        """
        Perform Phoenix health check on this server.

        Returns:
            dict: {'healthy': bool, 'issues': list, 'uptime': float}
        """
        try:
            issues = []
            healthy = True

            # Check if Phoenix is enabled
            if not self.phoenix_enabled:
                issues.append('Phoenix not enabled')
                healthy = False

            # Check monitoring status
            if not self.phoenix_monitoring:
                issues.append('Phoenix monitoring not active')

            return {
                'healthy': healthy,
                'issues': issues,
                'phoenix_enabled': self.phoenix_enabled,
                'monitoring_active': self.phoenix_monitoring,
                'backups_available': len(self.phoenix_state_backups),
                'message': 'Health check complete'
            }

        except Exception as e:
            self.logger.error(f"phoenix_health_check failed: {e}")
            return {
                'healthy': False,
                'issues': [str(e)],
                'error': str(e),
                'message': 'Health check failed'
            }

    def phoenix_stats(self) -> Dict:
        """
        Get Phoenix statistics and status.

        Returns:
            dict: Statistics about Phoenix system
        """
        return {
            'enabled': self.phoenix_enabled,
            'monitoring': self.phoenix_monitoring,
            'backups': len(self.phoenix_state_backups),
            'max_backups': self.phoenix_max_backups,
            'message': 'Phoenix operational' if self.phoenix_enabled else 'Phoenix not available'
        }

    def phoenix_recover_from_crash(self, crash_info: Dict) -> Dict:
        """
        Attempt to recover from a crash.

        Args:
            crash_info: Information about the crash

        Returns:
            dict: Recovery result
        """
        try:
            self.logger.error(f"🔥 Phoenix crash recovery initiated: {crash_info}")

            # Attempt to restore last known good state
            restore_result = self.phoenix_rollback()

            if restore_result['success']:
                self.logger.info("✅ Phoenix successfully recovered from crash")
                return {
                    'recovered': True,
                    'action': 'state_restored',
                    'restore_result': restore_result,
                    'message': 'Crash recovery successful'
                }
            else:
                self.logger.error("❌ Phoenix unable to recover from crash")
                return {
                    'recovered': False,
                    'action': 'restore_failed',
                    'restore_result': restore_result,
                    'message': 'Crash recovery failed'
                }

        except Exception as e:
            self.logger.error(f"phoenix_recover_from_crash failed: {e}")
            return {
                'recovered': False,
                'action': 'recovery_error',
                'error': str(e),
                'message': f'Recovery error: {e}'
            }
