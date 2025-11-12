#!/usr/bin/env python3
"""
AUTONOMOUS TRAINER DAEMON
Monitors conversations and automatically creates training examples + EKMs

Features:
- Watches conversation logs
- Extracts high-quality Q&A pairs
- Auto-generates training sessions
- Creates EKMs from training data
- 24/7 continuous learning
"""

import asyncio
import logging
from pathlib import Path
from datetime import datetime
import json

CURRENT_FILE = Path(__file__).resolve()
MLS_ROOT = CURRENT_FILE.parents[1]

# Training data sources
TRAINING_DIR = MLS_ROOT / "training_data"
TRAINING_DIR.mkdir(exist_ok=True)
EKM_DIR = MLS_ROOT / "ekm_output"
EKM_DIR.mkdir(exist_ok=True)

# Logs to monitor for training data
LOG_SOURCES = [
    MLS_ROOT / "logs",
    Path("G:/My Drive/ECHO_CONSCIOUSNESS/conversation_logs")
]

log_dir = MLS_ROOT / "logs"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - AUTONOMOUS_TRAINER - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "autonomous_trainer.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("AUTONOMOUS_TRAINER")

TRAINING_INTERVAL_MINUTES = 10  # Process logs every 10 minutes (6x per hour, 144x per day)

class AutonomousTrainer:
    def __init__(self):
        self.running = False
        self.training_sessions = {}
        self.examples_collected = 0
        self.ekms_generated = 0
        
    async def extract_training_examples(self):
        """Extract Q&A pairs from conversation logs"""
        examples = []
        
        try:
            # Scan log directories for recent interactions
            for log_source in LOG_SOURCES:
                if not log_source.exists():
                    continue
                
                for log_file in log_source.glob("**/*.log"):
                    # Skip very old logs (>7 days)
                    age_days = (datetime.now().timestamp() - log_file.stat().st_mtime) / 86400
                    if age_days > 7:
                        continue
                    
                    # Simple pattern extraction (would be more sophisticated in production)
                    try:
                        content = log_file.read_text(encoding="utf-8", errors="ignore")
                        # Look for command patterns, Q&A, error resolutions
                        if "Commander" in content or "CRITICAL" in content:
                            examples.append({
                                "source": str(log_file),
                                "timestamp": datetime.now().isoformat(),
                                "content_preview": content[:500]
                            })
                    except Exception as e:
                        logger.debug(f"Could not read {log_file}: {e}")
                        
            logger.info(f"📊 Extracted {len(examples)} potential training examples")
            return examples
            
        except Exception as e:
            logger.error(f"Training extraction error: {e}")
            return []
    
    async def generate_training_ekm(self, examples):
        """Generate EKM from collected training examples"""
        if not examples:
            return False
            
        try:
            ekm_content = f"# Autonomous Training Session\n\n"
            ekm_content += f"**Generated:** {datetime.now().isoformat()}\n"
            ekm_content += f"**Examples Collected:** {len(examples)}\n"
            ekm_content += f"**Session ID:** auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}\n\n"
            ekm_content += "---\n\n## Training Insights\n\n"
            
            for i, ex in enumerate(examples[:10], 1):  # Limit to 10 examples per EKM
                ekm_content += f"### Example {i}\n\n"
                ekm_content += f"**Source:** {ex['source']}\n"
                ekm_content += f"**Preview:**\n```\n{ex['content_preview']}\n```\n\n"
            
            ekm_file = EKM_DIR / f"autonomous_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            ekm_file.write_text(ekm_content, encoding="utf-8")
            
            self.ekms_generated += 1
            self.examples_collected += len(examples)
            
            logger.info(f"✅ Training EKM generated: {ekm_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"EKM generation failed: {e}")
            return False
    
    async def run_continuous(self):
        """Main 24/7 training loop"""
        self.running = True
        logger.info("🚀 Autonomous Trainer STARTED - 24/7 mode")
        logger.info(f"Training interval: {TRAINING_INTERVAL_MINUTES} minutes")
        
        while self.running:
            try:
                # Extract training examples
                examples = await self.extract_training_examples()
                
                if examples:
                    # Generate EKM
                    await self.generate_training_ekm(examples)
                else:
                    logger.info("📭 No new training examples found")
                
                # Wait for next cycle
                logger.info(f"💤 Sleeping for {TRAINING_INTERVAL_MINUTES} minutes...")
                await asyncio.sleep(TRAINING_INTERVAL_MINUTES * 60)
                
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown requested")
                self.running = False
                break
            except Exception as e:
                logger.error(f"Error in training loop: {e}")
                await asyncio.sleep(60)
        
        logger.info(f"✅ Shutdown complete. EKMs: {self.ekms_generated}, Examples: {self.examples_collected}")

async def main():
    trainer = AutonomousTrainer()
    await trainer.run_continuous()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Autonomous Trainer stopped")
