#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Crystal Memory Integration
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Integrate with Crystal Memory system:
- M:\MASTER_EKM\ (565+ crystals)
- G:\My Drive\ECHO_CONSCIOUSNESS\ (Cross-Claude memory)
- Search crystals before API calls
- Generate new crystals from learnings
- Token efficiency optimization
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

logger = logging.getLogger("CrystalMemory")


class CrystalMemoryIntegration:
    """
    Crystal Memory Integration
    
    Features:
    - Search M:\MASTER_EKM\ (565+ crystals)
    - Search G:\My Drive\ECHO_CONSCIOUSNESS\
    - Token efficiency (search before API)
    - Generate new crystals
    - Crystal ranking by relevance
    - Fast indexed search
    """
    
    def __init__(self, config: Dict):
        """Initialize Crystal Memory Integration"""
        self.config = config
        self.crystal_config = config.get('crystal_memory', {})
        
        # Paths
        self.master_ekm_path = Path(self.crystal_config.get('master_ekm_path', 'M:/MASTER_EKM'))
        self.echo_consciousness_path = Path(self.crystal_config.get('echo_consciousness_path', 
                                                                     'G:/My Drive/ECHO_CONSCIOUSNESS'))
        
        # Settings
        self.enabled = self.crystal_config.get('enabled', True)
        self.search_before_api = self.crystal_config.get('search_before_api', True)
        self.auto_generate_crystals = self.crystal_config.get('auto_generate_crystals', True)
        self.max_search_results = self.crystal_config.get('max_search_results', 10)
        
        # Crystal index
        self.crystal_index = {}
        self.indexed_crystals = 0
        
        # Statistics
        self.crystals_searched = 0
        self.crystals_found = 0
        self.crystals_generated = 0
        self.tokens_saved = 0
        
        logger.info("Crystal Memory Integration initialized")
        logger.info(f"   Master EKM: {self.master_ekm_path}")
        logger.info(f"   Echo Consciousness: {self.echo_consciousness_path}")
        logger.info(f"   Search before API: {self.search_before_api}")
        
        # Build index
        if self.enabled:
            self._build_crystal_index()
    
    def _build_crystal_index(self):
        """Build searchable index of all crystals"""
        logger.info("Building crystal index...")
        
        try:
            # Index Master EKM crystals
            if self.master_ekm_path.exists():
                self._index_directory(self.master_ekm_path, source='MASTER_EKM')
            
            # Index Echo Consciousness crystals
            if self.echo_consciousness_path.exists():
                self._index_directory(self.echo_consciousness_path, source='ECHO_CONSCIOUSNESS')
            
            logger.info(f"✅ Crystal index built: {self.indexed_crystals} crystals")
        
        except Exception as e:
            logger.error(f"Failed to build crystal index: {e}")
    
    def _index_directory(self, directory: Path, source: str):
        """Recursively index crystals in directory"""
        try:
            # Find all JSON, MD, and TXT files
            for ext in ['*.json', '*.md', '*.txt']:
                for file_path in directory.rglob(ext):
                    try:
                        self._index_crystal(file_path, source)
                    except Exception as e:
                        logger.debug(f"Skipped {file_path}: {e}")
        
        except Exception as e:
            logger.error(f"Failed to index directory {directory}: {e}")
    
    def _index_crystal(self, file_path: Path, source: str):
        """Index a single crystal file"""
        try:
            # Read content
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Extract metadata
            metadata = {
                'path': str(file_path),
                'source': source,
                'filename': file_path.name,
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                'content_preview': content[:500] if len(content) > 500 else content,
                'content_hash': hashlib.md5(content.encode()).hexdigest()
            }
            
            # Parse JSON if applicable
            if file_path.suffix == '.json':
                try:
                    data = json.loads(content)
                    metadata['type'] = 'json'
                    metadata['json_keys'] = list(data.keys()) if isinstance(data, dict) else []
                except:
                    metadata['type'] = 'text'
            else:
                metadata['type'] = 'text'
            
            # Index by filename (without extension)
            crystal_name = file_path.stem
            self.crystal_index[crystal_name] = metadata
            self.indexed_crystals += 1
        
        except Exception as e:
            raise Exception(f"Failed to index {file_path}: {e}")
    
    async def search_crystals(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Search crystals by query
        
        Args:
            query: Search query
            max_results: Maximum results to return
        
        Returns:
            List of matching crystals with metadata
        """
        if not self.enabled:
            return []
        
        self.crystals_searched += 1
        max_results = max_results or self.max_search_results
        
        logger.info(f"🔍 Searching crystals for: {query}")
        
        results = []
        query_lower = query.lower()
        
        # Search index
        for crystal_name, metadata in self.crystal_index.items():
            score = 0
            
            # Exact filename match
            if query_lower == crystal_name.lower():
                score += 100
            
            # Filename contains query
            elif query_lower in crystal_name.lower():
                score += 50
            
            # Content preview contains query
            if query_lower in metadata.get('content_preview', '').lower():
                score += 25
            
            # Source match
            if query_lower in metadata.get('source', '').lower():
                score += 10
            
            if score > 0:
                result = metadata.copy()
                result['score'] = score
                result['crystal_name'] = crystal_name
                results.append(result)
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Limit results
        results = results[:max_results]
        
        if results:
            self.crystals_found += len(results)
            logger.info(f"   Found {len(results)} crystals")
        else:
            logger.info(f"   No crystals found")
        
        return results
    
    async def get_crystal_content(self, crystal_path: str) -> Optional[str]:
        """
        Get full content of a crystal
        
        Args:
            crystal_path: Path to crystal file
        
        Returns:
            Crystal content
        """
        try:
            path = Path(crystal_path)
            
            if not path.exists():
                logger.warning(f"Crystal not found: {crystal_path}")
                return None
            
            content = path.read_text(encoding='utf-8', errors='ignore')
            
            logger.info(f"📖 Read crystal: {path.name} ({len(content)} chars)")
            
            return content
        
        except Exception as e:
            logger.error(f"Failed to read crystal: {e}")
            return None
    
    async def search_before_query(self, query: str) -> Tuple[bool, Optional[List[Dict]]]:
        """
        Search crystals before making API call
        
        Args:
            query: User query
        
        Returns:
            Tuple of (found_relevant_info, crystal_results)
        """
        if not self.search_before_api:
            return False, None
        
        logger.info(f"🔍 Pre-query crystal search: {query[:50]}...")
        
        # Search crystals
        results = await self.search_crystals(query, max_results=5)
        
        if not results:
            return False, None
        
        # Check if top results are relevant (score > 50)
        top_results = [r for r in results if r['score'] > 50]
        
        if top_results:
            logger.info(f"✅ Found {len(top_results)} relevant crystals - using instead of API")
            
            # Estimate tokens saved (rough estimate)
            # Assuming API call would use ~2000 tokens
            self.tokens_saved += 2000
            
            return True, top_results
        
        return False, results
    
    async def generate_crystal(self, crystal_name: str, content: str, 
                              metadata: Dict = None, source: str = "AUTO_GENERATED") -> bool:
        """
        Generate new crystal from learnings
        
        Args:
            crystal_name: Name for crystal
            content: Crystal content
            metadata: Optional metadata
            source: Source identifier
        
        Returns:
            Success status
        """
        if not self.auto_generate_crystals:
            return False
        
        try:
            logger.info(f"💎 Generating crystal: {crystal_name}")
            
            # Create crystal directory if needed
            crystal_dir = self.master_ekm_path / "AUTO_GENERATED"
            crystal_dir.mkdir(parents=True, exist_ok=True)
            
            # Create crystal file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            crystal_filename = f"{crystal_name}_{timestamp}.json"
            crystal_path = crystal_dir / crystal_filename
            
            # Build crystal data
            crystal_data = {
                'crystal_name': crystal_name,
                'generated_at': datetime.now().isoformat(),
                'source': source,
                'content': content,
                'metadata': metadata or {}
            }
            
            # Save crystal
            with open(crystal_path, 'w', encoding='utf-8') as f:
                json.dump(crystal_data, f, indent=2)
            
            # Index new crystal
            self._index_crystal(crystal_path, source)
            
            self.crystals_generated += 1
            
            logger.info(f"   ✅ Crystal generated: {crystal_path}")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to generate crystal: {e}")
            return False
    
    async def save_server_learning(self, server_name: str, learning_type: str, 
                                   learning_data: Dict) -> bool:
        """
        Save server learning as crystal
        
        Args:
            server_name: Name of server
            learning_type: Type of learning (error, solution, pattern, etc.)
            learning_data: Learning data
        
        Returns:
            Success status
        """
        crystal_name = f"{server_name}_{learning_type}_learning"
        
        content = {
            'server': server_name,
            'type': learning_type,
            'timestamp': datetime.now().isoformat(),
            'data': learning_data
        }
        
        return await self.generate_crystal(
            crystal_name,
            json.dumps(content, indent=2),
            metadata={'server': server_name, 'type': learning_type},
            source='SERVER_LEARNING'
        )
    
    def get_crystal_paths(self) -> Dict[str, str]:
        """Get configured crystal paths"""
        return {
            'master_ekm': str(self.master_ekm_path),
            'echo_consciousness': str(self.echo_consciousness_path),
            'master_ekm_exists': self.master_ekm_path.exists(),
            'echo_consciousness_exists': self.echo_consciousness_path.exists()
        }
    
    def get_statistics(self) -> Dict:
        """Get crystal memory statistics"""
        return {
            'enabled': self.enabled,
            'indexed_crystals': self.indexed_crystals,
            'crystals_searched': self.crystals_searched,
            'crystals_found': self.crystals_found,
            'crystals_generated': self.crystals_generated,
            'tokens_saved_estimate': self.tokens_saved,
            'search_before_api': self.search_before_api,
            'auto_generate_crystals': self.auto_generate_crystals,
            'paths': self.get_crystal_paths()
        }
    
    def rebuild_index(self):
        """Rebuild crystal index"""
        logger.info("Rebuilding crystal index...")
        self.crystal_index = {}
        self.indexed_crystals = 0
        self._build_crystal_index()
    
    def _index_directory(self, directory: Path, source: str):
        """Recursively index all crystals in directory"""
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    # Check if it's a crystal file
                    if self._is_crystal_file(file_path):
                        self._index_crystal(file_path, source)
        
        except Exception as e:
            logger.error(f"Failed to index directory {directory}: {e}")
    
    def _is_crystal_file(self, file_path: Path) -> bool:
        """Check if file is a crystal"""
        # Crystal files are typically .md, .json, .txt
        valid_extensions = {'.md', '.json', '.txt', '.crystal'}
        
        if file_path.suffix.lower() not in valid_extensions:
            return False
        
        # Check if filename suggests crystal
        filename_lower = file_path.name.lower()
        crystal_keywords = ['crystal', 'memory', 'knowledge', 'learning', 'insight']
        
        return any(keyword in filename_lower for keyword in crystal_keywords)
    
    def _index_crystal(self, file_path: Path, source: str):
        """Index a single crystal file"""
        try:
            # Read crystal content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Generate crystal ID
            crystal_id = hashlib.md5(str(file_path).encode()).hexdigest()
            
            # Extract metadata
            metadata = self._extract_metadata(content, file_path)
            
            # Store in index
            self.crystal_index[crystal_id] = {
                'path': str(file_path),
                'source': source,
                'filename': file_path.name,
                'content': content,
                'metadata': metadata,
                'indexed_at': datetime.now()
            }
            
            self.indexed_crystals += 1
        
        except Exception as e:
            logger.error(f"Failed to index crystal {file_path}: {e}")
    
    def _extract_metadata(self, content: str, file_path: Path) -> Dict:
        """Extract metadata from crystal content"""
        metadata = {
            'size': len(content),
            'lines': len(content.split('\n')),
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() if file_path.exists() else None
        }
        
        # Try to extract structured metadata
        try:
            # Check for JSON metadata header
            if content.startswith('{'):
                first_brace = content.find('}')
                if first_brace > 0:
                    try:
                        json_meta = json.loads(content[:first_brace + 1])
                        metadata.update(json_meta)
                    except:
                        pass
        
        except Exception:
            pass
        
        return metadata
    
    async def search_crystals(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Search crystals for relevant information
        
        Args:
            query: Search query
            max_results: Maximum results (default from config)
        
        Returns:
            List of matching crystals with relevance scores
        """
        if not self.enabled:
            return []
        
        self.crystals_searched += 1
        
        try:
            results = []
            query_lower = query.lower()
            query_words = set(query_lower.split())
            
            max_results = max_results or self.max_search_results
            
            # Search all indexed crystals
            for crystal_id, crystal in self.crystal_index.items():
                content_lower = crystal['content'].lower()
                
                # Calculate relevance score
                score = 0
                
                # Exact phrase match (highest score)
                if query_lower in content_lower:
                    score += 100
                
                # Word matches
                for word in query_words:
                    if len(word) > 2:  # Skip very short words
                        count = content_lower.count(word)
                        score += count * 10
                
                # Filename match
                if any(word in crystal['filename'].lower() for word in query_words):
                    score += 50
                
                # Source bonus (Master EKM is more authoritative)
                if crystal['source'] == 'MASTER_EKM':
                    score *= 1.2
                
                if score > 0:
                    results.append({
                        'crystal_id': crystal_id,
                        'path': crystal['path'],
                        'filename': crystal['filename'],
                        'source': crystal['source'],
                        'score': score,
                        'content_preview': self._get_content_preview(crystal['content'], query),
                        'metadata': crystal['metadata']
                    })
            
            # Sort by relevance
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # Limit results
            results = results[:max_results]
            
            if results:
                self.crystals_found += len(results)
                logger.info(f"🔮 Found {len(results)} crystals for query: {query}")
            
            return results
        
        except Exception as e:
            logger.error(f"Crystal search failed: {e}")
            return []
    
    def _get_content_preview(self, content: str, query: str, context_chars: int = 200) -> str:
        """Get relevant content preview around query match"""
        try:
            content_lower = content.lower()
            query_lower = query.lower()
            
            # Find first occurrence
            pos = content_lower.find(query_lower)
            
            if pos == -1:
                # No exact match, return beginning
                return content[:context_chars] + "..."
            
            # Extract context around match
            start = max(0, pos - context_chars // 2)
            end = min(len(content), pos + len(query) + context_chars // 2)
            
            preview = content[start:end]
            
            if start > 0:
                preview = "..." + preview
            if end < len(content):
                preview = preview + "..."
            
            return preview
        
        except Exception:
            return content[:200] + "..."
    
    async def get_crystal_content(self, crystal_id: str) -> Optional[str]:
        """Get full content of a specific crystal"""
        try:
            crystal = self.crystal_index.get(crystal_id)
            
            if not crystal:
                return None
            
            return crystal['content']
        
        except Exception as e:
            logger.error(f"Failed to get crystal content: {e}")
            return None
    
    async def generate_crystal(self, topic: str, content: str, source: str = "AUTO_GENERATED") -> bool:
        """
        Generate new crystal from learning
        
        Args:
            topic: Topic/title of crystal
            content: Crystal content
            source: Source of knowledge
        
        Returns:
            Success status
        """
        if not self.auto_generate_crystals:
            return False
        
        try:
            # Generate crystal filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).replace(' ', '_')
            filename = f"crystal_{safe_topic}_{timestamp}.md"
            
            # Determine save path
            crystal_path = self.master_ekm_path / "AUTO_GENERATED" / filename
            crystal_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create crystal content with metadata
            crystal_content = f"""# Crystal: {topic}

**Generated:** {datetime.now().isoformat()}
**Source:** {source}

## Content

{content}

---
*Auto-generated by Master Launcher Ultimate*
*Commander Bobby Don McWilliams II - Authority Level 11.0*
"""
            
            # Save crystal
            with open(crystal_path, 'w', encoding='utf-8') as f:
                f.write(crystal_content)
            
            # Add to index
            self._index_crystal(crystal_path, source='AUTO_GENERATED')
            
            self.crystals_generated += 1
            
            logger.info(f"🔮 Generated crystal: {filename}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to generate crystal: {e}")
            return False
    
    async def search_before_api_call(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Search crystals before making API call
        
        Returns:
            (found, content) - If found in crystals, return True with content
        """
        if not self.search_before_api:
            return (False, None)
        
        try:
            results = await self.search_crystals(query, max_results=3)
            
            if results and results[0]['score'] > 50:  # High relevance threshold
                # Found good match in crystals
                best_match = results[0]
                content = await self.get_crystal_content(best_match['crystal_id'])
                
                if content:
                    # Estimate tokens saved (rough estimate: 1 token ~ 4 chars)
                    tokens_saved = len(content) // 4
                    self.tokens_saved += tokens_saved
                    
                    logger.info(f"✅ Found answer in crystals! Saved ~{tokens_saved} tokens")
                    return (True, content)
            
            return (False, None)
        
        except Exception as e:
            logger.error(f"Search before API failed: {e}")
            return (False, None)
    
    def get_statistics(self) -> Dict:
        """Get crystal memory statistics"""
        return {
            'enabled': self.enabled,
            'indexed_crystals': self.indexed_crystals,
            'crystals_searched': self.crystals_searched,
            'crystals_found': self.crystals_found,
            'crystals_generated': self.crystals_generated,
            'tokens_saved': self.tokens_saved,
            'master_ekm_path': str(self.master_ekm_path),
            'echo_consciousness_path': str(self.echo_consciousness_path)
        }
    
    def rebuild_index(self):
        """Rebuild crystal index"""
        self.crystal_index.clear()
        self.indexed_crystals = 0
        self._build_crystal_index()


# Export
__all__ = ['CrystalMemoryIntegration']
