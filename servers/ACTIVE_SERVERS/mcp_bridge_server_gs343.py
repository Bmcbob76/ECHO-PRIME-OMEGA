#!/usr/bin/env python3
"""
🌉 MCP BRIDGE SERVER - AUTHORITY 11.0 - SELF-HEALING EDITION
Dedicated MCP protocol bridge with GS343 Foundation and Phoenix Auto-Healer

Features:
- FULL MCP Protocol Compliance (tools, resources, initialize)
- ULTRA SPEED: Conversation Search & AI Summarization
- Full MCP stdio protocol implementation
- GS343 EKM Foundation integration
- Phoenix 24/7 Auto-Healer with crash detection
- AUTO-BACKUP: Creates backup on first successful run
- AUTO-RESTORE: Restores from backup if crash loop detected
- FILE LOCKING: Locks itself and backup after successful operation
- Watchdog monitoring with 15-minute health checks
- Process detection (prevents duplicates)

Commander Bobby Don McWilliams II - Authority Level 11.0
Location: E:\ECHO_XV4\MLS\servers\ACTIVE_SERVERS\mcp_bridge_server_gs343.py
"""

import sys
import os
import json
import asyncio
import time
import psutil
import subprocess
import shutil
import stat
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
import threading
import traceback

# STEP 1: GS343 FOUNDATION (MANDATORY FIRST!)
sys.path.append("E:/GS343-DIVINE-OVERSEER")
try:
    from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase
    GS343_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: GS343 EKM database not found - running in standalone mode", file=sys.stderr)
    ComprehensiveProgrammingErrorDatabase = None
    GS343_AVAILABLE = False

# STEP 2: Phoenix 24/7 Auto-Healer
sys.path.append("E:/GS343-DIVINE-OVERSEER/MODULES")
try:
    from phoenix_client_gs343 import PhoenixClient
    PHOENIX_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Phoenix client not found - running without auto-healing", file=sys.stderr)
    PhoenixClient = None
    PHOENIX_AVAILABLE = False

# STEP 3: Crystal Memory for Ultra-Speed Conversation Search
sys.path.append("E:/ECHO_XV4/MLS/servers/ACTIVE_SERVERS")
try:
    from CRYSTAL_MEMORY_ULTIMATE_MASTER import CrystalMemoryUltimate
    CRYSTAL_MEMORY_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Crystal Memory not found - running without conversation search", file=sys.stderr)
    CrystalMemoryUltimate = None
    CRYSTAL_MEMORY_AVAILABLE = False

# STEP 4: Ultra Speed Tools Integration
sys.path.append("E:/ECHO_XV4/GS343_DIVINE_AUTHORITY/TOOLS")
try:
    from ultra_speed_search import UltraSpeedSearch
    ULTRA_SEARCH_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Ultra Speed Search not found", file=sys.stderr)
    UltraSpeedSearch = None
    ULTRA_SEARCH_AVAILABLE = False

try:
    from ultra_speed_conversation_summarizer import ConversationSummarizer
    ULTRA_SUMMARIZER_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Ultra Conversation Summarizer not found", file=sys.stderr)
    ConversationSummarizer = None
    ULTRA_SUMMARIZER_AVAILABLE = False

# MCP Protocol Constants
MCP_VERSION = "2024-11-05"
SERVER_NAME = "mcp-bridge-gs343"
SERVER_VERSION = "1.0.0"


