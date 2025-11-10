#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Server Discovery Engine
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Auto-discovers servers in ACTIVE_SERVERS/ and MCP_CONSTELLATION/
Classifies server types (HTTP, MCP, stdio, WebSocket)
Extracts port numbers and configuration
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess

# Optional env loader (E:\ECHO_XV4\CONFIG\echo_x_complete_api_keychain.env)
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except Exception:
    DOTENV_AVAILABLE = False

logger = logging.getLogger("ServerDiscovery")


class ServerDiscovery:
    """
    Server Auto-Discovery Engine
    
    Automatically finds and classifies all servers:
    - Scans ACTIVE_SERVERS/ directory
    - Scans MCP_CONSTELLATION/ directory
    - Extracts port numbers from source code
    - Classifies server types
    - Builds dynamic server registry
    """
    
    def __init__(self, config: Dict):
        """Initialize Server Discovery Engine"""
        self.config = config
        self.discovery_config = config.get('discovery', {})
        
        # Paths
        self.active_servers_path = Path(config.get('paths', {}).get('active_servers', 'E:/ECHO_XV4/MLS/servers/ACTIVE_SERVERS'))
        self.mcp_path = Path(config.get('paths', {}).get('mcp_constellation', 'E:/ECHO_XV4/MLS/servers/MCP_CONSTELLATION'))
        self.gateways_path = Path(config.get('paths', {}).get('gateways', 'E:/ECHO_XV4/MLS/servers/GATEWAYS'))
        
        # Settings
        self.auto_discovery = self.discovery_config.get('auto_discovery', True)
        self.process_detection = self.discovery_config.get('process_detection', True)
        self.detect_types = self.discovery_config.get('detect_types', ['HTTP', 'MCP', 'stdio', 'WebSocket'])
        # Curated discovery controls
        self.allow_names = set(self.discovery_config.get('allow_names', []))  # base filenames without .py
        self.exclude_dirs = set(self.discovery_config.get('exclude_dirs', []))  # substring match on full path
        
        # Server registry
        self.servers = {}
        self.discovered_count = 0
        
        logger.info("Server Discovery Engine initialized")
        logger.info(f"   Active Servers: {self.active_servers_path}")
        logger.info(f"   MCP Servers: {self.mcp_path}")
        logger.info(f"   Gateways: {self.gateways_path}")
        logger.info(f"   Auto-discovery: {self.auto_discovery}")
    
    def discover_all_servers(self) -> Dict[str, Dict]:
        """Discover all servers in configured directories"""
        logger.info("🔍 Starting server discovery...")
        
        self.servers = {}
        
        # Discover HTTP/Desktop servers
        if self.active_servers_path.exists():
            desktop_servers = self._discover_directory(
                self.active_servers_path,
                server_type='DESKTOP'
            )
            self.servers.update(desktop_servers)
            logger.info(f"   Found {len(desktop_servers)} desktop servers")
        
        # Discover MCP servers
        if self.mcp_path.exists():
            mcp_servers = self._discover_directory(
                self.mcp_path,
                server_type='MCP'
            )
            self.servers.update(mcp_servers)
            logger.info(f"   Found {len(mcp_servers)} MCP servers")
        
        # Discover Consolidated Gateways
        if self.gateways_path.exists():
            gw_servers = self._discover_directory(
                self.gateways_path,
                server_type='GATEWAY'
            )
            self.servers.update(gw_servers)
            logger.info(f"   Found {len(gw_servers)} gateway servers")
        
        self.discovered_count = len(self.servers)
        logger.info(f"✅ Discovery complete: {self.discovered_count} servers found")
        
        return self.servers
    
    def _discover_directory(self, directory: Path, server_type: str) -> Dict[str, Dict]:
        """Discover servers in a directory"""
        servers = {}
        
        try:
            # Find all Python files
            python_files = list(directory.glob("**/*.py"))
            
            for file_path in python_files:
                # Skip __pycache__ and test files
                if '__pycache__' in str(file_path) or 'test_' in file_path.name:
                    continue
                
                # Apply directory exclusions (substring match)
                if self.exclude_dirs:
                    sp = str(file_path)
                    if any(excl in sp for excl in self.exclude_dirs):
                        continue
                
                # Analyze file
                server_info = self._analyze_server_file(file_path, server_type)
                
                if server_info:
                    server_name = file_path.stem
                    # If allowlist is defined, only include those names
                    if self.allow_names and server_name not in self.allow_names:
                        continue
                    servers[server_name] = server_info
                    logger.debug(f"      Discovered: {server_name} ({server_info['type']})")
        
        except Exception as e:
            logger.error(f"Error discovering servers in {directory}: {e}")
        
        return servers
    
    def _analyze_server_file(self, file_path: Path, default_type: str) -> Optional[Dict]:
        """Analyze a server file to extract configuration"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract server information
            info = {
                'name': file_path.stem,
                'path': str(file_path),
                'type': default_type,
                'port': None,
                'protocol': None,
                'description': None,
                'dependencies': [],
                'auto_start': True
            }
            
            # Detect server type
            info['type'] = self._detect_server_type(content, default_type)
            
            # Extract port number
            info['port'] = self._extract_port(content)
            
            # Extract protocol
            info['protocol'] = self._detect_protocol(content)
            
            # Extract description from docstring
            info['description'] = self._extract_description(content)
            
            # Extract dependencies
            info['dependencies'] = self._extract_dependencies(content)
            
            return info
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def _detect_server_type(self, content: str, default_type: str) -> str:
        """Detect server type from content"""
        content_lower = content.lower()
        
        # Check for MCP server indicators
        if 'mcp' in content_lower or 'model context protocol' in content_lower:
            return 'MCP'
        
        # Check for stdio server
        if 'stdio' in content_lower or 'sys.stdin' in content_lower:
            return 'MCP_STDIO'
        
        # Check for HTTP server
        if any(keyword in content_lower for keyword in ['fastapi', 'flask', 'uvicorn', 'http.server']):
            return 'HTTP'
        
        # Check for WebSocket
        if 'websocket' in content_lower or 'ws://' in content_lower:
            return 'WEBSOCKET'
        
        return default_type
    
    def _extract_port(self, content: str) -> Optional[int]:
        """Extract port number from content"""
        # Common port patterns
        patterns = [
            r'port\s*=\s*(\d+)',
            r'PORT\s*=\s*(\d+)',
            r'listen.*?:(\d+)',
            r'localhost:(\d+)',
            r'127\.0\.0\.1:(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        
        return None
    
    def _detect_protocol(self, content: str) -> Optional[str]:
        """Detect communication protocol"""
        content_lower = content.lower()
        
        if 'http://' in content_lower or 'https://' in content_lower:
            return 'HTTP'
        elif 'ws://' in content_lower or 'wss://' in content_lower:
            return 'WebSocket'
        elif 'stdio' in content_lower:
            return 'stdio'
        
        return None
    
    def _extract_description(self, content: str) -> Optional[str]:
        """Extract description from docstring"""
        # Try to find module docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            # Get first line
            first_line = docstring.split('\n')[0].strip()
            return first_line if first_line else None
        
        return None
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract Python dependencies from imports"""
        dependencies = []
        
        # Find import statements
        import_pattern = r'^(?:from|import)\s+([a-zA-Z0-9_]+)'
        matches = re.finditer(import_pattern, content, re.MULTILINE)
        
        for match in matches:
            module = match.group(1)
            # Skip standard library
            if module not in ['os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'typing', 're']:
                if module not in dependencies:
                    dependencies.append(module)
        
        return dependencies
    
    def get_server_info(self, server_name: str) -> Optional[Dict]:
        """Get information about a specific server"""
        return self.servers.get(server_name)
    
    def get_servers_by_type(self, server_type: str) -> List[Dict]:
        """Get all servers of a specific type"""
        return [
            info for info in self.servers.values()
            if info['type'] == server_type
        ]
    
    def get_servers_by_port(self, port: int) -> List[Dict]:
        """Get servers using a specific port"""
        return [
            info for info in self.servers.values()
            if info['port'] == port
        ]
    
    def is_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        import socket
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0  # 0 means port is in use
        except:
            return False
    
    def find_available_port(self, start_port: int = 8000, end_port: int = 9000) -> Optional[int]:
        """Find an available port in range"""
        for port in range(start_port, end_port):
            if self.is_port_available(port):
                return port
        return None
    
    def detect_running_servers(self) -> List[Dict]:
        """Detect which servers are currently running"""
        running = []
        
        for name, info in self.servers.items():
            port = info.get('port')
            if port and not self.is_port_available(port):
                running.append({
                    'name': name,
                    'port': port,
                    'type': info['type']
                })
                logger.debug(f"   Detected running: {name} on port {port}")
        
        return running
    
    def get_statistics(self) -> Dict:
        """Get discovery statistics"""
        stats = {
            'total_servers': len(self.servers),
            'by_type': {},
            'with_ports': 0,
            'without_ports': 0
        }
        
        for info in self.servers.values():
            server_type = info['type']
            stats['by_type'][server_type] = stats['by_type'].get(server_type, 0) + 1
            
            if info['port']:
                stats['with_ports'] += 1
            else:
                stats['without_ports'] += 1
        
        return stats
    
    def generate_report(self) -> str:
        """Generate discovery report"""
        stats = self.get_statistics()
        
        report = []
        report.append("=" * 60)
        report.append("SERVER DISCOVERY REPORT")
        report.append("=" * 60)
        report.append(f"Total Servers Discovered: {stats['total_servers']}")
        report.append("")
        
        report.append("By Type:")
        for server_type, count in stats['by_type'].items():
            report.append(f"  {server_type}: {count}")
        report.append("")
        
        report.append(f"Servers with Ports: {stats['with_ports']}")
        report.append(f"Servers without Ports: {stats['without_ports']}")
        report.append("")
        
        # Running servers
        running = self.detect_running_servers()
        report.append(f"Currently Running: {len(running)}")
        for server in running:
            report.append(f"  - {server['name']} (port {server['port']})")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Export
__all__ = ['ServerDiscovery']
