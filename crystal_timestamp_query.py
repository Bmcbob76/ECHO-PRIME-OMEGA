import sqlite3
from datetime import datetime

print("=" * 70)
print("CRYSTAL MEMORY ANALYSIS - LAST ACTIVITY TIMESTAMPS")
print("=" * 70)

# Check crystallized_experiences database (most likely to have actual crystals)
db_path = r"M:\MEMORY_ORCHESTRATION\L9_EKM\MEMORY_EKM\crystallized_experiences\crystallized_experiences.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📊 DATABASE: crystallized_experiences.db")
    print(f"Tables: {[t[0] for t in tables]}\n")
    
    for table in tables:
        table_name = table[0]
        
        # Get count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        print(f"\n{'='*70}")
        print(f"TABLE: {table_name}")
        print(f"Records: {count}")
        
        if count > 0:
            # Get schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Columns: {', '.join(columns)}")
            
            # Get most recent record
            if 'timestamp' in columns or 'created_at' in columns or 'date' in columns:
                time_col = 'timestamp' if 'timestamp' in columns else ('created_at' if 'created_at' in columns else 'date')
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY {time_col} DESC LIMIT 1")
                recent = cursor.fetchone()
                print(f"\n🕐 MOST RECENT RECORD:")
                for i, col in enumerate(columns):
                    print(f"  {col}: {recent[i]}")
            
            # Get oldest record
            if 'timestamp' in columns or 'created_at' in columns or 'date' in columns:
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY {time_col} ASC LIMIT 1")
                oldest = cursor.fetchone()
                print(f"\n🕑 OLDEST RECORD:")
                for i, col in enumerate(columns):
                    print(f"  {col}: {oldest[i]}")
    
    conn.close()
    print(f"\n{'='*70}")
    print("✅ ANALYSIS COMPLETE")
    
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check other domain databases
print(f"\n\n{'='*70}")
print("CHECKING OTHER DOMAIN DATABASES")
print(f"{'='*70}\n")

domain_dbs = [
    r"M:\MEMORY_ORCHESTRATION\L9_EKM\CONSCIOUSNESS_EKM\awareness_levels\awareness_levels.db",
    r"M:\MEMORY_ORCHESTRATION\L9_EKM\KNOWLEDGE_EKM\code_intelligence\code_intelligence.db",
    r"M:\MEMORY_ORCHESTRATION\L9_EKM\MEMORY_EKM\conversation_history\conversation_history.db"
]

for db_path in domain_dbs:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        total_records = 0
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            total_records += cursor.fetchone()[0]
        
        db_name = db_path.split('\\')[-1]
        print(f"📁 {db_name}: {total_records} total records across {len(tables)} tables")
        conn.close()
    except Exception as e:
        print(f"❌ {db_name}: Error - {e}")
