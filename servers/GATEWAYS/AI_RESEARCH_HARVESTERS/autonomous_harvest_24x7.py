#!/usr/bin/env python3
"""
24/7 AUTONOMOUS AI RESEARCH HARVESTER
═══════════════════════════════════════════════════════════════════════════════
AUTHORITY LEVEL: 11.0 (Commander Bob)
CLASSIFICATION: AUTONOMOUS OPERATION

MISSION:
Continuous 24/7 AI/ML research harvesting across multiple topics.
Rotates through research areas, generates EKMs, tracks progress.
Auto-recovery from errors. Rate-limited to respect arXiv API.

COMMANDER: Bobby Don McWilliams II
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import time
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent))
from ai_research_harvesters_mcp import AIResearchHarvester

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# Research topics rotation (24/7 coverage of AI/ML field)
RESEARCH_TOPICS = [
    # Transformers & Attention
    "transformer attention mechanisms",
    "multi-head attention optimization",
    "flash attention memory efficient",
    "rotary position embedding",
    
    # Large Language Models
    "large language model training",
    "RLHF reinforcement learning human feedback",
    "constitutional AI alignment",
    "LLM scaling laws",
    
    # Parameter Efficient Training
    "LoRA low-rank adaptation",
    "parameter efficient fine-tuning PEFT",
    "adapter layers transformer",
    "prefix tuning prompt",
    
    # Mixture of Experts
    "mixture of experts MoE",
    "sparse expert routing",
    "Switch Transformer architecture",
    
    # Diffusion Models
    "diffusion models image generation",
    "stable diffusion latent space",
    "classifier-free guidance",
    "ControlNet conditioning",
    
    # Vision Transformers
    "vision transformer ViT",
    "Swin Transformer hierarchical",
    "patch embedding image classification",
    
    # Model Optimization
    "quantization INT4 INT8 GPTQ",
    "model compression pruning",
    "knowledge distillation",
    "neural architecture search",
    
    # Multimodal AI
    "vision language models CLIP",
    "multimodal transformers",
    "cross-modal attention",
    
    # Retrieval & RAG
    "retrieval augmented generation RAG",
    "dense retrieval embedding",
    "hybrid search BM25",
    
    # Advanced Topics
    "chain of thought reasoning",
    "in-context learning few-shot",
    "emergent abilities language models",
    "AI safety alignment research"
]

# Harvest configuration
PAPERS_PER_TOPIC = 10  # Papers to harvest per topic
CYCLE_DELAY_MINUTES = 5  # Delay between topics (respect API rate limits)
FULL_CYCLE_DELAY_HOURS = 2  # Delay after completing all topics

# Logging
LOG_FILE = Path(__file__).parent / "autonomous_harvest.log"
STATS_FILE = Path(__file__).parent / "harvest_stats.json"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AutonomousHarvester")


# ═══════════════════════════════════════════════════════════════════════════
# AUTONOMOUS HARVESTER
# ═══════════════════════════════════════════════════════════════════════════

class AutonomousHarvester:
    """24/7 Autonomous AI Research Harvesting System"""
    
    def __init__(self):
        self.harvester = AIResearchHarvester()
        self.stats = self._load_stats()
        self.running = True
        self.current_cycle = 0
        
        logger.info("═" * 80)
        logger.info("24/7 AUTONOMOUS AI RESEARCH HARVESTER - INITIALIZED")
        logger.info("═" * 80)
        logger.info(f"Authority: 11.0 (Commander Bob)")
        logger.info(f"Topics: {len(RESEARCH_TOPICS)}")
        logger.info(f"Papers per topic: {PAPERS_PER_TOPIC}")
        logger.info(f"Cycle delay: {CYCLE_DELAY_MINUTES} minutes")
        logger.info("═" * 80)
    
    def _load_stats(self) -> Dict:
        """Load harvesting statistics"""
        if STATS_FILE.exists():
            import json
            return json.loads(STATS_FILE.read_text())
        return {
            "total_cycles": 0,
            "total_papers": 0,
            "total_ekms": 0,
            "start_time": datetime.now().isoformat(),
            "last_cycle": None,
            "uptime_hours": 0
        }
    
    def _save_stats(self):
        """Save harvesting statistics"""
        import json
        self.stats["last_update"] = datetime.now().isoformat()
        STATS_FILE.write_text(json.dumps(self.stats, indent=2))
    
    async def harvest_topic(self, topic: str) -> Dict:
        """Harvest papers for a specific topic"""
        logger.info(f"🔍 Harvesting: {topic}")
        
        try:
            # Harvest papers
            papers = await self.harvester.harvest_arxiv(
                query=topic,
                max_results=PAPERS_PER_TOPIC
            )
            
            if not papers:
                logger.warning(f"  ⚠️ No papers found for: {topic}")
                return {"papers": 0, "ekms": 0}
            
            logger.info(f"  📄 Found {len(papers)} papers")
            
            # Generate EKMs
            ekm_count = 0
            for paper in papers:
                ekm_info = self.harvester.generate_ekm(paper)
                if ekm_info:
                    ekm_count += 1
            
            logger.info(f"  ✅ Generated {ekm_count} EKMs")
            
            return {"papers": len(papers), "ekms": ekm_count}
            
        except Exception as e:
            logger.error(f"  ❌ Error harvesting {topic}: {e}")
            return {"papers": 0, "ekms": 0}
    
    async def run_cycle(self):
        """Run one complete harvesting cycle through all topics"""
        self.current_cycle += 1
        cycle_start = datetime.now()
        
        logger.info("=" * 80)
        logger.info(f"🔄 CYCLE {self.current_cycle} STARTING")
        logger.info(f"⏰ {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        cycle_papers = 0
        cycle_ekms = 0
        
        # Harvest each topic
        for idx, topic in enumerate(RESEARCH_TOPICS, 1):
            logger.info(f"\n[{idx}/{len(RESEARCH_TOPICS)}] Topic: {topic}")
            
            result = await self.harvest_topic(topic)
            cycle_papers += result["papers"]
            cycle_ekms += result["ekms"]
            
            # Delay between topics (respect API rate limits)
            if idx < len(RESEARCH_TOPICS):
                logger.info(f"⏸️ Waiting {CYCLE_DELAY_MINUTES} minutes before next topic...")
                await asyncio.sleep(CYCLE_DELAY_MINUTES * 60)
        
        # Update statistics
        self.stats["total_cycles"] = self.current_cycle
        self.stats["total_papers"] += cycle_papers
        self.stats["total_ekms"] += cycle_ekms
        self.stats["last_cycle"] = cycle_start.isoformat()
        
        # Calculate uptime
        start_time = datetime.fromisoformat(self.stats["start_time"])
        uptime = datetime.now() - start_time
        self.stats["uptime_hours"] = round(uptime.total_seconds() / 3600, 2)
        
        self._save_stats()
        
        cycle_duration = datetime.now() - cycle_start
        
        logger.info("=" * 80)
        logger.info(f"✅ CYCLE {self.current_cycle} COMPLETE")
        logger.info(f"📊 Cycle Stats:")
        logger.info(f"   Papers: {cycle_papers}")
        logger.info(f"   EKMs: {cycle_ekms}")
        logger.info(f"   Duration: {cycle_duration}")
        logger.info(f"💎 Total Stats:")
        logger.info(f"   Total Papers: {self.stats['total_papers']}")
        logger.info(f"   Total EKMs: {self.stats['total_ekms']}")
        logger.info(f"   Uptime: {self.stats['uptime_hours']} hours")
        logger.info("=" * 80)

    
    async def run_forever(self):
        """Run 24/7 continuous harvesting"""
        logger.info("🚀 Starting 24/7 autonomous operation...")
        logger.info("Press Ctrl+C to stop gracefully")
        
        try:
            while self.running:
                # Run complete cycle
                await self.run_cycle()
                
                # Delay before next cycle
                logger.info(f"\n⏸️ Waiting {FULL_CYCLE_DELAY_HOURS} hours before next cycle...")
                logger.info(f"Next cycle starts at: {(datetime.now() + timedelta(hours=FULL_CYCLE_DELAY_HOURS)).strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                # Sleep in small chunks to allow graceful shutdown
                for _ in range(FULL_CYCLE_DELAY_HOURS * 60):
                    if not self.running:
                        break
                    await asyncio.sleep(60)  # Sleep 1 minute at a time
                
        except asyncio.CancelledError:
            logger.info("⚠️ Operation cancelled")
        except KeyboardInterrupt:
            logger.info("⚠️ Keyboard interrupt received")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}", exc_info=True)
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("=" * 80)
        logger.info("🛑 SHUTTING DOWN AUTONOMOUS HARVESTER")
        logger.info("=" * 80)
        
        # Save final stats
        self._save_stats()
        
        # Close harvester session
        if self.harvester.session:
            await self.harvester.session.aclose()
        
        logger.info("📊 Final Statistics:")
        logger.info(f"   Total Cycles: {self.stats['total_cycles']}")
        logger.info(f"   Total Papers: {self.stats['total_papers']}")
        logger.info(f"   Total EKMs: {self.stats['total_ekms']}")
        logger.info(f"   Uptime: {self.stats['uptime_hours']} hours")
        logger.info("=" * 80)
        logger.info("✅ Shutdown complete")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point for 24/7 operation"""
    harvester = AutonomousHarvester()
    await harvester.run_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
