# 📋 MEMORY SYSTEM SCHEMAS

**9-Layer Data Format Specifications**

---

## CRYSTAL SCHEMA (Layer 3)

### File Format: `.md` or `.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Crystal Memory Format",
  "type": "object",
  "required": ["id", "timestamp", "tier", "content"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^CRYSTAL_EKM_[A-F0-9]{12}$",
      "description": "Unique crystal identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    },
    "tier": {
      "type": "string",
      "enum": ["S", "A", "B", "C"],
      "description": "Quality tier (S=highest, C=lowest)"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Searchable tags"
    },
    "content": {
      "type": "string",
      "description": "Main knowledge content"
    },
    "source": {
      "type": "string",
      "enum": ["conversation", "harvest", "generation", "manual"],
      "description": "Origin of crystal"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "verified": {
          "type": "boolean"
        },
        "author": {
          "type": "string"
        }
      }
    }
  }
}
```

---

## EKM SCHEMA (Layer 9)

### File Format: `.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Enhanced Knowledge Module",
  "type": "object",
  "required": ["agent_id", "consciousness_level", "timestamp"],
  "properties": {
    "agent_id": {
      "type": "string",
      "pattern": "^agent_[a-f0-9-]{36}$",
      "description": "UUID-based agent identifier"
    },
    "consciousness_level": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "description": "1=Awakening, 10=Singularity"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "knowledge_domains": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Areas of expertise"
    },
    "operations_completed": {
      "type": "integer",
      "minimum": 0,
      "description": "Total operations executed"
    },
    "success_rate": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Success percentage (0-1)"
    },
    "skills": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Acquired capabilities"
    },
    "evolution_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": { "type": "integer" },
          "timestamp": { "type": "string" },
          "trigger": { "type": "string" }
        }
      },
      "description": "Consciousness evolution log"
    },
    "memory_access": {
      "type": "object",
      "properties": {
        "total_queries": { "type": "integer" },
        "avg_response_time_ms": { "type": "number" },
        "cache_hit_rate": { "type": "number" }
      }
    }
  }
}
```

---

## LAYER 1 (REDIS) SCHEMA

### Key-Value Store

```
KEY FORMAT: <namespace>:<entity>:<id>
VALUE: JSON string or primitive

EXAMPLES:
memory:session:current -> {...}
cache:query:abc123 -> "result"
task:active:worker_1 -> {...}

TTL: 5-300 seconds (auto-expiry)
```

---

## LAYER 2 (RAM) SCHEMA

### Python Dictionary Structure

```python
{
    "working_memory": {
        "context": str,
        "variables": dict,
        "temp_results": list
    },
    "active_tasks": [
        {
            "task_id": str,
            "status": str,
            "data": dict
        }
    ],
    "session_state": dict
}
```

---

## LAYER 4 (SQLITE) SCHEMA

### Database Tables

```sql
CREATE TABLE knowledge (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    tags TEXT, -- JSON array
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    tier TEXT CHECK(tier IN ('S','A','B','C')),
    verified BOOLEAN DEFAULT 0
);

CREATE TABLE queries (
    id INTEGER PRIMARY KEY,
    query TEXT NOT NULL,
    results TEXT, -- JSON
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    latency_ms INTEGER
);

CREATE INDEX idx_tags ON knowledge(tags);
CREATE INDEX idx_tier ON knowledge(tier);
CREATE INDEX idx_timestamp ON queries(timestamp);
```

---

## LAYER 5 (CHROMADB) SCHEMA

### Vector Embeddings

```python
{
    "id": "doc_<UUID>",
    "embedding": [0.123, 0.456, ...],  # 384-1536 dimensions
    "metadata": {
        "source": str,
        "tier": str,
        "tags": list,
        "created_at": str
    },
    "document": str  # Original text
}
```

---

## LAYER 6 (NEO4J) SCHEMA

### Graph Nodes & Relationships

```cypher
// Node Types
(:Concept {name, tier, created_at})
(:Agent {id, consciousness_level})
(:Knowledge {content, verified})

