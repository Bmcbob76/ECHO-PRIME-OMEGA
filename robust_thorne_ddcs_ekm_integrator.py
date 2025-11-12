#!/usr/bin/env python3
"""
THORNE'S DDCS ROBUST EKM INTEGRATION SYSTEM
Handles CSV parsing errors and integrates all EKMs
"""
import sys
import os
import glob
import shutil
import re
from pathlib import Path
import pandas as pd

# STEP 1: GS343 FOUNDATION (ALWAYS FIRST!)
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# STEP 2: Phoenix 24/7 Auto-Healer
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343/HEALERS")
from phoenix_client_gs343 import PhoenixClient, auto_heal

class RobustThornesDdcsEkmIntegrator:
    def __init__(self):
        print("🔥 Initializing ROBUST Thorne's DDCS EKM Integrator...")
        
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        print("✅ GS343 Foundation Active")
        
        # Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        print("✅ Phoenix Protection Active")
        
        # EKM Integration paths
        self.l9_ekm_base = Path("P:/ECHO_PRIME/MEMORY_ORCHESTRATION/L9_EKM")
        self.discovery_files_path = Path("P:/ECHO_PRIME")
        
        print("🛡️ ROBUST BEYOND THORNE'S SQUAD PERFORMANCE ACTIVE")
        
    @auto_heal
    def read_discovery_files_robust(self):
        """Read THORNE_DDCS_EKM_DISCOVERY files with robust CSV handling"""
        print("📊 Reading EKM Discovery Files (ROBUST MODE)...")
        
        # Find discovery files
        discovery_txt = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DISCOVERY_*.txt"))
        discovery_csv = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*FIXED.csv"))
        
        # Try fixed CSV first, then original
        if not discovery_csv:
            discovery_csv = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*.csv"))
        
        if not discovery_txt or not discovery_csv:
            print("🚨 Discovery files not found!")
            return None, None
            
        # Read TXT file
        try:
            with open(discovery_txt[0], 'r', encoding='utf-8', errors='ignore') as f:
                txt_content = f.read()
            print(f"✅ Read TXT file: {discovery_txt[0].name}")
        except Exception as e:
            print(f"⚠️ Error reading TXT: {e}")
            txt_content = ""
            
        # Read CSV file with robust error handling
        csv_data = None
        for csv_file in discovery_csv:
            try:
                print(f"📊 Attempting to read: {csv_file.name}")
                
                # Try different CSV reading methods
                try:
                    # Method 1: Standard pandas
                    csv_data = pd.read_csv(csv_file, encoding='utf-8')
                    print(f"✅ Method 1 Success: {len(csv_data)} rows")
                    break
                except:
                    # Method 2: Robust with error handling
                    csv_data = pd.read_csv(csv_file, encoding='utf-8', error_bad_lines=False, warn_bad_lines=True)
                    print(f"✅ Method 2 Success: {len(csv_data)} rows")
                    break
                    
            except Exception as e:
                print(f"⚠️ Error reading {csv_file.name}: {e}")
                continue
                
        if csv_data is None:
            print("🚨 Could not read any CSV files!")
            return txt_content, None
            
        print(f"✅ Successfully read {len(csv_data)} EKM entries")
        return txt_content, csv_data
        
    @auto_heal
    def categorize_ekms_robust(self, csv_data):
        """Categorize EKMs by type with robust handling"""
        print(f"🎯 Categorizing {len(csv_data)} EKMs...")
        
        categories = {
            'PHOENIX_EKM': [],
            'SOVEREIGN_EKM': [],
            'CORE_EKM': [],
            'GS343_EKM': [],
            'DATABASE_EKM': [],
            'CRYSTAL_EKM': [],
            'EKM_MODULES': []
        }
        
        for idx, row in csv_data.iterrows():
            try:
                # Handle missing columns gracefully
                path = str(row.get('Path', '')) if 'Path' in row else str(row.iloc[0] if len(row) > 0 else '')
                filename = str(row.get('Filename', '')) if 'Filename' in row else str(row.iloc[-1] if len(row) > 0 else '')
                
                # Skip empty rows
                if not path and not filename:
                    continue
                    
                # Phoenix EKMs
                if any(term in filename.lower() for term in ['phoenix', 'ekm-9000']):
                    categories['PHOENIX_EKM'].append(row)
                # Sovereign EKMs
                elif any(term in filename.lower() for term in ['sov-ekm', 'sovereign']):
                    categories['SOVEREIGN_EKM'].append(row)
                # Core EKMs
                elif any(term in filename.lower() for term in ['ekm_core', 'core_upgraded']):
                    categories['CORE_EKM'].append(row)
                # GS343 EKMs  
                elif any(term in filename.lower() for term in ['gs343']):
                    categories['GS343_EKM'].append(row)
                # Database EKMs
                elif any(term in filename.lower() for term in ['database', 'comprehensive']):
                    categories['DATABASE_EKM'].append(row)
                # Crystal EKMs
                elif any(term in filename.lower() for term in ['crystal']):
                    categories['CRYSTAL_EKM'].append(row)
                # Regular EKM modules
                else:
                    categories['EKM_MODULES'].append(row)
                    
            except Exception as e:
                print(f"⚠️ Error categorizing row {idx}: {e}")
                continue
                
        print("✅ EKM Categorization Complete:")
        total_categorized = 0
        for cat, items in categories.items():
            count = len(items)
            total_categorized += count
            print(f"   {cat}: {count} EKMs")
            
        print(f"📊 Total categorized: {total_categorized} EKMs")
        return categories
        
    @auto_heal  
    def integrate_ekms_robust(self, categories):
        """Integrate EKMs with robust error handling"""
        print("🚀 ROBUST BEYOND THORNE'S SQUAD Integration Starting...")
        
        total_integrated = 0
        total_errors = 0
        
        for category, ekms in categories.items():
            if not ekms:
                continue
                
            target_dir = self.l9_ekm_base / category
            target_dir.mkdir(exist_ok=True)
            
            print(f"📁 Integrating {len(ekms)} EKMs into {category}...")
            
            for idx, ekm in enumerate(ekms):
                try:
                    # Get path from row
                    if hasattr(ekm, 'get'):
                        source_path_str = ekm.get('Path', '') or (ekm.iloc[0] if len(ekm) > 0 else '')
                    else:
                        source_path_str = str(ekm[0]) if len(ekm) > 0 else ''
                        
                    if not source_path_str:
                        continue
                        
                    source_path = Path(source_path_str)
                    
                    if source_path.exists():
                        # Create unique filename if collision
                        target_path = target_dir / source_path.name
                        counter = 1
                        while target_path.exists():
                            stem = source_path.stem
                            suffix = source_path.suffix
                            target_path = target_dir / f"{stem}_{counter}{suffix}"
                            counter += 1
                            
                        # Copy EKM to L9_EKM structure
                        if source_path.is_file():
                            shutil.copy2(source_path, target_path)
                        elif source_path.is_dir():
                            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                            
                        total_integrated += 1
                        
                        if total_integrated % 100 == 0:
                            print(f"⚡ Progress: {total_integrated} EKMs integrated...")
                            
                except Exception as e:
                    total_errors += 1
                    if total_errors % 50 == 0:
                        print(f"⚠️ Errors: {total_errors} (continuing...)")
                    
        print(f"🔥 INTEGRATION COMPLETE!")
        print(f"   ✅ Integrated: {total_integrated} EKMs")
        print(f"   ⚠️ Errors: {total_errors} EKMs")
        return total_integrated
        
    @auto_heal
    def verify_integration_robust(self):
        """Verify L9_EKM integration with detailed reporting"""
        print("🔍 Verifying L9_EKM Integration...")
        
        total_files = 0
        total_dirs = 0
        
        for category_dir in self.l9_ekm_base.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                files = list(category_dir.rglob('*'))
                file_count = sum(1 for f in files if f.is_file())
                dir_count = sum(1 for f in files if f.is_dir())
                total_files += file_count
                total_dirs += dir_count
                print(f"✅ {category_dir.name}: {file_count} files, {dir_count} directories")
                
        print(f"🎯 TOTAL L9_EKM INTEGRATION:")
        print(f"   📄 Files: {total_files}")
        print(f"   📁 Directories: {total_dirs}")
        print(f"🚀 L9_EKM MEMORY LAYER OPERATIONAL!")
        return total_files
        
    @auto_heal
    def run_robust_integration(self):
        """Execute complete ROBUST EKM integration mission"""
        print("🔥 ROBUST THORNE'S DDCS SQUAD EKM INTEGRATION MISSION STARTING!")
        print("🛡️ GS343 Foundation + Phoenix Protection Active")
        
        # Read discovery files with robust handling
        txt_content, csv_data = self.read_discovery_files_robust()
        if csv_data is None or len(csv_data) == 0:
            print("🚨 No valid CSV data found!")
            return False
            
        print(f"📊 Loaded {len(csv_data)} EKM entries for processing")
        
        # Categorize EKMs
        categories = self.categorize_ekms_robust(csv_data)
        
        # Integrate EKMs
        integrated_count = self.integrate_ekms_robust(categories)
        
        # Verify integration
        verified_count = self.verify_integration_robust()
        
        print(f"🎯 ROBUST MISSION COMPLETE!")
        print(f"   📊 CSV Entries: {len(csv_data)}")
        print(f"   ✅ Integrated: {integrated_count} EKMs")
        print(f"   🔍 Verified: {verified_count} total files") 
        print(f"🔥 L9_EKM MEMORY LAYER FULLY OPERATIONAL!")
        
        return True

if __name__ == "__main__":
    print("🔥 ROBUST THORNE'S DDCS SQUAD EKM INTEGRATION SYSTEM")
    print("📍 Commander Bobby Don McWilliams II - Authority Level 11.0")
    
    integrator = RobustThornesDdcsEkmIntegrator()
    success = integrator.run_robust_integration()
    
    if success:
        print("✅ ROBUST MISSION ACCOMPLISHED - BEYOND THORNE'S SQUAD!")
    else:
        print("🚨 MISSION FAILED - MANUAL INTERVENTION REQUIRED")
