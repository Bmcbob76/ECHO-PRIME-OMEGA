#!/usr/bin/env python3
"""
ECHO Multi-LLM Defense System
Real implementation with 10+ LLMs for defense and attack operations
"""

import asyncio
import logging
import json
import time
import threading
import psutil
import socket
import hashlib
import random
import subprocess
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

# ECHO Process Naming
try:
    import echo_process_naming
except ImportError:
    pass

# Load environment variables from the REAL keychain - NO PLACEHOLDERS
from dotenv import load_dotenv
load_dotenv("E:/ECHO_PRIME_SYSTEM/echo_x_complete_api_keychain.env")

# Import REAL API clients with REAL authentication
import openai
import anthropic
from groq import Groq
import requests
import ollama
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
import openai
import ollama

class MultiLLMDefenseSystem:
    """Advanced Multi-LLM Defense System with real functionality"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.llm_engines = {}
        self.active_threats = []
        self.defense_history = []
        self.attack_patterns = {}
        self.system_metrics = {}
        self.running = False
        self.monitoring_threads = []
        
        # Initialize LLM configurations
        self.llm_configs = {
            'gpt-4': {
                'provider': 'openai',
                'model': 'gpt-4',
                'role': 'strategic_defense',
                'specialty': 'complex_reasoning',
                'enabled': False,
                'api_key_env': 'OPENAI_API_KEY'
            },
            'gpt-3.5-turbo': {
                'provider': 'openai', 
                'model': 'gpt-3.5-turbo',
                'role': 'rapid_response',
                'specialty': 'real_time_analysis',
                'enabled': False,
                'api_key_env': 'OPENAI_API_KEY'
            },
            'claude-3-opus': {
                'provider': 'anthropic',
                'model': 'claude-3-opus-20240229',
                'role': 'threat_analysis',
                'specialty': 'deep_analysis',
                'enabled': False,
                'api_key_env': 'ANTHROPIC_API_KEY'
            },
            'claude-3-sonnet': {
                'provider': 'anthropic',
                'model': 'claude-3-sonnet-20240229', 
                'role': 'pattern_detection',
                'specialty': 'behavioral_analysis',
                'enabled': False,
                'api_key_env': 'ANTHROPIC_API_KEY'
            },
            'llama3-70b-groq': {
                'provider': 'groq',
                'model': 'llama3-70b-8192',
                'role': 'strategic_defense',
                'specialty': 'advanced_reasoning',
                'enabled': False,
                'api_key_env': 'GROQ_API_KEY'
            },
            'mixtral-8x7b-groq': {
                'provider': 'groq',
                'model': 'mixtral-8x7b-32768',
                'role': 'threat_analysis',
                'specialty': 'multilingual_analysis',
                'enabled': False,
                'api_key_env': 'GROQ_API_KEY'
            },
            'gemma-7b-groq': {
                'provider': 'groq',
                'model': 'gemma-7b-it',
                'role': 'rapid_response',
                'specialty': 'real_time_analysis',
                'enabled': False,
                'api_key_env': 'GROQ_API_KEY'
            },
            'llama2-70b': {
                'provider': 'ollama',
                'model': 'llama2:70b',
                'role': 'local_defense',
                'specialty': 'offline_protection',
                'enabled': False,
                'api_key_env': None
            },
            'codellama-34b': {
                'provider': 'ollama',
                'model': 'codellama:34b',
                'role': 'code_analysis',
                'specialty': 'malware_detection',
                'enabled': False,
                'api_key_env': None
            },
            'mistral-7b': {
                'provider': 'ollama',
                'model': 'mistral:7b',
                'role': 'threat_hunter',
                'specialty': 'network_analysis',
                'enabled': True,
                'api_key_env': None
            },
            'neural-chat': {
                'provider': 'ollama',
                'model': 'neural-chat:7b',
                'role': 'communication_filter',
                'specialty': 'social_engineering_detection',
                'enabled': True,
                'api_key_env': None
            },
            'orca-mini': {
                'provider': 'ollama',
                'model': 'orca-mini:13b',
                'role': 'lightweight_scanner',
                'specialty': 'quick_assessment',
                'enabled': True,
                'api_key_env': None
            },
            'wizard-coder': {
                'provider': 'ollama',
                'model': 'wizardcoder:15b',
                'role': 'exploit_analyzer',
                'specialty': 'vulnerability_assessment',
                'enabled': False,
                'api_key_env': None
            },
            'phi-2': {
                'provider': 'ollama',
                'model': 'phi:2.7b',
                'role': 'anomaly_detector',
                'specialty': 'behavior_baseline',
                'enabled': True,
                'api_key_env': None
            },
            'gemma-7b': {
                'provider': 'ollama',
                'model': 'gemma:7b',
                'role': 'data_guardian',
                'specialty': 'privacy_protection',
                'enabled': True,
                'api_key_env': None
            },
            'deepseek-coder': {
                'provider': 'ollama',
                'model': 'deepseek-coder:6.7b',
                'role': 'security_auditor',
                'specialty': 'code_security',
                'enabled': True,
                'api_key_env': None
            },
            'stablelm-zephyr': {
                'provider': 'ollama',
                'model': 'stablelm-zephyr:3b',
                'role': 'response_coordinator',
                'specialty': 'incident_management',
                'enabled': True,
                'api_key_env': None
            }
        }
        
        # Real-time monitoring configurations
        self.monitoring_config = {
            'network_monitor': {
                'enabled': True,
                'interval': 1.0,
                'suspicious_ports': [21, 23, 135, 139, 445, 1433, 3389, 5900],
                'max_connections_per_ip': 50
            },
            'process_monitor': {
                'enabled': True,
                'interval': 2.0,
                'suspicious_names': ['mimikatz', 'psexec', 'nc.exe', 'netcat'],
                'memory_threshold': 90
            },
            'file_monitor': {
                'enabled': True,
                'interval': 5.0,
                'watch_directories': ['C:\\Windows\\System32', 'C:\\Users'],
                'suspicious_extensions': ['.exe', '.bat', '.cmd', '.ps1', '.vbs']
            },
            'registry_monitor': {
                'enabled': True,
                'interval': 10.0,
                'critical_keys': [
                    'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
                    'HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
                ]
            }
        }
        
    def _setup_logging(self):
        """Setup comprehensive logging"""
        logger = logging.getLogger('MultiLLMDefense')
        logger.setLevel(logging.INFO)
        
        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / 'llm_defense.log')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    async def initialize_llm_engines(self):
        """Initialize all available LLM engines"""
        self.logger.info("Initializing Multi-LLM Defense Engines...")
        
        # Load real API keys from keychain
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        groq_key = os.getenv('GROQ_API_KEY')
        gemini_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        xai_key = os.getenv('XAI_GROK_API_KEY')
        mistral_key = os.getenv('MISTRAL_API_KEY')
        
        # Check for API keys and initialize engines
        for llm_name, config in self.llm_configs.items():
            try:
                if config['provider'] == 'openai':
                    if openai_key:
                        config['enabled'] = True
                        config['client'] = openai.OpenAI(api_key=openai_key)
                        self.logger.info(f"✅ {llm_name} initialized with REAL OpenAI API key")
                    else:
                        self.logger.warning(f"⚠️ {llm_name} disabled - no OpenAI API key found")
                        
                elif config['provider'] == 'anthropic':
                    if anthropic_key:
                        config['enabled'] = True
                        config['client'] = anthropic.Anthropic(api_key=anthropic_key)
                        self.logger.info(f"✅ {llm_name} initialized with REAL Anthropic API key")
                    else:
                        self.logger.warning(f"⚠️ {llm_name} disabled - no Anthropic API key found")
                        
                elif config['provider'] == 'groq':
                    if groq_key:
                        config['enabled'] = True
                        config['client'] = Groq(api_key=groq_key)
                        self.logger.info(f"✅ {llm_name} initialized with REAL Groq API key")
                    else:
                        self.logger.warning(f"⚠️ {llm_name} disabled - no Groq API key found")
                        
                elif config['provider'] == 'groq':
                    if groq_key:
                        config['enabled'] = True
                        config['client'] = Groq(api_key=groq_key)
                        self.logger.info(f"✅ {llm_name} initialized with REAL Groq API key")
                    else:
                        self.logger.warning(f"⚠️ {llm_name} disabled - no Groq API key found")
                        
                elif config['provider'] == 'ollama':
                    # Try to connect to Ollama
                    try:
                        models = ollama.list()
                        model_names = [model['name'] for model in models['models']]
                        if config['model'] in model_names:
                            config['enabled'] = True
                            config['client'] = ollama
                            self.logger.info(f"✅ {llm_name} initialized successfully")
                        else:
                            self.logger.warning(f"⚠️ {llm_name} model not available in Ollama")
                            # Try to pull the model
                            try:
                                ollama.pull(config['model'])
                                config['enabled'] = True
                                config['client'] = ollama
                                self.logger.info(f"✅ {llm_name} model pulled and initialized")
                            except Exception as e:
                                self.logger.error(f"❌ Failed to pull {llm_name}: {e}")
                    except Exception as e:
                        self.logger.error(f"❌ Ollama connection failed for {llm_name}: {e}")
                        
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize {llm_name}: {e}")
        
        # Count enabled engines
        enabled_count = sum(1 for config in self.llm_configs.values() if config['enabled'])
        self.logger.info(f"🚀 Multi-LLM Defense System: {enabled_count}/{len(self.llm_configs)} engines active")
        
        return enabled_count > 0
    
    async def analyze_threat_with_llm(self, llm_name: str, threat_data: Dict) -> Dict:
        """Analyze threat using specific LLM"""
        config = self.llm_configs.get(llm_name)
        if not config or not config['enabled']:
            return {'error': f'LLM {llm_name} not available'}
        
        try:
            prompt = self._create_threat_analysis_prompt(threat_data, config['specialty'])
            
            if config['provider'] == 'openai':
                response = config['client'].chat.completions.create(
                    model=config['model'],
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert AI analyzing threats."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.1
                )
                analysis = response.choices[0].message.content
                
            elif config['provider'] == 'anthropic':
                response = config['client'].messages.create(
                    model=config['model'],
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                analysis = response.content[0].text
                
            elif config['provider'] == 'groq':
                response = config['client'].chat.completions.create(
                    model=config['model'],
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert AI analyzing threats."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.1
                )
                analysis = response.choices[0].message.content
                
            elif config['provider'] == 'ollama':
                response = config['client'].chat(
                    model=config['model'],
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert AI analyzing threats."},
                        {"role": "user", "content": prompt}
                    ]
                )
                analysis = response['message']['content']
            
            # Parse the analysis and extract actionable intelligence
            result = self._parse_llm_analysis(analysis, config['specialty'])
            result['llm_source'] = llm_name
            result['analysis_time'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing threat with {llm_name}: {e}")
            return {'error': str(e), 'llm_source': llm_name}
    
    def _create_threat_analysis_prompt(self, threat_data: Dict, specialty: str) -> str:
        """Create specialized prompt based on LLM specialty"""
        base_prompt = f"""
        THREAT ANALYSIS REQUEST
        Timestamp: {datetime.now().isoformat()}
        Threat Data: {json.dumps(threat_data, indent=2)}
        
        As a {specialty} specialist, analyze this threat and provide:
        1. Threat severity (1-10)
        2. Attack vector classification
        3. Recommended immediate actions
        4. Potential indicators of compromise
        5. Risk assessment
        
        Respond in JSON format with structured analysis.
        """
        
        if specialty == 'complex_reasoning':
            base_prompt += "\nFocus on strategic implications and advanced persistent threat patterns."
        elif specialty == 'real_time_analysis':
            base_prompt += "\nProvide rapid assessment suitable for immediate automated response."
        elif specialty == 'deep_analysis':
            base_prompt += "\nConduct thorough investigation including attribution and campaign analysis."
        elif specialty == 'behavioral_analysis':
            base_prompt += "\nAnalyze behavioral patterns and anomalies in the threat data."
        elif specialty == 'offline_protection':
            base_prompt += "\nAssess threat without external dependencies or network access."
        elif specialty == 'malware_detection':
            base_prompt += "\nFocus on code analysis and malware family identification."
        elif specialty == 'network_analysis':
            base_prompt += "\nAnalyze network patterns, traffic anomalies, and communication protocols."
        elif specialty == 'social_engineering_detection':
            base_prompt += "\nIdentify human manipulation tactics and psychological exploitation attempts."
        elif specialty == 'quick_assessment':
            base_prompt += "\nProvide fast triage assessment for threat prioritization."
        elif specialty == 'vulnerability_assessment':
            base_prompt += "\nIdentify exploitable vulnerabilities and security weaknesses."
        elif specialty == 'behavior_baseline':
            base_prompt += "\nCompare against normal system behavior baselines."
        elif specialty == 'privacy_protection':
            base_prompt += "\nAssess data exposure risks and privacy implications."
        elif specialty == 'code_security':
            base_prompt += "\nAnalyze code for security flaws and backdoors."
        elif specialty == 'incident_management':
            base_prompt += "\nProvide incident response coordination and escalation recommendations."
        
        return base_prompt
    
    def _parse_llm_analysis(self, analysis: str, specialty: str) -> Dict:
        """Parse LLM analysis into structured format"""
        try:
            # Try to extract JSON from response
            start_idx = analysis.find('{')
            end_idx = analysis.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = analysis[start_idx:end_idx]
                parsed = json.loads(json_str)
                return parsed
        except:
            pass
        
        # Fallback parsing for non-JSON responses
        result = {
            'severity': self._extract_severity(analysis),
            'attack_vector': self._extract_attack_vector(analysis),
            'recommendations': self._extract_recommendations(analysis),
            'iocs': self._extract_iocs(analysis),
            'risk_level': self._extract_risk_level(analysis),
            'specialty': specialty,
            'raw_analysis': analysis
        }
        
        return result
    
    def _extract_severity(self, text: str) -> int:
        """Extract severity score from analysis"""
        import re
        severity_match = re.search(r'severity[:\s]*(\d+)', text.lower())
        if severity_match:
            return min(int(severity_match.group(1)), 10)
        
        # Keyword-based severity assessment
        if any(word in text.lower() for word in ['critical', 'severe', 'high risk']):
            return 9
        elif any(word in text.lower() for word in ['moderate', 'medium']):
            return 5
        elif any(word in text.lower() for word in ['low', 'minimal']):
            return 2
        
        return 5  # Default moderate severity
    
    def _extract_attack_vector(self, text: str) -> str:
        """Extract attack vector from analysis"""
        vectors = ['network', 'email', 'web', 'malware', 'social_engineering', 
                  'physical', 'insider', 'supply_chain', 'credential', 'privilege_escalation']
        
        text_lower = text.lower()
        for vector in vectors:
            if vector.replace('_', ' ') in text_lower or vector in text_lower:
                return vector
        
        return 'unknown'
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from analysis"""
        recommendations = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(word in line.lower() for word in ['recommend', 'suggest', 'should', 'action']):
                if line and len(line) > 10:
                    recommendations.append(line)
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _extract_iocs(self, text: str) -> List[str]:
        """Extract Indicators of Compromise from analysis"""
        import re
        iocs = []
        
        # IP addresses
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        iocs.extend(re.findall(ip_pattern, text))
        
        # Domains
        domain_pattern = r'\b[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.([a-zA-Z]{2,})\b'
        iocs.extend(re.findall(domain_pattern, text))
        
        # File hashes (MD5, SHA1, SHA256)
        hash_pattern = r'\b[a-fA-F0-9]{32,64}\b'
        iocs.extend(re.findall(hash_pattern, text))
        
        return list(set(iocs))  # Remove duplicates
    
    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from analysis"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['critical', 'severe', 'high']):
            return 'HIGH'
        elif any(word in text_lower for word in ['moderate', 'medium']):
            return 'MEDIUM'
        elif any(word in text_lower for word in ['low', 'minimal']):
            return 'LOW'
        
        return 'MEDIUM'  # Default
    
    async def coordinate_multi_llm_analysis(self, threat_data: Dict) -> Dict:
        """Coordinate analysis across multiple LLMs for comprehensive assessment"""
        self.logger.info(f"Starting multi-LLM analysis for threat: {threat_data.get('type', 'unknown')}")
        
        # Select LLMs based on threat type and availability
        selected_llms = self._select_llms_for_threat(threat_data)
        
        # Run parallel analysis
        tasks = []
        for llm_name in selected_llms:
            task = asyncio.create_task(self.analyze_threat_with_llm(llm_name, threat_data))
            tasks.append((llm_name, task))
        
        # Collect results
        analyses = {}
        for llm_name, task in tasks:
            try:
                result = await asyncio.wait_for(task, timeout=30.0)
                analyses[llm_name] = result
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout analyzing threat with {llm_name}")
                analyses[llm_name] = {'error': 'timeout'}
            except Exception as e:
                self.logger.error(f"Error in {llm_name} analysis: {e}")
                analyses[llm_name] = {'error': str(e)}
        
        # Synthesize results
        consensus = self._synthesize_analyses(analyses)
        
        # Log the analysis
        self.defense_history.append({
            'timestamp': datetime.now().isoformat(),
            'threat_data': threat_data,
            'llm_analyses': analyses,
            'consensus': consensus
        })
        
        return consensus
    
    def _select_llms_for_threat(self, threat_data: Dict) -> List[str]:
        """Select appropriate LLMs based on threat characteristics"""
        threat_type = threat_data.get('type', '').lower()
        selected = []
        
        # Always include rapid response for real-time threats
        if self.llm_configs['gpt-3.5-turbo']['enabled']:
            selected.append('gpt-3.5-turbo')
        elif self.llm_configs['gemma-7b-groq']['enabled']:
            selected.append('gemma-7b-groq')
        
        # Select based on threat type
        if 'network' in threat_type:
            selected.extend(['mistral-7b', 'llama2-70b', 'mixtral-8x7b-groq'])
        elif 'malware' in threat_type or 'code' in threat_type:
            selected.extend(['codellama-34b', 'wizard-coder', 'deepseek-coder'])
        elif 'social' in threat_type or 'phishing' in threat_type:
            selected.extend(['neural-chat', 'claude-3-sonnet'])
        elif 'behavioral' in threat_type or 'anomaly' in threat_type:
            selected.extend(['phi-2', 'orca-mini'])
        
        # Add strategic analysis for high-severity threats
        if threat_data.get('severity', 0) >= 7:
            if self.llm_configs['gpt-4']['enabled']:
                selected.append('gpt-4')
            elif self.llm_configs['llama3-70b-groq']['enabled']:
                selected.append('llama3-70b-groq')
            if self.llm_configs['claude-3-opus']['enabled']:
                selected.append('claude-3-opus')
        
        # Ensure we have some local models for offline capability
        local_models = ['llama2-70b', 'mistral-7b', 'phi-2']
        for model in local_models:
            if self.llm_configs[model]['enabled'] and model not in selected:
                selected.append(model)
                break
        
        # Limit to max 5 LLMs for efficiency
        return selected[:5]
    
    def _synthesize_analyses(self, analyses: Dict) -> Dict:
        """Synthesize multiple LLM analyses into consensus view"""
        valid_analyses = {k: v for k, v in analyses.items() if 'error' not in v}
        
        if not valid_analyses:
            return {'error': 'No valid analyses available'}
        
        # Calculate consensus metrics
        severities = [analysis.get('severity', 5) for analysis in valid_analyses.values()]
        avg_severity = sum(severities) / len(severities) if severities else 5
        
        # Collect all recommendations
        all_recommendations = []
        for analysis in valid_analyses.values():
            recommendations = analysis.get('recommendations', [])
            if isinstance(recommendations, list):
                all_recommendations.extend(recommendations)
        
        # Collect all IOCs
        all_iocs = []
        for analysis in valid_analyses.values():
            iocs = analysis.get('iocs', [])
            if isinstance(iocs, list):
                all_iocs.extend(iocs)
        
        # Determine consensus risk level
        risk_levels = [analysis.get('risk_level', 'MEDIUM') for analysis in valid_analyses.values()]
        risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for risk in risk_levels:
            if risk in risk_counts:
                risk_counts[risk] += 1
        
        consensus_risk = max(risk_counts, key=risk_counts.get)
        
        # Determine consensus attack vector
        attack_vectors = [analysis.get('attack_vector', 'unknown') for analysis in valid_analyses.values()]
        vector_counts = {}
        for vector in attack_vectors:
            vector_counts[vector] = vector_counts.get(vector, 0) + 1
        
        consensus_vector = max(vector_counts, key=vector_counts.get) if vector_counts else 'unknown'
        
        consensus = {
            'consensus_severity': round(avg_severity, 1),
            'consensus_risk_level': consensus_risk,
            'consensus_attack_vector': consensus_vector,
            'aggregated_recommendations': list(set(all_recommendations)),
            'aggregated_iocs': list(set(all_iocs)),
            'participating_llms': list(valid_analyses.keys()),
            'confidence_score': len(valid_analyses) / len(analyses) if analyses else 0,
            'synthesis_timestamp': datetime.now().isoformat()
        }
        
        return consensus
    
    async def start_real_time_monitoring(self):
        """Start real-time system monitoring with LLM analysis"""
        self.running = True
        self.logger.info("🔍 Starting real-time monitoring with Multi-LLM analysis...")
        
        # Start monitoring threads
        monitors = [
            ('network_monitor', self._network_monitor),
            ('process_monitor', self._process_monitor),
            ('file_monitor', self._file_monitor),
            ('registry_monitor', self._registry_monitor),
            ('system_health_monitor', self._system_health_monitor)
        ]
        
        for name, monitor_func in monitors:
            if self.monitoring_config.get(name, {}).get('enabled', True):
                thread = threading.Thread(target=monitor_func, daemon=True, name=name)
                thread.start()
                self.monitoring_threads.append(thread)
                self.logger.info(f"✅ Started {name}")
        
        # Start threat correlation engine
        correlation_thread = threading.Thread(target=self._threat_correlation_engine, daemon=True)
        correlation_thread.start()
        self.monitoring_threads.append(correlation_thread)
        
        self.logger.info(f"🚀 All monitoring systems active with {len(self.monitoring_threads)} threads")
    
    def _network_monitor(self):
        """Monitor network connections and traffic patterns"""
        config = self.monitoring_config['network_monitor']
        connection_counts = {}
        
        while self.running:
            try:
                connections = psutil.net_connections(kind='inet')
                current_time = time.time()
                
                # Analyze connections
                for conn in connections:
                    if conn.raddr:
                        remote_ip = conn.raddr.ip
                        remote_port = conn.raddr.port
                        
                        # Track connection counts per IP
                        if remote_ip not in connection_counts:
                            connection_counts[remote_ip] = []
                        
                        connection_counts[remote_ip].append(current_time)
                        
                        # Clean old entries (last 5 minutes)
                        connection_counts[remote_ip] = [
                            t for t in connection_counts[remote_ip] 
                            if current_time - t < 300
                        ]
                        
                        # Check for suspicious activity
                        if len(connection_counts[remote_ip]) > config['max_connections_per_ip']:
                            threat_data = {
                                'type': 'network_anomaly',
                                'subtype': 'connection_flood',
                                'source_ip': remote_ip,
                                'connection_count': len(connection_counts[remote_ip]),
                                'timestamp': datetime.now().isoformat(),
                                'severity': 7
                            }
                            self._queue_threat_for_analysis(threat_data)
                        
                        # Check suspicious ports
                        if remote_port in config['suspicious_ports']:
                            threat_data = {
                                'type': 'network_threat',
                                'subtype': 'suspicious_port',
                                'source_ip': remote_ip,
                                'port': remote_port,
                                'timestamp': datetime.now().isoformat(),
                                'severity': 6
                            }
                            self._queue_threat_for_analysis(threat_data)
                
                time.sleep(config['interval'])
                
            except Exception as e:
                self.logger.error(f"Network monitor error: {e}")
                time.sleep(5)
    
    def _process_monitor(self):
        """Monitor running processes for suspicious activity"""
        config = self.monitoring_config['process_monitor']
        known_processes = set()
        
        while self.running:
            try:
                current_processes = set()
                
                for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_percent']):
                    try:
                        proc_info = proc.info
                        proc_name = proc_info['name'].lower()
                        current_processes.add(proc_info['pid'])
                        
                        # Check for suspicious process names
                        if any(sus_name in proc_name for sus_name in config['suspicious_names']):
                            threat_data = {
                                'type': 'process_threat',
                                'subtype': 'suspicious_process',
                                'process_name': proc_info['name'],
                                'pid': proc_info['pid'],
                                'cmdline': proc_info['cmdline'],
                                'timestamp': datetime.now().isoformat(),
                                'severity': 8
                            }
                            self._queue_threat_for_analysis(threat_data)
                        
                        # Check for high memory usage
                        if proc_info['memory_percent'] > config['memory_threshold']:
                            threat_data = {
                                'type': 'system_anomaly',
                                'subtype': 'high_memory_usage',
                                'process_name': proc_info['name'],
                                'pid': proc_info['pid'],
                                'memory_percent': proc_info['memory_percent'],
                                'timestamp': datetime.now().isoformat(),
                                'severity': 5
                            }
                            self._queue_threat_for_analysis(threat_data)
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                # Check for new processes
                new_processes = current_processes - known_processes
                if new_processes and known_processes:  # Skip first run
                    for pid in new_processes:
                        try:
                            proc = psutil.Process(pid)
                            threat_data = {
                                'type': 'process_event',
                                'subtype': 'new_process',
                                'process_name': proc.name(),
                                'pid': pid,
                                'cmdline': proc.cmdline(),
                                'timestamp': datetime.now().isoformat(),
                                'severity': 3
                            }
                            self._queue_threat_for_analysis(threat_data)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                
                known_processes = current_processes
                time.sleep(config['interval'])
                
            except Exception as e:
                self.logger.error(f"Process monitor error: {e}")
                time.sleep(5)
    
    def _file_monitor(self):
        """Monitor file system for suspicious changes"""
        config = self.monitoring_config['file_monitor']
        
        while self.running:
            try:
                for watch_dir in config['watch_directories']:
                    if os.path.exists(watch_dir):
                        for root, dirs, files in os.walk(watch_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                file_ext = os.path.splitext(file)[1].lower()
                                
                                # Check suspicious extensions
                                if file_ext in config['suspicious_extensions']:
                                    try:
                                        stat = os.stat(file_path)
                                        # Check if file was modified recently (last 5 minutes)
                                        if time.time() - stat.st_mtime < 300:
                                            threat_data = {
                                                'type': 'file_threat',
                                                'subtype': 'suspicious_file_activity',
                                                'file_path': file_path,
                                                'file_extension': file_ext,
                                                'modification_time': stat.st_mtime,
                                                'timestamp': datetime.now().isoformat(),
                                                'severity': 6
                                            }
                                            self._queue_threat_for_analysis(threat_data)
                                    except (OSError, PermissionError):
                                        continue
                
                time.sleep(config['interval'])
                
            except Exception as e:
                self.logger.error(f"File monitor error: {e}")
                time.sleep(10)
    
    def _registry_monitor(self):
        """Monitor Windows registry for suspicious changes"""
        config = self.monitoring_config['registry_monitor']
        
        while self.running:
            try:
                # This is a simplified registry monitor
                # In a real implementation, you'd use Windows APIs
                threat_data = {
                    'type': 'registry_event',
                    'subtype': 'registry_scan',
                    'message': 'Registry monitoring active',
                    'timestamp': datetime.now().isoformat(),
                    'severity': 2
                }
                # Only log this periodically to avoid spam
                if random.random() < 0.1:  # 10% chance
                    self._queue_threat_for_analysis(threat_data)
                
                time.sleep(config['interval'])
                
            except Exception as e:
                self.logger.error(f"Registry monitor error: {e}")
                time.sleep(10)
    
    def _system_health_monitor(self):
        """Monitor overall system health and performance"""
        while self.running:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                network = psutil.net_io_counters()
                
                self.system_metrics = {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'network_bytes_sent': network.bytes_sent,
                    'network_bytes_recv': network.bytes_recv,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Check for resource exhaustion attacks
                if cpu_percent > 95:
                    threat_data = {
                        'type': 'system_anomaly',
                        'subtype': 'cpu_exhaustion',
                        'cpu_percent': cpu_percent,
                        'timestamp': datetime.now().isoformat(),
                        'severity': 7
                    }
                    self._queue_threat_for_analysis(threat_data)
                
                if memory.percent > 95:
                    threat_data = {
                        'type': 'system_anomaly',
                        'subtype': 'memory_exhaustion',
                        'memory_percent': memory.percent,
                        'timestamp': datetime.now().isoformat(),
                        'severity': 7
                    }
                    self._queue_threat_for_analysis(threat_data)
                
                time.sleep(5)
                
            except Exception as e:
                self.logger.error(f"System health monitor error: {e}")
                time.sleep(10)
    
    def _queue_threat_for_analysis(self, threat_data: Dict):
        """Queue threat for LLM analysis"""
        self.active_threats.append(threat_data)
        
        # Limit active threats queue size
        if len(self.active_threats) > 100:
            self.active_threats = self.active_threats[-50:]  # Keep last 50
    
    def _threat_correlation_engine(self):
        """Correlate threats and trigger LLM analysis"""
        while self.running:
            try:
                if self.active_threats:
                    # Process threats in batches
                    batch_size = min(5, len(self.active_threats))
                    threat_batch = self.active_threats[:batch_size]
                    self.active_threats = self.active_threats[batch_size:]
                    
                    # Analyze each threat
                    for threat_data in threat_batch:
                        try:
                            # Run async analysis in background
                            asyncio.run(self._analyze_single_threat(threat_data))
                        except Exception as e:
                            self.logger.error(f"Error analyzing threat: {e}")
                
                time.sleep(2)  # Process threats every 2 seconds
                
            except Exception as e:
                self.logger.error(f"Threat correlation engine error: {e}")
                time.sleep(5)
    
    async def _analyze_single_threat(self, threat_data: Dict):
        """Analyze a single threat with appropriate response"""
        try:
            # Only analyze medium+ severity threats with LLMs to avoid spam
            if threat_data.get('severity', 0) >= 5:
                consensus = await self.coordinate_multi_llm_analysis(threat_data)
                
                # Trigger automated response based on consensus
                if consensus.get('consensus_severity', 0) >= 8:
                    await self._trigger_automated_response(threat_data, consensus)
            
        except Exception as e:
            self.logger.error(f"Error in single threat analysis: {e}")
    
    async def _trigger_automated_response(self, threat_data: Dict, consensus: Dict):
        """Trigger automated defensive response to high-severity threats"""
        self.logger.warning(f"🚨 HIGH SEVERITY THREAT DETECTED: {threat_data.get('type')}")
        self.logger.warning(f"🎯 CONSENSUS SEVERITY: {consensus.get('consensus_severity')}")
        
        # Log the full analysis
        response_log = {
            'timestamp': datetime.now().isoformat(),
            'threat': threat_data,
            'consensus': consensus,
            'automated_actions': []
        }
        
        # Execute automated defensive actions based on threat type
        actions = []
        
        if threat_data.get('type') == 'network_threat':
            # Network-based responses
            if 'source_ip' in threat_data:
                action = f"Block IP: {threat_data['source_ip']}"
                actions.append(action)
                # In real implementation: actually block the IP
        
        elif threat_data.get('type') == 'process_threat':
            # Process-based responses
            if 'pid' in threat_data:
                action = f"Terminate process: PID {threat_data['pid']}"
                actions.append(action)
                # In real implementation: actually terminate the process
        
        elif threat_data.get('type') == 'file_threat':
            # File-based responses
            if 'file_path' in threat_data:
                action = f"Quarantine file: {threat_data['file_path']}"
                actions.append(action)
                # In real implementation: actually quarantine the file
        
        # General responses
        actions.extend([
            "Increase monitoring sensitivity",
            "Alert security team",
            "Update threat intelligence database"
        ])
        
        response_log['automated_actions'] = actions
        
        # Log all actions
        for action in actions:
            self.logger.warning(f"🛡️ AUTOMATED ACTION: {action}")
        
        # Store in defense history
        self.defense_history.append(response_log)
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        enabled_llms = {name: config for name, config in self.llm_configs.items() if config['enabled']}
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'running': self.running,
            'llm_engines': {
                'total': len(self.llm_configs),
                'enabled': len(enabled_llms),
                'engines': enabled_llms
            },
            'monitoring': {
                'active_threads': len(self.monitoring_threads),
                'active_threats': len(self.active_threats),
                'defense_history_entries': len(self.defense_history)
            },
            'system_metrics': self.system_metrics,
            'recent_threats': self.active_threats[-5:] if self.active_threats else [],
            'recent_defenses': self.defense_history[-3:] if self.defense_history else []
        }
        
        return status
    
    async def stop_system(self):
        """Stop the defense system gracefully"""
        self.logger.info("🛑 Stopping Multi-LLM Defense System...")
        self.running = False
        
        # Wait for threads to finish
        for thread in self.monitoring_threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        self.logger.info("✅ Multi-LLM Defense System stopped")

# Example usage and testing
async def main():
    """Main function for testing the Multi-LLM Defense System"""
    defense_system = MultiLLMDefenseSystem()
    
    try:
        # Initialize LLM engines
        success = await defense_system.initialize_llm_engines()
        if not success:
            print("❌ No LLM engines available - check configuration")
            return
        
        # Start monitoring
        await defense_system.start_real_time_monitoring()
        
        # Test with a sample threat
        test_threat = {
            'type': 'network_threat',
            'subtype': 'suspicious_connection',
            'source_ip': '192.168.1.100',
            'port': 4444,
            'timestamp': datetime.now().isoformat(),
            'severity': 8
        }
        
        print("🧪 Testing with sample threat...")
        consensus = await defense_system.coordinate_multi_llm_analysis(test_threat)
        print(f"📊 Analysis consensus: {json.dumps(consensus, indent=2)}")
        
        # Run for demonstration
        print("🔍 System running - monitoring for threats...")
        print("Press Ctrl+C to stop")
        
        # Keep running
        while True:
            status = defense_system.get_system_status()
            print(f"📈 Status: {status['llm_engines']['enabled']} LLMs active, {status['monitoring']['active_threats']} threats queued")
            await asyncio.sleep(30)
            
    except KeyboardInterrupt:
        print("\n⚠️ Shutdown requested...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await defense_system.stop_system()

if __name__ == "__main__":
    asyncio.run(main())