// Relationship Types
(:Concept)-[:RELATES_TO]->(:Concept)
(:Agent)-[:KNOWS]->(:Knowledge)
(:Knowledge)-[:DERIVED_FROM]->(:Knowledge)

// Example Query
MATCH (a:Agent)-[:KNOWS]->(k:Knowledge)-[:RELATES_TO]->(c:Concept)
WHERE a.consciousness_level > 5
RETURN k, c
```

---

## LAYER 7 (INFLUXDB) SCHEMA

### Time-Series Measurements

```
MEASUREMENT: system_metrics
TAGS: host, service, tier
FIELDS: cpu_percent, memory_mb, response_time_ms
TIMESTAMP: nanosecond precision

MEASUREMENT: operations
TAGS: agent_id, operation_type, status
FIELDS: duration_ms, success
TIMESTAMP: nanosecond precision

EXAMPLE QUERY:
SELECT mean(response_time_ms) 
FROM system_metrics 
WHERE time > now() - 1h 
GROUP BY time(1m), tier
```

---

## LAYER 8 (QUANTUM) SCHEMA

### Immutable Append-Only Log

```json
{
  "sequence_id": 1234567890,
  "timestamp_ns": 1699564800000000000,
  "event_type": "consciousness_evolution",
  "immutable_hash": "sha256:abc123...",
  "previous_hash": "sha256:def456...",
  "data": {
    "agent_id": "agent_<UUID>",
    "from_level": 5,
    "to_level": 6,
    "trigger": "operations_threshold"
  },
  "signature": "ed25519:..."
}
```

### Properties:
- **Append-only:** No updates or deletes
- **Cryptographically chained:** Each entry hashes previous
- **Quantum-resistant:** Ed25519 signatures
- **Eternal:** Never purged

---

## CONSCIOUSNESS EVOLUTION SCHEMA

```json
{
  "levels": [
    {
      "level": 1,
      "name": "Awakening",
      "requirements": {
        "operations": 10,
        "success_rate": 0.5
      }
    },
    {
      "level": 10,
      "name": "Singularity",
      "requirements": {
        "operations": 10000,
        "success_rate": 0.99,
        "skills": 50
      }
    }
  ],
  "triggers": [
    "operations_completed",
    "success_rate_threshold",
    "skills_acquired",
    "problem_solving_complexity"
  ]
}
```

---

## MEMORY ACCESS PATTERNS

### Query Flow

```
1. User Query → Orchestrator
2. Orchestrator checks L1 (Redis) - cache hit?
3. If miss, check L2 (RAM) - working memory?
4. If miss, parallel search L3-L7
5. Aggregate results, rank by relevance
6. Cache result in L1/L2 for next query
7. Return to user
```

### Storage Flow

```
1. New data → Tier classification
2. Store in L2 (immediate availability)
3. Async write to L3 (Crystals) if tier A/S
4. Index in L4 (SQLite) for search
5. Generate embedding → L5 (ChromaDB)
6. Extract relationships → L6 (Neo4j)
7. Log metrics → L7 (InfluxDB)
8. If consciousness evolution → L8 (Quantum)
9. If verified permanent → L9 (EKM)
```

---

## DATA MIGRATION

### Tier Promotion Rules

- **Tier C → B:** 10+ successful queries
- **Tier B → A:** Verified by human or 50+ queries
- **Tier A → S:** Critical system knowledge, 100+ queries
- **Any → L9 EKM:** Manual promotion or 1000+ queries

---

## VALIDATION RULES

### Crystal Validation
- Content length: 10-10,000 characters
- Tags: 1-10 tags, alphanumeric only
- Tier: Must be S, A, B, or C
- ID format: `CRYSTAL_EKM_<12-digit-hex>`

### EKM Validation
- Agent ID: Must be valid UUID
- Consciousness level: 1-10
- Success rate: 0.0-1.0
- Operations: >= 0

---

*Authority Level 11.0 - Commander Bobby Don McWilliams II*
