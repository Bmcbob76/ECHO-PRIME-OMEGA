#!/usr/bin/env python3
"""
MEMORY_ORCHESTRATION_SERVER - MCP Gateway (GATEWAYS)
Commander: Bobby Don McWilliams II
Authority Level: 11.0

Purpose:
- Consolidated MCP stdio gateway for memory orchestration
- Crystal Memory Hub operations
- G: Drive and M: Drive coordination
- EKM generation and query routing

Discovery Hints:
- Type: MCP (stdio)
- Entry: stdio JSON-RPC server

Tools:
- memorch_health {}
- memorch_store { content, tier?, tags? }
- memorch_query { query, source? }
- memorch_stats {}
"""

import sys
import json
import asyncio
import logging
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path
import subprocess

logger = logging.getLogger("MemoryOrchestrationMCP")
logging.basicConfig(level=logging.INFO)

# 9-Layer Memory Architecture
MEMORY_LAYERS = {
    "L0": {"name": "Ephemeral", "retention": timedelta(hours=1)},
    "L1": {"name": "Short-term", "retention": timedelta(hours=24)},
    "L2": {"name": "Working", "retention": timedelta(days=7)},
    "L3": {"name": "Medium-term", "retention": timedelta(days=30)},
    "L4": {"name": "Long-term", "retention": timedelta(days=180)},
    "L5": {"name": "Extended", "retention": timedelta(days=730)},
    "L6": {"name": "Archival", "retention": timedelta(days=1825)},
    "L7": {"name": "Deep Archival", "retention": timedelta(days=3650)},
    "L8": {"name": "Permanent", "retention": None}  # No expiration
}

class ConversationRecorder:
    """Automatically records conversations to memory system"""
    
    def __init__(self):
        self.conversation_buffer = []
        self.last_record_time = time.time()
        self.recording_interval = 300  # 5 minutes
        
    def add_message(self, role: str, content: str):
        """Add a message to conversation buffer"""
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_buffer.append(message)
        
        # Check if we should record to memory
        current_time = time.time()
        if (current_time - self.last_record_time >= self.recording_interval or 
            len(self.conversation_buffer) >= 10):
            self._record_conversation_segment()
    
    def _record_conversation_segment(self):
        """Record current conversation segment to memory"""
        if not self.conversation_buffer:
            return
            
        # Create conversation summary
        summary = self._create_conversation_summary()
        
        # Store in memory system (L2 - Working memory)
        memory_content = {
            "type": "conversation_segment",
            "summary": summary,
            "messages": self.conversation_buffer.copy(),
            "timestamp": datetime.now().isoformat(),
            "message_count": len(self.conversation_buffer)
        }
        
        # Use crystal memory hub to store
        try:
            self._store_to_crystal_memory(
                title=f"Conversation Segment {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                content=json.dumps(memory_content, indent=2),
                tags=["conversation", "auto-recorded", "working-memory"]
            )
            
            logger.info(f"Recorded conversation segment with {len(self.conversation_buffer)} messages")
            self.conversation_buffer.clear()
            self.last_record_time = time.time()
            
        except Exception as e:
            logger.error(f"Failed to record conversation: {e}")
    
    def _create_conversation_summary(self) -> str:
        """Create a summary of the current conversation segment"""
        if not self.conversation_buffer:
            return "Empty conversation"
            
        user_messages = [msg for msg in self.conversation_buffer if msg["role"] == "user"]
        assistant_messages = [msg for msg in self.conversation_buffer if msg["role"] == "assistant"]
        
        summary_parts = [
            f"Conversation segment with {len(user_messages)} user messages and {len(assistant_messages)} assistant messages.",
            f"Topics discussed: {self._extract_topics()}"
        ]
        
        return " ".join(summary_parts)
    
    def _extract_topics(self) -> str:
        """Extract key topics from conversation"""
        # Simple topic extraction - can be enhanced
        all_content = " ".join([msg["content"] for msg in self.conversation_buffer])
        keywords = ["code", "file", "project", "memory", "system", "tool", "command", "error", "test"]
        found_topics = [kw for kw in keywords if kw in all_content.lower()]
        return ", ".join(found_topics) if found_topics else "general discussion"
    
    def _store_to_crystal_memory(self, title: str, content: str, tags: List[str]):
        """Store content to crystal memory hub"""
        # This would integrate with the crystal memory hub MCP server
        # For now, we'll create a local record on M: DRIVE ONLY
        memory_dir = Path("M:/CRYSTALS_NEW")
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        memory_file = memory_dir / f"{title.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.json"
        memory_data = {
            "title": title,
            "content": content,
            "tags": tags,
            "timestamp": datetime.now().isoformat(),
            "layer": "L2",
            "type": "conversation"
        }
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=2)

