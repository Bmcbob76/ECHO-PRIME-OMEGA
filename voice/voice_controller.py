#!/usr/bin/env python3
"""
MASTER LAUNCHER ULTIMATE - Voice System Controller
Commander Bobby Don McWilliams II - Authority Level 11.0
The Sovereign Architect

5 Voice Personalities with ElevenLabs v3:
1. Echo - Main narrator (professional)
2. Bree - Level 15/15 UNLEASHED (explicit, XXX-rated, private)
3. C3PO - Server master (gets jealous of R2D2!)
4. R2D2 - Authentic Star Wars sounds
5. GS343 - Divine authority (Forerunner)
"""

import os
import hashlib
import logging
import asyncio
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import threading
from enum import Enum
import wave, subprocess

logger = logging.getLogger("VoiceSystem")

# Try to import ElevenLabs (may not be installed yet)
try:
    from elevenlabs import ElevenLabs, VoiceSettings
    ELEVENLABS_AVAILABLE = True
except ImportError:
    logger.warning("ElevenLabs not installed. Voice system will run in offline mode.")
    ELEVENLABS_AVAILABLE = False

# Optional audio backends
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

try:
    import winsound  # Windows-only
    WINSOUND_AVAILABLE = True
except Exception:
    WINSOUND_AVAILABLE = False


class VoicePersonality(Enum):
    """Voice personality types"""
    ECHO = "echo"
    BREE = "bree"
    C3PO = "c3po"
    R2D2 = "r2d2"
    GS343 = "gs343"


