import os
from pathlib import Path

print("=" * 70)
print("B: DRIVE CRYSTAL MEMORY SCAN")
print("=" * 70)

base_path = Path(r"B:\Videos backup\ECHO_MEMORY_V2")

directories_to_check = [
    base_path / "L3_CRYSTALS" / "active",
    base_path / "L3_CRYSTALS" / "archive",
    base_path / "L3_CRYSTALS" / "overflow",
    base_path / "CRYSTAL_OVERFLOW",
    base_path / "L4_SQLITE",
    base_path / "L5_COLD",
    base_path / "L6_COLD",
    base_path / "L7_INFLUX",
    base_path / "L8_QUANTUM",
    base_path / "ARCHIVE",
    base_path / "BACKUP"
]

total_files = 0
total_size = 0
results = []

for directory in directories_to_check:
    if directory.exists():
        file_count = 0
        dir_size = 0
        
        for item in directory.rglob('*'):
            if item.is_file():
                file_count += 1
                dir_size += item.stat().st_size
        
        total_files += file_count
        total_size += dir_size
        
        results.append({
            'path': str(directory.relative_to(base_path)),
            'files': file_count,
            'size_mb': dir_size / (1024 * 1024)
        })
    else:
        results.append({
            'path': str(directory.relative_to(base_path)),
            'files': 0,
            'size_mb': 0,
            'status': 'NOT FOUND'
        })

# Print results
for result in results:
    status = result.get('status', '')
    print(f"\n📁 {result['path']}")
    print(f"   Files: {result['files']}")
    print(f"   Size: {result['size_mb']:.2f} MB")
    if status:
        print(f"   Status: {status}")

print("\n" + "=" * 70)
print(f"TOTAL FILES: {total_files}")
print(f"TOTAL SIZE: {total_size / (1024 * 1024):.2f} MB ({total_size / (1024 * 1024 * 1024):.2f} GB)")
print("=" * 70)

# Look for specific crystal file types
print("\n" + "=" * 70)
print("SEARCHING FOR CRYSTAL FILES")
print("=" * 70)

crystal_extensions = ['.json', '.db', '.crystal', '.mem', '.sqlite', '.pkl']
crystal_files = []

for ext in crystal_extensions:
    for file in base_path.rglob(f'*{ext}'):
        crystal_files.append({
            'name': file.name,
            'path': str(file.relative_to(base_path)),
            'size': file.stat().st_size,
            'modified': file.stat().st_mtime
        })

if crystal_files:
    # Sort by modified time
    crystal_files.sort(key=lambda x: x['modified'], reverse=True)
    
    print(f"\nFound {len(crystal_files)} potential crystal files:")
    print(f"\nMost recent 20:")
    for i, cf in enumerate(crystal_files[:20], 1):
        from datetime import datetime
        mod_time = datetime.fromtimestamp(cf['modified']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{i}. {cf['name']}")
        print(f"   Path: {cf['path']}")
        print(f"   Size: {cf['size'] / 1024:.2f} KB")
        print(f"   Modified: {mod_time}")
else:
    print("\n❌ NO CRYSTAL FILES FOUND")

print("\n" + "=" * 70)
