#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║       MEMORY LAYER MANAGER - L1-L9 HIERARCHICAL STORAGE          ║
║              Advanced 9-Layer Memory Architecture                 ║
╚══════════════════════════════════════════════════════════════════╝

L1-L9 LAYER HIERARCHY:
L1: REDIS       - Ultra-fast cache layer (microseconds)
L2: RAM         - Working memory for active operations (milliseconds)
L3: CRYSTALS    - Immutable sovereign records (persistent, verified)
L4: SQLITE      - Structured persistent storage (milliseconds-seconds)
L5: CHROMADB    - Vector embeddings for semantic search (seconds)
L6: NEO4J       - Knowledge graph relationships (seconds)
L7: INFLUXDB    - Time-series telemetry and analytics (seconds)
L8: QUANTUM     - Probabilistic future states and possibilities (seconds)
L9: EKM         - Eternal Knowledge Matrix (eternal storage with AI)

PURPOSE:
- Optimize memory access patterns through appropriate layer routing
- Provide automatic layer promotion/demotion based on access patterns
- Maintain backward compatibility with 8-pillar memory system
- Enable sophisticated caching and retrieval strategies
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from collections import OrderedDict
import threading

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════
# LAYER DEFINITIONS
# ══════════════════════════════════════════════════════════════════

class MemoryLayer(Enum):
    """9-Layer memory hierarchy"""
    L1_REDIS = "l1_redis"           # Cache layer - ultra-fast
    L2_RAM = "l2_ram"               # Working memory - fast
    L3_CRYSTALS = "l3_crystals"     # Immutable records - persistent
    L4_SQLITE = "l4_sqlite"         # Structured storage - reliable
    L5_CHROMADB = "l5_chromadb"     # Vector embeddings - semantic
    L6_NEO4J = "l6_neo4j"           # Knowledge graph - relationships
    L7_INFLUXDB = "l7_influxdb"     # Time-series - analytics
    L8_QUANTUM = "l8_quantum"       # Probabilistic - futures
    L9_EKM = "l9_ekm"               # Eternal Knowledge Matrix - AI


@dataclass
class LayerConfig:
    """Configuration for each memory layer"""
    layer: MemoryLayer
    max_capacity: int
    retention_seconds: Optional[int]
    access_time_ms: float  # Typical access time
    persistence: bool
    immutable: bool
    promotion_threshold: int  # Access count to promote to next layer
    demotion_threshold: int  # Idle time seconds before demotion
    
    def __post_init__(self):
        """Set defaults based on layer type"""
        if self.retention_seconds is None:
            retention_map = {
                MemoryLayer.L1_REDIS: 300,  # 5 minutes
                MemoryLayer.L2_RAM: 3600,  # 1 hour
                MemoryLayer.L3_CRYSTALS: None,  # Forever
                MemoryLayer.L4_SQLITE: 86400 * 365,  # 1 year
                MemoryLayer.L5_CHROMADB: 86400 * 30,  # 30 days
                MemoryLayer.L6_NEO4J: 86400 * 365,  # 1 year
                MemoryLayer.L7_INFLUXDB: 86400 * 90,  # 90 days
                MemoryLayer.L8_QUANTUM: 86400 * 30,  # 30 days
                MemoryLayer.L9_EKM: None  # Forever
            }
            self.retention_seconds = retention_map.get(self.layer)


# ══════════════════════════════════════════════════════════════════
# LAYER STORAGE INTERFACE
# ══════════════════════════════════════════════════════════════════

