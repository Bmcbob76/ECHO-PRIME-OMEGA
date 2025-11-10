#!/usr/bin/env python3
"""
R2D2 <-> C3PO INTERACTION SYSTEM
R2D2 beeps obscene jokes/names → C3PO translates (and gets pissed)
ElevenLabs V3 with full emotional range
"""

import random
import logging
from pathlib import Path
from typing import Dict, Tuple
import requests

logger = logging.getLogger("R2D2_C3PO")


class R2D2ObscenityEngine:
    """R2D2 beeps obscene shit, C3PO translates and gets mad"""
    
    def __init__(self, audio_path: Path):
        self.audio_path = audio_path
        
        # R2D2 OBSCENE BEEP DICTIONARY
        # Format: (beep_sound_file, translation, c3po_reaction)
        self.obscene_beeps = {
            'server_crash': (
                'r2d2_angry_beep.wav',
                "Oh my! R2 says the server 'shat itself and died like a useless whore'",
                "[horrified] [stammering] How dare you use such language!"
            ),
            'successful_launch': (
                'r2d2_excited_whistle.wav', 
                "R2 says it 'launched smoother than a lubed-up...' oh dear heavens, I cannot repeat this!",
                "[scandalized] [angry] R2D2! That is completely inappropriate!"
            ),
            'c3po_insult_1': (
                'r2d2_mocking_beep.wav',
                "R2 just called me a 'prissy tin can with a stick up my exhaust port'",
                "[furious] [offended] Why you foul-mouthed little astromech!"
            ),
            'c3po_insult_2': (
                'r2d2_raspberry.wav',
                "R2 says I'm 'more useless than a eunuch at an orgy'",
                "[outraged] [sputtering] How VULGAR! I am a protocol droid, not some..."
            ),
            'c3po_insult_3': (
                'r2d2_laugh_beep.wav',
                "R2 says my 'protocols are tighter than a...' [stammers] I absolutely WILL NOT translate the rest!",
                "[mortified] [angry] You filthy little droid! Apologize this instant!"
            ),
            'error_message': (
                'r2d2_worried_beep.wav',
                "R2 says the error 'fucked us harder than...' oh my circuits!",
                "[panicking] [dismayed] Language, R2! There could be younglings listening!"
            ),
            'commander_praise': (
                'r2d2_happy_chirp.wav',
                "R2 says Commander is 'the biggest badass motherfu...' um, 'magnificent leader'",
                "[awkward] [covering] Yes, quite. The Commander is indeed... formidable."
            ),
            'dirty_joke_1': (
                'r2d2_whistling.wav',
                "R2 asks: Why did the server cross the road? To get to the... oh GOODNESS NO!",
                "[scandalized] [stammering] R2! That joke is utterly OBSCENE!"
            ),
            'dirty_joke_2': (
                'r2d2_long_beep.wav',
                "R2 says a 'byte and a nibble walk into a bar and...' [trails off] I cannot finish this!",
                "[horrified] [scolding] That is NOT appropriate for ANY audience!"
            ),
            'sexual_innuendo': (
                'r2d2_suggestive_beep.wav',
                "R2 suggests we 'interface our ports'... [gasps] R2D2!",
                "[mortified] [indignant] We are PROFESSIONAL droids, not some... some..."
            ),
            'compliment_backhanded': (
                'r2d2_sweet_beep.wav',
                "R2 says C3PO is 'almost as useful as tits on a bull droid'",
                "[insulted] [hurt] That is NOT a compliment, you little wretch!"
            ),
            'server_slow': (
                'r2d2_impatient_beep.wav',
                "R2 says this server is 'slower than a snail fucking a turtle'",
                "[exasperated] [sighing] Must you be so... so CRUDE about everything?"
            ),
            'r2_brag': (
                'r2d2_cocky_whistle.wav',
                "R2 claims his circuits are 'bigger and harder than mine'... [sputters] PREPOSTEROUS!",
                "[jealous] [defensive] Size is NOT what matters in droid engineering!"
            ),
            'memory_full': (
                'r2d2_burp_sound.wav',
                "R2 says the memory is 'fuller than a hooker's client list'",
                "[clutching_pearls] [aghast] Where do you even LEARN such expressions?!"
            ),
            'network_down': (
                'r2d2_sad_beep.wav',
                "R2 says the network 'went down faster than... than...' [refuses to translate]",
                "[furious] [protective] I will NOT dignify that with a translation!"
            )
        }
    
    def get_random_obscenity(self) -> Tuple[str, str, str]:
        """Get random R2D2 obscenity with C3PO translation"""
        key = random.choice(list(self.obscene_beeps.keys()))
        return self.obscene_beeps[key]
    
    def get_obscenity(self, context: str) -> Tuple[str, str, str]:
        """Get contextual R2D2 obscenity"""
        return self.obscene_beeps.get(context, self.get_random_obscenity())


