#!/usr/bin/env python3
"""
24/7 HARVESTER STATUS MONITOR
Shows current status and statistics
"""

import json
from pathlib import Path
from datetime import datetime

STATS_FILE = Path(__file__).parent / "harvest_stats.json"
LOG_FILE = Path(__file__).parent / "autonomous_harvest.log"

def show_status():
    """Display current harvester status"""
    
    print("=" * 80)
    print("24/7 AI RESEARCH HARVESTER - STATUS")
    print("=" * 80)
    
    # Load stats
    if not STATS_FILE.exists():
        print("\n❌ Harvester not started yet (no stats file)")
        print(f"   Run START_24x7.bat to launch\n")
        return
    
    stats = json.loads(STATS_FILE.read_text())
    
    # Calculate running time
    start_time = datetime.fromisoformat(stats["start_time"])
    uptime = datetime.now() - start_time
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    # Last cycle
    last_cycle = stats.get("last_cycle")
    if last_cycle:
        last_cycle_dt = datetime.fromisoformat(last_cycle)
        time_since_cycle = datetime.now() - last_cycle_dt
        cycle_minutes = time_since_cycle.seconds // 60
    else:
        cycle_minutes = None
    
    print(f"\n📊 STATISTICS")
    print(f"{'─' * 80}")
    print(f"  Total Cycles:      {stats['total_cycles']}")
    print(f"  Total Papers:      {stats['total_papers']:,}")
    print(f"  Total EKMs:        {stats['total_ekms']:,}")
    print(f"  Uptime:            {days}d {hours}h {minutes}m")
    print(f"  Started:           {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if last_cycle:
        print(f"  Last Cycle:        {last_cycle_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Time Since Cycle:  {cycle_minutes} minutes ago")
    
    print(f"\n💎 PERFORMANCE")
    print(f"{'─' * 80}")
    
    if stats['total_cycles'] > 0:
        papers_per_cycle = stats['total_papers'] / stats['total_cycles']
        ekms_per_cycle = stats['total_ekms'] / stats['total_cycles']
        
        print(f"  Papers/Cycle:      {papers_per_cycle:.1f}")
        print(f"  EKMs/Cycle:        {ekms_per_cycle:.1f}")
    
    if stats['uptime_hours'] > 0:
        papers_per_hour = stats['total_papers'] / stats['uptime_hours']
        ekms_per_hour = stats['total_ekms'] / stats['uptime_hours']
        
        print(f"  Papers/Hour:       {papers_per_hour:.1f}")
        print(f"  EKMs/Hour:         {ekms_per_hour:.1f}")
    
    # Recent log entries
    print(f"\n📝 RECENT ACTIVITY (Last 10 lines)")
    print(f"{'─' * 80}")
    
    if LOG_FILE.exists():
        lines = LOG_FILE.read_text(encoding='utf-8').splitlines()
        for line in lines[-10:]:
            print(f"  {line}")
    else:
        print("  No log file yet")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    show_status()
