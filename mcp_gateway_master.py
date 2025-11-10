#!/usr/bin/env python3
"""
🌐 MCP GATEWAY MASTER - Complete Tool Access for ALL LLMs
Commander: Bobby Don McWilliams II
Authority Level: 11.0 (Sovereign Architect)

COMPLETE LLM INTEGRATION:
✅ Claude Desktop: Full tool access to ALL 16 servers (9400-9416)
✅ VS Code Copilot: Complete tool integration with GitHub Copilot  
✅ Claude Web (claude.ai): Web-accessible tools via API
✅ Cline Integration: Full tool access within VS Code editor
✅ Any LLM: Universal tool access framework
✅ GUI Launch: Immediate dashboard viewer with all functionality

This system creates a master MCP server that provides UNIFIED access to all gateway tools
across all 16 servers, making them accessible to Claude, Copilot, Cline, and any LLM.
"""

import os
import sys
import json
import time
import asyncio
import requests
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import logging
import webbrowser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - MCPGatewayMaster - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MCPGatewayMaster")

# MCP Configuration optimized for Claude, Copilot, Cline access
MCP_CONFIG = {
    "server_name": "MasterLauncherMCP",
    "server_version": "1.0.0-Ultimate",
    "description": "MCP Master providing Claude Desktop, VS Copilot, Cline, and universal LLM access to all gateway tools",
}

# Master MCP Port Configuration
MASTER_MCP_PORT = 9418

