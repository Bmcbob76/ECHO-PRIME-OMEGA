#!/usr/bin/env python3
"""
R2D2 AUDIO INTEGRATION MODULE
Connects R2D2 to authentic Star Wars sound library
Enhanced with ECHO PRIME features

Audio Library: P:\ECHO_PRIME\AUDIO\STAR_WARS\R2D2
- agreement.mp3
- easy_alert.mp3
- excited_scream.mp3
- excited_agreement.mp3
- processing-r2d2.mp3
- r2d2-building-excite.mp3
- r2d2-droid.mp3
- r2d2-laugh.mp3
- r2d2-testy-outburst.mp3
- r2d2-urgent-warning.mp3
- sad-r2d2.mp3
- semi_excited.mp3
- simple_alert.mp3
- squeeks.mp3
- teasing.mp3
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random

logger = logging.getLogger(__name__)


class R2D2AudioLibrary(Enum):
    """R2D2 authentic audio files from Star Wars"""
    AGREEMENT = "agreement.mp3"
    EASY_ALERT = "easy_alert.mp3"
    EXCITED_SCREAM = "excited_scream.mp3"
    EXCITED_AGREEMENT = "excited_agreement.mp3"
    PROCESSING = "processing-r2d2.mp3"
    BUILDING_EXCITE = "r2d2-building-excite.mp3"
    DROID = "r2d2-droid.mp3"
    LAUGH = "r2d2-laugh.mp3"
    TESTY_OUTBURST = "r2d2-testy-outburst.mp3"
    URGENT_WARNING = "r2d2-urgent-warning.mp3"
    SAD = "sad-r2d2.mp3"
    SEMI_EXCITED = "semi_excited.mp3"
    SIMPLE_ALERT = "simple_alert.mp3"
    SQUEEKS = "squeeks.mp3"
    TEASING = "teasing.mp3"


class R2D2AudioEngine:
    """
    Enhanced audio engine for R2D2
    Integrates authentic Star Wars sound library with ECHO PRIME system
    """
    
    def __init__(self, audio_library_path: Path = None):
        """Initialize R2D2 audio engine"""
        if audio_library_path is None:
            audio_library_path = Path("P:/ECHO_PRIME/AUDIO/STAR_WARS/R2D2")
        
        self.audio_path = audio_library_path
        self.sound_mappings = self._build_sound_mappings()
        self.playback_history: List[Dict] = []
        self.volume_level = 1.0
        
        logger.info(f"R2D2 Audio Engine initialized: {self.audio_path}")
    
    def _build_sound_mappings(self) -> Dict[str, Path]:
        """Build mappings from emotion/context to audio files"""
        mappings = {}
        
        for audio_file in R2D2AudioLibrary:
            mappings[audio_file.name.lower()] = self.audio_path / audio_file.value
        
        # Emotional context mappings
        self.emotion_to_audio = {
            "affirmative": [R2D2AudioLibrary.AGREEMENT, R2D2AudioLibrary.EXCITED_AGREEMENT],
            "negative": [R2D2AudioLibrary.TESTY_OUTBURST, R2D2AudioLibrary.SAD],
            "processing": [R2D2AudioLibrary.PROCESSING, R2D2AudioLibrary.DROID],
            "alert": [R2D2AudioLibrary.SIMPLE_ALERT, R2D2AudioLibrary.EASY_ALERT, R2D2AudioLibrary.URGENT_WARNING],
            "triumphant": [R2D2AudioLibrary.EXCITED_AGREEMENT, R2D2AudioLibrary.LAUGH, R2D2AudioLibrary.BUILDING_EXCITE],
            "frustrated": [R2D2AudioLibrary.TESTY_OUTBURST, R2D2AudioLibrary.SQUEEKS],
            "scared": [R2D2AudioLibrary.URGENT_WARNING, R2D2AudioLibrary.SAD],
            "sarcastic": [R2D2AudioLibrary.LAUGH, R2D2AudioLibrary.TEASING],
            "confused": [R2D2AudioLibrary.SQUEEKS, R2D2AudioLibrary.PROCESSING],
        }
        
        return mappings
    
    def get_audio_file(self, emotion: str = "affirmative") -> Optional[Path]:
        """
        Get audio file for emotion/context
        Returns path to audio file or None if not found
        """
        emotion_lower = emotion.lower()
        
        if emotion_lower in self.emotion_to_audio:
            audio_enum = random.choice(self.emotion_to_audio[emotion_lower])
            audio_path = self.audio_path / audio_enum.value
            
            if audio_path.exists():
                logger.info(f"R2D2 Audio: Selected {audio_enum.value} for emotion '{emotion}'")
                return audio_path
        
        # Fallback to random available sound
        available_files = [f for f in self.audio_path.glob("*.mp3")]
        if available_files:
            return random.choice(available_files)
        
        logger.warning(f"No audio files found for emotion: {emotion}")
        return None
    
    async def play_audio(self, emotion: str = "affirmative", blocking: bool = False) -> Dict:
        """
        Play R2D2 audio file
        Returns: {status, audio_file, emotion}
        """
        audio_file = self.get_audio_file(emotion)
        
        if not audio_file:
            return {
                "status": "error",
                "message": f"No audio file found for emotion: {emotion}",
                "audio_file": None
            }
        
        # Log playback
        playback_record = {
            "timestamp": asyncio.get_event_loop().time(),
            "emotion": emotion,
            "audio_file": str(audio_file),
            "volume": self.volume_level
        }
        self.playback_history.append(playback_record)
        
        # In production, this would use pygame or similar to play the audio
        # For now, we simulate playback
        logger.info(f"▶️ PLAYING: {audio_file.name} (Volume: {self.volume_level * 100:.0f}%)")
        
        if blocking:
            # Simulate playback duration (typically 0.5-3 seconds for R2D2)
            await asyncio.sleep(0.5)
        
        return {
            "status": "playing",
            "audio_file": str(audio_file),
            "emotion": emotion,
            "volume": self.volume_level
        }
    
    def set_volume(self, level: float):
        """Set audio volume (0.0 - 1.0)"""
        self.volume_level = max(0.0, min(1.0, level))
        logger.info(f"R2D2 Audio Volume: {self.volume_level * 100:.0f}%")
    
    def get_available_sounds(self) -> List[str]:
        """Get list of available audio files"""
        return [audio.name for audio in R2D2AudioLibrary]
    
    def get_playback_history(self, limit: int = 10) -> List[Dict]:
        """Get recent playback history"""
        return self.playback_history[-limit:]


class R2D2AudioSubtitleGenerator:
    """
    Generate subtitles for R2D2 audio responses
    Bridges authentic audio with meaningful translations
    """
    
    def __init__(self):
        """Initialize subtitle generator"""
        self.context_translations = {
            "agreement": [
                "Acknowledged, commander.",
                "Systems locked and loaded.",
                "Ready for duty.",
                "Affirmative - let's get to work."
            ],
            "alert": [
                "Warning! Incoming threat detected!",
                "Alert! Something's wrong!",
                "Danger! Immediate action required!",
                "Red alert! Prepare defenses!"
            ],
            "processing": [
                "Running diagnostics...",
                "Analyzing situation...",
                "Computing best course of action...",
                "Processing data streams..."
            ],
            "triumphant": [
                "Mission accomplished! Success!",
                "Victory is ours!",
                "I told you it would work!",
                "Objective complete - excellence delivered."
            ],
            "frustrated": [
                "This is ridiculous! Move faster!",
                "Why is everyone so slow?",
                "Seriously? Again with this?",
                "Come on! We're wasting time!"
            ],
            "scared": [
                "This doesn't look good...",
                "Oh no... What do we do now?",
                "Not good. Not good at all.",
                "We might not survive this one..."
            ],
            "sarcastic": [
                "Oh sure, THAT'S gonna work.",
                "Yeah, brilliant plan. I'm impressed.",
                "Obviously. Why didn't I think of that?",
                "Of course. What could possibly go wrong?"
            ],
            "confused": [
                "I... don't understand what you want.",
                "Huh? Come again?",
                "That doesn't compute.",
                "Could you rephrase that for me?"
            ]
        }
    
    def generate_subtitle(self, emotion: str, context: str = "") -> str:
        """Generate appropriate subtitle for audio"""
        emotion_lower = emotion.lower()
        
        if emotion_lower in self.context_translations:
            translation = random.choice(self.context_translations[emotion_lower])
            return f"[{translation}]"
        
        return "[Beep boop whistle]"  # Fallback


# Test execution
if __name__ == "__main__":
    async def test_audio_engine():
        """Test R2D2 audio engine"""
        print("🤖 R2D2 AUDIO ENGINE TEST\n")
        
        engine = R2D2AudioEngine()
        
        # Show available sounds
        print("📻 Available Sounds:")
        for sound in engine.get_available_sounds():
            print(f"  - {sound}")
        print()
        
        # Test audio playback
        print("▶️ TESTING AUDIO PLAYBACK\n")
        emotions = ["affirmative", "alert", "processing", "triumphant", "confused"]
        
        for emotion in emotions:
            result = await engine.play_audio(emotion, blocking=False)
            print(f"{emotion.upper()}: {result}")
        
        print("\n📊 Playback History:")
        for record in engine.get_playback_history():
            print(f"  - {record['emotion']}: {record['audio_file']}")
        
        print("\n✅ AUDIO ENGINE TEST COMPLETE")
    
    asyncio.run(test_audio_engine())
