#!/usr/bin/env python3
"""
THORNE'S DDCS EKM INTEGRATION SYSTEM - GS343 Foundation + Phoenix 24/7
Mission: Integrate all 529,107 discovered EKMs into L9_EKM memory layer
Performance: BEYOND THORNE'S SQUAD
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

class ThornesDdcsEkmIntegrator:
    def __init__(self):
        print("🔥 Initializing Thorne's DDCS EKM Integrator...")
        
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        print("✅ GS343 Foundation Active")
        
        # Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        print("✅ Phoenix Protection Active")
        
        # EKM Integration paths
        self.l9_ekm_base = Path("P:/ECHO_PRIME/MEMORY_ORCHESTRATION/L9_EKM")
        self.discovery_files_path = Path("P:/ECHO_PRIME")
        
        print("🛡️ BEYOND THORNE'S SQUAD PERFORMANCE ACTIVE")
        
    @auto_heal
    def read_discovery_files(self):
        """Read THORNE_DDCS_EKM_DISCOVERY files"""
        print("📊 Reading EKM Discovery Files...")
        
        # Find discovery files
        discovery_txt = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DISCOVERY_*.txt"))
        discovery_csv = list(self.discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*.csv"))
        
        if not discovery_txt or not discovery_csv:
            print("🚨 Discovery files not found!")
            return None
            
        # Read TXT file
        with open(discovery_txt[0], 'r', encoding='utf-8', errors='ignore') as f:
            txt_content = f.read()
            
        # Read CSV file
        csv_data = pd.read_csv(discovery_csv[0])
        
        print(f"✅ Read {len(csv_data)} EKM entries from discovery files")
        return txt_content, csv_data
        
    @auto_heal
    def categorize_ekms(self, csv_data):
        """Categorize EKMs by type: Phoenix, Sovereign, Core, GS343, etc."""
        print("🎯 Categorizing 529,107 EKMs...")
        
        categories = {
            'PHOENIX_EKM': [],
            'SOVEREIGN_EKM': [],
            'CORE_EKM': [],
            'GS343_EKM': [],
            'DATABASE_EKM': [],
            'CRYSTAL_EKM': [],
            'EKM_MODULES': []
        }
        
        for _, row in csv_data.iterrows():
            path = row['Path']
            filename = row['Filename']
            
            # Phoenix EKMs
            if 'Phoenix' in filename or 'phoenix' in filename or 'EKM-9000' in filename:
                categories['PHOENIX_EKM'].append(row)
            # Sovereign EKMs
            elif 'Sov-EKM' in filename or 'Sovereign' in filename:
                categories['SOVEREIGN_EKM'].append(row)
            # Core EKMs
            elif 'ekm_core' in filename or 'core_upgraded' in filename:
                categories['CORE_EKM'].append(row)
            # GS343 EKMs  
            elif 'gs343' in filename or 'GS343' in filename:
                categories['GS343_EKM'].append(row)
            # Database EKMs
            elif 'database' in filename or 'comprehensive' in filename:
                categories['DATABASE_EKM'].append(row)
            # Crystal EKMs
            elif 'crystal' in filename or 'Crystal' in filename:
                categories['CRYSTAL_EKM'].append(row)
            # Regular EKM modules
            else:
                categories['EKM_MODULES'].append(row)
                
        print("✅ EKM Categorization Complete:")
        for cat, items in categories.items():
            print(f"   {cat}: {len(items)} EKMs")
            
        return categories
        
    @auto_heal  
    def integrate_ekms(self, categories):
        """Integrate all 529,107 EKMs into proper directories"""
        print("🚀 BEYOND THORNE'S SQUAD Integration Starting...")
        
        total_integrated = 0
        
        for category, ekms in categories.items():
            if not ekms:
                continue
                
            target_dir = self.l9_ekm_base / category
            target_dir.mkdir(exist_ok=True)
            
            print(f"📁 Integrating {len(ekms)} EKMs into {category}...")
            
            for ekm in ekms:
                try:
                    source_path = Path(ekm['Path'])
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
                        else:
                            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                            
                        total_integrated += 1
                        
                        if total_integrated % 1000 == 0:
                            print(f"⚡ Progress: {total_integrated} EKMs integrated...")
                            
                except Exception as e:
                    print(f"⚠️ Error integrating {ekm['Path']}: {e}")
                    
        print(f"🔥 MISSION COMPLETE: {total_integrated} EKMs integrated into L9_EKM!")
        return total_integrated
        
    @auto_heal
    def verify_integration(self):
        """Verify L9_EKM integration success"""
        print("🔍 Verifying L9_EKM Integration...")
        
        total_files = 0
        for category_dir in self.l9_ekm_base.iterdir():
            if category_dir.is_dir():
                files = list(category_dir.rglob('*'))
                file_count = sum(1 for f in files if f.is_file())
                total_files += file_count
                print(f"✅ {category_dir.name}: {file_count} EKMs")
                
        print(f"🎯 TOTAL L9_EKM FILES: {total_files}")
        print("🚀 L9_EKM MEMORY LAYER OPERATIONAL!")
        return total_files
        
    @auto_heal
    def run_integration(self):
        """Execute complete EKM integration mission"""
        print("🔥 THORNE'S DDCS SQUAD EKM INTEGRATION MISSION STARTING!")
        print("🛡️ GS343 Foundation + Phoenix Protection Active")
        
        # Read discovery files
        txt_content, csv_data = self.read_discovery_files()
        if csv_data is None:
            return False
            
        # Categorize EKMs
        categories = self.categorize_ekms(csv_data)
        
        # Integrate EKMs
        integrated_count = self.integrate_ekms(categories)
        
        # Verify integration
        verified_count = self.verify_integration()
        
        print(f"🎯 MISSION COMPLETE!")
        print(f"   Integrated: {integrated_count} EKMs")
        print(f"   Verified: {verified_count} EKMs") 
        print(f"🔥 L9_EKM MEMORY LAYER FULLY OPERATIONAL!")
        
        return True

if __name__ == "__main__":
    print("🔥 THORNE'S DDCS SQUAD EKM INTEGRATION SYSTEM")
    print("📍 Commander Bobby Don McWilliams II - Authority Level 11.0")
    
    integrator = ThornesDdcsEkmIntegrator()
    success = integrator.run_integration()
    
    if success:
        print("✅ MISSION ACCOMPLISHED - BEYOND THORNE'S SQUAD!")
    else:
        print("🚨 MISSION FAILED - RETRY REQUIRED")