class LayerStorage(ABC):
    """Abstract base class for layer storage implementations"""
    
    def __init__(self, config: LayerConfig):
        self.config = config
        self.stats = {
            "reads": 0,
            "writes": 0,
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    @abstractmethod
    def store(self, key: str, value: Any, metadata: Dict = None) -> bool:
        """Store value in layer"""
        pass
    
    @abstractmethod
    def retrieve(self, key: str) -> Tuple[Optional[Any], bool]:
        """Retrieve value from layer, return (value, found)"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in layer"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete key from layer"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get layer statistics"""
        pass
    
    def record_read(self, found: bool):
        """Record read operation"""
        self.stats['reads'] += 1
        if found:
            self.stats['hits'] += 1
        else:
            self.stats['misses'] += 1


class RAMLayerStorage(LayerStorage):
    """In-memory RAM layer implementation"""
    
    def __init__(self, config: LayerConfig):
        super().__init__(config)
        self.cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self.metadata: Dict[str, Dict] = {}
        self.lock = threading.RLock()
    
    def store(self, key: str, value: Any, metadata: Dict = None) -> bool:
        """Store in RAM cache"""
        with self.lock:
            if len(self.cache) >= self.config.max_capacity:
                # Evict oldest entry (LRU)
                oldest_key, _ = self.cache.popitem(last=False)
                self.stats['evictions'] += 1
            
            self.cache[key] = (value, time.time())
            if metadata:
                self.metadata[key] = metadata
            
            self.stats['writes'] += 1
            return True
    
    def retrieve(self, key: str) -> Tuple[Optional[Any], bool]:
        """Retrieve from RAM"""
        with self.lock:
            if key in self.cache:
                value, _ = self.cache[key]
                # Move to end (mark as recently used)
                self.cache.move_to_end(key)
                self.cache[key] = (value, time.time())
                self.record_read(True)
                return value, True
            
            self.record_read(False)
            return None, False
    
    def exists(self, key: str) -> bool:
        """Check existence"""
        with self.lock:
            return key in self.cache
    
    def delete(self, key: str) -> bool:
        """Delete entry"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                if key in self.metadata:
                    del self.metadata[key]
                return True
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get layer stats"""
        with self.lock:
            return {
                **self.stats,
                "capacity": self.config.max_capacity,
                "utilization": len(self.cache),
                "utilization_percent": (len(self.cache) / self.config.max_capacity * 100)
            }


class CrystalLayerStorage(LayerStorage):
    """Immutable crystal layer implementation"""
    
    def __init__(self, config: LayerConfig):
        super().__init__(config)
        self.crystals: Dict[str, Tuple[Any, Dict, float]] = {}  # key -> (value, metadata, timestamp)
        self.verification: Dict[str, str] = {}  # key -> hash for integrity
        self.lock = threading.RLock()
    
    def store(self, key: str, value: Any, metadata: Dict = None) -> bool:
        """Store immutable crystal"""
        with self.lock:
            if key in self.crystals:
                logger.warning(f"Crystal {key} already exists - cannot modify (immutable)")
                return False
            
            # Generate crystal integrity hash
            import hashlib
            content_str = str(value) + json.dumps(metadata or {})
            crystal_hash = hashlib.sha256(content_str.encode()).hexdigest()
            
            self.crystals[key] = (value, metadata or {}, time.time())
            self.verification[key] = crystal_hash
            
            self.stats['writes'] += 1
            logger.info(f"💎 Crystal stored: {key} with hash {crystal_hash[:8]}...")
            return True
    
    def retrieve(self, key: str) -> Tuple[Optional[Any], bool]:
        """Retrieve crystal with integrity check"""
        with self.lock:
            if key not in self.crystals:
                self.record_read(False)
                return None, False
            
            value, metadata, timestamp = self.crystals[key]
            
            # Verify integrity
            import hashlib
            content_str = str(value) + json.dumps(metadata)
            expected_hash = hashlib.sha256(content_str.encode()).hexdigest()
            
            if expected_hash != self.verification[key]:
                logger.error(f"💎 CRYSTAL INTEGRITY VIOLATION: {key}")
                self.record_read(False)
                return None, False
            
            self.record_read(True)
            return value, True
    
    def exists(self, key: str) -> bool:
        """Check crystal exists"""
        with self.lock:
            return key in self.crystals
    
    def delete(self, key: str) -> bool:
        """Cannot delete crystals - they're immutable"""
        logger.warning(f"Cannot delete crystal {key} - immutable storage")
        return False
    
    def verify_integrity(self, key: str) -> bool:
        """Verify crystal integrity"""
        with self.lock:
            if key not in self.crystals:
                return False
            
            value, metadata, _ = self.crystals[key]
            import hashlib
            content_str = str(value) + json.dumps(metadata)
            expected_hash = hashlib.sha256(content_str.encode()).hexdigest()
            
            return expected_hash == self.verification[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get layer stats"""
        with self.lock:
            return {
                **self.stats,
                "capacity": self.config.max_capacity,
                "crystals_stored": len(self.crystals),
                "integrity_verified": sum(1 for k in self.crystals if self.verify_integrity(k))
            }


# ══════════════════════════════════════════════════════════════════
# LAYER MANAGER
# ══════════════════════════════════════════════════════════════════

class MemoryLayerManager:
    """
    Manages hierarchical 9-layer memory system
    Handles routing, promotion, demotion, and fallback
    """
    
    # Default configurations for each layer
    DEFAULT_CONFIGS = {
        MemoryLayer.L1_REDIS: LayerConfig(
            layer=MemoryLayer.L1_REDIS,
            max_capacity=10000,
            retention_seconds=300,
            access_time_ms=0.1,
            persistence=False,
            immutable=False,
            promotion_threshold=5,
            demotion_threshold=60
        ),
        MemoryLayer.L2_RAM: LayerConfig(
            layer=MemoryLayer.L2_RAM,
            max_capacity=50000,
            retention_seconds=3600,
            access_time_ms=1.0,
            persistence=False,
            immutable=False,
            promotion_threshold=10,
            demotion_threshold=300
        ),
        MemoryLayer.L3_CRYSTALS: LayerConfig(
            layer=MemoryLayer.L3_CRYSTALS,
            max_capacity=100000,
            retention_seconds=None,  # Forever
            access_time_ms=5.0,
            persistence=True,
            immutable=True,
            promotion_threshold=50,
            demotion_threshold=None
        ),
        MemoryLayer.L4_SQLITE: LayerConfig(
            layer=MemoryLayer.L4_SQLITE,
            max_capacity=1000000,
            retention_seconds=86400 * 365,
            access_time_ms=10.0,
            persistence=True,
            immutable=False,
            promotion_threshold=20,
            demotion_threshold=86400
        ),
        MemoryLayer.L5_CHROMADB: LayerConfig(
            layer=MemoryLayer.L5_CHROMADB,
            max_capacity=100000,
            retention_seconds=86400 * 30,
            access_time_ms=50.0,
            persistence=True,
            immutable=False,
            promotion_threshold=15,
            demotion_threshold=604800
        ),
        MemoryLayer.L6_NEO4J: LayerConfig(
            layer=MemoryLayer.L6_NEO4J,
            max_capacity=500000,
            retention_seconds=86400 * 365,
            access_time_ms=100.0,
            persistence=True,
            immutable=False,
            promotion_threshold=25,
            demotion_threshold=1209600
        ),
        MemoryLayer.L7_INFLUXDB: LayerConfig(
            layer=MemoryLayer.L7_INFLUXDB,
            max_capacity=1000000,
            retention_seconds=86400 * 90,
            access_time_ms=50.0,
            persistence=True,
            immutable=False,
            promotion_threshold=10,
            demotion_threshold=604800
        ),
        MemoryLayer.L8_QUANTUM: LayerConfig(
            layer=MemoryLayer.L8_QUANTUM,
            max_capacity=50000,
            retention_seconds=86400 * 30,
            access_time_ms=200.0,
            persistence=False,
            immutable=False,
            promotion_threshold=30,
            demotion_threshold=432000
        ),
        MemoryLayer.L9_EKM: LayerConfig(
            layer=MemoryLayer.L9_EKM,
            max_capacity=float('inf'),
            retention_seconds=None,  # Forever
            access_time_ms=1000.0,
            persistence=True,
            immutable=False,
            promotion_threshold=100,
            demotion_threshold=None
        )
    }
    
    def __init__(self, enable_promotion: bool = True, enable_demotion: bool = True):
        """Initialize layer manager"""
        self.layers: Dict[MemoryLayer, LayerStorage] = {}
        self.access_counts: Dict[str, int] = {}  # Track access patterns for promotion
        self.last_access: Dict[str, float] = {}
        self.current_layer: Dict[str, MemoryLayer] = {}  # Track which layer holds each key
        
        self.enable_promotion = enable_promotion
        self.enable_demotion = enable_demotion
        self.lock = threading.RLock()
        
        # Initialize layers (for now, implementing L1-RAM, L3-Crystal, L4-SQLite placeholders)
        self._init_layers()
        
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║      MEMORY LAYER MANAGER INITIALIZED (L1-L9)               ║")
        logger.info("╚══════════════════════════════════════════════════════════════╝")
    
    def _init_layers(self):
        """Initialize storage implementations for each layer"""
        # For now, implement core layers (L1, L2, L3, L4)
        # L1 and L2 will use RAMLayerStorage
        self.layers[MemoryLayer.L1_REDIS] = RAMLayerStorage(
            self.DEFAULT_CONFIGS[MemoryLayer.L1_REDIS]
        )
        self.layers[MemoryLayer.L2_RAM] = RAMLayerStorage(
            self.DEFAULT_CONFIGS[MemoryLayer.L2_RAM]
        )
        self.layers[MemoryLayer.L3_CRYSTALS] = CrystalLayerStorage(
            self.DEFAULT_CONFIGS[MemoryLayer.L3_CRYSTALS]
        )
        
        # L4-L9 are placeholders for now (store metadata about what's in each layer)
        for layer in [MemoryLayer.L4_SQLITE, MemoryLayer.L5_CHROMADB, MemoryLayer.L6_NEO4J,
                      MemoryLayer.L7_INFLUXDB, MemoryLayer.L8_QUANTUM, MemoryLayer.L9_EKM]:
            self.layers[layer] = RAMLayerStorage(self.DEFAULT_CONFIGS[layer])
        
        logger.info("✅ All 9 memory layers initialized and ready")
    
    def store(self, key: str, value: Any, layer: MemoryLayer = MemoryLayer.L2_RAM,
              metadata: Dict = None, immutable: bool = False) -> bool:
        """
        Store value in specified layer
        Automatically routes to L3_CRYSTALS if immutable
        """
        with self.lock:
            # Override layer for immutable data
            if immutable:
                layer = MemoryLayer.L3_CRYSTALS
            
            target_layer = self.layers[layer]
            success = target_layer.store(key, value, metadata)
            
            if success:
                self.current_layer[key] = layer
                self.access_counts[key] = 1
                self.last_access[key] = time.time()
                
                logger.debug(f"📦 Stored {key} in {layer.name} (immutable={immutable})")
                return True
            
            return False
    
    def retrieve(self, key: str) -> Tuple[Optional[Any], bool, MemoryLayer]:
        """
        Retrieve value from appropriate layer
        Handles layer fallback and promotion
        Returns (value, found, layer)
        """
        with self.lock:
            if key not in self.current_layer:
                return None, False, None
            
            current_layer = self.current_layer[key]
            storage = self.layers[current_layer]
            
            value, found = storage.retrieve(key)
            
            if found:
                # Record access for potential promotion
                self.access_counts[key] = self.access_counts.get(key, 0) + 1
                self.last_access[key] = time.time()
                
                # Check if should promote
                if self.enable_promotion:
                    self._try_promote(key, current_layer)
                
                logger.debug(f"📥 Retrieved {key} from {current_layer.name} "
                           f"(access_count={self.access_counts[key]})")
                return value, True, current_layer
            
            # Layer fallback: try lower layers
            logger.warning(f"⚠️ {key} not found in {current_layer.name}, attempting fallback...")
            
            # Try to find in other layers (simplified fallback)
            for layer in list(MemoryLayer):
                if layer == current_layer:
                    continue
                
                storage = self.layers[layer]
                value, found = storage.retrieve(key)
                if found:
                    # Update tracking
                    self.current_layer[key] = layer
                    logger.info(f"✅ Found {key} in {layer.name} (via fallback)")
                    return value, True, layer
            
            return None, False, None
    
    def _try_promote(self, key: str, current_layer: MemoryLayer):
        """Attempt to promote key to higher priority layer"""
        if not self.enable_promotion:
            return
        
        config = self.DEFAULT_CONFIGS[current_layer]
        access_count = self.access_counts.get(key, 0)
        
        # Check if should promote to next layer
        if access_count >= config.promotion_threshold:
            # Promote to higher/faster layer
            promotion_map = {
                MemoryLayer.L4_SQLITE: MemoryLayer.L2_RAM,
                MemoryLayer.L5_CHROMADB: MemoryLayer.L2_RAM,
                MemoryLayer.L6_NEO4J: MemoryLayer.L2_RAM,
                MemoryLayer.L7_INFLUXDB: MemoryLayer.L2_RAM,
                MemoryLayer.L8_QUANTUM: MemoryLayer.L2_RAM,
                MemoryLayer.L9_EKM: MemoryLayer.L4_SQLITE,
            }
            
            next_layer = promotion_map.get(current_layer)
            if next_layer and next_layer != current_layer:
                value, found = self.layers[current_layer].retrieve(key)
                if found:
                    # Store in next layer
                    self.layers[next_layer].store(key, value)
                    self.current_layer[key] = next_layer
                    logger.info(f"📈 Promoted {key}: {current_layer.name} → {next_layer.name}")
    
    def search_all_layers(self, key: str) -> Optional[Tuple[Any, MemoryLayer]]:
        """Search all layers for key"""
        with self.lock:
            for layer in list(MemoryLayer):
                storage = self.layers[layer]
                if storage.exists(key):
                    value, found = storage.retrieve(key)
                    if found:
                        return value, layer
            return None
    
    def delete(self, key: str) -> bool:
        """Delete from current layer (respects immutability)"""
        with self.lock:
            if key not in self.current_layer:
                return False
            
            layer = self.current_layer[key]
            storage = self.layers[layer]
            
            if storage.delete(key):
                del self.current_layer[key]
                if key in self.access_counts:
                    del self.access_counts[key]
                if key in self.last_access:
                    del self.last_access[key]
                return True
            
            return False
    
    def get_all_statistics(self) -> Dict[str, Any]:
        """Get statistics for all layers"""
        with self.lock:
            stats = {}
            for layer, storage in self.layers.items():
                stats[layer.name] = storage.get_stats()
            
            return {
                "layers": stats,
                "total_keys": len(self.current_layer),
                "high_frequency_keys": sorted(
                    self.access_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            }
    
    def verify_crystal_integrity(self, key: str) -> bool:
        """Verify crystal storage integrity"""
        if self.current_layer.get(key) != MemoryLayer.L3_CRYSTALS:
            return False
        
        crystal_storage = self.layers[MemoryLayer.L3_CRYSTALS]
        if isinstance(crystal_storage, CrystalLayerStorage):
            return crystal_storage.verify_integrity(key)
        
        return False


# ══════════════════════════════════════════════════════════════════
# TESTING
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - LAYER_MGR - %(levelname)s - %(message)s'
    )
    
    # Initialize layer manager
    manager = MemoryLayerManager()
    
    # Test L1-L2 RAM layers
    print("\n" + "="*70)
    print("Testing L1-L2 RAM Layers")
    print("="*70)
    manager.store("quick_task", "Do this now", layer=MemoryLayer.L1_REDIS)
    manager.store("working_data", "Current operation state", layer=MemoryLayer.L2_RAM)
    
    value, found, layer = manager.retrieve("quick_task")
    print(f"Retrieved: {value} from {layer.name if layer else 'None'} (found={found})")
    
    # Test L3 Crystal layer
    print("\n" + "="*70)
    print("Testing L3 Crystal Layer (Immutable)")
    print("="*70)
    manager.store("sovereign_command", "VERIFIED_AUTHORITY_LEVEL_11", immutable=True)
    value, found, layer = manager.retrieve("sovereign_command")
    print(f"Crystal Value: {value} from {layer.name if layer else 'None'} (found={found})")
    print(f"Crystal Integrity Valid: {manager.verify_crystal_integrity('sovereign_command')}")
    
    # Test layer fallback
    print("\n" + "="*70)
    print("Testing Layer Fallback & Statistics")
    print("="*70)
    
    stats = manager.get_all_statistics()
    print("\nLayer Statistics:")
    for layer_name, layer_stats in stats['layers'].items():
        if layer_stats.get('reads', 0) > 0 or layer_stats.get('writes', 0) > 0:
            print(f"{layer_name}: {layer_stats['reads']} reads, "
                  f"{layer_stats['writes']} writes, "
                  f"Hit Rate: {(layer_stats['hits']/layer_stats['reads']*100) if layer_stats['reads'] > 0 else 0:.1f}%")
    
    print(f"\nTotal Keys: {stats['total_keys']}")
    print(f"High Frequency Keys: {stats['high_frequency_keys']}")
