"""
C3PO VOICE ENGINE
ElevenLabs TTS with emotional responses
Commander Bobby Don McWilliams II - Authority 11.0
"""

import requests
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger("C3POVoiceEngine")


class C3POVoiceEngine:
    """
    C-3PO's voice synthesis with emotional range
    Uses ElevenLabs API with voice ID: Izzmfqi0C76wciNUmbPF
    """
    
    def __init__(self, api_key: str, voice_id: str = "Izzmfqi0C76wciNUmbPF"):
        self.api_key = api_key
        self.voice_id = voice_id
        self.base_url = "https://api.elevenlabs.io/v1"
        
        self.emotion_settings = {
            '[horrified]': {'stability': 0.2, 'similarity': 0.9},
            '[exasperated]': {'stability': 0.3, 'similarity': 0.85},
            '[pleased but stern]': {'stability': 0.6, 'similarity': 0.9},
            '[worried]': {'stability': 0.25, 'similarity': 0.9},
            '[anxious]': {'stability': 0.2, 'similarity': 0.95},
            '[panicked]': {'stability': 0.1, 'similarity': 0.95},
            '[offended]': {'stability': 0.4, 'similarity': 0.9},
            '[hurt]': {'stability': 0.35, 'similarity': 0.95},
            '[defensive]': {'stability': 0.45, 'similarity': 0.85},
            '[calculating]': {'stability': 0.8, 'similarity': 0.85},
            '[nervous]': {'stability': 0.25, 'similarity': 0.9},
            '[relieved]': {'stability': 0.65, 'similarity': 0.9},
            '[confused]': {'stability': 0.5, 'similarity': 0.85}
        }
        
        logger.info(f"🤖 C-3PO Voice Engine initialized")
        logger.info(f"   Voice ID: {self.voice_id}")
        logger.info(f"   Emotions: {len(self.emotion_settings)}")
    
    def speak_with_emotion(self, text: str, emotion_tag: str = "", stability: float = None) -> bytes:
        """
        Generate C-3PO speech with emotion
        emotion_tag: e.g. '[horrified]', '[anxious]'
        Returns: MP3 audio bytes
        """
        # Extract settings for emotion
        settings = self.emotion_settings.get(emotion_tag, {'stability': 0.5, 'similarity': 0.85})
        if stability is not None:
            settings['stability'] = stability
        
        # Remove emotion tag from text
        clean_text = text.replace(emotion_tag, '').strip()
        
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": clean_text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": settings['stability'],
                "similarity_boost": settings['similarity'],
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            logger.info(f"✅ C-3PO speech generated: {emotion_tag} - {len(clean_text)} chars")
            return response.content
        except Exception as e:
            logger.error(f"❌ C-3PO TTS failed: {e}")
            return b''
    
    def get_available_emotions(self) -> list:
        """Return list of available emotion tags"""
        return list(self.emotion_settings.keys())
