"""
🎙️ FIND BETTER VOICE FOR GS343
Test different voice IDs to find a faster, more authoritative one
"""

import sys
sys.path.insert(0, "E:/ECHO_XV4/EPCP3O_COPILOT")

from epcp3o_voice_integrated import EPCP3OVoiceSystem
import asyncio

voice = EPCP3OVoiceSystem()
voice.initialize()

print("🎙️ TESTING DIFFERENT VOICES FOR GS343")
print("=" * 70)

# Available voices from your system
voices = {
    "GS343 (Current)": "8ATB4Ory7NkyCVRpePdw",
    "Echo": "keDMh3sQlEXKM4EQxvvi",
    "C3PO": "0UTDtgGGkpqERQn1s0YK",
    "Bree": "pzKXffibtCDxnrVO8d1U"
}

test_message = "GS343 Divine Authority System initialized - Authority Level 11 - Commander authenticated"

for name, voice_id in voices.items():
    print(f"\n🎙️ Testing {name} ({voice_id[:8]}...)")
    try:
        asyncio.run(voice.speak_c3po(test_message, voice_id=voice_id, emotion='confident'))
        input(f"   Press Enter for next voice...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("Which voice sounds BEST for GS343 authority announcements?")
print("1 = GS343 (current)")
print("2 = Echo")
print("3 = C3PO")
print("4 = Bree")
print("\nOr maybe GS343 just needs LESS announcement frequency?")