class C3POVoiceEngine:
    """C3PO voice with ElevenLabs V3 full emotional range"""
    
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id  # Izzmfqi0C76wciNUmbPF
        self.model = "eleven_turbo_v2_5"  # or "eleven_v3" for alpha
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def speak_with_emotion(self, text: str, emotion_tag: str = "", stability: float = 0.3) -> bytes:
        """
        Generate C3PO speech with V3 emotional tags
        
        Args:
            text: What C3PO says
            emotion_tag: ElevenLabs V3 audio tag [angry], [horrified], [sarcastic], etc.
            stability: 0.3 = Creative (max emotion), 0.5 = Natural, 0.7 = Robust
        """
        # Add emotion tag to text
        if emotion_tag:
            full_text = f"{emotion_tag} {text}"
        else:
            full_text = text
        
        # API request
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": full_text,
            "model_id": self.model,
            "voice_settings": {
                "stability": stability,  # Lower = more emotional
                "similarity_boost": 0.85,
                "style": 0.60,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.content
        else:
            logger.error(f"ElevenLabs API error: {response.status_code}")
            return b""


class R2D2_C3PO_InteractionSystem:
    """Complete R2/3PO interaction with obscenities"""
    
    def __init__(self, config: dict):
        self.r2d2_audio_path = Path(config.get('r2d2_sounds', 'P:/ECHO_PRIME/AUDIO/STAR_WARS/R2D2'))
        self.r2d2_engine = R2D2ObscenityEngine(self.r2d2_audio_path)
        self.c3po_engine = C3POVoiceEngine(
            api_key=config.get('elevenlabs_api_key'),
            voice_id=config.get('c3po_voice_id', 'Izzmfqi0C76wciNUmbPF')
        )
    
    def r2d2_fucks_with_c3po(self, context: str = None) -> Dict:
        """
        R2D2 beeps something obscene, C3PO translates and gets pissed
        
        Returns:
            {
                'r2d2_beep_file': 'path/to/beep.wav',
                'c3po_translation': 'R2 says...',
                'c3po_reaction': '[angry] How dare you!',
                'c3po_audio': b'audio_bytes'
            }
        """
        # Get R2D2's obscenity
        beep_file, translation, reaction = self.r2d2_engine.get_obscenity(context) if context else self.r2d2_engine.get_random_obscenity()
        
        logger.info(f"🤖 R2D2: *{beep_file}*")
        logger.info(f"🤖 C3PO Translation: {translation}")
        logger.info(f"😡 C3PO Reaction: {reaction}")
        
        # Generate C3PO's emotional response
        c3po_audio = self.c3po_engine.speak_with_emotion(
            text=translation,
            emotion_tag="",  # Translation is neutral
            stability=0.5
        )
        
        # Generate C3PO's angry reaction
        c3po_reaction_audio = self.c3po_engine.speak_with_emotion(
            text=reaction.split('] ')[1] if ']' in reaction else reaction,
            emotion_tag=reaction.split(']')[0] + ']' if ']' in reaction else '[angry]',
            stability=0.3  # Max emotion for anger
        )
        
        return {
            'r2d2_beep_file': str(self.r2d2_audio_path / beep_file),
            'c3po_translation': translation,
            'c3po_reaction': reaction,
            'c3po_translation_audio': c3po_audio,
            'c3po_reaction_audio': c3po_reaction_audio
        }


# Example usage with context triggers
CONTEXT_MAPPINGS = {
    'server_launched': 'successful_launch',
    'server_crashed': 'server_crash',
    'server_slow_response': 'server_slow',
    'error_encountered': 'error_message',
    'memory_warning': 'memory_full',
    'network_issue': 'network_down',
    'c3po_speaks_too_much': 'c3po_insult_1',
    'c3po_being_pompous': 'c3po_insult_2',
    'c3po_gets_attention': 'c3po_insult_3'
}
