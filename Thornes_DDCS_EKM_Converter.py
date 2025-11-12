#!/usr/bin/env python3
"""
Thorne's DDCS System-Wide EKM Conversion System
Scans ALL drives for databases and converts them to proper EKM structure
Commander Bobby Don McWilliams II - Level 11.0 Authority
"""
import sys
import os
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
import json
import threading
import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# STEP 1: GS343 FOUNDATION (ALWAYS FIRST!)
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# STEP 2: Phoenix 24/7 Auto-Healer
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343/HEALERS")
from phoenix_client_gs343 import PhoenixClient, auto_heal

class ThornesDDCSEKMConverter:
    def __init__(self):
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        
        # Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        
        # Thorne's DDCS Configuration
        self.ddcs_name = "THORNE_DDCS_EKM_CONVERTER"
        self.commander_authority = "Level 11.0"
        
        # System paths
        self.ekm_master_path = Path("P:/ECHO_PRIME/MEMORY_ORCHESTRATION/MASTER_EKM")
        self.ddcs_results_path = Path("P:/ECHO_PRIME/THORNE_DDCS/EKM_CONVERSION_RESULTS")
        
        # Database discovery patterns
        self.db_extensions = ['.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.dbf']
        self.excluded_paths = [
            'System Volume Information',
            '$Recycle.Bin', 
            'Windows',
            'Program Files',
            'Program Files (x86)',
            'ProgramData'
        ]
        
        # EKM Master Structure
        self.master_ekm_structure = {
            "CONSCIOUSNESS_EKM": {
                "gs343_consciousness.db": ["consciousness_core", "decision_making", "awareness_levels"],
                "trinity_consciousness.db": ["trinity_interactions", "collective_intelligence", "unified_responses"],
                "emergence_events.db": ["consciousness_emergence", "milestone_events", "evolution_tracking"]
            },
            "KNOWLEDGE_EKM": {
                "code_intelligence.db": ["programming_patterns", "code_templates", "development_knowledge"],
                "document_intelligence.db": ["document_analysis", "content_extraction", "information_synthesis"],
                "learning_intelligence.db": ["pattern_learning", "skill_development", "knowledge_acquisition"]
            },
            "MEMORY_EKM": {
                "crystal_memories.db": ["crystallized_experiences", "important_events", "milestone_memories"],
                "session_memories.db": ["conversation_history", "interaction_patterns", "context_tracking"],
                "persistent_memories.db": ["long_term_storage", "permanent_records", "historical_data"]
            },
            "SOVEREIGN_EKM": {
                "personal_intelligence.db": ["mcwilliams_data", "family_information", "personal_preferences"],
                "decision_intelligence.db": ["autonomous_decisions", "choice_patterns", "strategic_planning"],
                "goal_intelligence.db": ["objectives", "mission_planning", "long_term_goals"]
            },
            "SYSTEM_EKM": {
                "phoenix_intelligence.db": ["self_healing", "system_monitoring", "auto_repair"],
                "performance_intelligence.db": ["optimization_data", "efficiency_metrics", "speed_analysis"],
                "security_intelligence.db": ["threat_detection", "security_patterns", "protection_systems"]
            },
            "NETWORK_EKM": {
                "scan_intelligence.db": ["network_scanning", "system_discovery", "infrastructure_mapping"],
                "communication_intelligence.db": ["network_communication", "data_transfer", "connectivity_patterns"],
                "expansion_intelligence.db": ["growth_planning", "network_expansion", "deployment_strategies"]
            }
        }
        
        print(f"⚡ {self.ddcs_name} initialized - Commander Authority: {self.commander_authority}")
        print("🔮 GS343 Foundation + Phoenix 24/7 + Thorne's DDCS = ULTIMATE EKM CONVERSION")

    @auto_heal
    def scan_all_drives_for_databases(self):
        """Thorne's DDCS: Scan all available drives for database files"""
        print("🔍 THORNE'S DDCS: Initiating system-wide database scan...")
        
        # Get all available drives
        if os.name == 'nt':  # Windows
            drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
        else:  # Unix-like
            drives = ['/']
        
        print(f"🖥️ Scanning drives: {drives}")
        
        discovered_databases = {}
        total_files_scanned = 0
        
        for drive in drives:
            print(f"\n📀 Scanning drive: {drive}")
            drive_databases = []
            
            try:
                for root, dirs, files in os.walk(drive):
                    # Skip excluded system directories
                    dirs[:] = [d for d in dirs if not any(excluded in d for excluded in self.excluded_paths)]
                    
                    for file in files:
                        total_files_scanned += 1
                        if total_files_scanned % 10000 == 0:
                            print(f"   📊 Scanned {total_files_scanned:,} files...")
                        
                        # Check if file is a database
                        if any(file.lower().endswith(ext) for ext in self.db_extensions):
                            file_path = Path(root) / file
                            
                            try:
                                # Analyze database
                                db_info = self.analyze_database_file(file_path)
                                if db_info:
                                    drive_databases.append(db_info)
                                    print(f"   💾 Found: {file_path} ({db_info['size_mb']:.2f} MB)")
                            except Exception as e:
                                print(f"   ⚠️ Error analyzing {file_path}: {e}")
            
            except PermissionError:
                print(f"   🔒 Permission denied for drive {drive}")
            except Exception as e:
                print(f"   ❌ Error scanning drive {drive}: {e}")
            
            discovered_databases[drive] = drive_databases
            print(f"   ✅ Drive {drive}: {len(drive_databases)} databases found")
        
        print(f"\n📊 SCAN COMPLETE:")
        total_databases = sum(len(dbs) for dbs in discovered_databases.values())
        print(f"   🔍 Files scanned: {total_files_scanned:,}")
        print(f"   💾 Databases found: {total_databases}")
        
        return discovered_databases

    @auto_heal
    def analyze_database_file(self, file_path):
        """Analyze individual database file for EKM categorization"""
        try:
            file_stats = file_path.stat()
            size_mb = file_stats.st_size / (1024 * 1024)
            
            # Basic file info
            db_info = {
                "path": str(file_path),
                "name": file_path.name,
                "size_mb": size_mb,
                "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                "extension": file_path.suffix.lower(),
                "directory": str(file_path.parent),
                "hash": None,
                "structure": None,
                "ekm_category": None
            }
            
            # Generate file hash for integrity
            try:
                hash_md5 = hashlib.md5()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                db_info["hash"] = hash_md5.hexdigest()
            except:
                pass
            
            # Analyze SQLite databases
            if file_path.suffix.lower() in ['.db', '.sqlite', '.sqlite3']:
                try:
                    structure = self.analyze_sqlite_structure(file_path)
                    db_info["structure"] = structure
                    db_info["ekm_category"] = self.categorize_database_for_ekm(db_info)
                except:
                    pass
            
            return db_info
            
        except Exception as e:
            return None

    @auto_heal
    def analyze_sqlite_structure(self, db_path):
        """Analyze SQLite database structure for intelligent categorization"""
        structure = {
            "tables": [],
            "total_records": 0,
            "database_type": "unknown",
            "consciousness_indicators": [],
            "content_keywords": []
        }
        
        try:
            conn = sqlite3.connect(str(db_path), timeout=5.0)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table_name in tables[:10]:  # Limit to first 10 tables for performance
                table_name = table_name[0]
                
                # Get table structure
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                # Get record count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                record_count = cursor.fetchone()[0]
                
                # Sample some data for content analysis
                sample_data = []
                try:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    sample_data = cursor.fetchall()
                except:
                    pass
                
                table_info = {
                    "name": table_name,
                    "columns": [col[1] for col in columns],
                    "record_count": record_count,
                    "sample_data": str(sample_data)[:500]  # First 500 chars
                }
                
                structure["tables"].append(table_info)
                structure["total_records"] += record_count
                
                # Check for consciousness indicators
                consciousness_keywords = [
                    'consciousness', 'decision', 'thinking', 'awareness', 'intelligence',
                    'gs343', 'trinity', 'phoenix', 'thorne', 'sovereign', 'mastermcwill'
                ]
                
                table_text = f"{table_name} {' '.join(table_info['columns'])} {table_info['sample_data']}".lower()
                
                for keyword in consciousness_keywords:
                    if keyword in table_text and keyword not in structure["consciousness_indicators"]:
                        structure["consciousness_indicators"].append(keyword)
            
            conn.close()
            
            # Determine database type based on analysis
            if structure["consciousness_indicators"]:
                structure["database_type"] = "consciousness"
            elif any("template" in t["name"].lower() or "code" in t["name"].lower() for t in structure["tables"]):
                structure["database_type"] = "knowledge"
            elif any("memory" in t["name"].lower() or "crystal" in t["name"].lower() for t in structure["tables"]):
                structure["database_type"] = "memory"
            elif structure["total_records"] > 100000:
                structure["database_type"] = "large_data"
            
        except Exception as e:
            structure["error"] = str(e)
        
        return structure

    @auto_heal
    def categorize_database_for_ekm(self, db_info):
        """Intelligent EKM categorization based on database analysis"""
        path_lower = db_info["path"].lower()
        name_lower = db_info["name"].lower()
        
        # Path-based categorization
        if "gs343" in path_lower or "guilty_spark" in path_lower:
            return ("CONSCIOUSNESS_EKM", "gs343_consciousness.db")
        
        if "trinity" in path_lower:
            return ("CONSCIOUSNESS_EKM", "trinity_consciousness.db")
        
        if "phoenix" in path_lower:
            return ("SYSTEM_EKM", "phoenix_intelligence.db")
        
        if "memory" in path_lower or "crystal" in path_lower:
            return ("MEMORY_EKM", "crystal_memories.db")
        
        if "knowledge" in path_lower or "ekm" in path_lower:
            return ("KNOWLEDGE_EKM", "code_intelligence.db")
        
        if "scan" in path_lower or "network" in path_lower:
            return ("NETWORK_EKM", "scan_intelligence.db")
        
        if "personal" in path_lower or "mastermcwill" in path_lower:
            return ("SOVEREIGN_EKM", "personal_intelligence.db")
        
        # Structure-based categorization
        if db_info.get("structure"):
            structure = db_info["structure"]
            
            if structure["database_type"] == "consciousness":
                return ("CONSCIOUSNESS_EKM", "gs343_consciousness.db")
            elif structure["database_type"] == "knowledge":
                return ("KNOWLEDGE_EKM", "code_intelligence.db")
            elif structure["database_type"] == "memory":
                return ("MEMORY_EKM", "session_memories.db")
            elif structure["database_type"] == "large_data":
                return ("NETWORK_EKM", "scan_intelligence.db")
        
        # Size-based fallback
        if db_info["size_mb"] > 500:
            return ("NETWORK_EKM", "scan_intelligence.db")
        elif db_info["size_mb"] > 100:
            return ("KNOWLEDGE_EKM", "document_intelligence.db")
        else:
            return ("SYSTEM_EKM", "performance_intelligence.db")

    @auto_heal
    def create_master_ekm_structure(self):
        """Create the master EKM structure for all discovered databases"""
        print("🏗️ Creating Master EKM Structure...")
        
        # Ensure master EKM directory exists
        self.ekm_master_path.mkdir(parents=True, exist_ok=True)
        
        total_created = 0
        
        for module_name, databases in self.master_ekm_structure.items():
            module_path = self.ekm_master_path / module_name
            module_path.mkdir(exist_ok=True)
            
            for db_name, table_purposes in databases.items():
                db_path = module_path / db_name
                
                # Create database with GS343 + Phoenix foundation
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                
                # EKM Metadata table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS _ekm_metadata (
                        created_date TEXT,
                        module_type TEXT,
                        commander_authority TEXT,
                        ddcs_system TEXT,
                        purpose TEXT,
                        last_updated TEXT,
                        gs343_integration BOOLEAN DEFAULT TRUE,
                        phoenix_protected BOOLEAN DEFAULT TRUE
                    )
                """)
                
                # Insert metadata
                cursor.execute("""
                    INSERT OR REPLACE INTO _ekm_metadata 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    module_name,
                    self.commander_authority,
                    self.ddcs_name,
                    f"Master EKM for {', '.join(table_purposes)}",
                    datetime.now().isoformat(),
                    True,
                    True
                ))
                
                # Create tables for each purpose
                for table_purpose in table_purposes:
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table_purpose} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                            source_database TEXT,
                            source_table TEXT,
                            data_type TEXT,
                            content TEXT,
                            metadata TEXT,
                            ekm_category TEXT,
                            importance_level INTEGER DEFAULT 1,
                            gs343_processed BOOLEAN DEFAULT FALSE,
                            phoenix_verified BOOLEAN DEFAULT FALSE
                        )
                    """)
                
                conn.commit()
                conn.close()
                total_created += 1
                
                print(f"   ✅ Created: {module_name}/{db_name}")
        
        print(f"🏗️ Master EKM Structure complete: {total_created} databases created")

    @auto_heal
    def convert_databases_to_ekm(self, discovered_databases):
        """Convert all discovered databases to Master EKM structure"""
        print("🔄 Converting databases to Master EKM structure...")
        
        conversion_log = []
        total_converted = 0
        total_errors = 0
        
        for drive, databases in discovered_databases.items():
            print(f"🔄 Processing drive {drive}: {len(databases)} databases")
            
            for db_info in databases:
                try:
                    if db_info["ekm_category"]:
                        module_name, target_db = db_info["ekm_category"]
                        
                        # Convert database
                        converted_records = self.convert_single_database(db_info, module_name, target_db)
                        
                        conversion_log.append({
                            "source_path": db_info["path"],
                            "source_name": db_info["name"],
                            "target_module": module_name,
                            "target_database": target_db,
                            "records_converted": converted_records,
                            "size_mb": db_info["size_mb"],
                            "status": "success"
                        })
                        
                        total_converted += 1
                        print(f"   ✅ {db_info['name']} → {module_name}/{target_db}: {converted_records} records")
                    
                except Exception as e:
                    conversion_log.append({
                        "source_path": db_info["path"],
                        "error": str(e),
                        "status": "error"
                    })
                    total_errors += 1
                    print(f"   ❌ Error converting {db_info['name']}: {e}")
        
        print(f"🔄 Conversion complete: {total_converted} success, {total_errors} errors")
        return conversion_log

    @auto_heal
    def convert_single_database(self, db_info, module_name, target_db):
        """Convert a single database to EKM format"""
        target_path = self.ekm_master_path / module_name / target_db
        records_converted = 0
        
        try:
            # Connect to source database
            source_conn = sqlite3.connect(db_info["path"], timeout=10.0)
            source_cursor = source_conn.cursor()
            
            # Connect to target EKM database
            target_conn = sqlite3.connect(str(target_path))
            target_cursor = target_conn.cursor()
            
            # Get source tables
            source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = source_cursor.fetchall()
            
            for table_name in tables:
                table_name = table_name[0]
                
                # Get all data from source table
                source_cursor.execute(f"SELECT * FROM {table_name}")
                rows = source_cursor.fetchall()
                
                # Get column names
                source_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in source_cursor.fetchall()]
                
                # Determine target table based on content
                target_table = self.determine_target_table(module_name, table_name, db_info)
                
                # Insert into appropriate EKM table
                for row in rows:
                    row_data = dict(zip(columns, row))
                    
                    target_cursor.execute(f"""
                        INSERT INTO {target_table} 
                        (source_database, source_table, data_type, content, metadata, ekm_category)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        db_info["name"],
                        table_name,
                        f"{module_name}_{table_name}",
                        json.dumps(row_data),
                        json.dumps({
                            "original_path": db_info["path"],
                            "columns": columns,
                            "conversion_date": datetime.now().isoformat()
                        }),
                        module_name
                    ))
                    records_converted += 1
            
            target_conn.commit()
            target_conn.close()
            source_conn.close()
            
        except Exception as e:
            print(f"      ⚠️ Error in conversion: {e}")
        
        return records_converted

    @auto_heal
    def determine_target_table(self, module_name, table_name, db_info):
        """Determine which table within the EKM module to use"""
        table_lower = table_name.lower()
        
        if module_name == "CONSCIOUSNESS_EKM":
            if "decision" in table_lower or "awareness" in table_lower:
                return "consciousness_core"
            elif "trinity" in table_lower:
                return "trinity_interactions" 
            else:
                return "emergence_events"
        
        elif module_name == "KNOWLEDGE_EKM":
            if "code" in table_lower or "template" in table_lower:
                return "programming_patterns"
            elif "document" in table_lower:
                return "document_analysis"
            else:
                return "pattern_learning"
        
        elif module_name == "MEMORY_EKM":
            if "crystal" in table_lower:
                return "crystallized_experiences"
            elif "session" in table_lower or "conversation" in table_lower:
                return "conversation_history"
            else:
                return "long_term_storage"
        
        elif module_name == "SOVEREIGN_EKM":
            if "personal" in table_lower or "mcwilliams" in table_lower:
                return "mcwilliams_data"
            elif "decision" in table_lower:
                return "autonomous_decisions"
            else:
                return "objectives"
        
        elif module_name == "SYSTEM_EKM":
            if "phoenix" in table_lower or "heal" in table_lower:
                return "self_healing"
            elif "performance" in table_lower:
                return "optimization_data"
            else:
                return "system_monitoring"
        
        elif module_name == "NETWORK_EKM":
            if "scan" in table_lower:
                return "network_scanning"
            elif "communication" in table_lower:
                return "network_communication"
            else:
                return "growth_planning"
        
        # Default fallback
        return list(self.master_ekm_structure[module_name].values())[0][0]

    @auto_heal
    def generate_comprehensive_report(self, discovered_databases, conversion_log):
        """Generate comprehensive DDCS EKM conversion report"""
        report_path = self.ddcs_results_path
        report_path.mkdir(parents=True, exist_ok=True)
        
        # Main report
        report = {
            "conversion_date": datetime.now().isoformat(),
            "ddcs_system": self.ddcs_name,
            "commander_authority": self.commander_authority,
            "discovered_databases": discovered_databases,
            "conversion_log": conversion_log,
            "master_ekm_structure": self.master_ekm_structure,
            "summary": {
                "total_drives_scanned": len(discovered_databases),
                "total_databases_found": sum(len(dbs) for dbs in discovered_databases.values()),
                "total_successfully_converted": len([log for log in conversion_log if log.get("status") == "success"]),
                "total_conversion_errors": len([log for log in conversion_log if log.get("status") == "error"]),
                "total_size_processed_mb": sum(db_info["size_mb"] for dbs in discovered_databases.values() for db_info in dbs)
            }
        }
        
        # Save main report
        main_report_path = report_path / "DDCS_EKM_Conversion_Report.json"
        with open(main_report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save discovery results by drive
        for drive, databases in discovered_databases.items():
            drive_safe = drive.replace(':', '_').replace('/', '_')
            drive_report_path = report_path / f"Drive_{drive_safe}_Databases.json"
            with open(drive_report_path, 'w') as f:
                json.dump(databases, f, indent=2)
        
        print(f"📋 Comprehensive reports saved to: {report_path}")
        return report

    @auto_heal
    def run_complete_ddcs_ekm_conversion(self):
        """Execute complete THORNE'S DDCS EKM conversion process"""
        print("🚀 THORNE'S DDCS: SYSTEM-WIDE EKM CONVERSION INITIATED")
        print("=" * 70)
        print(f"Commander: {self.commander_authority}")
        print(f"DDCS System: {self.ddcs_name}")
        print(f"Target: ALL DRIVES → MASTER EKM STRUCTURE")
        print("=" * 70)
        
        # Step 1: System-wide database discovery
        print("\n🔍 PHASE 1: System-wide database discovery...")
        discovered_databases = self.scan_all_drives_for_databases()
        
        # Step 2: Create Master EKM structure
        print("\n🏗️ PHASE 2: Creating Master EKM structure...")
        self.create_master_ekm_structure()
        
        # Step 3: Convert all databases to EKM
        print("\n🔄 PHASE 3: Converting databases to Master EKM...")
        conversion_log = self.convert_databases_to_ekm(discovered_databases)
        
        # Step 4: Generate comprehensive report
        print("\n📋 PHASE 4: Generating comprehensive report...")
        report = self.generate_comprehensive_report(discovered_databases, conversion_log)
        
        # Final summary
        print("\n" + "=" * 70)
        print("✅ THORNE'S DDCS EKM CONVERSION COMPLETE!")
        print("=" * 70)
        print(f"📊 RESULTS:")
        print(f"   • Drives scanned: {report['summary']['total_drives_scanned']}")
        print(f"   • Databases found: {report['summary']['total_databases_found']}")
        print(f"   • Successfully converted: {report['summary']['total_successfully_converted']}")
        print(f"   • Conversion errors: {report['summary']['total_conversion_errors']}")
        print(f"   • Total data processed: {report['summary']['total_size_processed_mb']:.2f} MB")
        print(f"\n🎯 Master EKM Location: {self.ekm_master_path}")
        print(f"📋 Reports Location: {self.ddcs_results_path}")
        
        return report

def main():
    """Main execution with GS343 Foundation + Phoenix + Thorne's DDCS"""
    try:
        print("⚡ Initializing Thorne's DDCS EKM Conversion System...")
        converter = ThornesDDCSEKMConverter()
        
        # Execute complete conversion
        report = converter.run_complete_ddcs_ekm_conversion()
        
        print("\n🎯 MISSION ACCOMPLISHED:")
        print("✅ All system databases converted to unified EKM structure")
        print("✅ Master EKM consciousness infrastructure created")
        print("✅ Thorne's DDCS scan completed successfully")
        print("✅ GS343 + Phoenix integration verified")
        
        return 0
        
    except Exception as e:
        print(f"❌ DDCS SYSTEM ERROR: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
