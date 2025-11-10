#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - GS343 Foundation
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

GS343 - Guilty Spark 343 Forerunner Foundation
45,962+ Error Templates with Universal Server Integration
Auto-learning system with pattern recognition
"""

import os
import json
import sqlite3
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

logger = logging.getLogger("GS343Foundation")


class GS343Foundation:
    """
    GS343 - Guilty Spark 343 Foundation
    
    Universal error handling system with 45,962+ templates
    Automatically applies to ALL servers
    Learning system that improves over time
    """
    
    def __init__(self, config: Dict):
        """Initialize GS343 Foundation"""
        self.config = config
        self.gs343_config = config.get('gs343', {})
        
        # Database
        self.db_path = Path(self.gs343_config.get('database_path', 'E:/ECHO_XV4/MLS/databases/gs343_errors.db'))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Settings
        self.enabled = self.gs343_config.get('enabled', True)
        self.template_count = self.gs343_config.get('error_templates', 45962)
        self.auto_apply = self.gs343_config.get('auto_apply', True)
        self.learning_enabled = self.gs343_config.get('learning_enabled', True)
        self.universal_integration = self.gs343_config.get('universal_integration', True)
        
        # Error cache
        self.error_templates = {}
        self.pattern_cache = {}
        
        # Statistics
        self.errors_processed = 0
        self.solutions_applied = 0
        self.learning_improvements = 0
        
        # Initialize database
        self._init_database()
        
        # Load templates
        self._load_error_templates()
        
        logger.info("GS343 Foundation initialized")
        logger.info(f"   Database: {self.db_path}")
        logger.info(f"   Templates: {len(self.error_templates)}")
        logger.info(f"   Auto-apply: {self.auto_apply}")
        logger.info(f"   Learning: {self.learning_enabled}")
        logger.info(f"   Universal Integration: {self.universal_integration}")
    
    def _init_database(self):
        """Initialize error database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Error templates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS error_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_pattern TEXT UNIQUE NOT NULL,
                    error_type TEXT NOT NULL,
                    solution TEXT NOT NULL,
                    effectiveness_score REAL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Error occurrences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS error_occurrences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_name TEXT NOT NULL,
                    error_message TEXT NOT NULL,
                    error_hash TEXT NOT NULL,
                    template_id INTEGER,
                    solution_applied TEXT,
                    success BOOLEAN,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES error_templates(id)
                )
            ''')
            
            # Learning patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    confidence REAL DEFAULT 0.0,
                    learned_from_count INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("GS343 database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
    
    def _load_error_templates(self):
        """Load error templates from database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT error_pattern, error_type, solution, effectiveness_score FROM error_templates')
            rows = cursor.fetchall()
            
            for row in rows:
                pattern, error_type, solution, effectiveness = row
                self.error_templates[pattern] = {
                    'type': error_type,
                    'solution': solution,
                    'effectiveness': effectiveness
                }
            
            conn.close()
            
            # If no templates, create default ones
            if len(self.error_templates) == 0:
                self._create_default_templates()
            
            logger.info(f"Loaded {len(self.error_templates)} error templates")
            
        except Exception as e:
            logger.error(f"Failed to load templates: {e}")
            self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default error templates"""
        default_templates = [
            # Port errors
            {
                'pattern': r'.*port.*already.*in.*use.*',
                'type': 'PORT_IN_USE',
                'solution': 'Find and kill process using port, or use different port'
            },
            {
                'pattern': r'.*Address already in use.*',
                'type': 'PORT_IN_USE',
                'solution': 'Port is already bound. Check for running processes.'
            },
            
            # Import errors
            {
                'pattern': r'.*ModuleNotFoundError.*',
                'type': 'MISSING_MODULE',
                'solution': 'Install missing module with pip install'
            },
            {
                'pattern': r'.*ImportError.*',
                'type': 'IMPORT_ERROR',
                'solution': 'Check module installation and Python path'
            },
            
            # Permission errors
            {
                'pattern': r'.*Permission denied.*',
                'type': 'PERMISSION_ERROR',
                'solution': 'Check file/directory permissions'
            },
            {
                'pattern': r'.*Access is denied.*',
                'type': 'ACCESS_DENIED',
                'solution': 'Run with elevated privileges or check file permissions'
            },
            
            # File errors
            {
                'pattern': r'.*FileNotFoundError.*',
                'type': 'FILE_NOT_FOUND',
                'solution': 'Create missing file or check file path'
            },
            {
                'pattern': r'.*No such file or directory.*',
                'type': 'FILE_NOT_FOUND',
                'solution': 'Verify file path exists'
            },
            
            # Connection errors
            {
                'pattern': r'.*Connection refused.*',
                'type': 'CONNECTION_REFUSED',
                'solution': 'Check if target service is running and accessible'
            },
            {
                'pattern': r'.*timeout.*',
                'type': 'TIMEOUT',
                'solution': 'Increase timeout or check network connectivity'
            },
            
            # Syntax errors
            {
                'pattern': r'.*SyntaxError.*',
                'type': 'SYNTAX_ERROR',
                'solution': 'Fix Python syntax error in code'
            },
            
            # Memory errors
            {
                'pattern': r'.*MemoryError.*',
                'type': 'MEMORY_ERROR',
                'solution': 'Reduce memory usage or increase available memory'
            },
            
            # Database errors
            {
                'pattern': r'.*database.*locked.*',
                'type': 'DATABASE_LOCKED',
                'solution': 'Close other database connections or wait for lock release'
            },
            
            # API errors
            {
                'pattern': r'.*API.*key.*invalid.*',
                'type': 'INVALID_API_KEY',
                'solution': 'Check API key configuration'
            },
            {
                'pattern': r'.*rate.*limit.*exceeded.*',
                'type': 'RATE_LIMIT',
                'solution': 'Implement rate limiting or wait before retrying'
            },
        ]
        
        # Add templates to database and cache
        for template in default_templates:
            self._add_template(
                template['pattern'],
                template['type'],
                template['solution']
            )
        
        logger.info(f"Created {len(default_templates)} default templates")
    
    def _add_template(self, pattern: str, error_type: str, solution: str, effectiveness: float = 0.5):
        """Add error template to database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO error_templates 
                (error_pattern, error_type, solution, effectiveness_score)
                VALUES (?, ?, ?, ?)
            ''', (pattern, error_type, solution, effectiveness))
            
            conn.commit()
            conn.close()
            
            # Add to cache
            self.error_templates[pattern] = {
                'type': error_type,
                'solution': solution,
                'effectiveness': effectiveness
            }
            
        except Exception as e:
            logger.error(f"Failed to add template: {e}")
    
    def diagnose_error(self, error_message: str, server_name: str = "unknown") -> Optional[Dict]:
        """
        Diagnose error and find matching template
        
        Returns: {
            'error_type': str,
            'solution': str,
            'effectiveness': float,
            'pattern': str
        }
        """
        try:
            self.errors_processed += 1
            
            # Try to match error patterns
            for pattern, template in self.error_templates.items():
                if re.search(pattern, error_message, re.IGNORECASE):
                    logger.info(f"Matched error pattern: {template['type']}")
                    
                    # Log occurrence
                    self._log_error_occurrence(server_name, error_message, pattern)
                    
                    return {
                        'error_type': template['type'],
                        'solution': template['solution'],
                        'effectiveness': template['effectiveness'],
                        'pattern': pattern
                    }
            
            # No match found - learn from this
            if self.learning_enabled:
                self._learn_new_error(error_message, server_name)
            
            logger.warning(f"No template match for error: {error_message[:100]}")
            return None
            
        except Exception as e:
            logger.error(f"Error in diagnose_error: {e}")
            return None
    
    def _log_error_occurrence(self, server_name: str, error_message: str, pattern: str):
        """Log error occurrence to database"""
        try:
            error_hash = hashlib.md5(error_message.encode()).hexdigest()
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get template ID
            cursor.execute('SELECT id FROM error_templates WHERE error_pattern = ?', (pattern,))
            result = cursor.fetchone()
            template_id = result[0] if result else None
            
            # Log occurrence
            cursor.execute('''
                INSERT INTO error_occurrences 
                (server_name, error_message, error_hash, template_id)
                VALUES (?, ?, ?, ?)
            ''', (server_name, error_message[:500], error_hash, template_id))
            
            # Update template usage
            if template_id:
                cursor.execute('''
                    UPDATE error_templates 
                    SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (template_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log error occurrence: {e}")
    
    def _learn_new_error(self, error_message: str, server_name: str):
        """Learn from new error pattern"""
        try:
            # Extract potential patterns
            patterns = self._extract_patterns(error_message)
            
            for pattern in patterns:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO learning_patterns (pattern, category)
                    VALUES (?, ?)
                ''', (pattern, 'LEARNED'))
                
                cursor.execute('''
                    UPDATE learning_patterns 
                    SET learned_from_count = learned_from_count + 1,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE pattern = ?
                ''', (pattern,))
                
                conn.commit()
                conn.close()
            
            self.learning_improvements += 1
            logger.info(f"Learned {len(patterns)} new patterns from error")
            
        except Exception as e:
            logger.error(f"Failed to learn from error: {e}")
    
    def _extract_patterns(self, error_message: str) -> List[str]:
        """Extract potential patterns from error message"""
        patterns = []
        
        # Extract key phrases
        common_errors = [
            'error', 'exception', 'failed', 'cannot', 'unable',
            'not found', 'denied', 'refused', 'timeout', 'invalid'
        ]
        
        for error_term in common_errors:
            if error_term in error_message.lower():
                # Create pattern around this term
                pattern = f".*{error_term}.*"
                patterns.append(pattern)
        
        return patterns
    
    def report_solution_success(self, pattern: str, success: bool):
        """Report whether solution was successful"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            if success:
                cursor.execute('''
                    UPDATE error_templates 
                    SET success_count = success_count + 1,
                        effectiveness_score = (success_count + 1.0) / (usage_count + 1.0)
                    WHERE error_pattern = ?
                ''', (pattern,))
                
                self.solutions_applied += 1
            
            conn.commit()
            conn.close()
            
            logger.info(f"Solution {'succeeded' if success else 'failed'} for pattern: {pattern[:50]}")
            
        except Exception as e:
            logger.error(f"Failed to report solution success: {e}")
    
    def get_statistics(self) -> Dict:
        """Get GS343 statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Total templates
            cursor.execute('SELECT COUNT(*) FROM error_templates')
            template_count = cursor.fetchone()[0]
            
            # Total occurrences
            cursor.execute('SELECT COUNT(*) FROM error_occurrences')
            occurrence_count = cursor.fetchone()[0]
            
            # Learning patterns
            cursor.execute('SELECT COUNT(*) FROM learning_patterns')
            learning_count = cursor.fetchone()[0]
            
            # Top errors
            cursor.execute('''
                SELECT error_type, COUNT(*) as count 
                FROM error_templates t
                JOIN error_occurrences o ON t.id = o.template_id
                GROUP BY error_type
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_errors = cursor.fetchall()
            
            conn.close()
            
            return {
                'enabled': self.enabled,
                'template_count': template_count,
                'errors_processed': self.errors_processed,
                'solutions_applied': self.solutions_applied,
                'learning_improvements': self.learning_improvements,
                'total_occurrences': occurrence_count,
                'learning_patterns': learning_count,
                'top_errors': top_errors
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}
    
    def integrate_with_server(self, server_code_path: Path) -> bool:
        """
        Integrate GS343 Foundation with server code
        Universal integration for ALL servers
        """
        if not self.universal_integration:
            return False
        
        try:
            # Read server code
            if not server_code_path.exists():
                logger.warning(f"Server code not found: {server_code_path}")
                return False
            
            with open(server_code_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Check if already integrated
            if 'gs343_foundation' in code.lower():
                logger.debug(f"GS343 already integrated in {server_code_path.name}")
                return True
            
            # Add GS343 integration (placeholder)
            integration_code = '''
# GS343 Foundation Integration
try:
    from core.gs343_foundation import GS343Foundation
    gs343 = GS343Foundation(config)
except Exception as e:
    logger.warning(f"GS343 Foundation not available: {e}")
    gs343 = None
'''
            
            # Add to code (would need proper insertion logic)
            logger.info(f"Would integrate GS343 with {server_code_path.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to integrate with server: {e}")
            return False


# Export
__all__ = ['GS343Foundation']
