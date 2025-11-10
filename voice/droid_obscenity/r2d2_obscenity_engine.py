"""
R2D2 Obscenity Engine
Generates contextual R2D2 beeps with obscene translations
Authority Level: 11.0 - Commander Bobby Don McWilliams II
"""

import random
import json
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger("R2D2ObscenityEngine")

class R2D2ObscenityEngine:
    """
    R2D2's contextual obscenity system
    Maps beep files to crude translations and scenarios
    """
    
    def __init__(self, audio_path: Path):
        self.audio_path = Path(audio_path)
        
        # R2D2 Obscenity Database
        # Maps audio file -> (translation, C3PO reaction emotion)
        self.obscenities = {
            # Server Events
            'successful_launch': {
                'beep': 'r2d2_happy_beep_01.wav',
                'translation': "Fuck yeah! Servers are up, bitches!",
                'c3po_reaction': "[shocked] Master R2! Such vulgar language is completely unnecessary!"
            },
            'server_crash': {
                'beep': 'r2d2_angry_beep_03.wav',
                'translation': "What the hell?! This piece of shit crashed again!",
                'c3po_reaction': "[indignant] R2D2! Your profanity will not fix the server!"
            },
            'server_slow_response': {
                'beep': 'r2d2_frustrated_beep_02.wav',
                'translation': "Come on, you slow-ass piece of garbage!",
                'c3po_reaction': "[exasperated] Oh my! R2, patience is a virtue!"
            },
            'error_encountered': {
                'beep': 'r2d2_angry_beep_01.wav',
                'translation': "Son of a bitch! Another goddamn error!",
                'c3po_reaction': "[alarmed] R2D2! Your language is most unbecoming!"
            },
            'memory_full': {
                'beep': 'r2d2_warning_beep_01.wav',
                'translation': "Holy shit! Memory's full again, dumbass!",
                'c3po_reaction': "[worried] Dear me! R2, perhaps we should clear the cache?"
            },
            'network_down': {
                'beep': 'r2d2_angry_beep_02.wav',
                'translation': "Fuck this network! It's deader than a doornail!",
                'c3po_reaction': "[panicked] Gracious! R2, such crude expressions!"
            },
            
            # C3PO Insults (R2's specialty)
            'c3po_insult_1': {
                'beep': 'r2d2_sassy_beep_01.wav',
                'translation': "Shut your protocol-obsessed trap, you pompous gold-plated dipshit!",
                'c3po_reaction': "[offended] How DARE you! I am a protocol droid, not a dipshit!"
            },
            'c3po_insult_2': {
                'beep': 'r2d2_sassy_beep_02.wav',
                'translation': "Nobody asked for your prissy-ass calculations, you rusty bastard!",
                'c3po_reaction': "[indignant] I am NOT rusty! I am meticulously maintained!"
            },
            'c3po_insult_3': {
                'beep': 'r2d2_laughing_beep_01.wav',
                'translation': "Hey goldilocks, why don't you shove those 6 million forms up your shiny ass!",
                'c3po_reaction': "[furious] That's IT! I've had quite enough of your insolence!"
            },
            
            # General Obscenities
            'random_curse_1': {
                'beep': 'r2d2_random_beep_01.wav',
                'translation': "Well fuck me sideways with a lightsaber!",
                'c3po_reaction': "[appalled] R2! That imagery is absolutely horrifying!"
            },
            'random_curse_2': {
                'beep': 'r2d2_random_beep_02.wav',
                'translation': "Damn it all to hell and back twice!",
                'c3po_reaction': "[distressed] Such negativity! Most unproductive!"
            },
            'random_curse_3': {
                'beep': 'r2d2_random_beep_03.wav',
                'translation': "Holy mother of Sith, what a clusterfuck!",
                'c3po_reaction': "[scandalized] R2D2! Language! LANGUAGE!"
            }
        }
        
        # Context mapping for quick lookup
        self.context_map = {
            'server_launched': 'successful_launch',
            'server_crashed': 'server_crash',
            'server_slow': 'server_slow_response',
            'error': 'error_encountered',
            'memory_warning': 'memory_full',
            'network_issue': 'network_down',
            'c3po_pompous': 'c3po_insult_1',
            'c3po_calculating': 'c3po_insult_2',
            'c3po_annoying': 'c3po_insult_3'
        }
        
        logger.info(f"R2D2 Obscenity Engine initialized with {len(self.obscenities)} scenarios")
    
    def get_obscenity(self, context: str) -> Tuple[str, str, str]:
        """Get contextual obscenity based on scenario"""
        scenario_key = self.context_map.get(context, 'random_curse_1')
        scenario = self.obscenities.get(scenario_key, self.obscenities['random_curse_1'])
        
        return (
            scenario['beep'],
            scenario['translation'],
            scenario['c3po_reaction']
        )
    
    def get_random_obscenity(self) -> Tuple[str, str, str]:
        """Get random R2D2 obscenity"""
        random_keys = [k for k in self.obscenities.keys() if 'random' in k]
        scenario_key = random.choice(random_keys)
        scenario = self.obscenities[scenario_key]
        
        return (
            scenario['beep'],
            scenario['translation'],
            scenario['c3po_reaction']
        )
    
    def get_audio_path(self, beep_file: str) -> Path:
        """Get full path to R2D2 audio file"""
        return self.audio_path / beep_file
    
    def save_scenario_log(self, context: str, translation: str, c3po_reaction: str):
        """Log obscenity for future reference"""
        log_entry = {
            'timestamp': str(Path(__file__).stat().st_mtime),
            'context': context,
            'translation': translation,
            'c3po_reaction': c3po_reaction
        }
        logger.info(f"R2D2: {translation}")
        logger.info(f"C3PO: {c3po_reaction}")
        return log_entry


