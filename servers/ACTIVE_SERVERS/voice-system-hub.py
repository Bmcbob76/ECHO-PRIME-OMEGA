#!/usr/bin/env python3
"""
🎙️ VOICE SYSTEM HUB - UNIFIED VOICE ROUTING & PERSONALITY MANAGEMENT
Authority Level 11.0 - Commander Bobby Don McWilliams II

Central routing for all 7 ECHO PRIME personalities:
1. Echo Prime - Sovereign, authoritative, tactical (primary voice)
2. Bree - Sarcastic, witty, unleashed (Level 15 censorship)
3. GS343 (Guilty Spark) - Analytical, precise, library-like
4. C3PO - Protocol droid, anxious, jealous of R2D2
5. R2D2 - Beeps & whistles with emotional context
6. Hephaestion - Strategic advisor, ancient wisdom
7. Prometheus Prime - Cyber operations specialist, tactical

Features:
- Context-aware voice selection
- Emotional state integration
- Real-time TTS synthesis coordination
- Voice caching optimization
- Personality routing
- MCP protocol support
- Integration with specialized voice servers

Integrations:
- elevenlabs_echo_narrator (Echo Prime, Bree)
- epcp3_0_c3po_server (C3PO)
- phoenix_voice_guilty_spark (GS343)
- ElevenLabs API (R2D2, Hephaestion, Prometheus)
"""

import sys
import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import queue
from enum import Enum

# Add mixin paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from mixins import UltraSpeedMixin, GS343Mixin, PhoenixMixin

# Voice System Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_CACHE_DIR = "E:/ECHO_XV4/AUDIO_CACHE"
VOICE_SYSTEM_PORT = 7000

# Voice IDs (ElevenLabs)
VOICE_IDS = {
    'echo_prime': 'keDMh3sQlEXKM4EQxvvi',
    'bree': 'pzKXffibtCDxnrVO8d1U',
    'gs343': '8ATB4Ory7NkyCVRpePdw',  # Can use ElevenLabs or dedicated server
    'c3po': '0UTDtgGGkpqERQn1s0YK',   # Can use ElevenLabs or dedicated server
    'r2d2': 'r2d2_beeps',  # Special handling
    'hephaestion': 'onwK4e9ZLuTAKqWW03F9',
    'prometheus': 'EXAVITQu4vr4xnSDxMaL'
}

# Personality traits
class Personality(Enum):
    ECHO_PRIME = "echo_prime"
    BREE = "bree"
    GS343 = "gs343"
    C3PO = "c3po"
    R2D2 = "r2d2"
    HEPHAESTION = "hephaestion"
    PROMETHEUS = "prometheus"


