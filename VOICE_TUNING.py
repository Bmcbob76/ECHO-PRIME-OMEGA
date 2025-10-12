"""
🎙️ VOICE TUNING UTILITY - Working Version
Authority Level 11.0 - Commander Bobby Don McWilliams II
"""

import sys
sys.path.insert(0, "E:/ECHO_XV4/EPCP3O_COPILOT")

from epcp3o_voice_integrated import EPCP3OVoiceSystem
import asyncio

voice = EPCP3OVoiceSystem()
voice.initialize()

print("🎙️ VOICE CAST TUNING")
print("=" * 70)

# Test GS343 with different emotions (emotion is the key parameter)
print("\n1️⃣ Testing GS343 - CALM (Original - Too Slow)")
asyncio.run(voice.speak_c3po(
    "GS343 Divine Authority System initialized",
    voice_id='8ATB4Ory7NkyCVRpePdw',
    emotion='calm'
))

print("\n2️⃣ Testing GS343 - CONFIDENT (More Energy)")
asyncio.run(voice.speak_c3po(
    "GS343 Divine Authority System initialized - Authority Level 11",
    voice_id='8ATB4Ory7NkyCVRpePdw',
    emotion='confident'
))

print("\n3️⃣ Testing GS343 - EXCITED (High Energy)")
asyncio.run(voice.speak_c3po(
    "GS343 Divine Authority System initialized - Commander authenticated",
    voice_id='8ATB4Ory7NkyCVRpePdw',
    emotion='excited'
))

print("\n4️⃣ Testing GS343 - ANGRY (Commanding)")
asyncio.run(voice.speak_c3po(
    "GS343 Divine Authority System initialized - Maximum authority",
    voice_id='8ATB4Ory7NkyCVRpePdw',
    emotion='angry'
))

print("\n5️⃣ Testing Echo - CONFIDENT")
asyncio.run(voice.speak_c3po(
    "All systems operational Commander - Mission success",
    voice_id='keDMh3sQlEXKM4EQxvvi',
    emotion='confident'
))

print("\n6️⃣ Testing C3PO - CALM")
asyncio.run(voice.speak_c3po(
    "Server Orchestrator online on port 8000 - All systems green",
    voice_id='0UTDtgGGkpqERQn1s0YK',
    emotion='calm'
))

print("\n7️⃣ Testing Bree - ANGRY (BRUTAL)")
asyncio.run(voice.speak_bree(
    "Are you fucking kidding me?! This server crashed AGAIN! This code is absolute garbage!",
    voice_id='pzKXffibtCDxnrVO8d1U',
    emotion='angry'
))

print("\n" + "=" * 70)
print("✅ Voice tuning complete!")
print("\nWhich GS343 emotion do you prefer?")
print("1 = calm (slow, boring)")
print("2 = confident (better energy)")
print("3 = excited (high energy)")
print("4 = angry (commanding)")
