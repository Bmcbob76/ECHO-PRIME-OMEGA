#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Backup Manager
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Auto-backup before every launch
File locking after successful operation
Backup file locking (prevents corruption)
Restore from backup on crash loop
"""

import os
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger("BackupManager")


class BackupManager:
    """
    Backup Manager
    
    Features:
    - Auto-backup before every launch
    - File locking after successful operation
    - Backup file locking (prevents corruption)
    - Restore from backup on crash loop
    - Timestamped backups
    - Backup rotation (keep last N backups)
    """
    
    def __init__(self, config: Dict):
        """Initialize Backup Manager"""
        self.config = config
        self.backup_config = config.get('backup', {})
        
        # Paths
        self.backup_dir = Path(config.get('paths', {}).get('backups', 'E:/ECHO_XV4/MLS/BACKUPS'))
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Settings
        self.enabled = self.backup_config.get('enabled', True)
        self.backup_before_launch = self.backup_config.get('backup_before_launch', True)
        self.lock_after_success = self.backup_config.get('lock_after_success', True)
        self.lock_backups = self.backup_config.get('lock_backups', True)
        self.max_backups = self.backup_config.get('max_backups', 10)
        
        # Auto-restore
        self.auto_restore_on_crash = self.backup_config.get('auto_restore_on_crash', True)
        self.crash_threshold = self.backup_config.get('crash_threshold', 3)
        
        # Statistics
        self.backups_created = 0
        self.backups_restored = 0
        self.files_locked = 0
        
        # Lock tracking
        self.locked_files = set()
        
        logger.info("Backup Manager initialized")
        logger.info(f"   Backup directory: {self.backup_dir}")
        logger.info(f"   Auto-backup: {self.backup_before_launch}")
        logger.info(f"   Lock after success: {self.lock_after_success}")
        logger.info(f"   Max backups: {self.max_backups}")
    
    def backup_file(self, file_path: Path, server_name: str) -> Optional[Path]:
        """
        Create backup of a file
        
        Args:
            file_path: Path to file to backup
            server_name: Name of server
        
        Returns:
            Path to backup file, or None on failure
        """
        if not self.enabled:
            return None
        
        try:
            if not file_path.exists():
                logger.warning(f"File not found for backup: {file_path}")
                return None
            
            # Create server backup directory
            server_backup_dir = self.backup_dir / server_name
            server_backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
            backup_path = server_backup_dir / backup_name
            
            # Copy file
            shutil.copy2(file_path, backup_path)
            
            # Lock backup file if configured
            if self.lock_backups:
                self._lock_file(backup_path)
            
            self.backups_created += 1
            logger.info(f"✅ Backup created: {backup_name}")
            
            # Rotate old backups
            self._rotate_backups(server_backup_dir)
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def backup_directory(self, dir_path: Path, server_name: str) -> Optional[Path]:
        """
        Create backup of entire directory
        
        Args:
            dir_path: Path to directory to backup
            server_name: Name of server
        
        Returns:
            Path to backup directory, or None on failure
        """
        if not self.enabled:
            return None
        
        try:
            if not dir_path.exists() or not dir_path.is_dir():
                logger.warning(f"Directory not found for backup: {dir_path}")
                return None
            
            # Create server backup directory
            server_backup_dir = self.backup_dir / server_name
            server_backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate backup directory name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{dir_path.name}_backup_{timestamp}"
            backup_path = server_backup_dir / backup_name
            
            # Copy directory
            shutil.copytree(dir_path, backup_path)
            
            self.backups_created += 1
            logger.info(f"✅ Directory backup created: {backup_name}")
            
            # Rotate old backups
            self._rotate_backups(server_backup_dir)
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create directory backup: {e}")
            return None
    
    def restore_latest_backup(self, server_name: str, target_path: Path) -> bool:
        """
        Restore latest backup for a server
        
        Args:
            server_name: Name of server
            target_path: Path to restore to
        
        Returns:
            Success status
        """
        try:
            server_backup_dir = self.backup_dir / server_name
            
            if not server_backup_dir.exists():
                logger.warning(f"No backups found for {server_name}")
                return False
            
            # Find latest backup
            backups = sorted(server_backup_dir.glob("*_backup_*"), reverse=True)
            
            if not backups:
                logger.warning(f"No backup files found for {server_name}")
                return False
            
            latest_backup = backups[0]
            
            logger.info(f"🔄 Restoring backup: {latest_backup.name}")
            
            # Unlock target if locked
            if target_path in self.locked_files:
                self._unlock_file(target_path)
            
            # Restore file/directory
            if latest_backup.is_dir():
                shutil.copytree(latest_backup, target_path, dirs_exist_ok=True)
            else:
                shutil.copy2(latest_backup, target_path)
            
            self.backups_restored += 1
            logger.info(f"✅ Backup restored successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False
    
    def _rotate_backups(self, backup_dir: Path):
        """Rotate backups, keeping only max_backups"""
        try:
            backups = sorted(backup_dir.glob("*_backup_*"), reverse=True)
            
            if len(backups) > self.max_backups:
                # Delete oldest backups
                for backup in backups[self.max_backups:]:
                    if backup.is_dir():
                        shutil.rmtree(backup)
                    else:
                        backup.unlink()
                    
                    logger.debug(f"Rotated old backup: {backup.name}")
        
        except Exception as e:
            logger.error(f"Failed to rotate backups: {e}")
    
    def lock_file(self, file_path: Path) -> bool:
        """
        Lock a file (make it read-only)
        
        Args:
            file_path: Path to file to lock
        
        Returns:
            Success status
        """
        if not self.lock_after_success:
            return False
        
        return self._lock_file(file_path)
    
    def _lock_file(self, file_path: Path) -> bool:
        """Internal file locking"""
        try:
            if not file_path.exists():
                return False
            
            # Make file read-only (Windows)
            os.chmod(file_path, 0o444)
            
            self.locked_files.add(file_path)
            self.files_locked += 1
            
            logger.debug(f"🔒 File locked: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to lock file: {e}")
            return False
    
    def unlock_file(self, file_path: Path) -> bool:
        """
        Unlock a file (make it writable)
        
        Args:
            file_path: Path to file to unlock
        
        Returns:
            Success status
        """
        return self._unlock_file(file_path)
    
    def _unlock_file(self, file_path: Path) -> bool:
        """Internal file unlocking"""
        try:
            if not file_path.exists():
                return False
            
            # Make file writable (Windows)
            os.chmod(file_path, 0o644)
            
            if file_path in self.locked_files:
                self.locked_files.remove(file_path)
            
            logger.debug(f"🔓 File unlocked: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unlock file: {e}")
            return False
    
    def get_backup_list(self, server_name: str) -> list:
        """Get list of backups for a server"""
        server_backup_dir = self.backup_dir / server_name
        
        if not server_backup_dir.exists():
            return []
        
        backups = []
        for backup_path in sorted(server_backup_dir.glob("*_backup_*"), reverse=True):
            backups.append({
                'name': backup_path.name,
                'path': str(backup_path),
                'size': backup_path.stat().st_size if backup_path.is_file() else 0,
                'created': datetime.fromtimestamp(backup_path.stat().st_ctime),
                'is_directory': backup_path.is_dir()
            })
        
        return backups
    
    def get_statistics(self) -> Dict:
        """Get backup statistics"""
        total_size = 0
        total_backups = 0
        
        if self.backup_dir.exists():
            for backup_file in self.backup_dir.glob("**/*_backup_*"):
                if backup_file.is_file():
                    total_size += backup_file.stat().st_size
                    total_backups += 1
        
        return {
            'enabled': self.enabled,
            'backup_directory': str(self.backup_dir),
            'backups_created': self.backups_created,
            'backups_restored': self.backups_restored,
            'files_locked': self.files_locked,
            'total_backups': total_backups,
            'total_size_mb': total_size / (1024 * 1024),
            'max_backups': self.max_backups
        }


# Export
__all__ = ['BackupManager']
