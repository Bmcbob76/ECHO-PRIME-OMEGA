#!/usr/bin/env python3
"""
TRAINERS_GATEWAY - MCP stdio Server
AI model training and fine-tuning gateway

Tools:
- train_health: Health check
- train_start_session: Start training session
- train_add_example: Add training example
- train_evaluate: Evaluate current training
- train_export: Export trained model/dataset
- train_stats: Get training statistics
"""

import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

CURRENT_FILE = Path(__file__).resolve()
MLS_ROOT = CURRENT_FILE.parents[3]
TRAINING_DIR = MLS_ROOT / "training_data"
TRAINING_DIR.mkdir(exist_ok=True)
EKM_DIR = MLS_ROOT / "ekm_output"  # Share EKM dir with harvesters
EKM_DIR.mkdir(exist_ok=True)

log_dir = MLS_ROOT / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - TRAINERS_GATEWAY - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "trainers_gateway_mcp.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("TRAINERS_GATEWAY")

training_sessions = {}
train_stats = {
    "total_sessions": 0,
    "total_examples": 0,
    "active_sessions": 0
}

class TrainersMCPServer:
    def __init__(self):
        self.client_type = "unknown"
    
    def get_tools(self):
        return [
            {
                "name": "train_health",
                "description": "Check Trainers Gateway health",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "train_start_session",
                "description": "Start a new training session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Session name"},
                        "model_type": {"type": "string", "description": "Model type to train"},
                        "description": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "Session description"}
                    },
                    "required": ["name", "model_type"]
                }
            },
            {
                "name": "train_add_example",
                "description": "Add training example to session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Training session ID"},
                        "input": {"type": "string", "description": "Training input"},
                        "output": {"type": "string", "description": "Expected output"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Example tags"}
                    },
                    "required": ["session_id", "input", "output"]
                }
            },
            {
                "name": "train_evaluate",
                "description": "Evaluate training session progress",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Training session ID"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "train_export",
                "description": "Export training data/model",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Training session ID"},
                        "format": {"type": "string", "description": "Export format (json|csv|jsonl)", "default": "jsonl"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "train_stats",
                "description": "Get training statistics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "train_generate_ekm",
                "description": "Generate EKM from training session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Training session ID"},
                        "include_examples": {"type": "boolean", "description": "Include all examples in EKM", "default": True}
                    },
                    "required": ["session_id"]
                }
            }
        ]
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any]):
        try:
            if name == "train_health":
                return {"success": True, "service": "TRAINERS_GATEWAY", "training_dir": str(TRAINING_DIR), "active_sessions": train_stats["active_sessions"]}
            
            if name == "train_stats":
                return {"success": True, "stats": train_stats, "sessions": list(training_sessions.keys())}
            
            if name == "train_start_session":
                session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                training_sessions[session_id] = {
                    "name": arguments["name"],
                    "model_type": arguments["model_type"],
                    "description": arguments.get("description", ""),
                    "created": datetime.now().isoformat(),
                    "examples": [],
                    "status": "active"
                }
                train_stats["total_sessions"] += 1
                train_stats["active_sessions"] += 1
                logger.info(f"Started training session: {session_id}")
                return {"success": True, "session_id": session_id, "details": training_sessions[session_id]}
            
            if name == "train_add_example":
                session_id = arguments["session_id"]
                if session_id not in training_sessions:
                    return {"success": False, "error": "Session not found"}
                
                example = {
                    "input": arguments["input"],
                    "output": arguments["output"],
                    "tags": arguments.get("tags", []),
                    "added": datetime.now().isoformat()
                }
                training_sessions[session_id]["examples"].append(example)
                train_stats["total_examples"] += 1
                
                return {"success": True, "example_count": len(training_sessions[session_id]["examples"])}
            
            if name == "train_evaluate":
                session_id = arguments["session_id"]
                if session_id not in training_sessions:
                    return {"success": False, "error": "Session not found"}
                
                session = training_sessions[session_id]
                evaluation = {
                    "session_id": session_id,
                    "example_count": len(session["examples"]),
                    "status": session["status"],
                    "quality_score": min(100, len(session["examples"]) * 10),  # Simple quality metric
                    "ready_for_export": len(session["examples"]) >= 5
                }
                return {"success": True, "evaluation": evaluation}
            
            if name == "train_export":
                session_id = arguments["session_id"]
                if session_id not in training_sessions:
                    return {"success": False, "error": "Session not found"}
                
                session = training_sessions[session_id]
                format_type = arguments.get("format", "jsonl")
                
                export_file = TRAINING_DIR / f"{session['name']}_{session_id}.{format_type}"
                
                if format_type == "jsonl":
                    with export_file.open("w", encoding="utf-8") as f:
                        for ex in session["examples"]:
                            f.write(json.dumps({"input": ex["input"], "output": ex["output"]}) + "\n")
                elif format_type == "json":
                    export_file.write_text(json.dumps(session, indent=2), encoding="utf-8")
                else:
                    return {"success": False, "error": f"Unsupported format: {format_type}"}
                
                training_sessions[session_id]["status"] = "exported"
                train_stats["active_sessions"] -= 1
                
                return {"success": True, "export_file": str(export_file), "format": format_type, "example_count": len(session["examples"])}
            
            if name == "train_generate_ekm":
                session_id = arguments["session_id"]
                if session_id not in training_sessions:
                    return {"success": False, "error": "Session not found"}
                
                session = training_sessions[session_id]
                include_examples = arguments.get("include_examples", True)
                
                # Generate EKM from training session
                ekm_content = f"# Training Session EKM: {session['name']}\n\n"
                ekm_content += f"**Model Type:** {session['model_type']}\n"
                ekm_content += f"**Description:** {session.get('description', 'N/A')}\n"
                ekm_content += f"**Created:** {session['created']}\n"
                ekm_content += f"**Status:** {session['status']}\n"
                ekm_content += f"**Example Count:** {len(session['examples'])}\n\n"
                ekm_content += "---\n\n"
                
                if include_examples and session['examples']:
                    ekm_content += "## Training Examples\n\n"
                    for i, ex in enumerate(session['examples'], 1):
                        ekm_content += f"### Example {i}\n\n"
                        ekm_content += f"**Input:**\n```\n{ex['input']}\n```\n\n"
                        ekm_content += f"**Output:**\n```\n{ex['output']}\n```\n\n"
                        if ex.get('tags'):
                            ekm_content += f"**Tags:** {', '.join(ex['tags'])}\n\n"
                    
                ekm_file = EKM_DIR / f"ekm_training_{session['name']}_{session_id}.md"
                ekm_file.write_text(ekm_content, encoding="utf-8")
                train_stats["total_examples"] += 1  # Track EKM generation
                
                return {"success": True, "ekm_file": str(ekm_file), "session_id": session_id, "example_count": len(session['examples'])}
            
            return {"success": False, "error": f"Unknown tool: {name}"}
        
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "error": str(e)}
    
    async def handle_initialize(self, params):
        client_info = params.get("clientInfo", {})
        name = client_info.get("name", "unknown").lower()
        if "copilot" in name:
            self.client_type = "vscode_copilot"
        elif "claude" in name:
            self.client_type = "claude_desktop"
        logger.info(f"MCP initialize from: {self.client_type}")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "trainers-gateway", "version": "1.0.0"}
        }
    
    async def handle_list_tools(self):
        return {"tools": self.get_tools()}
    
    async def handle_call_tool(self, params):
        name = params.get("name")
        arguments = params.get("arguments", {})
        logger.info(f"Tool call: {name}")
        result = await self.execute_tool(name, arguments)
        content_text = json.dumps(result, indent=2)
        return {"content": [{"type": "text", "text": content_text}], "isError": not result.get("success", False)}
    
    async def handle_request(self, request):
        method = request.get("method")
        params = request.get("params", {})
        if method == "initialize":
            return await self.handle_initialize(params)
        elif method == "tools/list":
            return await self.handle_list_tools()
        elif method == "tools/call":
            return await self.handle_call_tool(params)
        return {"error": {"code": -32601, "message": f"Method not found: {method}"}}
    
    async def run(self):
        logger.info("TRAINERS_GATEWAY MCP starting...")
        loop = asyncio.get_event_loop()
        while True:
            try:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                request = json.loads(line)
                req_id = request.get("id")
                if req_id is not None:
                    req_id = str(req_id)
                result = await self.handle_request(request)
                if "error" in result:
                    response = {"jsonrpc": "2.0", "id": req_id, "error": result["error"]}
                else:
                    response = {"jsonrpc": "2.0", "id": req_id, "result": result}
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
        logger.info("TRAINERS_GATEWAY MCP shutting down")

async def main():
    server = TrainersMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
