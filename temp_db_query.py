import sqlite3
import os
from datetime import datetime

# Connect to main EKM database
db_path = r"M:\MEMORY_ORCHESTRATION\L9_EKM\ekm_training.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("EKM TRAINING DATABASE ANALYSIS")
print("=" * 60)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nTables found: {len(tables)}")
for table in tables:
    print(f"  - {table[0]}")

# For each table, get row count and sample data
print("\n" + "=" * 60)
print("TABLE CONTENTS")
print("=" * 60)

for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"\n{table_name}: {count} records")
    
    # Get schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"  Columns: {', '.join([col[1] for col in columns])}")
    
    # Get recent records if any exist
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        samples = cursor.fetchall()
        print(f"  Sample records: {len(samples)}")

conn.close()

print("\n" + "=" * 60)
print("DATABASE SCAN COMPLETE")
print("=" * 60)
