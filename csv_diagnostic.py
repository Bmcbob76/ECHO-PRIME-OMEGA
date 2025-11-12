#!/usr/bin/env python3
"""
CSV DIAGNOSTIC TOOL
Diagnose why 0 EKMs were integrated from the CSV
"""
import pandas as pd
from pathlib import Path

def diagnose_csv():
    print("*** CSV DIAGNOSTIC TOOL ***")
    
    # Find CSV file
    discovery_files_path = Path("P:/ECHO_PRIME")
    csv_files = list(discovery_files_path.glob("THORNE_DDCS_EKM_DATABASE_*.csv"))
    
    if not csv_files:
        print("!!! No CSV files found!")
        return
    
    csv_file = csv_files[0]
    print(f">>> Analyzing: {csv_file.name}")
    
    # Read CSV
    try:
        csv_data = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip')
        print(f">>> Loaded {len(csv_data)} rows")
    except:
        csv_data = pd.read_csv(csv_file, encoding='latin-1', on_bad_lines='skip')
        print(f">>> Loaded {len(csv_data)} rows (latin-1)")
    
    # Examine structure
    print(f">>> Columns: {list(csv_data.columns)}")
    print(f">>> Data types: {csv_data.dtypes.to_dict()}")
    
    # Show first 5 rows
    print(">>> First 5 rows:")
    for i in range(min(5, len(csv_data))):
        print(f"   Row {i}: {dict(csv_data.iloc[i])}")
    
    # Check Path column specifically
    if 'Path' in csv_data.columns:
        path_col = csv_data['Path']
        print(f">>> Path column analysis:")
        print(f"   Non-null paths: {path_col.notna().sum()}")
        print(f"   Null paths: {path_col.isna().sum()}")
        
        # Show first 10 non-null paths
        valid_paths = path_col.dropna().head(10)
        print(f">>> First 10 valid paths:")
        for i, path in enumerate(valid_paths):
            path_obj = Path(str(path))
            exists = path_obj.exists() if path_obj else False
            print(f"   {i+1}: {path} (Exists: {exists})")
    
    # Check if files actually exist
    existing_count = 0
    missing_count = 0
    
    for idx, row in csv_data.iterrows():
        if 'Path' in row and pd.notna(row['Path']):
            path_str = str(row['Path'])
            if Path(path_str).exists():
                existing_count += 1
            else:
                missing_count += 1
                if missing_count <= 5:  # Show first 5 missing
                    print(f"   Missing: {path_str}")
    
    print(f">>> File existence check:")
    print(f"   Existing files: {existing_count}")
    print(f"   Missing files: {missing_count}")
    
    return csv_data

if __name__ == "__main__":
    csv_data = diagnose_csv()