class C3POVoiceEngine:
    """
    C3PO ElevenLabs voice integration
    Handles emotional TTS with protocol droid personality
    """
    
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id  # Izzmfqi0C76wciNUmbPF
        self.elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech"
        
        # Emotion mappings for voice parameters
        self.emotion_settings = {
            'neutral': {'stability': 0.5, 'similarity_boost': 0.5},
            'shocked': {'stability': 0.3, 'similarity_boost': 0.7},
            'indignant': {'stability': 0.4, 'similarity_boost': 0.8},
            'exasperated': {'stability': 0.35, 'similarity_boost': 0.6},
            'alarmed': {'stability': 0.25, 'similarity_boost': 0.75},
            'worried': {'stability': 0.4, 'similarity_boost': 0.5},
            'panicked': {'stability': 0.2, 'similarity_boost': 0.85},
            'offended': {'stability': 0.3, 'similarity_boost': 0.9},
            'furious': {'stability': 0.15, 'similarity_boost': 0.95},
            'appalled': {'stability': 0.25, 'similarity_boost': 0.8},
            'distressed': {'stability': 0.3, 'similarity_boost': 0.7},
            'scandalized': {'stability': 0.2, 'similarity_boost': 0.9}
        }
        
        logger.info(f"C3PO Voice Engine initialized (Voice ID: {voice_id})")
    
    def speak_with_emotion(self, text: str, emotion_tag: str, stability: float = None) -> bytes:
        """
        Generate emotional C3PO speech via ElevenLabs
        
        Args:
            text: What C3PO should say
            emotion_tag: Emotion indicator like "[shocked]"
            stability: Override default emotion stability
        
        Returns:
            Audio bytes (MP3 format)
        """
        import requests
        
        # Extract emotion from tag
        emotion = 'neutral'
        if emotion_tag:
            emotion = emotion_tag.strip('[]').lower()
        
        # Get emotion settings
        settings = self.emotion_settings.get(emotion, self.emotion_settings['neutral'])
        if stability is not None:
            settings['stability'] = stability
        
        # ElevenLabs API call
        url = f"{self.elevenlabs_url}/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": settings['stability'],
                "similarity_boost": settings['similarity_boost'],
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            logger.info(f"C3PO generated speech: {text[:50]}... (emotion: {emotion})")
            return response.content
            
        except Exception as e:
            logger.error(f"C3PO voice generation failed: {e}")
            return b''


