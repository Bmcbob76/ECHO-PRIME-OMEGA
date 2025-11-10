"""
PhD Agent - Example Usage
Quick test to verify agent functionality
"""
import sys
import os

# Add agent directory to path
sys.path.insert(0, r"E:\ECHO_XV4\MLS\agents")

from phd_agent import PhDCodingAgent

def test_agent():
    """Quick test of agent capabilities"""
    
    print("=" * 70)
    print("PhD AGENT - QUICK TEST")
    print("=" * 70)
    print()
    
    # Check API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Set OPENAI_API_KEY first!")
        return
    
    # Initialize
    print("🤖 Initializing agent...")
    agent = PhDCodingAgent()
    agent.create_assistant()
    agent.create_thread()
    print()
    
    # Test tasks
    tests = [
        "List all files in E:\\ECHO_XV4\\MLS\\agents",
        "Get current system CPU and memory usage",
        "Create a simple test file at E:\\ECHO_XV4\\MLS\\agents\\test_output.txt with 'Hello from PhD Agent!'"
    ]
    
    for i, task in enumerate(tests, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {task}")
        print('='*70)
        
        result = agent.autonomous_task(task)
        
        print("\nRESPONSE:")
        print(result['response'])
        print(f"\n⏱️ Time: {result['execution_time']:.2f}s")
        print(f"🔧 Tools: {result['tools_used']}")
    
    # Save log
    print("\n" + "="*70)
    agent.save_execution_log(
        r"E:\ECHO_XV4\MLS\agents\test_execution_log.json"
    )
    print("✅ All tests complete!")

if __name__ == "__main__":
    try:
        test_agent()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