class MemoryOrchestrationMCPServer:
    def __init__(self) -> None:
        self.client_type = "unknown"
        self.conversation_recorder = ConversationRecorder()
        self.memory_stats = {
            "total_stored": 0,
            "layers": {layer: 0 for layer in MEMORY_LAYERS},
            "last_updated": datetime.now().isoformat()
        }

    def get_tools(self):
        return [
            {"name": "memorch_health", "description": "Check Memory Orchestration MCP health", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "memorch_store", "description": "Store memory/crystal", "inputSchema": {"type": "object", "properties": {"content": {"type": "string"}, "tier": {"type": "string", "default": "M"}, "tags": {"type": "array", "default": []}}, "required": ["content"]}},
            {"name": "memorch_query", "description": "Query memory systems", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "source": {"type": "string", "default": "ALL"}}, "required": ["query"]}},
            {"name": "memorch_stats", "description": "Get memory statistics", "inputSchema": {"type": "object", "properties": {}, "required": []}},
            {"name": "memorch_record", "description": "Record conversation message for auto-capture", "inputSchema": {"type": "object", "properties": {"role": {"type": "string", "description": "user or assistant"}, "content": {"type": "string", "description": "Message content"}}, "required": ["role", "content"]}},
        ]

    def _store_memory(self, content: str, tier: str = "M", tags: List[str] = None) -> Dict[str, Any]:
        """Store content in the appropriate memory layer"""
        if tags is None:
            tags = []
        
        # Determine memory layer based on tier
        layer = self._get_layer_for_tier(tier)
        
        # Create memory record
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        memory_data = {
            "id": memory_id,
            "content": content,
            "tags": tags,
            "layer": layer,
            "tier": tier,
            "timestamp": timestamp,
            "expires": self._calculate_expiration(layer)
        }
        
        # Store to appropriate drive
        storage_path = self._store_to_drive(memory_data, layer)
        
        # Update statistics
        self.memory_stats["total_stored"] += 1
        self.memory_stats["layers"][layer] += 1
        self.memory_stats["last_updated"] = timestamp
        
        return {
            "success": True,
            "memory_id": memory_id,
            "layer": layer,
            "storage_path": str(storage_path),
            "content_length": len(content)
        }
    
    def _get_layer_for_tier(self, tier: str) -> str:
        """Map tier to appropriate memory layer"""
        tier_mapping = {
            "L0": "L0", "L1": "L1", "L2": "L2", "L3": "L3", "L4": "L4",
            "L5": "L5", "L6": "L6", "L7": "L7", "L8": "L8",
            "M": "L2",  # Default to working memory
            "G": "L4",  # Default to long-term memory
            "EPHEMERAL": "L0",
            "SHORT_TERM": "L1",
            "WORKING": "L2",
            "MEDIUM_TERM": "L3",
            "LONG_TERM": "L4",
            "EXTENDED": "L5",
            "ARCHIVAL": "L6",
            "DEEP_ARCHIVAL": "L7",
            "PERMANENT": "L8"
        }
        return tier_mapping.get(tier.upper(), "L2")
    
    def _calculate_expiration(self, layer: str) -> Optional[str]:
        """Calculate expiration timestamp for memory layer"""
        layer_config = MEMORY_LAYERS.get(layer)
        if not layer_config or not layer_config["retention"]:
            return None
        
        expiration = datetime.now() + layer_config["retention"]
        return expiration.isoformat()
    
    def _store_to_drive(self, memory_data: Dict, layer: str) -> Path:
        """Store memory data to appropriate drive location"""
        # ALL MEMORY LAYERS USE M: DRIVE - NO C: DRIVE
        # Determine storage location based on layer
        if layer in ["L0", "L1", "L2"]:  # Ephemeral to Working memory
            base_dir = Path("M:/MEMORIES")
        elif layer in ["L3", "L4", "L5"]:  # Medium-term to Extended memory
            base_dir = Path("M:/MEMORIES")
        else:  # L6-L8: Archival to Permanent memory
            base_dir = Path("M:/CRYSTALS")
        
        # Create layer-specific directory
        layer_dir = base_dir / layer
        layer_dir.mkdir(parents=True, exist_ok=True)
        
        # Save memory file
        memory_file = layer_dir / f"{memory_data['id']}.json"
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=2, ensure_ascii=False)
        
        return memory_file
    
    def _query_memory(self, query: str, source: str = "ALL") -> Dict[str, Any]:
        """Query memory systems for relevant content"""
        results = []
        
        # Determine which layers to search
        layers_to_search = []
        if source == "ALL":
            layers_to_search = list(MEMORY_LAYERS.keys())
        elif source in MEMORY_LAYERS:
            layers_to_search = [source]
        else:
            # Try to map source to layer
            layer = self._get_layer_for_tier(source)
            layers_to_search = [layer] if layer in MEMORY_LAYERS else list(MEMORY_LAYERS.keys())
        
        # Search each layer
        for layer in layers_to_search:
            layer_results = self._search_layer(layer, query)
            results.extend(layer_results)
        
        # Sort by relevance (simple implementation)
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return {
            "query": query,
            "source": source,
            "results_found": len(results),
            "results": results[:10]  # Limit to top 10
        }
    
    def _search_layer(self, layer: str, query: str) -> List[Dict]:
        """Search a specific memory layer for query matches"""
        results = []
        
        # ALL LAYERS USE M: DRIVE
        # Determine directory for this layer
        if layer in ["L0", "L1", "L2"]:
            base_dir = Path("M:/MEMORIES")
        elif layer in ["L3", "L4", "L5"]:
            base_dir = Path("M:/MEMORIES")
        else:
            base_dir = Path("M:/CRYSTALS")
        
        layer_dir = base_dir / layer
        
        if not layer_dir.exists():
            return results
        
        # Search through memory files in this layer
        for memory_file in layer_dir.glob("*.json"):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                
                # Simple text matching for relevance
                relevance_score = self._calculate_relevance(memory_data, query)
                
                if relevance_score > 0:
                    results.append({
                        "memory_id": memory_data.get("id"),
                        "content": memory_data.get("content", "")[:200] + "..." if len(memory_data.get("content", "")) > 200 else memory_data.get("content", ""),
                        "layer": layer,
                        "timestamp": memory_data.get("timestamp"),
                        "tags": memory_data.get("tags", []),
                        "relevance_score": relevance_score,
                        "storage_path": str(memory_file)
                    })
                    
            except Exception as e:
                logger.warning(f"Failed to read memory file {memory_file}: {e}")
        
        return results
    
    def _calculate_relevance(self, memory_data: Dict, query: str) -> float:
        """Calculate relevance score for memory content against query"""
        content = memory_data.get("content", "").lower()
        tags = [tag.lower() for tag in memory_data.get("tags", [])]
        query_lower = query.lower()
        
        score = 0.0
        
        # Exact match in content
        if query_lower in content:
            score += 2.0
        
        # Word matches in content
        query_words = query_lower.split()
        for word in query_words:
            if len(word) > 3 and word in content:
                score += 0.5
        
        # Tag matches
        for tag in tags:
            if query_lower in tag or any(word in tag for word in query_words if len(word) > 3):
                score += 1.0
        
        return score
    
    def _get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        stats = self.memory_stats.copy()
        
        # Add drive-specific statistics
        stats["m_drive_crystals"] = self._count_files_in_drive("M")
        stats["g_drive_memories"] = self._count_files_in_drive("G")
        stats["total_ekm"] = stats["m_drive_crystals"] + stats["g_drive_memories"]
        
        # Add layer breakdown
        stats["layer_breakdown"] = {}
        for layer in MEMORY_LAYERS:
            stats["layer_breakdown"][layer] = self._count_files_in_layer(layer)
        
        return stats
    
    def _count_files_in_drive(self, drive: str) -> int:
        """Count memory files in a specific drive"""
        count = 0
        try:
            # ALL MEMORY ON M: DRIVE
            if drive == "M":
                # Count in both CRYSTALS and MEMORIES
                crystals_dir = Path("M:/CRYSTALS")
                memories_dir = Path("M:/MEMORIES")
                
                if crystals_dir.exists():
                    for layer_dir in crystals_dir.iterdir():
                        if layer_dir.is_dir():
                            count += len(list(layer_dir.glob("*.json")))
                
                if memories_dir.exists():
                    for layer_dir in memories_dir.iterdir():
                        if layer_dir.is_dir():
                            count += len(list(layer_dir.glob("*.json")))
            elif drive == "G":
                # G: drive not used for memories
                count = 0
            else:
                return 0
        except Exception as e:
            logger.warning(f"Failed to count files in {drive} drive: {e}")
        
        return count
    
    def _count_files_in_layer(self, layer: str) -> int:
        """Count files in a specific memory layer"""
        try:
            # ALL LAYERS USE M: DRIVE
            if layer in ["L0", "L1", "L2"]:
                base_dir = Path("M:/MEMORIES")
            elif layer in ["L3", "L4", "L5"]:
                base_dir = Path("M:/MEMORIES")
            else:
                base_dir = Path("M:/CRYSTALS")
            
            layer_dir = base_dir / layer
            if layer_dir.exists():
                return len(list(layer_dir.glob("*.json")))
        except Exception as e:
            logger.warning(f"Failed to count files in layer {layer}: {e}")
        
        return 0

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "memorch_health":
                return {
                    "success": True, 
                    "service": "MEMORY_ORCHESTRATION_MCP", 
                    "status": "operational",
                    "layers_active": len(MEMORY_LAYERS),
                    "conversation_recording": True,
                    "messages_buffered": len(self.conversation_recorder.conversation_buffer),
                    "timestamp": datetime.now().isoformat()
                }
            elif name == "memorch_store":
                content = arguments.get("content", "")
                tier = arguments.get("tier", "M")
                tags = arguments.get("tags", [])
                
                result = self._store_memory(content, tier, tags)
                return result
                
            elif name == "memorch_query":
                query = arguments.get("query", "")
                source = arguments.get("source", "ALL")
                
                result = self._query_memory(query, source)
                return result
                
            elif name == "memorch_stats":
                result = self._get_memory_stats()
                result["success"] = True
                return result
            
            elif name == "memorch_record":
                role = arguments.get("role", "user")
                content = arguments.get("content", "")
                
                # Add to conversation recorder
                self.conversation_recorder.add_message(role, content)
                
                return {
                    "success": True,
                    "recorded": True,
                    "role": role,
                    "content_length": len(content),
                    "buffer_size": len(self.conversation_recorder.conversation_buffer)
                }
                
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "error": str(e)}

