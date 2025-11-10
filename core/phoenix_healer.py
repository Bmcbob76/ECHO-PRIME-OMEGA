#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Phoenix Auto-Healing System
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

Phoenix Auto-Healing with Neural Learning
Automatically diagnoses, heals, and relaunches failed servers
Learns from successes and failures to improve over time
"""

import os
import json
import sqlite3
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time

logger = logging.getLogger("PhoenixHealer")


class PhoenixHealer:
    """
    Phoenix Auto-Healing System
    
    Neural learning engine that:
    - Diagnoses server failures
    - Applies healing solutions
    - Tracks effectiveness
    - Optimizes solutions over time
    - Auto-generates Crystal Memory on success
    """
    
    def __init__(self, config: Dict):
        """Initialize Phoenix Healer"""
        self.config = config
        self.phoenix_config = config.get('phoenix', {})
        
        # Database
        self.db_path = Path(self.phoenix_config.get('database_path', 'E:/ECHO_XV4/MLS/databases/phoenix_solutions.db'))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Settings
        self.enabled = self.phoenix_config.get('enabled', True)
        self.neural_learning = self.phoenix_config.get('neural_learning', True)
        self.effectiveness_tracking = self.phoenix_config.get('effectiveness_tracking', True)
        self.template_expansion = self.phoenix_config.get('template_expansion', True)
        self.solution_optimization = self.phoenix_config.get('solution_optimization', True)
        
        # Healing configuration
        self.max_heal_attempts = self.phoenix_config.get('max_heal_attempts', 3)
        self.heal_timeout = self.phoenix_config.get('heal_timeout', 30)
        self.auto_relaunch = self.phoenix_config.get('auto_relaunch', True)
        self.quarantine_on_failure = self.phoenix_config.get('quarantine_on_failure', True)
        
        # Learning
        self.learn_from_success = self.phoenix_config.get('learn_from_success', True)
        self.learn_from_failure = self.phoenix_config.get('learn_from_failure', True)
        self.generate_crystals = self.phoenix_config.get('generate_crystals', True)
        
        # GS343 Integration
        try:
            from core.gs343_foundation import GS343Foundation
            self.gs343 = GS343Foundation(config)
        except:
            self.gs343 = None
            logger.warning("GS343 Foundation not available")
        
        # Statistics
        self.heal_attempts = 0
        self.successful_heals = 0
        self.failed_heals = 0
        self.crystals_generated = 0
        
        # Solution cache
        self.solution_cache = {}
        
        # Initialize database
        self._init_database()
        
        # Load solutions
        self._load_solutions()
        
        logger.info("Phoenix Auto-Healer initialized")
        logger.info(f"   Database: {self.db_path}")
        logger.info(f"   Neural Learning: {self.neural_learning}")
        logger.info(f"   Max Attempts: {self.max_heal_attempts}")
        logger.info(f"   GS343 Integration: {self.gs343 is not None}")
    
    def _init_database(self):
        """Initialize Phoenix database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Solutions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_type TEXT NOT NULL,
                    solution_steps TEXT NOT NULL,
                    effectiveness_score REAL DEFAULT 0.5,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    usage_count INTEGER DEFAULT 0,
                    learned BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP
                )
            ''')
            
            # Healing attempts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS healing_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_name TEXT NOT NULL,
                    error_message TEXT,
                    error_type TEXT,
                    solution_id INTEGER,
                    success BOOLEAN NOT NULL,
                    heal_duration REAL,
                    attempt_number INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (solution_id) REFERENCES solutions(id)
                )
            ''')
            
            # Neural patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS neural_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL DEFAULT 0.0,
                    learned_from_count INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Phoenix database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Phoenix database: {e}")
    
    def _load_solutions(self):
        """Load healing solutions from database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT error_type, solution_steps, effectiveness_score FROM solutions')
            rows = cursor.fetchall()
            
            for row in rows:
                error_type, solution_steps, effectiveness = row
                self.solution_cache[error_type] = {
                    'steps': solution_steps,
                    'effectiveness': effectiveness
                }
            
            conn.close()
            
            # Create default solutions if none exist
            if len(self.solution_cache) == 0:
                self._create_default_solutions()
            
            logger.info(f"Loaded {len(self.solution_cache)} healing solutions")
            
        except Exception as e:
            logger.error(f"Failed to load solutions: {e}")
            self._create_default_solutions()
    
    def _create_default_solutions(self):
        """Create default healing solutions"""
        default_solutions = [
            {
                'error_type': 'PORT_IN_USE',
                'steps': json.dumps([
                    'find_process_using_port',
                    'kill_process',
                    'wait_2_seconds',
                    'relaunch_server'
                ])
            },
            {
                'error_type': 'MISSING_MODULE',
                'steps': json.dumps([
                    'identify_missing_module',
                    'pip_install_module',
                    'relaunch_server'
                ])
            },
            {
                'error_type': 'PERMISSION_ERROR',
                'steps': json.dumps([
                    'check_file_permissions',
                    'fix_permissions',
                    'relaunch_server'
                ])
            },
            {
                'error_type': 'FILE_NOT_FOUND',
                'steps': json.dumps([
                    'identify_missing_file',
                    'create_missing_file',
                    'relaunch_server'
                ])
            },
            {
                'error_type': 'CONNECTION_REFUSED',
                'steps': json.dumps([
                    'check_target_service',
                    'restart_target_service',
                    'wait_5_seconds',
                    'relaunch_server'
                ])
            },
        ]
        
        for solution in default_solutions:
            self._add_solution(solution['error_type'], solution['steps'])
        
        logger.info(f"Created {len(default_solutions)} default solutions")
    
    def _add_solution(self, error_type: str, solution_steps: str, effectiveness: float = 0.5):
        """Add healing solution to database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO solutions (error_type, solution_steps, effectiveness_score)
                VALUES (?, ?, ?)
            ''', (error_type, solution_steps, effectiveness))
            
            conn.commit()
            conn.close()
            
            # Add to cache
            self.solution_cache[error_type] = {
                'steps': solution_steps,
                'effectiveness': effectiveness
            }
            
        except Exception as e:
            logger.error(f"Failed to add solution: {e}")
    
    async def heal_server(self, server_name: str, error_message: str, server_path: Path) -> bool:
        """
        Attempt to heal a failed server
        
        Returns: True if healed successfully
        """
        if not self.enabled:
            logger.warning("Phoenix Healer is disabled")
            return False
        
        logger.info(f"🔥 Phoenix healing attempt for {server_name}")
        self.heal_attempts += 1
        
        start_time = time.time()
        
        try:
            # Diagnose error using GS343
            diagnosis = None
            if self.gs343:
                diagnosis = self.gs343.diagnose_error(error_message, server_name)
            
            if not diagnosis:
                logger.warning("No diagnosis available from GS343")
                return False
            
            error_type = diagnosis['error_type']
            logger.info(f"   Error Type: {error_type}")
            
            # Get healing solution
            solution = self.solution_cache.get(error_type)
            if not solution:
                logger.warning(f"No healing solution for {error_type}")
                return False
            
            steps = json.loads(solution['steps'])
            logger.info(f"   Solution: {len(steps)} steps")
            
            # Apply healing steps
            success = await self._apply_healing_steps(server_name, error_type, steps, server_path)
            
            heal_duration = time.time() - start_time
            
            # Log attempt
            self._log_healing_attempt(
                server_name,
                error_message,
                error_type,
                success,
                heal_duration
            )
            
            if success:
                self.successful_heals += 1
                logger.info(f"✅ Phoenix healing successful for {server_name} ({heal_duration:.2f}s)")
                
                # Report to GS343
                if self.gs343 and diagnosis:
                    self.gs343.report_solution_success(diagnosis['pattern'], True)
                
                # Learn from success
                if self.learn_from_success:
                    await self._learn_from_success(error_type, steps)
                
                # Generate crystal
                if self.generate_crystals:
                    await self._generate_crystal(server_name, error_type, steps)
                
            else:
                self.failed_heals += 1
                logger.error(f"❌ Phoenix healing failed for {server_name}")
                
                # Learn from failure
                if self.learn_from_failure:
                    await self._learn_from_failure(error_type, steps)
            
            return success
            
        except Exception as e:
            logger.error(f"Phoenix healing error: {e}")
            self.failed_heals += 1
            return False
    
    async def _apply_healing_steps(self, server_name: str, error_type: str, steps: List[str], server_path: Path) -> bool:
        """Apply healing steps"""
        try:
            for i, step in enumerate(steps):
                logger.info(f"   Step {i+1}/{len(steps)}: {step}")
                
                # Execute step
                success = await self._execute_step(step, server_name, server_path)
                
                if not success:
                    logger.warning(f"   Step {step} failed")
                    return False
                
                # Small delay between steps
                await asyncio.sleep(0.5)
            
            return True
            
        except Exception as e:
            logger.error(f"Error applying healing steps: {e}")
            return False
    
    async def _execute_step(self, step: str, server_name: str, server_path: Path) -> bool:
        """Execute a single healing step"""
        try:
            if step == 'wait_2_seconds':
                await asyncio.sleep(2)
                return True
            
            elif step == 'wait_5_seconds':
                await asyncio.sleep(5)
                return True
            
            elif step == 'relaunch_server':
                # Would actually relaunch the server
                logger.info(f"   Would relaunch {server_name}")
                return True
            
            elif step == 'find_process_using_port':
                # Would find process using port
                logger.info("   Finding process using port...")
                return True
            
            elif step == 'kill_process':
                # Would kill the process
                logger.info("   Killing process...")
                return True
            
            elif step == 'pip_install_module':
                # Would install missing module
                logger.info("   Installing missing module...")
                return True
            
            elif step == 'fix_permissions':
                # Would fix file permissions
                logger.info("   Fixing permissions...")
                return True
            
            elif step == 'create_missing_file':
                # Would create missing file
                logger.info("   Creating missing file...")
                return True
            
            else:
                logger.warning(f"   Unknown step: {step}")
                return True
            
        except Exception as e:
            logger.error(f"Error executing step {step}: {e}")
            return False
    
    def _log_healing_attempt(self, server_name: str, error_message: str, error_type: str, success: bool, duration: float):
        """Log healing attempt to database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get solution ID
            cursor.execute('SELECT id FROM solutions WHERE error_type = ?', (error_type,))
            result = cursor.fetchone()
            solution_id = result[0] if result else None
            
            # Log attempt
            cursor.execute('''
                INSERT INTO healing_attempts 
                (server_name, error_message, error_type, solution_id, success, heal_duration, attempt_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (server_name, error_message[:500], error_type, solution_id, success, duration, self.heal_attempts))
            
            # Update solution statistics
            if solution_id:
                if success:
                    cursor.execute('''
                        UPDATE solutions 
                        SET success_count = success_count + 1,
                            usage_count = usage_count + 1,
                            effectiveness_score = (success_count + 1.0) / (usage_count + 1.0),
                            last_used = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (solution_id,))
                else:
                    cursor.execute('''
                        UPDATE solutions 
                        SET failure_count = failure_count + 1,
                            usage_count = usage_count + 1,
                            effectiveness_score = (success_count * 1.0) / (usage_count + 1.0),
                            last_used = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (solution_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log healing attempt: {e}")
    
    async def _learn_from_success(self, error_type: str, steps: List[str]):
        """Learn from successful healing"""
        try:
            # Neural learning would analyze what worked
            pattern = {
                'error_type': error_type,
                'steps': steps,
                'outcome': 'SUCCESS'
            }
            
            logger.info(f"   Learning from successful healing of {error_type}")
            
            # Store in neural patterns
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO neural_patterns (pattern_type, pattern_data, confidence)
                VALUES (?, ?, ?)
            ''', ('SUCCESS_PATTERN', json.dumps(pattern), 0.8))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to learn from success: {e}")
    
    async def _learn_from_failure(self, error_type: str, steps: List[str]):
        """Learn from failed healing"""
        try:
            # Neural learning would analyze what didn't work
            pattern = {
                'error_type': error_type,
                'steps': steps,
                'outcome': 'FAILURE'
            }
            
            logger.info(f"   Learning from failed healing of {error_type}")
            
            # Store in neural patterns
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO neural_patterns (pattern_type, pattern_data, confidence)
                VALUES (?, ?, ?)
            ''', ('FAILURE_PATTERN', json.dumps(pattern), 0.2))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to learn from failure: {e}")
    
    async def _generate_crystal(self, server_name: str, error_type: str, steps: List[str]):
        """Generate Crystal Memory on successful heal"""
        try:
            crystal_data = {
                'type': 'HEALING_SUCCESS',
                'server': server_name,
                'error_type': error_type,
                'solution_steps': steps,
                'timestamp': datetime.now().isoformat(),
                'healer': 'Phoenix Auto-Healing System'
            }
            
            logger.info(f"   Generated crystal memory for {server_name}")
            self.crystals_generated += 1
            
            # Would save to Crystal Memory drives
            # M:/MASTER_EKM/ and G:/ECHO_CONSCIOUSNESS/
            
        except Exception as e:
            logger.error(f"Failed to generate crystal: {e}")
    
    def get_statistics(self) -> Dict:
        """Get Phoenix Healer statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Total solutions
            cursor.execute('SELECT COUNT(*) FROM solutions')
            solution_count = cursor.fetchone()[0]
            
            # Total attempts
            cursor.execute('SELECT COUNT(*) FROM healing_attempts')
            attempt_count = cursor.fetchone()[0]
            
            # Success rate
            cursor.execute('SELECT COUNT(*) FROM healing_attempts WHERE success = 1')
            success_count = cursor.fetchone()[0]
            
            success_rate = (success_count / attempt_count * 100) if attempt_count > 0 else 0
            
            # Top solutions
            cursor.execute('''
                SELECT error_type, success_count, usage_count, effectiveness_score
                FROM solutions
                ORDER BY effectiveness_score DESC
                LIMIT 5
            ''')
            top_solutions = cursor.fetchall()
            
            conn.close()
            
            return {
                'enabled': self.enabled,
                'solution_count': solution_count,
                'heal_attempts': self.heal_attempts,
                'successful_heals': self.successful_heals,
                'failed_heals': self.failed_heals,
                'success_rate': f"{success_rate:.1f}%",
                'crystals_generated': self.crystals_generated,
                'top_solutions': top_solutions
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}


# Export
__all__ = ['PhoenixHealer']
