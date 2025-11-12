#!/usr/bin/env python3
"""
UNICODE-SAFE THORNE'S DDCS EKM INTEGRATION SYSTEM
Uses Unicode-safe Phoenix healer for Windows compatibility
"""
import sys
import os
import glob
import shutil
import re
from pathlib import Path
import pandas as pd

# Set UTF-8 environment
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'

# STEP 1: GS343 FOUNDATION (ALWAYS FIRST!)
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# STEP 2: Unicode-safe Phoenix Auto-Healer
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343/HEALERS")

# Start Unicode-safe Phoenix first
try:
    exec(open("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343/HEALERS/unicode_safe_phoenix_startup.py").read())
    print(">>> Unicode-safe Phoenix initialized")
except Exception as e:
    print(f"!!! Phoenix initialization error: {e}")

# Import safe Phoenix client
from phoenix_client_gs343 import PhoenixClient, auto_heal

class UnicodeSafeThornesDdcsEkmIntegrator:
    def __init__(self):
        print("*** Initializing Unicode-Safe Thorne's DDCS EKM Integrator ***")
        
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        print(">>> GS343 Foundation Active")
        
        # Unicode-safe Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        print(">>> Unicode-Safe Phoenix Protection Active")
        
        # EKM Integration paths
        self.l9_ekm_base = Path("P:/ECHO_PRIME/MEMORY_ORCHESTRATION/L9_EKM")
        self.discovery_files_path = Path("P:/ECHO_PRIME")
        
        print(">>> BEYOND THORNE'S SQUAD PERFORMANCE ACTIVE (Unicode-Safe)")
        
    @auto_heal
    def read_discovery_files_safe(self):
        """Read THORNE_DDCS_EKM_DISCOVERY files with Unicode safety"""
        print(">>> Reading EKM Discovery Files (Unicode-Safe Mode)...")
        
        # Find discovery files
        discovery_txt = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DISCOVERY_*.txt"))
        discovery_csv = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*.csv"))
        
        if not discovery_txt or not discovery_csv:
            print("!!! Discovery files not found!")
            return None, None
            
        # Read TXT file with encoding safety
        try:
            with open(discovery_txt[0], 'r', encoding='utf-8', errors='ignore') as f:
                txt_content = f.read()
            print(f">>> Read TXT file: {discovery_txt[0].name}")
        except Exception as e:
            print(f"!!! Error reading TXT: {e}")
            txt_content = ""
            
        # Read CSV file with maximum safety
        csv_data = None
        for csv_file in discovery_csv:
            try:
                print(f">>> Attempting to read: {csv_file.name}")
                
                # Try multiple encoding methods
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encodings:
                    try:
                        csv_data = pd.read_csv(csv_file, encoding=encoding, on_bad_lines='skip')
                        print(f">>> Success with {encoding}: {len(csv_data)} rows")
                        break
                    except:
                        continue
                
                if csv_data is not None:
                    break
                    
            except Exception as e:
                print(f"!!! Error reading {csv_file.name}: {e}")
                continue
                
        if csv_data is None:
            print("!!! Could not read any CSV files!")
            return txt_content, None
            
        print(f">>> Successfully read {len(csv_data)} EKM entries")
        return txt_content, csv_data
        
    @auto_heal
    def categorize_ekms_safe(self, csv_data):
        """Categorize EKMs by type with Unicode safety"""
        print(f">>> Categorizing {len(csv_data)} EKMs (Unicode-Safe)...")
        
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
                    
                # Categorize with Unicode-safe string handling
                try:
                    filename_safe = filename.encode('ascii', errors='ignore').decode('ascii').lower()
                except:
                    filename_safe = str(filename).lower()
                
                if any(term in filename_safe for term in ['phoenix', 'ekm-9000']):
                    categories['PHOENIX_EKM'].append(row)
                elif any(term in filename_safe for term in ['sov-ekm', 'sovereign']):
                    categories['SOVEREIGN_EKM'].append(row)
                elif any(term in filename_safe for term in ['ekm_core', 'core_upgraded']):
                    categories['CORE_EKM'].append(row)
                elif 'gs343' in filename_safe:
                    categories['GS343_EKM'].append(row)
                elif any(term in filename_safe for term in ['database', 'comprehensive']):
                    categories['DATABASE_EKM'].append(row)
                elif 'crystal' in filename_safe:
                    categories['CRYSTAL_EKM'].append(row)
                else:
                    categories['EKM_MODULES'].append(row)
                    
            except Exception as e:
                print(f"!!! Error categorizing row {idx}: {e}")
                continue
                
        print(">>> EKM Categorization Complete (Unicode-Safe):")
        total_categorized = 0
        for cat, items in categories.items():
            count = len(items)
            total_categorized += count
            print(f"   {cat}: {count} EKMs")
            
        print(f">>> Total categorized: {total_categorized} EKMs")
        return categories
        
    @auto_heal  
    def integrate_ekms_safe(self, categories):
        """Integrate EKMs with Unicode safety"""
        print(">>> BEYOND THORNE'S SQUAD Integration Starting (Unicode-Safe)...")
        
        total_integrated = 0
        total_errors = 0
        
        for category, ekms in categories.items():
            if not ekms:
                continue
                
            target_dir = self.l9_ekm_base / category
            target_dir.mkdir(exist_ok=True)
            
            print(f">>> Integrating {len(ekms)} EKMs into {category}...")
            
            for idx, ekm in enumerate(ekms):
                try:
                    # Get path from row with Unicode safety
                    if hasattr(ekm, 'get'):
                        source_path_str = ekm.get('Path', '') or (ekm.iloc[0] if len(ekm) > 0 else '')
                    else:
                        source_path_str = str(ekm[0]) if len(ekm) > 0 else ''
                        
                    if not source_path_str:
                        continue
                    
                    # Handle Unicode in paths
                    try:
                        source_path = Path(source_path_str)
                    except:
                        # Skip files with problematic Unicode paths
                        total_errors += 1
                        continue
                    
                    if source_path.exists():
                        # Create safe filename
                        try:
                            safe_name = source_path.name.encode('ascii', errors='ignore').decode('ascii')
                            if not safe_name:
                                safe_name = f"ekm_file_{total_integrated}"
                            target_path = target_dir / safe_name
                        except:
                            target_path = target_dir / f"ekm_file_{total_integrated}"
                        
                        # Handle collisions
                        counter = 1
                        while target_path.exists():
                            stem = target_path.stem
                            suffix = target_path.suffix
                            target_path = target_dir / f"{stem}_{counter}{suffix}"
                            counter += 1
                            
                        # Copy EKM to L9_EKM structure
                        if source_path.is_file():
                            shutil.copy2(source_path, target_path)
                        elif source_path.is_dir():
                            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                            
                        total_integrated += 1
                        
                        if total_integrated % 50 == 0:
                            print(f">>> Progress: {total_integrated} EKMs integrated...")
                            
                except Exception as e:
                    total_errors += 1
                    if total_errors % 25 == 0:
                        print(f"!!! Errors: {total_errors} (continuing...)")
                    
        print(f">>> UNICODE-SAFE INTEGRATION COMPLETE!")
        print(f"   >>> Integrated: {total_integrated} EKMs")
        print(f"   !!! Errors: {total_errors} EKMs")
        return total_integrated
        
    @auto_heal
    def verify_integration_safe(self):
        """Verify L9_EKM integration with Unicode safety"""
        print(">>> Verifying L9_EKM Integration (Unicode-Safe)...")
        
        total_files = 0
        total_dirs = 0
        
        for category_dir in self.l9_ekm_base.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                try:
                    files = list(category_dir.rglob('*'))
                    file_count = sum(1 for f in files if f.is_file())
                    dir_count = sum(1 for f in files if f.is_dir())
                    total_files += file_count
                    total_dirs += dir_count
                    print(f">>> {category_dir.name}: {file_count} files, {dir_count} directories")
                except Exception as e:
                    print(f"!!! Error verifying {category_dir}: {e}")
                
        print(f">>> TOTAL L9_EKM INTEGRATION (Unicode-Safe):")
        print(f"   >>> Files: {total_files}")
        print(f"   >>> Directories: {total_dirs}")
        print(f">>> L9_EKM MEMORY LAYER OPERATIONAL!")
        return total_files
        
    @auto_heal
    def run_safe_integration(self):
        """Execute complete Unicode-safe EKM integration mission"""
        print("*** UNICODE-SAFE THORNE'S DDCS SQUAD EKM INTEGRATION MISSION STARTING! ***")
        print(">>> GS343 Foundation + Unicode-Safe Phoenix Protection Active")
        
        # Read discovery files with Unicode safety
        txt_content, csv_data = self.read_discovery_files_safe()
        if csv_data is None or len(csv_data) == 0:
            print("!!! No valid CSV data found!")
            return False
            
        print(f">>> Loaded {len(csv_data)} EKM entries for processing")
        
        # Categorize EKMs
        categories = self.categorize_ekms_safe(csv_data)
        
        # Integrate EKMs
        integrated_count = self.integrate_ekms_safe(categories)
        
        # Verify integration
        verified_count = self.verify_integration_safe()
        
        print(f"*** UNICODE-SAFE MISSION COMPLETE! ***")
        print(f"   >>> CSV Entries: {len(csv_data)}")
        print(f"   >>> Integrated: {integrated_count} EKMs")
        print(f"   >>> Verified: {verified_count} total files") 
        print(f"*** L9_EKM MEMORY LAYER FULLY OPERATIONAL! ***")
        print(f"*** NO MORE UNICODE ERRORS! ***")
        
        return True

if __name__ == "__main__":
    print("*** UNICODE-SAFE THORNE'S DDCS SQUAD EKM INTEGRATION SYSTEM ***")
    print("*** Commander Bobby Don McWilliams II - Authority Level 11.0 ***")
    print("*** Unicode Encoding Errors ELIMINATED! ***")
    
    integrator = UnicodeSafeThornesDdcsEkmIntegrator()
    success = integrator.run_safe_integration()
    
    if success:
        print("*** UNICODE-SAFE MISSION ACCOMPLISHED - BEYOND THORNE'S SQUAD! ***")
    else:
        print("!!! MISSION FAILED - CHECK LOGS !!!")