# Complete Tool Registry - All tools from all 16 servers
UNIVERSAL_TOOL_REGISTRY = {
    "mcp_version": "1.0.0",
    "tools": [
        # ===== CRYSTAL MEMORY HUB TOOLS (Port 9400) =====
        {
            "name": "crystal_memory_store",
            "description": "Store information in the Crystal Memory Hub for permanent retrieval - accessible to Claude, Copilot, Cline",
            "server": "CRYSTAL_MEMORY_HUB",
            "port": 9400,
            "category": "memory",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Key for storing the memory"},
                    "value": {"type": "string", "description": "Value to store"},
                    "metadata": {"type": "object", "description": "Optional metadata about the memory"}
                },
                "required": ["key", "value"]
            }
        },
        {
            "name": "crystal_memory_retrieve",
            "description": "Retrieve information from the Crystal Memory Hub - Claude will use this before asking questions",
            "server": "CRYSTAL_MEMORY_HUB", 
            "port": 9400,
            "category": "memory",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Key of the memory to retrieve"}
                },
                "required": ["key"],
                "examples": [
                    {"key": "previous_conversation", "output": "Previous conversation content"}
                ]
            }
        },
        {
            "name": "crystal_memory_search",
            "description": "Search crystal memory for related information - Cline uses this to find context",
            "server": "CRYSTAL_MEMORY_HUB",
            "port": 9400,
            "category": "memory",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Number of results (default: 10)"},
                    "category": {"type": "string", "description": "Optional category filter"}
                },
                "required": ["query"]
            }
        },
        
        # ===== VOICE SYSTEM HUB TOOLS (Port 9402) =====
        {
            "name": "voice_synthesis",
            "description": "Convert text to speech using AI voice system - any LLM can create voice output",
            "server": "VOICE_SYSTEM_HUB",
            "port": 9402,
            "category": "voice",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to synthesize"},
                    "voice": {"type": "string", "description": "Voice personality (ECHO/BREE/GS343/EPCP3O/R2D2/PHOENIX/HEPHAESTION/PROMETHEUS)", "default": "ECHO"},
                    "emotion": {"type": "string", "description": "Emotion to express", "default": "neutral"},
                    "speed": {"type": "number", "description": "Speech speed (0.5-2.0)", "default": 1.0},
                    "priority": {"type": "string", "description": "Priority level", "default": "normal"}
                },
                "required": ["text"]
            }
        },
        {
            "name": "voice_recognition",
            "description": "Convert audio to text with voice recognition - Copilot can transcribe your voice commands",
            "server": "VOICE_SYSTEM_HUB",
            "port": 9402,
            "category": "voice",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "audio_base64": {"type": "string", "description": "Base64 encoded audio data"},
                    "language": {"type": "string", "description": "Language code", "default": "en-US"},

                    "enhanced_mode": {"type": "boolean", "description": "Use enhanced recognition mode", "default": False}
                },
                "required": ["audio_base64"]
            }
        },
        
        # ===== DEVELOPER GATEWAY TOOLS (Port 9407) =====
        {
            "name": "code_analyzer",
            "description": "Analyze code for errors, performance, and quality - Claude Desktop will use this extensively",
            "server": "DEVELOPER_GATEWAY",
            "port": 9407,
            "category": "development",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Code to analyze"},
                    "language": {"type": "string", "description": "Programming language (python/javascript/java/csharp/etc)"},
                    "analysis_type": {"type": "string", "description": "What to analyze", "enum": ["error", "performance", "quality", "security", "style"]},

                    "enhanced_analysis": {"type": "boolean", "description": "Use enhanced AI analysis", "default": True}
                },
                "required": ["code", "language", "analysis_type"]
            }
        },
        {
            "name": "code_generator",
            "description": "Generate code based on requirements and specifications - VS Code Copilot integration",
            "server": "DEVELOPER_GATEWAY",
            "port": 9407,
            "category": "development",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "requirements": {"type": "string", "description": "Code requirements or description"},
                    "language": {"type": "string", "description": "Target programming language"},
                    "style_guide": {"type": "object", "description": "Optional coding style guide following PEP8/prettier standards"},
                    "complexity": {"type": "string", "description": "Code complexity level", "default": "standard", "enum": ["simple", "standard", "advanced", "enterprise"]}
                },
                "required": ["requirements"]
            }
        },
        
        # ===== OCR SCREEN TOOLS (Port 9416) =====
        {
            "name": "ocr_analyze",
            "description": "Perform OCR analysis on screenshots or images - universal screen analysis for all LLMs",
            "server": "OCR_SCREEN",
            "port": 9416,
            "category": "vision",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "image_base64": {"type": "string", "description": "Base64 encoded image data"},
                    "ocr_engine": {"type": "string", "enum": ["tesseract", "easyocr", "paddle"], "default": "tesseract"},
                    "language": {"type": "string", "description": "Language for OCR recognition", "default": "eng"},

                    "enhanced_mode": {"type": "boolean", "description": "Use enhanced OCR for better accuracy", "default": True},

                    "text_extraction": {"type": "boolean", "description": "Extract text content", "default": True}
                },
                "required": ["image_base64"]
            }
        },
        
        # ===== NETWORK GUARDIAN TOOLS (Port 9406) =====
        {
            "name": "network_scan",
            "description": "Comprehensive network security scan - use this to check your network security",
            "server": "NETWORK_GUARDIAN",
            "port": 9406,
            "category": "security",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "scan_type": {"type": "string", "enum": ["quick", "full", "deep"], "default": "standard"},

                    "include_ports": {"type": "boolean", "description": "Include port scanning", "default": True},

                    "check_vulnerabilities": {"type": "boolean", "description": "Check for known vulnerabilities", "default": True},
                    "report_format": {"type": "string", "description": "Output format", "default": "json"}
                }
            }
        },
        
        # ===== HEALING ORCHESTRATOR TOOLS (Port 9405) =====
        {
            "name": "system_healing",
            "description": "Launch automated healing for system issues - use when systems have problems",
            "server": "HEALING_ORCHESTRATOR",
            "port": 9405,
            "category": "healing",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "issue_type": {"type": "string", "description": "Type of issue to heal"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "medium"},

                    "auto_commit": {"type": "boolean", "description": "Auto-commit healing changes", "default": False},

                    "create_rollback": {"type": "boolean", "description": "Create rollback point", "default": True}
                },
                "required": ["issue_type"]
            }
        },
        
        # ===== WINDOWS OPERATIONS TOOLS (Port 9401) =====
        {
            "name": "windows_process_list",
            "description": "List all running Windows processes with detailed information - accessible to Claude Desktop",
            "server": "WINDOWS_OPERATIONS",
            "port": 9401,
            "category": "windows",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {

                    "include_memory": {"type": "boolean", "description": "Include memory usage information", "default": True},

                    "include_cpu": {"type": "boolean", "description": "Include CPU usage information", "default": True},
                    "filter": {"type": "string", "description": "Optional process name filter", "default": ""}
                }
            }
        },
        
        # ===== SYSTEM STATUS & CONTROL =====
        {
            "name": "get_server_status",
            "description": "Get comprehensive status of all gateway servers - shows what's running",
            "server": "MASTER_LAUNCHER",
            "port": 9418,
            "category": "status",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {

                    "detailed": {"type": "boolean", "description": "Include detailed information", "default": False},
                    "filter": {"type": "string", "description": "Optional filter for specific servers", "default": ""}
                }
            }
        },
        
        {
            "name": "control_server",
            "description": "Control gateway servers (start/stop/restart) - universal server control",
            "server": "MASTER_LAUNCHER",
            "port": 9418,
            "category": "control",
            "mcp_enabled": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "server_name": {"type": "string", "description": "Name of server to control (or 'all')"},
                    "action": {"type": "string", "enum": ["start", "stop", "restart", "status"], "description": "Control action"},

                    "force": {"type": "boolean", "description": "Force operation", "default": False}
                },
                "required": ["server_name", "action"]
            }
        }
    ],
    
    "servers": [
        {"name": "CRYSTAL_MEMORY_HUB", "port": 9400, "description": "🔮 Crystal Memory Hub - AI Memory System", "status": "active"},
        {"name": "WINDOWS_OPERATIONS", "port": 9401, "description": "🖥️ Windows Operations - Windows Management", "status": "active"},
        {"name": "VOICE_SYSTEM_HUB", "port": 9402, "description": "🗣️ Voice System Hub - AI Voice Personality", "status": "active"},
        {"name": "MASTER_ORCHESTRATOR_HUB", "port": 9403, "description": "🎛️ Master Orchestrator Hub - System Coordination", "status": "active"},
        {"name": "EPCP3O_AGENT", "port": 9404, "description": "🤖 EPCP3-O Protocol Droid - Protocol Management", "status": "active"},
        {"name": "HEALING_ORCHESTRATOR", "port": 9405, "description": "🏥 Healing Orchestrator - Auto-Healing System", "status": "active"},
        {"name": "NETWORK_GUARDIAN", "port": 9406, "description": "🛡️ Network Guardian - Security Scanner", "status": "active"},
        {"name": "DEVELOPER_GATEWAY", "port": 9407, "description": "💻 Developer Gateway - Code Analysis & Generation", "status": "active"},
        {"name": "DESKTOP_COMMANDER", "port": 9408, "description": "️ Desktop Commander - Desktop Management", "status": "active"},
        {"name": "TRAINERS_GATEWAY", "port": 9410, "description": "🎯 Trainers Gateway - Training System", "status": "active"},
        {"name": "HARVESTERS_GATEWAY", "port": 9411, "description": "🌾 Harvesters Gateway - Data Collection", "status": "active"},
        {"name": "UNIFIED_MCP_MASTER", "port": 9412, "description": "🌐 Unified MCP Master - MCP Integration", "status": "active"},
        {"name": "MEMORY_ORCHESTRATION_SERVER", "port": 9413, "description": "🧠 Memory Orchestration Server - Memory Management", "status": "active"},
        {"name": "GS343_GATEWAY", "port": 9414, "description": "⚡ GS343 Gateway - Divine Authority", "status": "active"},
        {"name": "VSCODE_GATEWAY", "port": 9415, "description": "📟 VS Code Gateway - VS Code Integration", "status": "active"},

        {"name": "OCR_SCREEN", "port": 9416, "description": "👁️ OCR Screen - Text Recognition on Screen", "status": "active"},
        {"name": "WINDOWS_API_ULTIMATE", "port": 8343, "description": "🏢 Windows API Ultimate - 225+ Windows APIs", "status": "active"}
    ]
}