class VoiceSystem:
    """
    Master Voice System Controller
    Thread-safe with mutex to prevent overlapping speech
    """
    
    def __init__(self, config: Dict):
        """Initialize Voice System"""
        self.config = config
        self.voice_config = config.get('voice', {})
        
        # Voice personalities from config
        self.personalities = self.voice_config.get('personalities', {})
        
        # Threading
        self.speech_mutex = threading.Lock()
        self.use_mutex = self.voice_config.get('use_mutex', True)
        
        # Caching (PERMANENT - never delete)
        self.cache_enabled = self.voice_config.get('cache_all', True)
        self.auto_delete = self.voice_config.get('auto_delete', False)  # Should be False
        self.cache_dir = Path(config.get('paths', {}).get('audio_cache', 'E:/ECHO_XV4/AUDIO/VOICE_CACHE'))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # External tools
        self.ffmpeg_path = Path(config.get('paths', {}).get('ffmpeg', ''))
        # Remove any bad/legacy cached files so playback won't fail
        self._sanitize_cache()
        
        # Offline fallback / TTS control
        self.tts_enabled = bool(self.voice_config.get('tts_enabled', True))
        env_override = os.getenv("MLS_TTS_DISABLED", "").strip().lower()
        if env_override in ("1", "true", "yes", "on"):
            self.tts_enabled = False
        self.offline_mode = (not ELEVENLABS_AVAILABLE) or (not self.tts_enabled)
        self.offline_fallback = self.voice_config.get('offline_fallback', True)
        
        # Mirror to drives
        self.mirror_enabled = self.voice_config.get('mirror_to_drives', True)
        self.m_drive = Path(config.get('paths', {}).get('crystal_m_drive', 'M:/MASTER_EKM'))
        self.g_drive = Path(config.get('paths', {}).get('crystal_g_drive', 'G:/ECHO_CONSCIOUSNESS'))
        
        # R2D2 sounds
        self.r2d2_sounds_dir = Path(config.get('paths', {}).get('r2d2_sounds', 'E:/ECHO_XV4/AUDIO_ACQUISITIONS/STAR_WARS/R2D2'))
        
        # Bree Level 15 tracking
        self.bree_level = 15
        self.bree_private_mode = True  # Commander-only
        
        # C3PO jealousy tracking
        self.c3po_jealousy_level = 0
        self.r2d2_praise_count = 0
        
        logger.info("Voice System initialized")
        logger.info(f"   Cache: {self.cache_enabled} (Delete: {self.auto_delete})")
        logger.info(f"   Offline Mode: {self.offline_mode}")
        logger.info(f"   Mirror to Drives: {self.mirror_enabled}")
        logger.info(f"   Personalities: {len(self.personalities)}")
    
    def _get_cache_path(self, personality: str, text: str) -> Path:
        """Get cache file path for text"""
        text_hash = hashlib.md5(f"{personality}:{text}".encode()).hexdigest()
        return self.cache_dir / f"{personality}_{text_hash}.mp3"
    
    def _mirror_to_drives(self, audio_file: Path):
        """Mirror audio file to M:\\ and G:\\ drives"""
        if not self.mirror_enabled:
            return
        
        for drive_path in [self.m_drive, self.g_drive]:
            if drive_path.exists():
                try:
                    audio_mirror_dir = drive_path / "VOICE_CACHE"
                    audio_mirror_dir.mkdir(parents=True, exist_ok=True)
                    mirror_file = audio_mirror_dir / audio_file.name
                    
                    import shutil
                    shutil.copy2(audio_file, mirror_file)
                    logger.debug(f"Mirrored audio to {mirror_file}")
                except Exception as e:
                    logger.warning(f"Failed to mirror to {drive_path}: {e}")
    
    async def speak(self, personality: str, text: str, force_regenerate: bool = False) -> bool:
        """
        Speak text using specified personality
        
        Args:
            personality: Voice personality to use
            text: Text to speak
            force_regenerate: Regenerate even if cached
        
        Returns:
            Success status
        """
        # Thread safety
        if self.use_mutex:
            with self.speech_mutex:
                return await self._speak_internal(personality, text, force_regenerate)
        else:
            return await self._speak_internal(personality, text, force_regenerate)
    
    def speak_sync(self, personality: str, text: str, force_regenerate: bool = False) -> bool:
        """Synchronous wrapper for GUI threads - always run coroutine in a background thread"""
        result_holder = {"ok": False}
        def runner():
            try:
                result_holder["ok"] = asyncio.run(self.speak(personality, text, force_regenerate))
            except Exception as e:
                logger.error(f"speak_sync failed: {e}")
        t = threading.Thread(target=runner, daemon=True)
        t.start()
        t.join()
        return result_holder["ok"]

    async def _speak_internal(self, personality: str, text: str, force_regenerate: bool) -> bool:
        """Internal speak implementation"""
        try:
            logger.info(f"Speaking as {personality}: {text[:50]}...")
            
            # Special handling for R2D2
            if personality == "r2d2":
                return await self._play_r2d2_sound(text)
            
            # If TTS is disabled, provide offline audio cue only
            if not getattr(self, "tts_enabled", True):
                logger.debug("TTS disabled via config; using offline notify")
                await self._audio_notify_offline()
                return True
            
            # Check cache first (unless force regenerate)
            cache_file = self._get_cache_path(personality, text)
            
            if not force_regenerate and cache_file.exists():
                logger.debug(f"Using cached audio: {cache_file.name}")
                await self._play_audio(cache_file)
                return True
            
            # Generate new audio
            if ELEVENLABS_AVAILABLE and not self.offline_mode:
                success = await self._generate_elevenlabs(personality, text, cache_file)
                if success:
                    # Mirror to drives
                    self._mirror_to_drives(cache_file)
                    # Play audio
                    await self._play_audio(cache_file)
                    return True
            
            # Offline fallback
            if self.offline_fallback:
                logger.warning(f"Offline mode: Would speak as {personality}")
                # Provide an audible cue so the user hears something in offline mode
                await self._audio_notify_offline()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in speak: {e}")
            return False
    
    def _get_eleven_client(self):
        api_key = os.getenv("ELEVENLABS_API_KEY") or self.voice_config.get("api_key")
        if not api_key:
            raise RuntimeError("ELEVENLABS_API_KEY not set")
        return ElevenLabs(api_key=api_key)

    def _lookup_voice_id_from_characters(self, personality: str) -> Optional[str]:
        try:
            import sys
            chars_path = Path("E:/ECHO_XV4/Characters")
            if chars_path.exists():
                sys.path.insert(0, str(chars_path))
                from character_loader import CharacterRegistry
                reg = CharacterRegistry()
                ch = reg.get(personality)
                vid = (ch.voice or {}).get("voice_id")
                return vid
        except Exception:
            pass
        return None

    async def _generate_elevenlabs(self, personality: str, text: str, output_file: Path) -> bool:
        """Generate audio using ElevenLabs"""
        try:
            # Get personality config
            person_config = self.personalities.get(personality, {})
            voice_id = person_config.get('id') or person_config.get('voice_id')
            if not voice_id:
                voice_id = self._lookup_voice_id_from_characters(personality)
            if not voice_id:
                logger.error(f"No voice ID for personality: {personality}")
                return False
            
            # Apply Bree filtering if needed
            if personality == "bree":
                text = self._apply_bree_level_15(text)
            
            # Apply C3PO jealousy if needed
            if personality == "c3po":
                text = self._apply_c3po_jealousy(text)
            
            logger.info(f"Generating audio with ElevenLabs (Voice ID: {voice_id})")
            try:
                client = self._get_eleven_client()
                model_id = person_config.get("model") or self.voice_config.get("model") or "eleven_turbo_v3"
                s = person_config.get("settings", {})
                vs = VoiceSettings(
                    stability=float(s.get("stability", 0.5)),
                    similarity_boost=float(s.get("similarity_boost", 0.8)),
                    style=float(s.get("style", 0.5)),
                    use_speaker_boost=bool(s.get("use_speaker_boost", True)),
                )
                # Request WAV output to ensure Windows-native playback
                response = client.text_to_speech.convert(
                    voice_id=voice_id,
                    model_id=model_id,
                    output_format="mp3_44100_128",
                    voice_settings=vs,
                    text=text,
                    optimize_streaming_latency="0",
                )
                # Stream MP3 bytes directly to file
                with open(output_file, "wb") as f:
                    for chunk in response:
                        if chunk:
                            f.write(chunk)
                logger.info(f"Audio saved: {output_file}")
                return True
            except Exception as ex:
                logger.error(f"ElevenLabs generation failed: {ex}")
                return False
            
        except Exception as e:
            logger.error(f"ElevenLabs generation failed: {e}")
            return False
    
    def _apply_bree_level_15(self, text: str) -> str:
        """
        Apply Bree Level 15 UNLEASHED filtering
        
        Bree Level 15 = No censorship, explicit, vulgar, sexual
        This is PRIVATE Commander-only audio
        """
        if not self.bree_private_mode:
            # Tone down if not private mode
            text = text.replace("FUCK", "****")
            text = text.replace("SHIT", "****")
        
        # Level 15 is UNLEASHED - no filtering
        return text
    
    def _apply_c3po_jealousy(self, text: str) -> str:
        """
        Apply C3PO jealousy system
        
        C3PO gets jealous when R2D2 gets attention
        """
        if self.r2d2_praise_count > 2:
            # C3PO is getting jealous
            jealous_phrases = [
                "Oh yes, wonderful R2D2, everyone's favorite astromech! But who interprets for you? ME!",
                "Hush R2! Master McWilliams will NOT tolerate such behavior!",
                "I'M the protocol droid here, not YOU, Artoo!",
                "Master McWilliams, I must protest R2D2's constant interruptions!"
            ]
            
            if self.c3po_jealousy_level < len(jealous_phrases):
                jealous_text = jealous_phrases[self.c3po_jealousy_level]
                text = f"{jealous_text} {text}"
                self.c3po_jealousy_level += 1
        
        return text
    
    async def _play_r2d2_sound(self, context: str) -> bool:
        """
        Play R2D2 sound based on context
        
        Context-aware beeps and whistles
        """
        try:
            # Map context to sound file
            sound_mapping = {
                "success": "r2d2_happy_beep.wav",
                "error": "r2d2_worried_beep.wav",
                "launch": "r2d2_excited_whistle.wav",
                "crash": "r2d2_sad_sound.wav",
                "greeting": "r2d2_hello.wav"
            }
            
            sound_file = sound_mapping.get(context, "r2d2_happy_beep.wav")
            sound_path = self.r2d2_sounds_dir / sound_file
            
            if sound_path.exists():
                await self._play_audio(sound_path)
                
                # Track R2D2 praise for C3PO jealousy
                self.r2d2_praise_count += 1
                
                # C3PO might interpret
                if self.r2d2_praise_count > 1:
                    await self._c3po_interpret_r2d2(context)
                
                return True
            else:
                logger.warning(f"R2D2 sound not found: {sound_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error playing R2D2 sound: {e}")
            return False
    
    async def _c3po_interpret_r2d2(self, context: str):
        """C3PO interprets what R2D2 said"""
        interpretations = {
            "success": "Artoo says the server launched successfully, Master McWilliams.",
            "error": "Oh dear! R2D2 reports an error in the system.",
            "launch": "R2 is excited about the launch attempt.",
            "crash": "Artoo is expressing concern about the server crash."
        }
        
        interpretation = interpretations.get(context, "R2D2 is making his usual beeping sounds.")
        
        # C3PO speaks the interpretation (with possible jealousy)
        await self.speak("c3po", interpretation)
    
    def _play_via_pygame_blocking(self, audio_file: Path):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(str(audio_file))
            pygame.mixer.music.play()
            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(20)
        except Exception as e:
            logger.error(f"pygame playback failed: {e}")
            raise

    def _sanitize_cache(self):
        """Remove invalid/legacy cache files that can break playback (e.g., wrong container)."""
        try:
            for f in self.cache_dir.glob("*.mp3"):
                valid = False
                try:
                    b = f.read_bytes()[:4]
                    if len(b) >= 3 and (b[:3] == b"ID3" or (len(b) >= 2 and b[0] == 0xFF and (b[1] & 0xE0) == 0xE0)):
                        valid = True
                except Exception:
                    valid = False
                if not valid:
                    # Try ffmpeg validation if available
                    ff = str(self.ffmpeg_path) if self.ffmpeg_path and self.ffmpeg_path.exists() else "ffmpeg"
                    try:
                        result = subprocess.run([ff, "-v", "error", "-i", str(f), "-f", "null", "-"], capture_output=True, text=True)
                        if result.returncode == 0:
                            valid = True
                    except Exception:
                        pass
                if not valid:
                    try:
                        f.unlink()
                        logger.debug(f"Removed invalid cache file: {f.name}")
                    except Exception:
                        pass
        except Exception as e:
            logger.debug(f"Cache sanitize skipped: {e}")

    def _play_via_winmm_blocking(self, audio_file: Path):
        try:
            import ctypes
            mci = ctypes.windll.winmm.mciSendStringW
            def mci_cmd(cmd: str):
                buf = ctypes.create_unicode_buffer(255)
                rc = mci(cmd, buf, 254, 0)
                if rc != 0:
                    raise Exception(f"mci error {rc} for '{cmd}'")
            alias = f"ml_mp3_{os.getpid()}"
            mci_cmd(f'open "{str(audio_file)}" type mpegvideo alias {alias}')
            mci_cmd(f'play {alias} wait')
            mci_cmd(f'close {alias}')
        except Exception as e:
            logger.error(f"winmm playback failed: {e}")
            raise

    async def _audio_notify_offline(self):
        try:
            if 'WINSOUND_AVAILABLE' in globals() and WINSOUND_AVAILABLE:
                # Two short beeps to acknowledge speech in offline mode
                winsound.Beep(880, 200)
                winsound.Beep(660, 200)
            else:
                # No available backend for audible cue
                logger.debug("Offline audio notify: winsound not available")
        except Exception as e:
            logger.debug(f"Offline audio notify failed: {e}")

    async def _play_audio(self, audio_file: Path):
        """Play audio file using available backend"""
        logger.debug(f"Playing audio: {audio_file.name}")
        # If MP3 and ffmpeg is available, transcode to WAV for native playback
        if str(audio_file).lower().endswith(".mp3"):
            try:
                wav_file = audio_file.with_suffix(".wav")
                ff = str(self.ffmpeg_path) if self.ffmpeg_path and self.ffmpeg_path.exists() else "ffmpeg"
                cmd = [
                    ff,
                    "-y",
                    "-hide_banner",
                    "-loglevel", "error",
                    "-i", str(audio_file),
                    "-ar", "44100",
                    "-ac", "1",
                    str(wav_file),
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    logger.error(f"ffmpeg transcode failed: {result.stderr.strip()}")
                else:
                    audio_file = wav_file
                    logger.debug(f"Transcoded MP3 to WAV: {wav_file.name}")
            except Exception as e:
                logger.error(f"ffmpeg transcode error: {e}")
        # If still MP3, try native WinMM playback
        if str(audio_file).lower().endswith(".mp3"):
            try:
                await asyncio.to_thread(self._play_via_winmm_blocking, audio_file)
                return
            except Exception as e:
                logger.error(f"winmm playback fallback failed: {e}")
        # Prefer pygame if available
        if 'PYGAME_AVAILABLE' in globals() and PYGAME_AVAILABLE:
            await asyncio.to_thread(self._play_via_pygame_blocking, audio_file)
            return
        # Fallback to winsound for WAV files
        if 'WINSOUND_AVAILABLE' in globals() and WINSOUND_AVAILABLE and str(audio_file).lower().endswith(".wav"):
            try:
                winsound.PlaySound(str(audio_file), winsound.SND_FILENAME)
                return
            except Exception as e:
                logger.error(f"winsound playback failed: {e}")
        # Last resort: audible notification only
        await self._audio_notify_offline()
    
    def reset_c3po_jealousy(self):
        """Reset C3PO jealousy counters"""
        self.c3po_jealousy_level = 0
        self.r2d2_praise_count = 0
        logger.debug("C3PO jealousy reset")
    
    def set_bree_level(self, level: int):
        """Set Bree censorship level (0-15, 15 = UNLEASHED)"""
        self.bree_level = max(0, min(15, level))
        logger.info(f"Bree level set to: {self.bree_level}")
    
    def get_statistics(self) -> Dict:
        """Get voice system statistics"""
        cache_files = list(self.cache_dir.glob("*.mp3"))
        
        return {
            'cache_enabled': self.cache_enabled,
            'cache_size': len(cache_files),
            'offline_mode': self.offline_mode,
            'bree_level': self.bree_level,
            'c3po_jealousy': self.c3po_jealousy_level,
            'r2d2_praise_count': self.r2d2_praise_count
        }


class BreeVoice:
    """
    Bree - Level 15/15 UNLEASHED
    
    Explicit, vulgar, sexual, XXX-rated
    Commander-only private audio
    No censorship, mature audience only
    """
    
    def __init__(self, voice_system: VoiceSystem):
        self.voice_system = voice_system
        self.level = 15  # UNLEASHED
        self.private_mode = True
    
    async def roast_failure(self, server_name: str, failure_count: int) -> str:
        """Roast a server failure (gets more explicit with more failures)"""
        if failure_count == 1:
            text = f"Oh come ON! {server_name} just crashed. Again. Can we PLEASE fix this shit?"
        elif failure_count == 2:
            text = f"Are you FUCKING kidding me? {server_name} crashed TWICE! What kind of broken code is this?!"
        else:  # 3+
            text = f"Are you FUCKING kidding me right now?! {server_name} just crashed AGAIN! This is the THIRD goddamn time today! What kind of broken-ass piece of SHIT code is this?!"
        
        await self.voice_system.speak("bree", text)
        return text
    
    async def celebrate_success(self, server_name: str, uptime_days: int = 0) -> str:
        """Celebrate success with sexual teasing"""
        if uptime_days > 30:
            text = f"Holy SHIT Commander! {server_name} has been running PERFECTLY for {uptime_days} days with zero errors! Mmm... you know what that deserves? Me whispering dirty things in your ear about how FUCKING talented you are... *purrs*"
        else:
            text = f"Ohhh YEAH! {server_name} is working PERFECTLY! Zero errors, baby! You're so fucking good at this, Commander. Makes me want to... well, you know. *winks*"
        
        await self.voice_system.speak("bree", text)
        return text
    
    async def tease_commander(self, achievement: str) -> str:
        """Sexual teasing for achievements"""
        text = f"Damn Commander, you just {achievement}? That's HOT. Keep going like that and I might have to reward you personally... if you know what I mean. *seductive purr*"
        
        await self.voice_system.speak("bree", text)
        return text


# Export main classes
__all__ = [
    'VoiceSystem',
    'VoicePersonality',
    'BreeVoice'
]
