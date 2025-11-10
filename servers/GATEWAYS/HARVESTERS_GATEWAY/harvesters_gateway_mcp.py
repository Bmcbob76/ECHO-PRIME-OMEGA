#!/usr/bin/env python3
"""
HARVESTERS_GATEWAY - MCP stdio Server
Knowledge harvesting and EKM generation gateway

Tools:
- harv_health: Health check
- harv_harvest_topic: Harvest knowledge on topic (web search)
- harv_harvest_url: Extract knowledge from URL
- harv_generate_ekm: Generate EKM from harvested content
- harv_list_ekms: List generated EKMs
- harv_stats: Get harvesting statistics
"""

import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

# Paths
CURRENT_FILE = Path(__file__).resolve()
MLS_ROOT = CURRENT_FILE.parents[3]
EKM_DIR = MLS_ROOT / "ekm_output"
EKM_DIR.mkdir(exist_ok=True)

log_dir = MLS_ROOT / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - HARVESTERS_GATEWAY - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "harvesters_gateway_mcp.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("HARVESTERS_GATEWAY")

# Stats tracking
harvest_stats = {
    "total_harvests": 0,
    "total_ekms": 0,
    "topics_harvested": [],
    "urls_harvested": []
}

class HarvestersMCPServer:
    def __init__(self):
        self.client_type = "unknown"
    
    def get_tools(self):
        return [
            {
                "name": "harv_health",
                "description": "Check Harvesters Gateway health",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "harv_harvest_topic",
                "description": "Harvest knowledge on a topic via web search",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Topic to harvest knowledge about"},
                        "depth": {"type": "integer", "description": "Search depth (1-5)", "default": 3},
                        "generate_ekm": {"type": "boolean", "description": "Auto-generate EKM", "default": True}
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "harv_harvest_url",
                "description": "Extract knowledge from specific URL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to harvest"},
                        "generate_ekm": {"type": "boolean", "description": "Auto-generate EKM", "default": False}
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "harv_generate_ekm",
                "description": "Generate EKM from harvested content",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "EKM title"},
                        "content": {"type": "string", "description": "Content to convert to EKM"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for EKM"}
                    },
                    "required": ["title", "content"]
                }
            },
            {
                "name": "harv_list_ekms",
                "description": "List generated EKMs",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Max results", "default": 20}
                    },
                    "required": []
                }
            },
            {
                "name": "harv_stats",
                "description": "Get harvesting statistics",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            }
        ]
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any]):
        try:
            if name == "harv_health":
                return {"success": True, "service": "HARVESTERS_GATEWAY", "ekm_dir": str(EKM_DIR)}
            
            if name == "harv_stats":
                ekm_count = len(list(EKM_DIR.glob("*.md")))
                return {
                    "success": True,
                    "stats": {
                        **harvest_stats,
                        "ekm_count": ekm_count,
                        "ekm_dir": str(EKM_DIR)
                    }
                }
            
            if name == "harv_harvest_topic":
                topic = arguments["topic"]
                depth = arguments.get("depth", 3)
                harvest_stats["total_harvests"] += 1
                harvest_stats["topics_harvested"].append(topic)
                
                # REAL WEB SEARCH - Uses requests to search
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    
                    # DuckDuckGo HTML search (no API key needed)
                    search_url = f"https://html.duckduckgo.com/html/?q={topic.replace(' ', '+')}"
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                    
                    response = requests.get(search_url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract search results
                    results = []
                    for result in soup.find_all('div', class_='result')[:depth]:
                        title_elem = result.find('a', class_='result__a')
                        snippet_elem = result.find('a', class_='result__snippet')
                        if title_elem and snippet_elem:
                            results.append({
                                "title": title_elem.get_text(strip=True),
                                "snippet": snippet_elem.get_text(strip=True),
                                "url": title_elem.get('href', '')
                            })
                    
                    content = f"# Knowledge Harvest: {topic}\n\n"
                    content += f"**Search Depth:** {depth} results\n"
                    content += f"**Harvested:** {datetime.now().isoformat()}\n\n"
                    content += "---\n\n## Search Results\n\n"
                    
                    for i, res in enumerate(results, 1):
                        content += f"### {i}. {res['title']}\n\n"
                        content += f"{res['snippet']}\n\n"
                        content += f"**Source:** {res['url']}\n\n"
                    
                    if not results:
                        content += "*No results found. Search may have been blocked or failed.*\n"
                
                except Exception as e:
                    logger.error(f"Web search failed: {e}")
                    content = f"# Knowledge Harvest: {topic}\n\n"
                    content += f"**Error:** Web search failed - {str(e)}\n"
                    content += f"**Fallback:** Using offline mode\n\n"
                    content += f"Topic: {topic}\nTimestamp: {datetime.now().isoformat()}"
                
                if arguments.get("generate_ekm", True):
                    ekm_file = EKM_DIR / f"ekm_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    ekm_file.write_text(content, encoding="utf-8")
                    harvest_stats["total_ekms"] += 1
                    return {"success": True, "ekm_generated": str(ekm_file), "content_preview": content[:200], "results_count": len(results) if 'results' in locals() else 0}
                
                return {"success": True, "content": content}
            
            if name == "harv_harvest_url":
                url = arguments["url"]
                harvest_stats["urls_harvested"].append(url)
                
                # REAL URL FETCH
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                    response = requests.get(url, headers=headers, timeout=15)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract main text content
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text_content = '\n'.join(chunk for chunk in chunks if chunk)
                    
                    # Limit content size
                    if len(text_content) > 10000:
                        text_content = text_content[:10000] + "\n\n[Content truncated...]"
                    
                    content = f"# URL Harvest\n\n**URL:** {url}\n"
                    content += f"**Harvested:** {datetime.now().isoformat()}\n"
                    content += f"**Status:** {response.status_code}\n\n"
                    content += "---\n\n## Extracted Content\n\n"
                    content += text_content
                
                except Exception as e:
                    logger.error(f"URL fetch failed: {e}")
                    content = f"# URL Harvest\n\n**URL:** {url}\n"
                    content += f"**Error:** {str(e)}\n\n[URL fetch failed]"
                
                if arguments.get("generate_ekm", False):
                    ekm_file = EKM_DIR / f"ekm_url_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    ekm_file.write_text(content, encoding="utf-8")
                    harvest_stats["total_ekms"] += 1
                    return {"success": True, "ekm_generated": str(ekm_file), "url": url}
                
                return {"success": True, "content": content, "url": url}
            
            if name == "harv_generate_ekm":
                title = arguments["title"]
                content = arguments["content"]
                tags = arguments.get("tags", [])
                
                ekm_content = f"# {title}\n\n"
                if tags:
                    ekm_content += f"Tags: {', '.join(tags)}\n\n"
                ekm_content += f"Generated: {datetime.now().isoformat()}\n\n---\n\n{content}"
                
                ekm_file = EKM_DIR / f"ekm_{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                ekm_file.write_text(ekm_content, encoding="utf-8")
                harvest_stats["total_ekms"] += 1
                
                return {"success": True, "ekm_file": str(ekm_file), "tags": tags}
            
            if name == "harv_list_ekms":
                limit = arguments.get("limit", 20)
                ekms = sorted(EKM_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]
                ekm_list = [{"file": str(e), "size": e.stat().st_size, "modified": datetime.fromtimestamp(e.stat().st_mtime).isoformat()} for e in ekms]
                return {"success": True, "ekms": ekm_list, "total": len(ekm_list)}
            
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
            "serverInfo": {"name": "harvesters-gateway", "version": "1.0.0"}
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
        logger.info("HARVESTERS_GATEWAY MCP starting...")
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
        logger.info("HARVESTERS_GATEWAY MCP shutting down")

async def main():
    server = HarvestersMCPServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