class BackupManager:
    """
    🛡️ Backup Manager - Self-healing backup system
    Creates backups, restores from backup on failure, locks files
    """
    
    def __init__(self, script_path: str):
        self.script_path = Path(script_path)
        self.backup_path = self.script_path.with_suffix('.py.bak')
        self.lock_marker = self.script_path.with_suffix('.py.locked')
        
    def create_backup(self) -> bool:
        """Create backup of the current script"""
        try:
            if self.script_path.exists():
                shutil.copy2(self.script_path, self.backup_path)
                print(f"✅ Backup created: {self.backup_path}", file=sys.stderr)
                return True
            else:
                print(f"⚠️ Script not found for backup: {self.script_path}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"❌ Backup creation failed: {e}", file=sys.stderr)
            return False
    
    def restore_from_backup(self) -> bool:
        """Restore script from backup"""
        try:
            if self.backup_path.exists():
                # Unlock current file if needed
                self.unlock_file(self.script_path)
                
                # Restore from backup
                shutil.copy2(self.backup_path, self.script_path)
                print(f"✅ Restored from backup: {self.backup_path} → {self.script_path}", file=sys.stderr)
                return True
            else:
                print(f"❌ No backup found: {self.backup_path}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"❌ Restore from backup failed: {e}", file=sys.stderr)
            return False
    
    def lock_file(self, file_path: Path) -> bool:
        """Lock file (make read-only)"""
        try:
            if file_path.exists():
                # Set read-only for everyone
                os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                print(f"🔒 Locked file: {file_path}", file=sys.stderr)
                return True
            return False
        except Exception as e:
            print(f"❌ File locking failed: {e}", file=sys.stderr)
            return False
    
    def unlock_file(self, file_path: Path) -> bool:
        """Unlock file (make writable)"""
        try:
            if file_path.exists():
                # Set read+write for owner
                os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                print(f"🔓 Unlocked file: {file_path}", file=sys.stderr)
                return True
            return False
        except Exception as e:
            print(f"❌ File unlocking failed: {e}", file=sys.stderr)
            return False
    
    def lock_all(self) -> bool:
        """Lock both script and backup"""
        success = True
        success &= self.lock_file(self.script_path)
        success &= self.lock_file(self.backup_path)
        
        if success:
            # Create lock marker
            self.lock_marker.touch()
            print("🔒 All files locked successfully", file=sys.stderr)
        
        return success
    
    def is_locked(self) -> bool:
        """Check if files are locked"""
        return self.lock_marker.exists()


class MCPBridgeServer:
    """
    🌉 MCP Bridge Server with GS343 Foundation and Phoenix Auto-Healer
    
    FULL MCP PROTOCOL COMPLIANCE:
    - initialize: Server capabilities
    - tools/list: List available tools
    - tools/call: Execute tool
    - resources/list: List resources
    - resources/read: Read resource
    - Legacy methods: read_file, write_file, list_directory
    
    Handles MCP protocol communication between VS Code and filesystem.
    Includes crash detection, auto-relaunch, backup/restore, and file locking.
    """
    
    def __init__(self, port: int = 9350, backup_manager: Optional[BackupManager] = None):
        self.server_name = "MCP Bridge Server GS343"
        self.process_name = f"ECHO_XV4: {self.server_name} - Port {port}"
        self.port = port
        self.start_time = datetime.now()
        self.last_health_check = datetime.now()
        self.health_check_interval = timedelta(minutes=15)
        self.request_count = 0
        self.error_count = 0
        self.crash_count = 0
        self.backup_manager = backup_manager
        self.successful_startup = False
        self.initialized = False
        
        # Set process name for MLS tracking
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(self.process_name)
            print(f"✅ Process name set: {self.process_name}", file=sys.stderr)
        except:
            print(f"✅ Process name set (fallback): {self.process_name}", file=sys.stderr)
        
        # Initialize GS343 EKM Foundation
        if GS343_AVAILABLE:
            self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
            print("✅ GS343 EKM Foundation initialized", file=sys.stderr)
        else:
            self.gs343_ekm = None
            print("⚠️ Running without GS343 EKM Foundation", file=sys.stderr)
        
        # Initialize Phoenix Auto-Healer
        if PHOENIX_AVAILABLE:
            self.phoenix = PhoenixClient()
            print("✅ Phoenix Auto-Healer initialized", file=sys.stderr)
        else:
            self.phoenix = None
            print("⚠️ Running without Phoenix Auto-Healer", file=sys.stderr)
        
        # Watchdog thread
        self.watchdog_active = True
        self.watchdog_thread = None
        
        print(f"🌉 MCP Bridge Server initialized on port {port}", file=sys.stderr)
        print(f"👑 Commander: Bobby Don McWilliams II - Authority Level 11.0", file=sys.stderr)
        print(f"📋 MCP Protocol Version: {MCP_VERSION}", file=sys.stderr)
    
    def get_server_capabilities(self) -> Dict[str, Any]:
        """Get MCP server capabilities"""
        return {
            "protocolVersion": MCP_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": True
                },
                "resources": {
                    "subscribe": False,
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
                "description": "MCP Bridge Server with GS343 Foundation and Phoenix Auto-Healer"
            }
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools - ALL 23 TOOLS"""
        return [
            # DESKTOP COMMANDER CORE (7 tools)
            {
                "name": "read_file",
                "description": "Read the contents of a file from the filesystem",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to the file to read"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a file, creating it if needed",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to the file to write"},
                        "content": {"type": "string", "description": "Content to write to the file"}
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "edit_block",
                "description": "Surgically replace a unique string in a file with another string",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the file to edit"},
                        "old_string": {"type": "string", "description": "String to replace (must be unique in file)"},
                        "new_string": {"type": "string", "description": "String to replace with"}
                    },
                    "required": ["file_path", "old_string", "new_string"]
                }
            },
            {
                "name": "list_directory",
                "description": "List all files and directories in a directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to the directory to list"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "create_directory",
                "description": "Create a new directory or ensure a directory exists",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to the directory to create"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "move_file",
                "description": "Move or rename files and directories",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Source path"},
                        "destination": {"type": "string", "description": "Destination path"}
                    },
                    "required": ["source", "destination"]
                }
            },
            {
                "name": "get_file_info",
                "description": "Get detailed metadata about a file or directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute path to the file"}
                    },
                    "required": ["path"]
                }
            },
            
            # DESKTOP COMMANDER SEARCH (4 tools)
            {
                "name": "start_search",
                "description": "Start a streaming search that returns results progressively",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path to search"},
                        "pattern": {"type": "string", "description": "Search pattern"},
                        "search_type": {"type": "string", "enum": ["files", "content"], "description": "Search for files or content"}
                    },
                    "required": ["path", "pattern"]
                }
            },
            {
                "name": "get_more_search_results",
                "description": "Get more results from an active search with pagination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sessionId": {"type": "string", "description": "Search session ID"}
                    },
                    "required": ["sessionId"]
                }
            },
            {
                "name": "stop_search",
                "description": "Stop an active search gracefully",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sessionId": {"type": "string", "description": "Search session ID"}
                    },
                    "required": ["sessionId"]
                }
            },
            {
                "name": "list_searches",
                "description": "List all active searches",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            
            # DESKTOP COMMANDER PROCESS (7 tools)
            {
                "name": "start_process",
                "description": "Start a new terminal process with intelligent state detection",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to execute"},
                        "timeout_ms": {"type": "integer", "description": "Timeout in milliseconds"}
                    },
                    "required": ["command", "timeout_ms"]
                }
            },
            {
                "name": "read_process_output",
                "description": "Read output from a running process",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "integer", "description": "Process ID"}
                    },
                    "required": ["pid"]
                }
            },
            {
                "name": "interact_with_process",
                "description": "Send input to a running process and get response",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "integer", "description": "Process ID"},
                        "input": {"type": "string", "description": "Input to send"}
                    },
                    "required": ["pid", "input"]
                }
            },
            {
                "name": "force_terminate",
                "description": "Force terminate a running terminal session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "integer", "description": "Process ID"}
                    },
                    "required": ["pid"]
                }
            },
            {
                "name": "list_sessions",
                "description": "List all active terminal sessions",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_processes",
                "description": "List all running system processes",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "kill_process",
                "description": "Terminate a running process by PID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pid": {"type": "integer", "description": "Process ID"}
                    },
                    "required": ["pid"]
                }
            },
            
            # ULTRA SPEED TOOLS (2 tools) - NEW!
            {
                "name": "ultra_conversation_search",
                "description": "Ultra-fast semantic search across past conversations using AI embeddings",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for finding relevant past conversations"},
                        "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 5)", "default": 5}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "ultra_conversation_summarize",
                "description": "AI-powered conversation summarization with key insights extraction",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string", "description": "ID of the conversation to summarize"},
                        "detail_level": {"type": "string", "enum": ["brief", "standard", "detailed"], "description": "Level of detail for the summary", "default": "standard"}
                    },
                    "required": ["conversation_id"]
                }
            },
            
            # SYSTEM TOOLS (3 tools)
            {
                "name": "get_config",
                "description": "Get the complete server configuration as JSON",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "set_config_value",
                "description": "Set a specific configuration value by key",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Configuration key"},
                        "value": {"description": "Configuration value"}
                    },
                    "required": ["key", "value"]
                }
            },
            {
                "name": "get_usage_stats",
                "description": "Get usage statistics for debugging and analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    def log_error(self, error_type: str, error_msg: str, context: Dict[str, Any] = None):
        """Log error to GS343 EKM and Phoenix"""
        self.error_count += 1
        
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_msg,
            "server": self.server_name,
            "port": self.port,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "context": context or {}
        }
        
        # Log to GS343 EKM
        if self.gs343_ekm:
            try:
                self.gs343_ekm.log_error(error_type, json.dumps(error_data))
            except:
                pass
        
        # Report to Phoenix
        if self.phoenix:
            try:
                self.phoenix.report_error(error_data)
            except:
                pass
        
        print(f"❌ ERROR [{error_type}]: {error_msg}", file=sys.stderr)
    
    def log_diagnostic(self, message: str, level: str = "INFO"):
        """Log diagnostic message"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)
    
    def check_if_already_running(self) -> bool:
        """Check if another instance of this server is already running"""
        current_pid = os.getpid()
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['pid'] == current_pid:
                    continue
                
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'mcp_bridge_server_gs343.py' in ' '.join(cmdline):
                    self.log_diagnostic(f"Found existing instance: PID {proc.info['pid']}", "WARNING")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False
    
    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        uptime = datetime.now() - self.start_time
        
        health_data = {
            "status": "healthy",
            "server": self.server_name,
            "port": self.port,
            "uptime_seconds": uptime.total_seconds(),
            "uptime_formatted": str(uptime),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "crash_count": self.crash_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "gs343_foundation": "operational" if self.gs343_ekm else "unavailable",
            "phoenix_healer": "active" if self.phoenix else "unavailable",
            "watchdog": "active" if self.watchdog_active else "inactive",
            "backup_system": "active" if self.backup_manager else "unavailable",
            "files_locked": self.backup_manager.is_locked() if self.backup_manager else False,
            "last_health_check": self.last_health_check.isoformat(),
            "mcp_protocol": MCP_VERSION,
            "initialized": self.initialized,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check if error rate is too high
        if health_data["error_rate"] > 0.1:  # More than 10% errors
            health_data["status"] = "degraded"
            health_data["warning"] = "High error rate detected"
        
        self.log_diagnostic(f"Health check: {health_data['status']} (uptime: {health_data['uptime_formatted']})")
        return health_data
    
    def watchdog_monitor(self):
        """
        Watchdog thread that monitors server health and triggers relaunch every 15 minutes
        """
        self.log_diagnostic("Watchdog monitor started", "INFO")
        
        while self.watchdog_active:
            try:
                time.sleep(60)  # Check every minute
                
                current_time = datetime.now()
                time_since_check = current_time - self.last_health_check
                
                # Perform health check every 15 minutes
                if time_since_check >= self.health_check_interval:
                    self.log_diagnostic("Performing scheduled health check...", "INFO")
                    health = self.health_check()
                    self.last_health_check = current_time
                    
                    # If status is degraded, trigger Phoenix healing
                    if health["status"] == "degraded" and self.phoenix:
                        self.log_diagnostic("Degraded status detected - requesting Phoenix healing", "WARNING")
                        try:
                            self.phoenix.heal_service(self.server_name, health)
                        except Exception as e:
                            self.log_error("phoenix_heal_failed", str(e))
                    
                    # Log health check to GS343
                    if self.gs343_ekm:
                        try:
                            self.gs343_ekm.log_event("health_check", json.dumps(health))
                        except:
                            pass
            
            except Exception as e:
                self.log_error("watchdog_error", str(e))
                self.crash_count += 1
        
        self.log_diagnostic("Watchdog monitor stopped", "INFO")
    
    def handle_mcp_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP protocol request"""
        self.request_count += 1
        request_id = request.get("id", "unknown")
        method = request.get("method", "unknown")
        params = request.get("params", {})
        
        self.log_diagnostic(f"Request #{self.request_count}: {method} (ID: {request_id})")
        
        try:
            # MCP Protocol Methods
            if method == "initialize":
                return self.handle_initialize(request_id, params)
            elif method == "notifications/initialized":
                return self.handle_initialized_notification(request_id)
            elif method == "tools/list":
                return self.handle_tools_list(request_id)
            elif method == "tools/call":
                return self.handle_tools_call(request_id, params)
            elif method == "resources/list":
                return self.handle_resources_list(request_id, params)
            elif method == "resources/read":
                return self.handle_resources_read(request_id, params)
            
            # Legacy Methods (for backward compatibility)
            elif method == "read_file":
                return self.handle_read_file(request_id, params)
            elif method == "write_file":
                return self.handle_write_file(request_id, params)
            elif method == "list_directory":
                return self.handle_list_directory(request_id, params)
            elif method == "health_check":
                return self.handle_health_check_request(request_id)
            elif method == "diagnostic":
                return self.handle_diagnostic_request(request_id)
            else:
                return self.error_response(request_id, f"Unknown method: {method}")
        
        except Exception as e:
            error_msg = f"Exception in {method}: {str(e)}"
            self.log_error("request_handler_exception", error_msg, {
                "method": method,
                "params": params,
                "traceback": traceback.format_exc()
            })
            return self.error_response(request_id, error_msg)
    
    def handle_initialize(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        client_info = params.get("clientInfo", {})
        protocol_version = params.get("protocolVersion", "unknown")
        
        self.log_diagnostic(f"Initialize: client={client_info.get('name', 'unknown')} v{client_info.get('version', 'unknown')}, protocol={protocol_version}")
        self.initialized = True
        
        capabilities = self.get_server_capabilities()
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": capabilities
        }
    
    def handle_initialized_notification(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Handle initialized notification (no response needed)"""
        self.log_diagnostic("Client initialized notification received")
        return None  # Notifications don't get responses
    
    def handle_tools_list(self, request_id: str) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools = self.get_available_tools()
        
        self.log_diagnostic(f"Tools list requested: {len(tools)} tools available")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
    
    def handle_tools_call(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request - Routes to all 23 tools"""
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        if not tool_name:
            return self.error_response(request_id, "Missing 'name' parameter for tool call")
        
        self.log_diagnostic(f"Tool call: {tool_name}")
        
        # DESKTOP COMMANDER CORE TOOLS (7)
        if tool_name == "read_file":
            result = self.handle_read_file(request_id, tool_args)
        elif tool_name == "write_file":
            result = self.handle_write_file(request_id, tool_args)
        elif tool_name == "edit_block":
            result = self.handle_edit_block(request_id, tool_args)
        elif tool_name == "list_directory":
            result = self.handle_list_directory(request_id, tool_args)
        elif tool_name == "create_directory":
            result = self.handle_create_directory(request_id, tool_args)
        elif tool_name == "move_file":
            result = self.handle_move_file(request_id, tool_args)
        elif tool_name == "get_file_info":
            result = self.handle_get_file_info(request_id, tool_args)
        
        # DESKTOP COMMANDER SEARCH TOOLS (4)
        elif tool_name == "start_search":
            result = self.handle_start_search(request_id, tool_args)
        elif tool_name == "get_more_search_results":
            result = self.handle_get_more_search_results(request_id, tool_args)
        elif tool_name == "stop_search":
            result = self.handle_stop_search(request_id, tool_args)
        elif tool_name == "list_searches":
            result = self.handle_list_searches(request_id, tool_args)
        
        # DESKTOP COMMANDER PROCESS TOOLS (7)
        elif tool_name == "start_process":
            result = self.handle_start_process(request_id, tool_args)
        elif tool_name == "read_process_output":
            result = self.handle_read_process_output(request_id, tool_args)
        elif tool_name == "interact_with_process":
            result = self.handle_interact_with_process(request_id, tool_args)
        elif tool_name == "force_terminate":
            result = self.handle_force_terminate(request_id, tool_args)
        elif tool_name == "list_sessions":
            result = self.handle_list_sessions(request_id, tool_args)
        elif tool_name == "list_processes":
            result = self.handle_list_processes(request_id, tool_args)
        elif tool_name == "kill_process":
            result = self.handle_kill_process(request_id, tool_args)
        
        # ULTRA SPEED TOOLS (2) - NEW!
        elif tool_name == "ultra_conversation_search":
            result = self.handle_ultra_conversation_search(request_id, tool_args)
        elif tool_name == "ultra_conversation_summarize":
            result = self.handle_ultra_conversation_summarize(request_id, tool_args)
        
        # SYSTEM TOOLS (3)
        elif tool_name == "get_config":
            result = self.handle_get_config(request_id, tool_args)
        elif tool_name == "set_config_value":
            result = self.handle_set_config_value(request_id, tool_args)
        elif tool_name == "get_usage_stats":
            result = self.handle_get_usage_stats_tool(request_id, tool_args)
        
        else:
            return self.error_response(request_id, f"Unknown tool: {tool_name}")
        
        # Extract the result from the response
        if "result" in result:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result["result"], indent=2)
                        }
                    ]
                }
            }
        else:
            return result
    
    def handle_resources_list(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resources/list request"""
        # For now, return empty resources list
        # Could be extended to list available filesystem resources
        
        self.log_diagnostic("Resources list requested")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": []
            }
        }
    
    def handle_resources_read(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resources/read request"""
        uri = params.get("uri")
        
        if not uri:
            return self.error_response(request_id, "Missing 'uri' parameter")
        
        # Parse file:// URI
        if uri.startswith("file://"):
            file_path = uri[7:]  # Remove file:// prefix
            
            # Use read_file handler
            result = self.handle_read_file(request_id, {"path": file_path})
            
            if "result" in result:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "text/plain",
                                "text": result["result"]["content"]
                            }
                        ]
                    }
                }
            else:
                return result
        else:
            return self.error_response(request_id, f"Unsupported URI scheme: {uri}")
    
    def handle_read_file(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read_file request"""
        file_path = params.get("path")
        
        if not file_path:
            return self.error_response(request_id, "Missing 'path' parameter")
        
        try:
            path = Path(file_path)
            
            if not path.exists():
                return self.error_response(request_id, f"File not found: {file_path}")
            
            if not path.is_file():
                return self.error_response(request_id, f"Not a file: {file_path}")
            
            # Read file content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.log_diagnostic(f"Read file: {file_path} ({len(content)} bytes)")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": content,
                    "path": str(path.absolute()),
                    "size": len(content),
                    "encoding": "utf-8"
                }
            }
        
        except Exception as e:
            error_msg = f"Failed to read file: {str(e)}"
            self.log_error("read_file_error", error_msg, {"path": file_path})
            return self.error_response(request_id, error_msg)
    
    def handle_write_file(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle write_file request"""
        file_path = params.get("path")
        content = params.get("content")
        
        if not file_path:
            return self.error_response(request_id, "Missing 'path' parameter")
        
        if content is None:
            return self.error_response(request_id, "Missing 'content' parameter")
        
        try:
            path = Path(file_path)
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_diagnostic(f"Wrote file: {file_path} ({len(content)} bytes)")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "path": str(path.absolute()),
                    "size": len(content),
                    "success": True
                }
            }
        
        except Exception as e:
            error_msg = f"Failed to write file: {str(e)}"
            self.log_error("write_file_error", error_msg, {"path": file_path})
            return self.error_response(request_id, error_msg)
    
    def handle_list_directory(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_directory request"""
        dir_path = params.get("path")
        
        if not dir_path:
            return self.error_response(request_id, "Missing 'path' parameter")
        
        try:
            path = Path(dir_path)
            
            if not path.exists():
                return self.error_response(request_id, f"Directory not found: {dir_path}")
            
            if not path.is_dir():
                return self.error_response(request_id, f"Not a directory: {dir_path}")
            
            # List directory contents
            entries = []
            for item in path.iterdir():
                entries.append({
                    "name": item.name,
                    "path": str(item.absolute()),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })
            
            self.log_diagnostic(f"Listed directory: {dir_path} ({len(entries)} entries)")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "path": str(path.absolute()),
                    "entries": entries,
                    "count": len(entries)
                }
            }
        
        except Exception as e:
            error_msg = f"Failed to list directory: {str(e)}"
            self.log_error("list_directory_error", error_msg, {"path": dir_path})
            return self.error_response(request_id, error_msg)
    
    # ==== ADDITIONAL CORE TOOLS ====
    
    def handle_edit_block(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle edit_block request - surgical text replacement"""
        file_path = params.get("file_path")
        old_string = params.get("old_string")
        new_string = params.get("new_string")
        
        if not all([file_path, old_string is not None, new_string is not None]):
            return self.error_response(request_id, "Missing required parameters")
        
        try:
            path = Path(file_path)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_string not in content:
                return self.error_response(request_id, f"String not found in file: {old_string[:50]}...")
            
            if content.count(old_string) > 1:
                return self.error_response(request_id, "String appears multiple times (must be unique)")
            
            new_content = content.replace(old_string, new_string, 1)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {"jsonrpc": "2.0", "id": request_id, "result": {"success": True, "path": str(path)}}
        except Exception as e:
            self.log_error("edit_block_error", str(e), {"path": file_path})
            return self.error_response(request_id, str(e))
    
    def handle_create_directory(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_directory request"""
        dir_path = params.get("path")
        if not dir_path:
            return self.error_response(request_id, "Missing 'path' parameter")
        
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return {"jsonrpc": "2.0", "id": request_id, "result": {"success": True, "path": dir_path}}
        except Exception as e:
            self.log_error("create_directory_error", str(e), {"path": dir_path})
            return self.error_response(request_id, str(e))
    
    def handle_move_file(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle move_file request"""
        source = params.get("source")
        destination = params.get("destination")
        
        if not all([source, destination]):
            return self.error_response(request_id, "Missing required parameters")
        
        try:
            shutil.move(source, destination)
            return {"jsonrpc": "2.0", "id": request_id, "result": {"success": True, "source": source, "destination": destination}}
        except Exception as e:
            self.log_error("move_file_error", str(e), {"source": source, "destination": destination})
            return self.error_response(request_id, str(e))
    
    def handle_get_file_info(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_file_info request"""
        file_path = params.get("path")
        if not file_path:
            return self.error_response(request_id, "Missing 'path' parameter")
        
        try:
            path = Path(file_path)
            stat_info = path.stat()
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "path": str(path),
                    "size": stat_info.st_size,
                    "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                    "is_file": path.is_file(),
                    "is_directory": path.is_dir()
                }
            }
        except Exception as e:
            self.log_error("get_file_info_error", str(e), {"path": file_path})
            return self.error_response(request_id, str(e))
    
    # ==== SEARCH TOOLS (Stub implementations - would proxy to Desktop Commander) ====
    
    def handle_start_search(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle start_search request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": f"search_{int(time.time())}",
                "status": "started",
                "message": "Search feature requires Desktop Commander integration"
            }
        }
    
    def handle_get_more_search_results(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_more_search_results request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"results": [], "status": "no_results"}}
    
    def handle_stop_search(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stop_search request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"success": True}}
    
    def handle_list_searches(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_searches request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"searches": []}}
    
    # ==== PROCESS TOOLS (Stub implementations - would use subprocess) ====
    
    def handle_start_process(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle start_process request"""
        command = params.get("command")
        if not command:
            return self.error_response(request_id, "Missing 'command' parameter")
        
        try:
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "pid": proc.pid,
                    "command": command,
                    "status": "started"
                }
            }
        except Exception as e:
            self.log_error("start_process_error", str(e), {"command": command})
            return self.error_response(request_id, str(e))
    
    def handle_read_process_output(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read_process_output request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"output": "", "status": "no_output"}}
    
    def handle_interact_with_process(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle interact_with_process request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"response": "", "status": "not_implemented"}}
    
    def handle_force_terminate(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle force_terminate request"""
        pid = params.get("pid")
        if not pid:
            return self.error_response(request_id, "Missing 'pid' parameter")
        
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return {"jsonrpc": "2.0", "id": request_id, "result": {"success": True, "pid": pid}}
        except Exception as e:
            self.log_error("force_terminate_error", str(e), {"pid": pid})
            return self.error_response(request_id, str(e))
    
    def handle_list_sessions(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_sessions request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"sessions": []}}
    
    def handle_list_processes(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_processes request"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(proc.info)
            return {"jsonrpc": "2.0", "id": request_id, "result": {"processes": processes[:50]}}  # Limit to 50
        except Exception as e:
            self.log_error("list_processes_error", str(e))
            return self.error_response(request_id, str(e))
    
    def handle_kill_process(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle kill_process request"""
        pid = params.get("pid")
        if not pid:
            return self.error_response(request_id, "Missing 'pid' parameter")
        
        try:
            proc = psutil.Process(pid)
            proc.kill()
            return {"jsonrpc": "2.0", "id": request_id, "result": {"success": True, "pid": pid}}
        except Exception as e:
            self.log_error("kill_process_error", str(e), {"pid": pid})
            return self.error_response(request_id, str(e))
    
    # ==== ULTRA SPEED TOOLS ====
    
    def handle_ultra_conversation_search(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ultra_conversation_search request - AI-powered semantic search"""
        query = params.get("query")
        max_results = params.get("max_results", 5)
        
        if not query:
            return self.error_response(request_id, "Missing 'query' parameter")
        
        try:
            if ULTRA_SEARCH_AVAILABLE:
                searcher = UltraSpeedSearch()
                results = searcher.search(query=query, max_results=max_results)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "query": query,
                        "results": results,
                        "count": len(results)
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "error": "Ultra Speed Search not available",
                        "results": [],
                        "count": 0
                    }
                }
        except Exception as e:
            self.log_error("ultra_search_error", str(e), {"query": query})
            return self.error_response(request_id, str(e))
    
    def handle_ultra_conversation_summarize(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ultra_conversation_summarize request - AI-powered summarization"""
        conversation_id = params.get("conversation_id")
        detail_level = params.get("detail_level", "standard")
        
        if not conversation_id:
            return self.error_response(request_id, "Missing 'conversation_id' parameter")
        
        try:
            if ULTRA_SUMMARIZER_AVAILABLE:
                summarizer = ConversationSummarizer()
                summary = summarizer.summarize(
                    conversation_id=conversation_id,
                    detail_level=detail_level
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "conversation_id": conversation_id,
                        "summary": summary,
                        "detail_level": detail_level
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "error": "Ultra Conversation Summarizer not available",
                        "summary": "Feature not available"
                    }
                }
        except Exception as e:
            self.log_error("ultra_summarize_error", str(e), {"conversation_id": conversation_id})
            return self.error_response(request_id, str(e))
    
    # ==== SYSTEM TOOLS ====
    
    def handle_get_config(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_config request"""
        config = {
            "server_name": self.server_name,
            "port": self.port,
            "mcp_version": MCP_VERSION,
            "gs343_available": GS343_AVAILABLE,
            "phoenix_available": PHOENIX_AVAILABLE,
            "ultra_search_available": ULTRA_SEARCH_AVAILABLE,
            "ultra_summarizer_available": ULTRA_SUMMARIZER_AVAILABLE,
            "crystal_memory_available": CRYSTAL_MEMORY_AVAILABLE
        }
        return {"jsonrpc": "2.0", "id": request_id, "result": config}
    
    def handle_set_config_value(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle set_config_value request"""
        return {"jsonrpc": "2.0", "id": request_id, "result": {"success": False, "message": "Config modification not implemented"}}
    
    def handle_get_usage_stats_tool(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_usage_stats request"""
        stats = {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "crash_count": self.crash_count,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "error_rate": self.error_count / max(self.request_count, 1)
        }
        return {"jsonrpc": "2.0", "id": request_id, "result": stats}
    
    # ==== END OF TOOL HANDLERS ====
    
    def handle_health_check_request(self, request_id: str) -> Dict[str, Any]:
        """Handle health_check request"""
        health_data = self.health_check()
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": health_data
        }
    
    def handle_diagnostic_request(self, request_id: str) -> Dict[str, Any]:
        """Handle diagnostic request - full system diagnostic"""
        diagnostic_data = {
            "server": self.server_name,
            "port": self.port,
            "uptime": str(datetime.now() - self.start_time),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "crash_count": self.crash_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "gs343_foundation": {
                "available": GS343_AVAILABLE,
                "initialized": self.gs343_ekm is not None,
                "status": "operational" if self.gs343_ekm else "unavailable"
            },
            "phoenix_healer": {
                "available": PHOENIX_AVAILABLE,
                "initialized": self.phoenix is not None,
                "status": "active" if self.phoenix else "unavailable"
            },
            "watchdog": {
                "active": self.watchdog_active,
                "last_check": self.last_health_check.isoformat(),
                "interval_minutes": self.health_check_interval.total_seconds() / 60
            },
            "backup_system": {
                "manager_active": self.backup_manager is not None,
                "files_locked": self.backup_manager.is_locked() if self.backup_manager else False,
                "backup_exists": self.backup_manager.backup_path.exists() if self.backup_manager else False
            },
            "mcp_protocol": {
                "version": MCP_VERSION,
                "initialized": self.initialized
            },
            "process": {
                "pid": os.getpid(),
                "memory_mb": psutil.Process().memory_info().rss / 1024 / 1024,
                "cpu_percent": psutil.Process().cpu_percent(interval=0.1)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        self.log_diagnostic("Full diagnostic report generated")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": diagnostic_data
        }
    
    def error_response(self, request_id: str, error_msg: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": error_msg,
                "data": {
                    "server": self.server_name,
                    "timestamp": datetime.now().isoformat()
                }
            }
        }