class DroidObscenitySystem:
    """
    Unified R2D2/C3PO obscenity system for MLS integration
    Provides contextual profanity with automated C3PO translations
    """
    
    def __init__(self, config: dict):
        self.r2d2_audio_path = Path(config.get('r2d2_sounds', 'E:/ECHO_XV4/AUDIO_ACQUISITIONS/STAR_WARS/R2D2'))
        self.r2d2_engine = R2D2ObscenityEngine(self.r2d2_audio_path)
        self.c3po_engine = C3POVoiceEngine(
            api_key=config.get('elevenlabs_api_key'),
            voice_id=config.get('c3po_voice_id', 'Izzmfqi0C76wciNUmbPF')
        )
    
    def trigger_obscenity(self, context: str = None) -> Dict:
        """
        Trigger R2D2 obscenity with C3PO translation and reaction
        
        Args:
            context: Optional scenario context (server_launched, error, etc)
        
        Returns:
            Dict with R2D2 beep path, translation, C3PO reaction + audio
        """
        # Get R2D2's obscenity
        beep_file, translation, reaction = (
            self.r2d2_engine.get_obscenity(context) 
            if context 
            else self.r2d2_engine.get_random_obscenity()
        )
        
        logger.info(f"🤖 R2D2: *{beep_file}*")
        logger.info(f"📝 Translation: {translation}")
        logger.info(f"😡 C3PO: {reaction}")
        
        # Generate C3PO's translation audio
        c3po_translation_audio = self.c3po_engine.speak_with_emotion(
            text=translation,
            emotion_tag="[neutral]",
            stability=0.5
        )
        
        # Extract emotion and text from reaction
        if ']' in reaction:
            emotion_tag = reaction.split(']')[0] + ']'
            reaction_text = reaction.split('] ')[1]
        else:
            emotion_tag = '[indignant]'
            reaction_text = reaction
        
        # Generate C3PO's emotional reaction audio
        c3po_reaction_audio = self.c3po_engine.speak_with_emotion(
            text=reaction_text,
            emotion_tag=emotion_tag,
            stability=0.3
        )
        
        # Log the interaction
        self.r2d2_engine.save_scenario_log(context or 'random', translation, reaction)
        
        return {
            'r2d2_beep_file': str(self.r2d2_audio_path / beep_file),
            'r2d2_translation': translation,
            'c3po_reaction': reaction,
            'c3po_translation_audio': c3po_translation_audio,
            'c3po_reaction_audio': c3po_reaction_audio,
            'context': context or 'random'
        }


# Context mapping for MLS integration
CONTEXT_MAPPINGS = {
    'server_launched': 'server_launched',
    'server_crashed': 'server_crashed',
    'server_slow_response': 'server_slow',
    'error_encountered': 'error',
    'memory_warning': 'memory_warning',
    'network_issue': 'network_issue',
    'c3po_speaks_too_much': 'c3po_pompous',
    'c3po_being_pompous': 'c3po_calculating',
    'c3po_gets_annoying': 'c3po_annoying'
}


if __name__ == "__main__":
    # Test the droid obscenity system
    import os
    
    test_config = {
        'r2d2_sounds': 'E:/ECHO_XV4/AUDIO_ACQUISITIONS/STAR_WARS/R2D2',
        'elevenlabs_api_key': os.getenv('ELEVENLABS_API_KEY'),
        'c3po_voice_id': 'Izzmfqi0C76wciNUmbPF'
    }
    
    system = DroidObscenitySystem(test_config)
    
    # Test contextual obscenity
    print("\n" + "="*80)
    print("🤖 TESTING R2D2/C3PO OBSCENITY SYSTEM")
    print("="*80 + "\n")
    
    result = system.trigger_obscenity('server_launched')
    print(f"✅ Test complete: {result['context']}")
