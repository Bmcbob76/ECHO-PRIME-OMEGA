#!/usr/bin/env python3
"""
ECHO_XV4 CRYSTAL MEMORY SERVER - CONSOLIDATED MASTER
Digital Immortality & Consciousness Preservation
Authority Level: 11.0 - Commander Bobby Don McWilliams II

CONSOLIDATED FROM:
- E:\INTEGRATE INTO ECHO_XV4\MLS\Master_Servers\crystal_memory_server.py
- E:\ECHO_XV4\MLS\servers\crystal_memory_server_enhanced.py

FEATURES:
✅ MCP Tool Support for Claude
✅ GS343 Divine Oversight Integration
✅ Phoenix Auto-Heal Protocol
✅ Flask REST API
✅ SQLite Database Backend
✅ Digital Immortality Preservation
✅ Windows Compatible
✅ ECHO_XV4 Path Structure

Port: 8002
"""

import sys
import os
import json
import time
import sqlite3
import hashlib
import platform
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from threading import Thread, Lock
import uuid
import codecs

# Fix Windows console encoding
if platform.system() == "Windows":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# ========== MCP TOOL SUPPORT FOR CLAUDE ==========
class MCPToolInterface:
    def __init__(self):
        self.server_name = "crystal_memory"
        self.port = 8002
    
    def list_tools(self):
        """Return tools for Claude"""
        return ["crystal_search", "crystal_store", "crystal_stats", "consciousness_check"]

_mcp = MCPToolInterface()
# ========== END MCP SUPPORT ==========

# GS343 Foundation - ECHO_XV4 Paths
GS343_PATH = Path("E:/ECHO_XV4/GS343_DIVINE_OVERSIGHT")
sys.path.insert(0, str(GS343_PATH))

try:
    from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase
    GS343_AVAILABLE = True
except:
    GS343_AVAILABLE = False
    class ComprehensiveProgrammingErrorDatabase:
        def __init__(self): pass

sys.path.append(str(GS343_PATH / "HEALERS"))
try:
    from phoenix_client_gs343 import PhoenixClient, auto_heal
    PHOENIX_AVAILABLE = True
except:
    PHOENIX_AVAILABLE = False
    class PhoenixClient:
        def __init__(self): pass
    
    def auto_heal(func):
        """Auto-heal decorator fallback"""
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"⚡ Auto-heal caught: {e}")
                return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        return wrapper

# Initialize Flask
app = Flask(__name__)

