#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Process Naming System
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Clear process naming for all servers
Format: "MLS - {server_name} [port] {status}"
Makes Task Manager readable and professional
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger("ProcessNaming")

# Try to import setproctitle
try:
    import setproctitle
    SETPROCTITLE_AVAILABLE = True
except ImportError:
    logger.warning("setproctitle not installed. Process naming will be limited.")
    SETPROCTITLE_AVAILABLE = False


class ProcessNamingManager:
    """
    Process Naming Manager
    
    Sets clear, descriptive process names for all servers
    Makes Task Manager and monitoring tools readable
    
    Format: MLS - {server_name} [{port}] {status}
    Example: "MLS - Crystal Memory [8080] Running"
    """
    
    def __init__(self, config: Dict):
        """Initialize Process Naming Manager"""
        self.config = config
        self.naming_config = config.get('process_naming', {})
        
        # Settings
        self.enabled = self.naming_config.get('enabled', True)
        self.library = self.naming_config.get('library', 'setproctitle')
        self.format = self.naming_config.get('format', 'MLS - {server_name}')
        self.include_port = self.naming_config.get('include_port', True)
        self.include_status = self.naming_config.get('include_status', True)
        
        # Track renamed processes
        self.renamed_processes = {}
        
        logger.info("Process Naming Manager initialized")
        logger.info(f"   Enabled: {self.enabled}")
        logger.info(f"   Library Available: {SETPROCTITLE_AVAILABLE}")
        logger.info(f"   Format: {self.format}")
    
    def set_process_name(self, server_name: str, port: Optional[int] = None, status: str = "Running") -> bool:
        """
        Set process name for current process
        
        Args:
            server_name: Name of the server
            port: Port number (optional)
            status: Current status (optional)
        
        Returns:
            Success status
        """
        if not self.enabled:
            return False
        
        if not SETPROCTITLE_AVAILABLE:
            logger.debug(f"Cannot set process name: setproctitle not available")
            return False
        
        try:
            # Build process name
            proc_name = self._build_process_name(server_name, port, status)
            
            # Set the process title
            setproctitle.setproctitle(proc_name)
            
            # Track it
            self.renamed_processes[server_name] = {
                'name': proc_name,
                'port': port,
                'status': status
            }
            
            logger.debug(f"Set process name: {proc_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set process name: {e}")
            return False
    
    def _build_process_name(self, server_name: str, port: Optional[int], status: str) -> str:
        """Build formatted process name"""
        # Start with base format
        name = self.format.format(server_name=server_name)
        
        # Add port if configured and available
        if self.include_port and port:
            name += f" [{port}]"
        
        # Add status if configured
        if self.include_status and status:
            name += f" {status}"
        
        return name
    
    def update_status(self, server_name: str, new_status: str) -> bool:
        """Update status in process name"""
        if server_name not in self.renamed_processes:
            return False
        
        info = self.renamed_processes[server_name]
        return self.set_process_name(server_name, info['port'], new_status)
    
    def get_current_name(self) -> Optional[str]:
        """Get current process name"""
        if not SETPROCTITLE_AVAILABLE:
            return None
        
        try:
            return setproctitle.getproctitle()
        except Exception as e:
            logger.error(f"Failed to get process name: {e}")
            return None
    
    def reset_process_name(self):
        """Reset process name to default"""
        if not SETPROCTITLE_AVAILABLE:
            return
        
        try:
            # Reset to Python default
            setproctitle.setproctitle("python")
            logger.debug("Process name reset to default")
        except Exception as e:
            logger.error(f"Failed to reset process name: {e}")
    
    def get_statistics(self) -> Dict:
        """Get process naming statistics"""
        return {
            'enabled': self.enabled,
            'library_available': SETPROCTITLE_AVAILABLE,
            'renamed_processes': len(self.renamed_processes),
            'format': self.format
        }


def set_server_process_name(server_name: str, port: Optional[int] = None, status: str = "Running"):
    """
    Convenience function to set process name for a server
    
    Usage:
        set_server_process_name("Crystal Memory", 8080, "Running")
    """
    if not SETPROCTITLE_AVAILABLE:
        return
    
    try:
        name = f"MLS - {server_name}"
        if port:
            name += f" [{port}]"
        name += f" {status}"
        
        setproctitle.setproctitle(name)
    except Exception as e:
        logger.error(f"Failed to set process name: {e}")


# Export
__all__ = ['ProcessNamingManager', 'set_server_process_name', 'SETPROCTITLE_AVAILABLE']
