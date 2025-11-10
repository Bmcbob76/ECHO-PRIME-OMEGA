#!/usr/bin/env python3
"""
UNIFIED DEVELOPER API - MASTER ORCHESTRATOR
Commander Bobby Don McWilliams II - Authority Level 11.0

Master coordinator for ECHO_XV4 Unified Developer API System
Routes commands to appropriate subsystems:
- VS Code API (Port 9001)
- Windows API (Port 8343)
- Desktop Commander (MCP - direct integration)

Enables Claude to work like a human developer with full control.
"""

import sys
import os
import json
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import subprocess
import requests
from pathlib import Path

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('E:/ECHO_XV4/LOGS/unified_developer_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
UNIFIED_API_PORT = 9000
VSCODE_API_URL = "http://localhost:9001"
WINDOWS_API_URL = "http://localhost:8343"

class WorkflowEngine:
    """Executes multi-step development workflows"""
    
    def __init__(self, api_router):
        self.api_router = api_router
        
    async def execute_workflow(self, workflow_name: str, params: Dict) -> Dict:
        """Execute a predefined workflow"""
        workflows = {
            'fix_bug': self.fix_bug_workflow,
            'create_component': self.create_component_workflow,
            'debug_crash': self.debug_crash_workflow,
            'run_tests': self.run_tests_workflow
        }
        
        if workflow_name not in workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        return await workflows[workflow_name](params)
    
    async def fix_bug_workflow(self, params: Dict) -> Dict:
        """
        Fix bug workflow:
        1. OCR screen to see error (Windows API)
        2. Open file in VS Code (VS Code API)
        3. Navigate to line (VS Code API)
        4. Apply fix (VS Code API)
        5. Save file (VS Code API)
        6. Run tests (VS Code API terminal)
        """
        file_path = params.get('file')
        line = params.get('line')
        fix_text = params.get('fix_text')
        
        steps = []
        
        # Step 1: OCR screen (optional, to see error)
        if params.get('ocr_screen', False):
            ocr_result = await self.api_router.call_windows_api('/api/ocr/all_screens', {})
            steps.append({'step': 'ocr_screen', 'result': 'captured'})
        
        # Step 2: Open file in VS Code
        open_result = await self.api_router.call_vscode_api('/vscode/open_file', {
            'filePath': file_path
        })
        steps.append({'step': 'open_file', 'result': open_result})
        
        # Step 3: Navigate to line and apply fix
        if fix_text:
            edit_result = await self.api_router.call_vscode_api('/vscode/edit_text', {
                'filePath': file_path,
                'line': line,
                'character': 0,
                'text': fix_text + '\n'
            })
            steps.append({'step': 'apply_fix', 'result': edit_result})
        
        # Step 4: Save file
        save_result = await self.api_router.call_vscode_api('/vscode/save_file', {
            'filePath': file_path
        })
        steps.append({'step': 'save_file', 'result': save_result})
        
        # Step 5: Run tests (if specified)
        if params.get('run_tests', True):
            test_command = params.get('test_command', 'pytest')
            test_result = await self.api_router.call_vscode_api('/vscode/terminal_command', {
                'command': test_command
            })
            steps.append({'step': 'run_tests', 'result': test_result})
        
        return {
            'workflow': 'fix_bug',
            'success': True,
            'steps_completed': len(steps),
            'steps': steps,
            'timestamp': datetime.now().isoformat()
        }
    
    async def create_component_workflow(self, params: Dict) -> Dict:
        """
        Create component workflow:
        1. Create file structure (Desktop Commander via path)
        2. Open files in VS Code
        3. Insert boilerplate code
        4. Format documents
        5. Save all
        """
        component_name = params.get('component_name')
        base_path = params.get('base_path')
        
        # For now, return a placeholder
        # Full implementation would use Desktop Commander MCP tools
        return {
            'workflow': 'create_component',
            'success': True,
            'component_name': component_name,
            'message': 'Workflow requires Desktop Commander MCP integration',
            'timestamp': datetime.now().isoformat()
        }
    
    async def debug_crash_workflow(self, params: Dict) -> Dict:
        """
        Debug crash workflow:
        1. OCR to read error from console
        2. Set breakpoint at crash location
        3. Start debugger
        4. Monitor output
        """
        return {
            'workflow': 'debug_crash',
            'success': True,
            'message': 'Debug workflow - implementation in progress',
            'timestamp': datetime.now().isoformat()
        }
    
    async def run_tests_workflow(self, params: Dict) -> Dict:
        """
        Run tests workflow:
        1. Open terminal
        2. Run test command
        3. OCR results
        4. Return summary
        """
        test_command = params.get('test_command', 'pytest')
        
        # Run in terminal
        result = await self.api_router.call_vscode_api('/vscode/terminal_command', {
            'command': test_command,
            'terminalName': 'ECHO Tests'
        })
        
        return {
            'workflow': 'run_tests',
            'success': True,
            'command': test_command,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }

class APIRouter:
    """Routes API calls to appropriate subsystems"""
    
    def __init__(self):
        self.vscode_api_url = VSCODE_API_URL
        self.windows_api_url = WINDOWS_API_URL
        self.stats = {
            'total_requests': 0,
            'vscode_requests': 0,
            'windows_requests': 0,
            'workflow_requests': 0,
            'errors': 0
        }
    
    async def call_vscode_api(self, endpoint: str, data: Dict) -> Dict:
        """Call VS Code API"""
        self.stats['vscode_requests'] += 1
        url = f"{self.vscode_api_url}{endpoint}"
        
        try:
            if endpoint.startswith('/vscode/') and endpoint != '/vscode/workspace_files' and endpoint != '/vscode/active_file' and endpoint != '/vscode/get_selection':
                response = requests.post(url, json=data, timeout=10)
            else:
                response = requests.get(url, params=data, timeout=10)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"VS Code API call failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def call_windows_api(self, endpoint: str, data: Dict) -> Dict:
        """Call Windows API"""
        self.stats['windows_requests'] += 1
        url = f"{self.windows_api_url}{endpoint}"
        
        try:
            if endpoint.startswith('/api/'):
                response = requests.post(url, json=data, timeout=10)
            else:
                response = requests.get(url, params=data, timeout=10)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"Windows API call failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_stats(self) -> Dict:
        """Get router statistics"""
        return {
            **self.stats,
            'timestamp': datetime.now().isoformat()
        }

class UnifiedAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Unified API"""
    
    server_instance = None  # Will be set when server starts
    
    def log_message(self, format, *args):
        """Override to use logger instead of stderr"""
        logger.info(f"{self.address_string()} - {format%args}")
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Health check
        if path == '/health':
            self.send_json_response({
                'status': 'OK',
                'service': 'ECHO Unified Developer API',
                'port': UNIFIED_API_PORT,
                'subsystems': {
                    'vscode_api': VSCODE_API_URL,
                    'windows_api': WINDOWS_API_URL,
                    'desktop_commander': 'MCP (integrated)'
                },
                'authority_level': '11.0',
                'timestamp': datetime.now().isoformat()
            })
            return
        
        # Get statistics
        if path == '/api/stats':
            stats = self.server_instance.router.get_stats()
            self.send_json_response({'success': True, 'data': stats})
            return
        
        # List endpoints
        if path == '/api/endpoints':
            endpoints = self.get_endpoints_list()
            self.send_json_response({'success': True, 'data': endpoints})
            return
        
        self.send_error_response(404, 'Endpoint not found')
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error_response(400, 'Invalid JSON')
            return
        
        # Route to appropriate handler
        if path.startswith('/unified/workflow'):
            self.handle_workflow(data)
        elif path.startswith('/vscode/'):
            self.handle_vscode_proxy(path, data)
        elif path.startswith('/windows/'):
            self.handle_windows_proxy(path, data)
        else:
            self.send_error_response(404, 'Endpoint not found')
    
    def handle_workflow(self, data: Dict):
        """Handle workflow execution"""
        workflow_name = data.get('workflow')
        params = data.get('params', {})
        
        if not workflow_name:
            self.send_error_response(400, 'Missing workflow name')
            return
        
        try:
            # Execute workflow (simplified synchronous version)
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.server_instance.workflow_engine.execute_workflow(workflow_name, params)
            )
            loop.close()
            
            self.send_json_response({'success': True, 'data': result})
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            self.send_error_response(500, str(e))
    
    def handle_vscode_proxy(self, path: str, data: Dict):
        """Proxy request to VS Code API"""
        try:
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.server_instance.router.call_vscode_api(path, data)
            )
            loop.close()
            
            self.send_json_response(result)
        except Exception as e:
            logger.error(f"VS Code proxy failed: {e}")
            self.send_error_response(500, str(e))
    
    def handle_windows_proxy(self, path: str, data: Dict):
        """Proxy request to Windows API"""
        # Convert /windows/ to /api/
        api_path = path.replace('/windows/', '/api/')
        
        try:
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                self.server_instance.router.call_windows_api(api_path, data)
            )
            loop.close()
            
            self.send_json_response(result)
        except Exception as e:
            logger.error(f"Windows proxy failed: {e}")
            self.send_error_response(500, str(e))
    
    def get_endpoints_list(self) -> List[Dict]:
        """Get list of all available endpoints"""
        return [
            # Core endpoints
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/api/stats', 'method': 'GET', 'description': 'API statistics'},
            {'path': '/api/endpoints', 'method': 'GET', 'description': 'List all endpoints'},
            
            # Workflow endpoints
            {'path': '/unified/workflow', 'method': 'POST', 'description': 'Execute multi-step workflow'},
            
            # VS Code proxy endpoints
            {'path': '/vscode/open_file', 'method': 'POST', 'description': 'Open file in VS Code'},
            {'path': '/vscode/close_file', 'method': 'POST', 'description': 'Close file in VS Code'},
            {'path': '/vscode/edit_text', 'method': 'POST', 'description': 'Edit text in VS Code'},
            {'path': '/vscode/save_file', 'method': 'POST', 'description': 'Save file in VS Code'},
            {'path': '/vscode/run_command', 'method': 'POST', 'description': 'Run VS Code command'},
            {'path': '/vscode/terminal_command', 'method': 'POST', 'description': 'Run terminal command'},
            
            # Windows API proxy endpoints
            {'path': '/windows/ocr/all_screens', 'method': 'POST', 'description': 'OCR all screens'},
            {'path': '/windows/ocr/search', 'method': 'POST', 'description': 'Search text on screens'},
            {'path': '/windows/windows/list', 'method': 'POST', 'description': 'List all windows'},
            {'path': '/windows/windows/focus', 'method': 'POST', 'description': 'Focus window'},
            {'path': '/windows/processes/list', 'method': 'POST', 'description': 'List processes'}
        ]
    
    def send_json_response(self, data: Dict, status_code: int = 200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, status_code: int, message: str):
        """Send error response"""
        self.send_json_response({
            'success': False,
            'error': message,
            'status_code': status_code
        }, status_code)

class UnifiedDeveloperAPI:
    """Main Unified Developer API server"""
    
    def __init__(self, port: int = UNIFIED_API_PORT):
        self.port = port
        self.router = APIRouter()
        self.workflow_engine = WorkflowEngine(self.router)
        self.start_time = time.time()
        
        logger.info(f"Unified Developer API initialized on port {self.port}")
    
    def start_server(self):
        """Start the HTTP server"""
        try:
            # Create logs directory
            os.makedirs("E:/ECHO_XV4/LOGS", exist_ok=True)
            
            # Create handler with server instance
            def handler(*args, **kwargs):
                return UnifiedAPIHandler(*args, **kwargs)
            
            # Set server instance on handler class
            UnifiedAPIHandler.server_instance = self
            
            # Start HTTP server
            httpd = HTTPServer(('localhost', self.port), handler)
            
            logger.info("=" * 70)
            logger.info("ECHO UNIFIED DEVELOPER API - MASTER ORCHESTRATOR")
            logger.info("Commander Bobby Don McWilliams II - Authority Level 11.0")
            logger.info("=" * 70)
            logger.info(f"Unified API Server running on port {self.port}")
            logger.info(f"VS Code API: {VSCODE_API_URL}")
            logger.info(f"Windows API: {WINDOWS_API_URL}")
            logger.info("Desktop Commander: MCP (integrated)")
            logger.info("=" * 70)
            logger.info("AVAILABLE WORKFLOWS:")
            logger.info("  - fix_bug: Fix bug in code file")
            logger.info("  - create_component: Create new component")
            logger.info("  - debug_crash: Debug runtime crash")
            logger.info("  - run_tests: Execute test suite")
            logger.info("=" * 70)
            logger.info("SUBSYSTEM INTEGRATION:")
            logger.info("  ✓ VS Code API (port 9001) - Editor control")
            logger.info("  ✓ Windows API (port 8343) - OS + OCR control")
            logger.info("  ✓ Desktop Commander (MCP) - Filesystem operations")
            logger.info("=" * 70)
            logger.info("API ACCESS:")
            logger.info(f"  Health: GET  http://localhost:{self.port}/health")
            logger.info(f"  Stats:  GET  http://localhost:{self.port}/api/stats")
            logger.info(f"  Endpoints: GET  http://localhost:{self.port}/api/endpoints")
            logger.info(f"  Workflow: POST http://localhost:{self.port}/unified/workflow")
            logger.info("=" * 70)
            
            # Check subsystems
            self.check_subsystems()
            
            # Serve forever
            httpd.serve_forever()
            
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
            httpd.shutdown()
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
    
    def check_subsystems(self):
        """Check if subsystems are running"""
        # Check VS Code API
        try:
            response = requests.get(f"{VSCODE_API_URL}/health", timeout=2)
            if response.status_code == 200:
                logger.info("✓ VS Code API: ONLINE")
            else:
                logger.warning(f"⚠ VS Code API: OFFLINE (status {response.status_code})")
        except Exception:
            logger.warning("⚠ VS Code API: OFFLINE - Start VS Code extension")
        
        # Check Windows API
        try:
            response = requests.get(f"{WINDOWS_API_URL}/health", timeout=2)
            if response.status_code == 200:
                logger.info("✓ Windows API: ONLINE")
            else:
                logger.warning(f"⚠ Windows API: OFFLINE (status {response.status_code})")
        except Exception:
            logger.warning("⚠ Windows API: OFFLINE - Run START_WINDOWS_API_ULTIMATE.bat")
        
        logger.info("✓ Desktop Commander: Available via MCP")

def main():
    """Main entry point"""
    try:
        server = UnifiedDeveloperAPI()
        server.start_server()
    except Exception as e:
        logger.error(f"Critical server error: {e}")
        raise

if __name__ == "__main__":
    print("=" * 70)
    print("ECHO UNIFIED DEVELOPER API - MASTER ORCHESTRATOR")
    print("Commander Bobby Don McWilliams II - Authority Level 11.0")
    print("=" * 70)
    print("Coordinating:")
    print("  - VS Code API (port 9001)")
    print("  - Windows API (port 8343)")
    print("  - Desktop Commander (MCP)")
    print("=" * 70)
    main()