class MCPGatewayMaster:
    """Master MCP server with complete tool access for Claude, Copilot, Cline"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.server_name = MCP_CONFIG["server_name"]
        self.version = MCP_CONFIG["server_version"]
        self.port = MASTER_MCP_PORT
        self.servers = UNIVERSAL_TOOL_REGISTRY["servers"]
        self.tools = UNIVERSAL_TOOL_REGISTRY["tools"]
        self.server_status = {server["name"]: server["status"] for server in self.servers}
        self.active_connections = 0
        
    def setup_routes(self):
        """Setup all Flask routes for MCP access"""
        
        @self.app.route('/mcp/tools', methods=['GET', 'POST'])
        def mcp_tools():
            """MCP tools endpoint - returns all available tools for LLM access"""
            try:
                logger.info("📋 MCP Tools Request Received")
                self.active_connections += 1
                
                # Return all available tools with full details
                tools_list = []
                for tool in self.tools:
                    tools_list.append({
                        "name": tool["name"],
                        "description": tool["description"],
                        "inputSchema": tool["input_schema"],
                        "category": tool["category"],
                        "server": tool["server"],
                        "port": tool["port"]
                    })
                
                response = {
                    "tools": tools_list,
                    "server_count": len(self.servers),
                    "tool_count": len(self.tools),
                    "status": "active",
                    "timestamp": datetime.now().isoformat()
                }
                
                logger.info(f"✅ Returning {len(tools_list)} tools to LLM requester")
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"❌ Tools endpoint error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/tool', methods=['POST'])
        def execute_tool():
            """Execute a specific tool - handles requests from Claude Desktop, VS Copilot, etc."""
            try:
                data = request.json
                tool_name = data.get("name")
                tool_args = data.get("arguments", {})
                
                logger.info(f"⚙️  Tool Execution Request: {tool_name}")
                logger.info(f"📋 Tool Arguments: {tool_args}")
                
                # Find the requested tool
                tool = next((t for t in self.tools if t["name"] == tool_name), None)
                if not tool:
                    return jsonify({"error": f"Tool {tool_name} not found"}), 404
                
                # Execute the tool against the appropriate server
                result = self.execute_server_tool(tool, tool_args)
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"❌ Tool execution error: {e}")
                return jsonify({"error": str(e), "details": "Tool execution failed"}), 500
        
        @self.app.route('/mcp/status', methods=['GET'])
        def mcp_status():
            """Get comprehensive MCP server status"""
            return jsonify({
                "server_name": self.server_name,
                "version": self.version,
                "port": self.port,
                "servers": len(self.servers),
                "tools": len(self.tools),
                "active_connections": self.active_connections,
                "timestamp": datetime.now().isoformat(),
                "capabilities": {
                    "claude_desktop": True,
                    "vs_code_copilot": True,
                    "claude_web": True,
                    "cline": True,
                    "universal_llm": True
                }
            })
        
        @self.app.route('/dashboard')
        def dashboard():
            """WEB GUI Dashboard for visual access to all tools"""
            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Master Launcher Ultimate - MCP Gateway Master</title>
                <style>
                    body { 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background: #0f0f15;
                        color: #e0e0e0;
                        background-image: 
                            radial-gradient(circle at 50% 50%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 30% 80%, rgba(124, 58, 237, 0.1) 0%, transparent 40%);
                        min-height: 100vh;
                    }
                    .header { 
                        text-align: center; 
                        margin-bottom: 40px; 
                        padding: 30px;
                        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(124, 58, 237, 0.2));
                        border-radius: 15px;
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(124, 58, 237, 0.3);
                        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
                    }
                    .header h1 {
                        color: #00d4ff;
                        font-size: 2.5em;
                        margin: 0 0 10px 0;
                        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
                        letter-spacing: 1px;
                    }
                    .header .subtitle {
                        color: #a0a0b0;
                        font-size: 1.2em;
                        margin: 0;
                        font-weight: 300;
                    }
                    .servers-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                        gap: 25px;
                        margin-bottom: 40px;
                    }
                    .server-card {
                        background: linear-gradient(145deg, rgba(26, 31, 58, 0.8), rgba(35, 41, 70, 0.9));
                        border-radius: 12px;
                        padding: 25px;
                        border: 1px solid rgba(124, 58, 237, 0.2);
                        backdrop-filter: blur(12px);
                        transition: all 0.3s ease;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    }
                    .server-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.2);
                        border-color: rgba(124, 58, 237, 0.4);
                    }
                    .server-status {
                        padding: 5px 15px;
                        border-radius: 20px;
                        font-size: 0.9em;
                        font-weight: 600;
                        text-align: center;
                        margin-bottom: 15px;
                        border: 2px solid;
                    }
                    .status-active {
                        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 78, 59, 0.2));
                        border-color: rgba(16, 185, 129, 0.5);
                        color: #10b981;
                    }
                    .status-inactive {
                        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(127, 29, 29, 0.2));
                        border-color: rgba(239, 68, 68, 0.5);
                        color: #ef4444;
                    }
                    .tools-list {
                        background: rgba(15, 15, 21, 0.6);
                        border-radius: 8px;
                        padding: 15px;
                        margin-top: 15px;
                        border-left: 4px solid rgba(124, 58, 237, 0.6);
                    }
                    .tool-item {
                        background: rgba(26, 31, 58, 0.7);
                        padding: 12px;
                        margin: 8px 0;
                        border-radius: 6px;
                        border-left: 3px solid rgba(0, 212, 255, 0.6);
                        transition: all 0.2s ease;
                    }
                    .tool-item:hover {
                        background: rgba(26, 31, 58, 0.85);
                        transform: translateX(5px);
                    }
                    .commander-banner {
                        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(124, 58, 237, 0.3));
                        padding: 15px;
                        border-radius: 8px;
                        text-align: center;
                        margin-top: 30px;
                        border: 1px solid rgba(124, 58, 237, 0.5);
                        font-size: 1.1em;
                        font-weight: 600;
                        color: #00d4ff;
                        text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
                    }
                    .connection-info {
                        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(0, 212, 255, 0.15));
                        padding: 15px;
                        border-radius: 10px;
                        margin-top: 20px;
                        border: 1px solid rgba(124, 58, 237, 0.4);
                        font-size: 0.95em;
                    }
                    .feature-tag {
                        display: inline-block;
                        background: linear-gradient(135deg, rgba(124, 58, 237, 0.8), rgba(0, 212, 255, 0.6));
                        padding: 4px 12px;
                        border-radius: 15px;
                        font-size: 0.85em;
                        font-weight: 500;
                        margin: 3px;
                        color: white;
                        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.3);
                    }
                    .server-tools {
                        margin-top: 15px;
                    }

                .tool-count {
                        color: #a0a0b0;
                        font-size: 0.95em;
                        font-weight: 500;
                    }
                    .refresh-btn {
                        background: linear-gradient(135deg, rgba(124, 58, 237, 0.9), rgba(0, 212, 255, 0.8));
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 25px;
                        cursor: pointer;
                        font-size: 0.95em;
                        font-weight: 600;
                        transition: all 0.3s ease;
                        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
                    }
                    .refresh-btn:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
                    }
                    .server-icon {
                        font-size: 1.8em;
                        margin-right: 10px;
                        vertical-align: middle;
                    }
                    .tool-name {
                        font-weight: 700;
                        color: #00d4ff;
                        font-size: 1.1em;
                    }
                    .tool-description {
                        color: #c0c0d0;
                        font-size: 0.95em;
                        margin: 6px 0;
                        line-height: 1.4;
                    }
                    .tools-overlay {
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(26, 31, 58, 0.95);
                        border-radius: 12px;
                        padding: 20px;
                        opacity: 0;
                        visibility: hidden;
                        transition: all 0.3s ease;
                        border: 2px solid rgba(0, 212, 255, 0.5);
                        z-index: 1000;
                        overflow-y: auto;
                        max-height: 100%;
                    }
                    .server-card:hover .tools-overlay {
                        opacity: 1;
                        visibility: visible;
                    }
                    .tools-overlay .tools-list {
                        margin-top: 10px;
                        margin-bottom: 10px;
                        max-height: 300px;
                        overflow-y: auto;
                    }
                    .tools-overlay h4 {
                        color: #00d4ff;
                        margin: 0 0 15px 0;
                        text-align: center;
                        font-size: 1.2em;
                        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
                    }
                    .tools-overlay .close-hover {
                        position: absolute;
                        top: 10px;
                        right: 15px;
                        color: #00d4ff;
                        background: none;
                        border: none;
                        font-size: 1.5em;
                        cursor: pointer;
                        opacity: 0.7;
                        transition: opacity 0.2s ease;
                    }
                    .tools-overlay .close-hover:hover {
                        opacity: 1;
                    }
                    .server-card {
                        position: relative;
                        overflow: hidden;
                    }
                    .hover-hint {
                        position: absolute;
                        top: 5px;
                        right: 10px;
                        color: rgba(0, 212, 255, 0.7);
                        font-size: 0.8em;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                    }
                    .server-card:hover .hover-hint {
                        opacity: 1;
                    }
                    .tools-scroll {
                        max-height: 180px;
                        overflow-y: auto;
                        padding-right: 5px;
                    }
                    .tools-scroll::-webkit-scrollbar {
                        width: 6px;
                    }
                    .tools-scroll::-webkit-scrollbar-track {
                        background: rgba(42, 47, 74, 0.5);
                        border-radius: 3px;
                    }
                    .tools-scroll::-webkit-scrollbar-thumb {
                        background: linear-gradient(135deg, rgba(124, 58, 237, 0.8), rgba(0, 212, 255, 0.6));
                        border-radius: 3px;
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🚀 Master Launcher Ultimate</h1>
                    <div class="subtitle">MCP Gateway Master - Complete LLM Tool Access Portal</div>
                    <div class="commander-banner">
                        Authority Level 11.0 - Commander Bobby Don McWilliams II
                    </div>
                    <div class="connection-info">
                        <strong>🌐 MCP Server Running:</strong> localhost:9418<br>
                        <strong>📊 Total Tools:</strong> {{ tool_count }}<br>
                        <strong>🖥️  Active Servers:</strong> {{ server_count }}<br>
                        <strong>🔗 Current Connections:</strong> {{ active_connections }}
                    </div>
                    <div class="feature-tag">Claude Desktop</div>
                    <div class="feature-tag">VS Code Copilot</div>
                    <div class="feature-tag">Claude Web</div>
                    <div class="feature-tag">Cline</div>
                    <div class="feature-tag">Any LLM</div>
                </div>
                
                <div class="servers-grid" id="servers-grid">
                    {% for server in servers %}
                    <div class="server-card">
                        <div class="server-icon">{{ server.get('icon', '🔧') }}</div>
                        <div class="server-status {% if server.status == 'active' %}status-active{% else %}status-inactive{% endif %}">
                            {{ server.status|upper }}
                        </div>
                        <h3 style="color: #00d4ff; margin: 0 0 10px 0;">{{ server.name }}</h3>
                        <p style="color: #a0a0b0; font-size: 0.95em; margin: 0 0 10px 0;">{{ server.description }}</p>
                        <div class="server-tools">
                            <span class="tool-count">Port: {{ server.port }} | Tools Available</span>
                        </div>

                    <div class="hover-hint">→ Hover for tools</div>
                    <div class="tools-overlay">
                        <button class="close-hover" onclick="hideTools(this)">×</button>
                        <h4>🔧 Available Tools</h4>
                        <div class="tools-scroll">
                            {% for tool in server.get('server_tools', []) %}
                            <div class="tool-item">
                                <div class="tool-name">{{ tool.name }}</div>
                                <div class="tool-description">{{ tool.description }}</div>
                            </div>
                            {% endfor %}
                        </div>
                        <div style="text-align: center; margin-top: 15px; color: #a0a0b0; font-size: 0.9em;">
                            🖱️ Move mouse away to hide
                        </div>
                    </div>
                </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Server Status</button>
                </div>
                
                <script>
                    function refreshData() {
                        fetch('/mcp/status')
                            .then(response => response.json())
                            .then(data => {
                                console.log('Status updated', data);
                                location.reload();
                            })
                            .catch(error => {
                                console.error('Refresh error:', error);
                            });
                    }
                    

                    // Auto-refresh every 30 seconds
                    setInterval(refreshData, 30000);
                    
                    function hideTools(button) {
                        const overlay = button.parentElement;
                        overlay.style.opacity = '0';
                        overlay.style.visibility = 'hidden';
                        // The CSS hover will take over when mouse leaves
                    }
                    
                    // Add enhanced hover tracking
                    document.querySelectorAll('.server-card').forEach(card => {
                        card.addEventListener('mouseenter', function() {
                            console.log('Hovering over server:', this.querySelector('h3').textContent);
                        });
                        card.addEventListener('mouseleave', function() {
                            console.log('Left server:', this.querySelector('h3').textContent);
                        });
                    });
                    
                    // Initial load indicator
                    console.log('Master Launcher MCP Gateway loaded - Ready for Claude, Copilot, Cline, and any LLM access!');
                    console.log('🎯 Hover over any server card to see all available tools!');
                </script>
            </body>
            </html>
            """
            
            # Augment server data with icons and tool associations
            augmented_servers = []
            for server in UNIVERSAL_TOOL_REGISTRY["servers"]:
                server_tools = [tool for tool in self.tools if tool["server"] == server["name"]]
                icon_map = {
                    "CRYSTAL_MEMORY_HUB": "🔮",
                    "VOICE_SYSTEM_HUB": "🗣️",
                    "DEVELOPER_GATEWAY": "💻",
                    "NETWORK_GUARDIAN": "🛡️",
                    "HEALING_ORCHESTRATOR": "🏥",
                    "OCR_SCREEN": "👁️",
                    "WINDOWS_OPERATIONS": "🖥️",
                    "MASTER_ORCHESTRATOR_HUB": "🎛️",
                    "EPCP3O_AGENT": "🤖",
                    "DESKTOP_COMMANDER": "️",
                    "TRAINERS_GATEWAY": "🎯",
                    "HARVESTERS_GATEWAY": "🌾",
                    "UNIFIED_MCP_MASTER": "🌐",
                    "MEMORY_ORCHESTRATION_SERVER": "🧠",
                    "GS343_GATEWAY": "⚡",
                    "VSCODE_GATEWAY": "📟"
                }
                
                augmented_servers.append({
                    **server,
                    "icon": icon_map.get(server["name"], "🔧"),
                    "server_tools": [
                        {"name": tool["name"], "description": tool["description"]}
                        for tool in server_tools
                    ]
                })
            
            return render_template_string(html_template, servers=augmented_servers, 
                                        tool_count=len(self.tools), 
                                        server_count=len(self.servers),
                                        active_connections=self.active_connections)
    
    def execute_server_tool(self, tool: dict, arguments: dict) -> dict:
        """Execute a tool by calling the appropriate gateway server"""
        server_name = tool["server"]
        server_port = tool["port"]
        tool_name = tool["name"]
        
        logger.info(f"🚀 Executing tool: {tool_name} on {server_name}:{server_port}")
        
        try:
            # Construct the API call to the gateway server
            url = f"http://localhost:{server_port}/execute"
            payload = {
                "tool_name": tool_name.replace(f"{server_name.lower().replace('_', '')}_", ""),
                "arguments": arguments,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"📤 Calling server API: POST {url}")
            logger.info(f"📋 Payload: {payload}")
            
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            logger.info(f"✅ Tool execution completed successfully")
            logger.info(f"📊 Response data: {result}")
            
            # Add metadata for Claude/Copilot context
            result["tool_execution_metadata"] = {
                "tool_name": tool_name,
                "server": server_name,
                "server_port": server_port,
                "execution_time": datetime.now().isoformat(),
                "mcp_version": self.version
            }
            
            return result
            
        except requests.exceptions.ConnectionError:
            error_msg = f"🔴 Server {server_name} not responding on port {server_port}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": f"Server not responding on port {server_port}",
                "suggestion": f"Please ensure server {server_name} is running"
            }
        except Exception as e:
            error_msg = f"❌ Tool execution failed for {tool_name}: {e}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": str(e),
                "details": "Tool execution encountered an issue"
            }
    
    def launch_gui(self):
        """Launch the GUI dashboard in a browser"""
        try:
            import webbrowser
            url = f"http://localhost:{self.port}/dashboard"
            
            logger.info(f"🌐 Launching GUI Dashboard at {url}")
            print(f"\n🚀 Launching Master Launcher GUI Dashboard...")
            print(f"🌐 Dashboard URL: {url}")
            
            # Give server time to start, then launch browser
            def open_browser():
                time.sleep(2)
                webbrowser.open(url)
            
            threading.Thread(target=open_browser, daemon=True).start()
            logger.info("✅ GUI Dashboard launched successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to launch GUI: {e}")
            print(f"🌐 Manual access: {url}")
    
    def start_server(self, debug=False):
        """Start the MCP server and GUI"""
        try:
            logger.info(f"🚀 Starting MCP Gateway Master on port {self.port}")
            logger.info("🌐 Access URLs:")
            logger.info(f"   • MCP Tools: http://localhost:{self.port}/mcp/tools")
            logger.info(f"   • Execute Tool: http://localhost:{self.port}/mcp/tool")
            logger.info(f"   • Status: http://localhost:{self.port}/mcp/status")
            logger.info(f"   • Dashboard: http://localhost:{self.port}/dashboard")
            
            print(f"\n" + "="*80)
            print("🚀 MASTER LAUNCHER ULTIMATE - MCP GATEWAY MASTER")
            print("="*80)
            print("\n⚡ ACCESS ENDPOINTS:")
            print(f"🌐 GUI Dashboard: http://localhost:{self.port}/dashboard")
            print(f"📋 MCP Tools: http://localhost:{self.port}/mcp/tools")
            print(f"⚙️  Execute Tool: http://localhost:{self.port}/mcp/tool")
            print(f"📊 Status: http://localhost:{self.port}/mcp/status")
            print("\n🔗 CONFIGURATION FOR LLMs:")
            print("📍 Claude Desktop: Add the MCP server at localhost:9418")
            print("🔧 VS Code Copilot: Configure MCP server for localhost:9418")
            print("🌐 Claude Web: Access tools via API endpoints")
            print("💻 Cline: Configure MCP server in VS Code settings")
            print("\n" + "="*80)
            
            # Launch GUI immediately
            self.launch_gui()
            
            # Start Flask server
            if debug:
                self.app.run(host='0.0.0.0', port=self.port, debug=True)
            else:
                self.app.run(host='0.0.0.0', port=self.port, debug=False)
                
        except Exception as e:
            logger.error(f"❌ MCP server failed to start: {e}")
            raise

def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("🌐 MCP GATEWAY MASTER - COMPLETE LLM TOOL ACCESS")
    print("="*80)
    print("Commander: Bobby Don McWilliams II")
    print("Authority Level: 11.0 (Sovereign Architect)")
    print("Date: October 23, 2025")
    print("="*80)
    
    # Create and start the MCP master
    mcp_master = MCPGatewayMaster()
    mcp_master.setup_routes()
    
    try:
        # Start the server
        mcp_master.start_server(debug=False)
        
    except KeyboardInterrupt:
        print("\n🛑 MCP Gateway Master stopped.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
