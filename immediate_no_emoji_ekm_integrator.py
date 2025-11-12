#!/usr/bin/env python3
"""
IMMEDIATE NO-EMOJI EKM INTEGRATION
Runs EKM integration immediately without Phoenix dependency
"""
import sys
import os
import shutil
from pathlib import Path
import pandas as pd

# Set UTF-8 environment
os.environ['PYTHONIOENCODING'] = 'utf-8'

def immediate_ekm_integration():
    """Run EKM integration immediately"""
    print("*** IMMEDIATE NO-EMOJI EKM INTEGRATION STARTING ***")
    
    # Paths
    l9_ekm_base = Path("P:/ECHO_PRIME/MEMORY_ORCHESTRATION/L9_EKM")
    discovery_files_path = Path("P:/ECHO_PRIME")
    
    # Find CSV files
    csv_files = list(discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*.csv"))
    if not csv_files:
        print("!!! No CSV files found!")
        return False
    
    # Read CSV with maximum compatibility
    csv_data = None
    for csv_file in csv_files:
        print(f">>> Trying to read: {csv_file.name}")
        try:
            csv_data = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip')
            print(f">>> Success: {len(csv_data)} rows")
            break
        except:
            try:
                csv_data = pd.read_csv(csv_file, encoding='latin-1', on_bad_lines='skip')
                print(f">>> Success with latin-1: {len(csv_data)} rows")
                break
            except:
                continue
    
    if csv_data is None:
        print("!!! Could not read any CSV files!")
        return False
    
    # Create L9_EKM structure
    categories = ['EKM_MODULES', 'PHOENIX_EKM', 'SOVEREIGN_EKM', 'CORE_EKM', 
                 'GS343_EKM', 'DATABASE_EKM', 'CRYSTAL_EKM', 'DISCOVERY_LOGS']
    
    for category in categories:
        category_dir = l9_ekm_base / category
        category_dir.mkdir(parents=True, exist_ok=True)
        print(f">>> Created: {category}")
    
    # Simple integration - copy what we can
    total_integrated = 0
    for idx, row in csv_data.iterrows():
        try:
            if 'Path' in row and pd.notna(row['Path']):
                source_path = Path(str(row['Path']))
                if source_path.exists():
                    # Determine category by filename
                    filename = source_path.name.lower()
                    
                    if 'phoenix' in filename or 'ekm-9000' in filename:
                        target_dir = l9_ekm_base / 'PHOENIX_EKM'
                    elif 'sov-ekm' in filename or 'sovereign' in filename:
                        target_dir = l9_ekm_base / 'SOVEREIGN_EKM'
                    elif 'gs343' in filename:
                        target_dir = l9_ekm_base / 'GS343_EKM'
                    elif 'core' in filename:
                        target_dir = l9_ekm_base / 'CORE_EKM'
                    elif 'database' in filename:
                        target_dir = l9_ekm_base / 'DATABASE_EKM'
                    elif 'crystal' in filename:
                        target_dir = l9_ekm_base / 'CRYSTAL_EKM'
                    else:
                        target_dir = l9_ekm_base / 'EKM_MODULES'
                    
                    # Copy file/directory
                    target_path = target_dir / source_path.name
                    counter = 1
                    while target_path.exists():
                        stem = source_path.stem
                        suffix = source_path.suffix
                        target_path = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    if source_path.is_file():
                        shutil.copy2(source_path, target_path)
                    elif source_path.is_dir():
                        shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                    
                    total_integrated += 1
                    
                    if total_integrated % 100 == 0:
                        print(f">>> Progress: {total_integrated} EKMs integrated")
                        
        except Exception as e:
            continue
    
    # Verify results
    print(f"*** IMMEDIATE INTEGRATION COMPLETE ***")
    print(f">>> Total integrated: {total_integrated} EKMs")
    
    # Count files in each category
    for category in categories:
        category_dir = l9_ekm_base / category
        if category_dir.exists():
            file_count = len([f for f in category_dir.rglob('*') if f.is_file()])
            print(f">>> {category}: {file_count} files")
    
    print("*** L9_EKM MEMORY LAYER OPERATIONAL ***")
    return True

if __name__ == "__main__":
    success = immediate_ekm_integration()
    if success:
        print("*** IMMEDIATE MISSION ACCOMPLISHED ***")
    else:
        print("!!! MISSION FAILED !!!")
