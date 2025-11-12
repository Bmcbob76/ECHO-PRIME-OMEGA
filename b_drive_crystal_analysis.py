import os
import json
from datetime import datetime
from pathlib import Path

base_path = Path(r"B:\Videos backup\ECHO_X_CRYSTALS")

print("=" * 70)
print("CRYSTAL MEMORY ARCHIVE ANALYSIS")
print("=" * 70)

# Count files by directory
directories = {
    "01_ACTIVE_CRYSTALS": 0,
    "02_COMPRESSED_CRYSTALS": 0,
    "03_ARCHIVED_BY_DATE": 0,
    "04_BACKUP_ORIGINALS": 0,
    "BATCH_01": 0,
    "BATCH_02": 0,
    "BATCH_03": 0,
}

total_size = 0
total_files = 0

for root, dirs, files in os.walk(base_path):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            size = os.path.getsize(file_path)
            total_size += size
            total_files += 1
        except:
            pass

print(f"\nTotal Files: {total_files:,}")
print(f"Total Size: {total_size / (1024**3):.2f} GB ({total_size / (1024**2):.2f} MB)")

# Count JSON crystals
json_files = list(base_path.rglob("*.json"))
print(f"\nJSON Crystals: {len(json_files):,}")

# Count DB files
db_files = list(base_path.rglob("*.db"))
print(f"Database Files: {len(db_files)}")

# Get recent crystals
active_crystals = sorted(
    (base_path / "01_ACTIVE_CRYSTALS").glob("*.json"),
    key=lambda x: x.stat().st_mtime,
    reverse=True
)[:5]

print(f"\n{'='*70}")
print("MOST RECENT 5 CRYSTALS")
print(f"{'='*70}")

for crystal in active_crystals:
    mtime = datetime.fromtimestamp(crystal.stat().st_mtime)
    size = crystal.stat().st_size
    print(f"\n{crystal.name}")
    print(f"  Last Modified: {mtime}")
    print(f"  Size: {size:,} bytes")
    
    # Try to read first few lines
    try:
        with open(crystal, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                print(f"  Keys: {list(data.keys())[:5]}")
    except:
        pass

print(f"\n{'='*70}")
print("DATABASE FILES")
print(f"{'='*70}")

for db in db_files:
    size = db.stat().st_size
    mtime = datetime.fromtimestamp(db.stat().st_mtime)
    print(f"\n{db.name}")
    print(f"  Size: {size:,} bytes ({size/1024:.1f} KB)")
    print(f"  Last Modified: {mtime}")