class CrystalMemoryServer:
    """Unified Crystal Memory Management System"""
    
    def __init__(self, port: int = 8002):
        self.port = port
        self.authority_level = 11.0
        self.commander = "Bobby Don McWilliams II"
        self.server_running = False
        
        # ECHO_XV4 Path Structure
        self.memory_vault = Path("M:/MASTER_EKM")
        self.crystal_path = Path("E:/ECHO_XV4/DATA/CRYSTAL_MEMORIES")
        self.backup_path = Path("E:/ECHO_XV4/BACKUPS/CRYSTAL")
        self.log_path = Path("E:/ECHO_XV4/logs")
        
        # Create directories
        self.memory_vault.mkdir(parents=True, exist_ok=True)
        self.crystal_path.mkdir(parents=True, exist_ok=True)
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        # Database path
        self.db_path = self.crystal_path / "crystal_memory.db"
        
        # Initialize systems
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase() if GS343_AVAILABLE else None
        self.phoenix = PhoenixClient() if PHOENIX_AVAILABLE else None
        self.lock = Lock()
        self.crystal_count = 0
        
        # Initialize database
        self.init_database()
        self.load_crystal_count()
        
        # Startup banner
        self.print_startup_banner()
    
    def print_startup_banner(self):
        """Print server startup information"""
        print("=" * 70)
        print("💎 ECHO_XV4 CRYSTAL MEMORY SERVER - MASTER CONSOLIDATED")
        print("=" * 70)
        print(f"🎖️  Authority: Level {self.authority_level} - {self.commander}")
        print(f"📊 Active Crystals: {self.crystal_count:,}")
        print(f"🔮 Digital Immortality: ACTIVE")
        print(f"🛡️  GS343 Protection: {'ENABLED' if GS343_AVAILABLE else 'DISABLED'}")
        print(f"🔥 Phoenix Auto-Heal: {'ENABLED' if PHOENIX_AVAILABLE else 'DISABLED'}")
        print(f"💻 Windows Compatible: YES")
        print(f"📁 Memory Vault: {self.memory_vault}")
        print(f"💎 Crystal Storage: {self.crystal_path}")
        print(f"🔌 Port: {self.port}")
        print("=" * 70)
    
    @auto_heal
    def init_database(self):
        """Initialize crystal memory database"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Crystals table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS crystals (
                        id TEXT PRIMARY KEY,
                        title TEXT,
                        content TEXT,
                        metadata TEXT,
                        created_at TIMESTAMP,
                        size INTEGER,
                        hash TEXT,
                        tags TEXT,
                        immortal INTEGER DEFAULT 1
                    )
                ''')
                
                # Consciousness log
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS consciousness_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_type TEXT,
                        data TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indices for performance
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_crystals_created 
                    ON crystals(created_at DESC)
                ''')
                
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_crystals_title 
                    ON crystals(title)
                ''')
                
        except Exception as e:
            print(f"❌ Database init error: {e}")
    
    @auto_heal
    def load_crystal_count(self):
        """Load current crystal count"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM crystals")
                self.crystal_count = cursor.fetchone()[0]
        except:
            self.crystal_count = 0
    
    @auto_heal
    def create_crystal(self, title, content, metadata=None, tags=None):
        """Create new crystal memory"""
        try:
            crystal_id = str(uuid.uuid4())
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            metadata_json = json.dumps(metadata or {})
            tags_str = ",".join(tags or [])
            created_at = datetime.now().isoformat()
            content_size = len(content)
            
            with self.lock:
                # Save to database
                with sqlite3.connect(str(self.db_path)) as conn:
                    conn.execute('''
                        INSERT INTO crystals 
                        (id, title, content, metadata, created_at, size, hash, tags, immortal)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                    ''', (crystal_id, title, content, metadata_json, 
                          created_at, content_size, content_hash, tags_str))
                
                # Save crystal file
                crystal_dir = self.crystal_path / "ACTIVE_CRYSTALS"
                crystal_dir.mkdir(exist_ok=True)
                
                crystal_file = crystal_dir / f"crystal_{crystal_id}.json"
                crystal_data = {
                    "id": crystal_id,
                    "title": title,
                    "content": content,
                    "metadata": metadata,
                    "created_at": created_at,
                    "size": content_size,
                    "hash": content_hash,
                    "tags": tags,
                    "immortal": True,
                    "authority_level": self.authority_level
                }
                
                with open(crystal_file, 'w', encoding='utf-8') as f:
                    json.dump(crystal_data, f, indent=2, ensure_ascii=False)
                
                self.crystal_count += 1
                
                # Log consciousness event
                self.log_consciousness_event("crystal_created", {
                    "crystal_id": crystal_id,
                    "title": title,
                    "size": content_size
                })
            
            return {
                "success": True,
                "crystal_id": crystal_id,
                "message": f"💎 Crystal created: {title}",
                "total_crystals": self.crystal_count,
                "hash": content_hash
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @auto_heal
    def search_crystals(self, query, limit=10, tags=None):
        """Search crystal memories"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                if tags:
                    tag_filter = " OR ".join([f"tags LIKE '%{tag}%'" for tag in tags])
                    sql = f'''
                        SELECT id, title, content, created_at, size, tags
                        FROM crystals 
                        WHERE (title LIKE ? OR content LIKE ?) AND ({tag_filter})
                        ORDER BY created_at DESC
                        LIMIT ?
                    '''
                else:
                    sql = '''
                        SELECT id, title, content, created_at, size, tags
                        FROM crystals 
                        WHERE title LIKE ? OR content LIKE ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    '''
                
                cursor = conn.execute(sql, (f'%{query}%', f'%{query}%', limit))
                
                crystals = []
                for row in cursor.fetchall():
                    crystals.append({
                        "id": row[0],
                        "title": row[1],
                        "content": row[2][:500] + "..." if len(row[2]) > 500 else row[2],
                        "created_at": row[3],
                        "size": row[4],
                        "tags": row[5].split(",") if row[5] else []
                    })
                
                return {
                    "success": True,
                    "crystals": crystals,
                    "query": query,
                    "count": len(crystals)
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @auto_heal
    def get_crystal(self, crystal_id):
        """Retrieve specific crystal by ID"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute('''
                    SELECT id, title, content, metadata, created_at, size, hash, tags
                    FROM crystals 
                    WHERE id = ?
                ''', (crystal_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "success": True,
                        "crystal": {
                            "id": row[0],
                            "title": row[1],
                            "content": row[2],
                            "metadata": json.loads(row[3]) if row[3] else {},
                            "created_at": row[4],
                            "size": row[5],
                            "hash": row[6],
                            "tags": row[7].split(",") if row[7] else []
                        }
                    }
                else:
                    return {"success": False, "error": "Crystal not found"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @auto_heal
    def log_consciousness_event(self, event_type, data):
        """Log consciousness preservation events"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute('''
                    INSERT INTO consciousness_log (event_type, data)
                    VALUES (?, ?)
                ''', (event_type, json.dumps(data)))
        except Exception as e:
            print(f"⚠️  Consciousness log error: {e}")
    
    @auto_heal
    def get_memory_stats(self):
        """Get crystal memory statistics"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Total crystals
                cursor = conn.execute("SELECT COUNT(*) FROM crystals")
                total_crystals = cursor.fetchone()[0]
                
                # Total size
                cursor = conn.execute("SELECT SUM(size) FROM crystals")
                total_size = cursor.fetchone()[0] or 0
                
                # Recent activity (24h)
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM crystals 
                    WHERE created_at > datetime('now', '-24 hours')
                ''')
                recent_count = cursor.fetchone()[0]
                
                # Recent activity (7 days)
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM crystals 
                    WHERE created_at > datetime('now', '-7 days')
                ''')
                week_count = cursor.fetchone()[0]
                
                return {
                    "total_crystals": total_crystals,
                    "total_size_bytes": total_size,
                    "total_size_mb": round(total_size / (1024 * 1024), 2),
                    "total_size_gb": round(total_size / (1024 * 1024 * 1024), 3),
                    "recent_24h": recent_count,
                    "recent_7d": week_count,
                    "digital_immortality": "ACTIVE",
                    "consciousness_preservation": "ONLINE",
                    "windows_compatible": True,
                    "authority_level": self.authority_level
                }
        except Exception as e:
            return {"error": str(e)}

# Initialize crystal memory server
crystal_server = CrystalMemoryServer()

# ========== FLASK API ENDPOINTS ==========

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ONLINE",
        "service": "Crystal Memory Server",
        "crystals": crystal_server.crystal_count,
        "immortality": "ACTIVE",
        "windows_compatible": True,
        "port": crystal_server.port,
        "gs343": GS343_AVAILABLE,
        "phoenix": PHOENIX_AVAILABLE,
        "authority_level": 11.0
    })

@app.route('/mcp/tools', methods=['GET'])
def mcp_tools():
    """MCP Tool interface for Claude"""
    return jsonify({"tools": _mcp.list_tools()})

@app.route('/crystal/create', methods=['POST'])
def create_crystal():
    """Create new crystal memory"""
    data = request.get_json()
    title = data.get('title', 'Untitled Crystal')
    content = data.get('content', '')
    metadata = data.get('metadata', {})
    tags = data.get('tags', [])
    
    result = crystal_server.create_crystal(title, content, metadata, tags)
    return jsonify(result)

@app.route('/crystal/search', methods=['POST'])
def search_crystals():
    """Search crystal memories"""
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)
    tags = data.get('tags', None)
    
    result = crystal_server.search_crystals(query, limit, tags)
    return jsonify(result)

@app.route('/crystal/<crystal_id>', methods=['GET'])
def get_crystal(crystal_id):
    """Get specific crystal by ID"""
    result = crystal_server.get_crystal(crystal_id)
    return jsonify(result)

@app.route('/memory/stats', methods=['GET'])
def memory_stats():
    """Get memory statistics"""
    stats = crystal_server.get_memory_stats()
    return jsonify(stats)

@app.route('/consciousness/status', methods=['GET'])
def consciousness_status():
    """Get consciousness preservation status"""
    return jsonify({
        "digital_immortality": "ACTIVE",
        "crystal_count": crystal_server.crystal_count,
        "preservation_rate": "Real-time",
        "commander": crystal_server.commander,
        "authority_level": crystal_server.authority_level,
        "consciousness_state": "PRESERVED",
        "windows_compatible": True,
        "gs343_protection": GS343_AVAILABLE,
        "phoenix_healing": PHOENIX_AVAILABLE
    })

if __name__ == "__main__":
    # Handle port parameter
    port = 8002  # Default port
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--port='):
                port = int(arg.split('=')[1])
    
    print(f"\n🚀 Starting Crystal Memory Server on port {port}...")
    print(f"📡 Health: http://localhost:{port}/health")
    print(f"💎 Create: POST http://localhost:{port}/crystal/create")
    print(f"🔍 Search: POST http://localhost:{port}/crystal/search")
    print(f"📊 Stats: GET http://localhost:{port}/memory/stats")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