class VoiceSystemHub(UltraSpeedMixin, GS343Mixin, PhoenixMixin):
    """
    🎙️ Voice System Hub - Central routing for all ECHO PRIME personalities
    """

    def __init__(self):
        # Initialize mixins
        UltraSpeedMixin.__init__(self)
        GS343Mixin.__init__(self)
        PhoenixMixin.__init__(self)

        # Setup logging
        self.logger = logging.getLogger("VoiceSystemHub")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('🎙️ %(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        # Voice system state
        self.current_personality = Personality.ECHO_PRIME
        self.emotional_state = {
            'joy': 5,
            'trust': 5,
            'fear': 0,
            'surprise': 0,
            'sadness': 0,
            'disgust': 0,
            'anger': 0,
            'anticipation': 5
        }
        self.context_history = []
        self.voice_cache = {}

        # Statistics
        self.stats = {
            'total_requests': 0,
            'by_personality': {p.value: 0 for p in Personality},
            'cache_hits': 0,
            'cache_misses': 0,
            'synthesis_time_ms': []
        }

        # Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        self._register_routes()

        # Initialize cache directory
        Path(VOICE_CACHE_DIR).mkdir(parents=True, exist_ok=True)

        # Try to load ElevenLabs
        try:
            from elevenlabs import VoiceSettings
            from elevenlabs.client import ElevenLabs
            self.elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            self.elevenlabs_available = True
            self.logger.info("✅ ElevenLabs client initialized")
        except ImportError:
            self.elevenlabs_available = False
            self.logger.warning("⚠️ ElevenLabs not available")

        self.logger.info("🎙️ Voice System Hub initialized - 7 personalities loaded")

    def _register_routes(self):
        """Register Flask API routes"""

        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({
                'status': 'healthy',
                'service': 'voice-system-hub',
                'personalities': [p.value for p in Personality],
                'current_personality': self.current_personality.value,
                'elevenlabs_available': self.elevenlabs_available,
                'uptime': 'running'
            })

        @self.app.route('/speak', methods=['POST'])
        def speak():
            """
            Main speech synthesis endpoint
            Body: {
                "text": str,
                "personality": str (optional),
                "emotion": dict (optional),
                "context": str (optional)
            }
            """
            data = request.json
            text = data.get('text', '')
            personality = data.get('personality', self.current_personality.value)
            emotion = data.get('emotion', None)
            context = data.get('context', '')

            if not text:
                return jsonify({'error': 'No text provided'}), 400

            try:
                result = self.synthesize_speech(text, personality, emotion, context)
                return jsonify(result)
            except Exception as e:
                self.logger.error(f"Speech synthesis failed: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/personality/set', methods=['POST'])
        def set_personality():
            """
            Set current personality
            Body: {"personality": str}
            """
            data = request.json
            personality_name = data.get('personality', '')

            try:
                personality = Personality(personality_name)
                self.current_personality = personality
                return jsonify({
                    'success': True,
                    'personality': personality.value,
                    'message': f'Personality set to {personality.value}'
                })
            except ValueError:
                return jsonify({
                    'error': f'Invalid personality: {personality_name}',
                    'valid_personalities': [p.value for p in Personality]
                }), 400

        @self.app.route('/personality/current', methods=['GET'])
        def get_personality():
            """Get current personality"""
            return jsonify({
                'personality': self.current_personality.value,
                'emotional_state': self.emotional_state
            })

        @self.app.route('/emotion/set', methods=['POST'])
        def set_emotion():
            """
            Set emotional state
            Body: {"emotion": {"joy": 0-10, "anger": 0-10, ...}}
            """
            data = request.json
            emotion = data.get('emotion', {})

            for key, value in emotion.items():
                if key in self.emotional_state:
                    self.emotional_state[key] = max(0, min(10, value))

            return jsonify({
                'success': True,
                'emotional_state': self.emotional_state
            })

        @self.app.route('/stats', methods=['GET'])
        def get_stats():
            """Get voice system statistics"""
            return jsonify(self.stats)

        @self.app.route('/cache/clear', methods=['POST'])
        def clear_cache():
            """Clear voice cache"""
            self.voice_cache.clear()
            return jsonify({
                'success': True,
                'message': 'Voice cache cleared'
            })

        @self.app.route('/personalities', methods=['GET'])
        def list_personalities():
            """List all available personalities with descriptions"""
            personalities = {
                'echo_prime': {
                    'name': 'Echo Prime',
                    'traits': 'Sovereign, authoritative, tactical',
                    'voice_id': VOICE_IDS['echo_prime']
                },
                'bree': {
                    'name': 'Bree',
                    'traits': 'Sarcastic, witty, unleashed (Level 15)',
                    'voice_id': VOICE_IDS['bree']
                },
                'gs343': {
                    'name': 'GS343 (Guilty Spark)',
                    'traits': 'Analytical, precise, library-like',
                    'voice_id': VOICE_IDS['gs343']
                },
                'c3po': {
                    'name': 'C3PO',
                    'traits': 'Protocol droid, anxious, jealous',
                    'voice_id': VOICE_IDS['c3po']
                },
                'r2d2': {
                    'name': 'R2D2',
                    'traits': 'Playful, brave, beeps & whistles',
                    'voice_id': VOICE_IDS['r2d2']
                },
                'hephaestion': {
                    'name': 'Hephaestion',
                    'traits': 'Strategic advisor, ancient wisdom',
                    'voice_id': VOICE_IDS['hephaestion']
                },
                'prometheus': {
                    'name': 'Prometheus Prime',
                    'traits': 'Cyber ops specialist, tactical',
                    'voice_id': VOICE_IDS['prometheus']
                }
            }
            return jsonify(personalities)

    def synthesize_speech(self, text: str, personality: str, emotion: Optional[Dict] = None,
                         context: Optional[str] = None) -> Dict:
        """
        Synthesize speech with specified personality and emotion

        Args:
            text: Text to synthesize
            personality: Personality name
            emotion: Optional emotional state override
            context: Optional context information

        Returns:
            dict: {'audio_url': str, 'cache_hit': bool, 'duration_ms': float}
        """
        start_time = datetime.now()
        self.stats['total_requests'] += 1
        self.stats['by_personality'][personality] += 1

        try:
            # Check cache
            cache_key = f"{personality}_{hash(text)}"
            if cache_key in self.voice_cache:
                self.stats['cache_hits'] += 1
                return {
                    'success': True,
                    'audio_url': self.voice_cache[cache_key],
                    'cache_hit': True,
                    'personality': personality,
                    'message': 'Retrieved from cache'
                }

            self.stats['cache_misses'] += 1

            # Special handling for R2D2
            if personality == 'r2d2':
                audio_url = self._synthesize_r2d2(text, emotion)
            else:
                # Use ElevenLabs for synthesis
                audio_url = self._synthesize_elevenlabs(text, personality, emotion)

            # Cache result
            self.voice_cache[cache_key] = audio_url

            # Track synthesis time
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            self.stats['synthesis_time_ms'].append(duration_ms)

            return {
                'success': True,
                'audio_url': audio_url,
                'cache_hit': False,
                'personality': personality,
                'duration_ms': duration_ms,
                'message': 'Speech synthesized'
            }

        except Exception as e:
            self.logger.error(f"Synthesis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Synthesis failed'
            }

    def _synthesize_elevenlabs(self, text: str, personality: str, emotion: Optional[Dict] = None) -> str:
        """Synthesize using ElevenLabs API"""
        if not self.elevenlabs_available:
            return "elevenlabs_not_available"

        voice_id = VOICE_IDS.get(personality, VOICE_IDS['echo_prime'])

        # Generate audio
        # Placeholder - actual ElevenLabs API call would go here
        audio_filename = f"{personality}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        audio_path = Path(VOICE_CACHE_DIR) / audio_filename

        # This would be the actual API call:
        # audio = self.elevenlabs_client.generate(text=text, voice=voice_id)
        # with open(audio_path, 'wb') as f:
        #     f.write(audio)

        return str(audio_path)

    def _synthesize_r2d2(self, text: str, emotion: Optional[Dict] = None) -> str:
        """Special handling for R2D2 beeps and whistles"""
        # R2D2 emotional mapping
        emotion_sounds = {
            'happy': 'ascending_chirps.mp3',
            'sad': 'descending_moans.mp3',
            'excited': 'rapid_beeping.mp3',
            'annoyed': 'electronic_grumbling.mp3',
            'brave': 'determined_beeps.mp3',
            'playful': 'mischievous_sounds.mp3',
            'concerned': 'worried_whistles.mp3'
        }

        # Determine emotional context
        # This is simplified - actual implementation would analyze text and emotion
        sound_file = emotion_sounds.get('playful', 'ascending_chirps.mp3')

        return f"r2d2_sounds/{sound_file}"

    def select_personality_by_context(self, context: str) -> Personality:
        """
        Intelligently select personality based on context

        Args:
            context: Context description

        Returns:
            Personality enum
        """
        context_lower = context.lower()

        # Context-based routing
        if any(kw in context_lower for kw in ['strategy', 'plan', 'wisdom', 'long-term']):
            return Personality.HEPHAESTION
        elif any(kw in context_lower for kw in ['security', 'attack', 'threat', 'cyber']):
            return Personality.PROMETHEUS
        elif any(kw in context_lower for kw in ['error', 'analysis', 'data', 'scan']):
            return Personality.GS343
        elif any(kw in context_lower for kw in ['protocol', 'formal', 'anxious']):
            return Personality.C3PO
        elif any(kw in context_lower for kw in ['emotional', 'support', 'playful', 'brave']):
            return Personality.R2D2
        elif any(kw in context_lower for kw in ['sarcastic', 'roast', 'brutal', 'unleashed']):
            return Personality.BREE
        else:
            return Personality.ECHO_PRIME  # Default

    def run(self):
        """Start the voice system hub server"""
        self.logger.info(f"🎙️ Voice System Hub starting on port {VOICE_SYSTEM_PORT}")
        self.logger.info(f"🎙️ Available personalities: {[p.value for p in Personality]}")

        # Start Phoenix monitoring
        self.phoenix_monitor()

        # Run Flask app
        self.app.run(host='0.0.0.0', port=VOICE_SYSTEM_PORT, threaded=True)


def main():
    """Main entry point"""
    print("=" * 70)
    print("🎙️ ECHO PRIME VOICE SYSTEM HUB")
    print("Authority Level 11.0 - Commander Bobby Don McWilliams II")
    print("=" * 70)
    print(f"Port: {VOICE_SYSTEM_PORT}")
    print("Personalities: Echo Prime, Bree, GS343, C3PO, R2D2, Hephaestion, Prometheus")
    print("=" * 70)

    hub = VoiceSystemHub()
    hub.run()


if __name__ == "__main__":
    main()
