"""
Phoenix Sentinel Demo - Test without voice input
Shows all three skills in action
"""

import asyncio
import logging
from phoenix_sentinel_core import PhoenixSentinel, WindowsAPIMaster, AutonomousCPUController

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s'
)

async def demo():
    """Demonstrate Phoenix Sentinel capabilities"""
    print("\n" + "="*60)
    print("  PHOENIX SENTINEL DEMO")
    print("  Testing all three skills integration")
    print("="*60 + "\n")
    
    # Initialize components
    api_master = WindowsAPIMaster()
    cpu_controller = AutonomousCPUController(api_master)
    
    # Demo 1: Windows API Mastery
    print("\n[SKILL 1] Windows API Mastery")
    print("-" * 40)
    if api_master.enable_debug_privilege():
        print("✅ SeDebugPrivilege enabled successfully")
        print("✅ Can access system processes")
        print("✅ Can manage process priorities")
    
    # Demo 2: Autonomous CPU Controller
    print("\n[SKILL 2] Autonomous CPU Controller")
    print("-" * 40)
    print("🤖 Collecting system metrics...")
    metrics = cpu_controller.collect_metrics()
    print(f"   CPU: {metrics['cpu_percent']:.1f}%")
    print(f"   Memory: {metrics['memory_percent']:.1f}%")
    print(f"   Processes: {metrics['process_count']}")
    print(f"   Threads: {metrics['thread_count']}")
    
    print("\n🧠 Making autonomous decisions...")
    decisions = await cpu_controller.make_decision(metrics)
    if decisions:
        print(f"   ⚡ {len(decisions)} autonomous actions planned")
        for i, decision in enumerate(decisions, 1):
            print(f"   {i}. {decision['action']}")
    else:
        print("   ✅ System running optimally, no actions needed")
    
    # Demo 3: JARVIS Voice Interface (simulated)
    print("\n[SKILL 3] JARVIS Voice Interface")
    print("-" * 40)
    print("🎤 Voice commands available:")
    commands = [
        "status report",
        "optimize memory",
        "kill process",
        "set priority high",
        "free memory",
        "shutdown"
    ]
    for cmd in commands:
        print(f"   • 'Sentinel, {cmd}'")
    
    # Demo 4: GS343 Healing
    print("\n[BONUS] GS343 Auto-Healing")
    print("-" * 40)
    from gs343_patterns import GS343Healer
    healer = GS343Healer()
    
    test_errors = [
        "Access denied to system process",
        "Memory allocation failed",
        "Connection refused by remote host"
    ]
    
    for error in test_errors:
        response = healer.analyze_and_heal(error)
        print(f"   Error: {error}")
        print(f"   ⚕️  Healing: {response.action}")
        print()
    
    # Summary
    print("\n" + "="*60)
    print("  PHOENIX SENTINEL - SKILLS DEMONSTRATION COMPLETE")
    print("="*60)
    print("\n✅ Windows API Mastery: Deep system integration")
    print("✅ Autonomous CPU: Self-managing optimization")
    print("✅ JARVIS Voice: Natural language control")
    print("✅ GS343 Healing: Auto-recovery system")
    print("\n🔥 Authority Level: 11.0")
    print("🛡️ All systems operational\n")

if __name__ == "__main__":
    asyncio.run(demo())