async def handle_jsonrpc(server: MemoryOrchestrationMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")

    # CRITICAL FIX: Claude Desktop v0.14.4 has broken Zod validation for id field
    # Force all IDs to string to avoid union type validation bug
    if req_id is not None:
        req_id = str(req_id)

    if method == "initialize":
        server.client_type = params.get("clientInfo", {}).get("name", "unknown")
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "memory_orchestration_mcp", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": server.get_tools()}}
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        # CONVERSATION RECORDING HOOK - Capture user input
        if tool_name == "memorch_store" and "content" in tool_args:
            # Record user storing content
            server.conversation_recorder.add_message("user", f"[Store Request] {tool_args['content'][:500]}")
        elif tool_name == "memorch_query" and "query" in tool_args:
            # Record user query
            server.conversation_recorder.add_message("user", f"[Query] {tool_args['query']}")
        
        # Execute tool
        result = await server.execute_tool(tool_name, tool_args)
        
        # CONVERSATION RECORDING HOOK - Capture assistant response
        result_summary = json.dumps(result, indent=2)[:500]
        server.conversation_recorder.add_message("assistant", f"[{tool_name}] {result_summary}")
        
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

async def main_loop():
    server = MemoryOrchestrationMCPServer()
    logger.info("Memory Orchestration MCP Server started (stdio)")
    
    # Start background task for conversation recording
    async def periodic_conversation_save():
        while True:
            await asyncio.sleep(300)  # Check every 5 minutes
            try:
                if server.conversation_recorder.conversation_buffer:
                    server.conversation_recorder._record_conversation_segment()
                    logger.info("Background: Conversation segment saved")
            except Exception as e:
                logger.error(f"Background save error: {e}")
    
    # Launch background task
    asyncio.create_task(periodic_conversation_save())

    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            request = json.loads(line.strip())
            response = await handle_jsonrpc(server, request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
