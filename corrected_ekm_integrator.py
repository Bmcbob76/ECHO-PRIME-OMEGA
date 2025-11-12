#!/usr/bin/env python3
"""
CORRECTED EKM INTEGRATION - Uses 'FullPath' column
Integrates all 3,158 EKMs from D:\ASSIMILATE ME structure
"""
import sys
import os
import shutil
from pathlib import Path
import pandas as pd

# Set UTF-8 environment
os.environ['PYTHONIOENCODING'] = 'utf-8'

def corrected_ekm_integration():
    """Run EKM integration with correct column names"""
    print("*** CORRECTED EKM INTEGRATION STARTING ***")
    print("*** Using 'FullPath' column from CSV ***")
    
    # Paths
    l9_ekm_base = Path("P:/ECHO_PRIME/MEMORY_ORCHESTRATION/L9_EKM")
    discovery_files_path = Path("P:/ECHO_PRIME")
    
    # Find CSV files
    csv_files = list(discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*.csv"))
    if not csv_files:
        print("!!! No CSV files found!")
        return False
    
    # Read CSV
    csv_file = csv_files[0]
    print(f">>> Reading: {csv_file.name}")
    
    try:
        csv_data = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip')
        print(f">>> Success: {len(csv_data)} rows")
    except:
        csv_data = pd.read_csv(csv_file, encoding='latin-1', on_bad_lines='skip')
        print(f">>> Success with latin-1: {len(csv_data)} rows")
    
    # Verify we have FullPath column
    if 'FullPath' not in csv_data.columns:
        print(f"!!! FullPath column not found! Available columns: {list(csv_data.columns)}")
        return False
    
    # Create L9_EKM structure
    categories = {
        'EKM_MODULES': [],
        'PHOENIX_EKM': [],
        'SOVEREIGN_EKM': [],
        'CORE_EKM': [],
        'GS343_EKM': [],
        'DATABASE_EKM': [],
        'CRYSTAL_EKM': []
    }
    
    for category in categories.keys():
        category_dir = l9_ekm_base / category
        category_dir.mkdir(parents=True, exist_ok=True)
        print(f">>> Created: {category}")
    
    # Process each EKM file
    total_integrated = 0
    total_missing = 0
    total_errors = 0
    
    print(f">>> Processing {len(csv_data)} EKM entries...")
    
    for idx, row in csv_data.iterrows():
        try:
            # Get full path (FullPath column)
            if pd.notna(row['FullPath']):
                source_path_str = str(row['FullPath'])
                filename = str(row['FileName'])
                
                # Convert Windows path to Path object
                source_path = Path(source_path_str)
                
                if source_path.exists():
                    # Categorize by filename
                    filename_lower = filename.lower()
                    
                    if any(term in filename_lower for term in ['phoenix', 'ekm-9000']):
                        target_category = 'PHOENIX_EKM'
                    elif any(term in filename_lower for term in ['sov-ekm', 'sovereign']):
                        target_category = 'SOVEREIGN_EKM'
                    elif any(term in filename_lower for term in ['gs343']):
                        target_category = 'GS343_EKM'
                    elif any(term in filename_lower for term in ['core', 'ekm_core']):
                        target_category = 'CORE_EKM'
                    elif any(term in filename_lower for term in ['database', 'comprehensive']):
                        target_category = 'DATABASE_EKM'
                    elif any(term in filename_lower for term in ['crystal']):
                        target_category = 'CRYSTAL_EKM'
                    else:
                        target_category = 'EKM_MODULES'
                    
                    # Set target directory
                    target_dir = l9_ekm_base / target_category
                    
                    # Create unique target path
                    target_path = target_dir / filename
                    counter = 1
                    while target_path.exists():
                        stem = Path(filename).stem
                        suffix = Path(filename).suffix
                        target_path = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    # Copy file or directory
                    try:
                        if source_path.is_file():
                            shutil.copy2(source_path, target_path)
                        elif source_path.is_dir():
                            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                        
                        total_integrated += 1
                        categories[target_category].append(filename)
                        
                        if total_integrated % 100 == 0:
                            print(f">>> Progress: {total_integrated} EKMs integrated...")
                            
                    except Exception as e:
                        total_errors += 1
                        if total_errors <= 5:  # Show first 5 errors
                            print(f"!!! Copy error for {filename}: {e}")
                        
                else:
                    total_missing += 1
                    if total_missing <= 5:  # Show first 5 missing
                        print(f"!!! Missing file: {source_path_str}")
                        
        except Exception as e:
            total_errors += 1
            if total_errors <= 5:
                print(f"!!! Row processing error {idx}: {e}")
    
    # Final results
    print(f"*** CORRECTED INTEGRATION COMPLETE ***")
    print(f">>> Total processed: {len(csv_data)} entries")
    print(f">>> Successfully integrated: {total_integrated} EKMs")
    print(f">>> Missing files: {total_missing}")
    print(f">>> Errors: {total_errors}")
    
    # Show category breakdown
    print(f"*** CATEGORY BREAKDOWN ***")
    for category, files in categories.items():
        category_dir = l9_ekm_base / category
        if category_dir.exists():
            file_count = len([f for f in category_dir.rglob('*') if f.is_file()])
            print(f">>> {category}: {file_count} files")
    
    print("*** L9_EKM MEMORY LAYER OPERATIONAL ***")
    return total_integrated > 0

if __name__ == "__main__":
    success = corrected_ekm_integration()
    if success:
        print("*** CORRECTED MISSION ACCOMPLISHED ***")
    else:
        print("!!! MISSION FAILED !!!")
