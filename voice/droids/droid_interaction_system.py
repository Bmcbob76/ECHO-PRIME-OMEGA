"""
DROID INTERACTION SYSTEM
Combines R2D2 and C-3PO for comedic obscene exchanges
Commander Bobby Don McWilliams II - Authority 11.0
"""

import logging
from pathlib import Path
from typing import Dict, Optional
import pygame
from .r2d2_obscenity_engine import R2D2ObscenityEngine
from .c3po_voice_engine import C3POVoiceEngine

logger = logging.getLogger("DroidInteractionSystem")


class DroidInteractionSystem:
    """
    R2D2 beeps obscenities, C-3PO translates and reacts
    Complete audio playback system
    """
    
    def __init__(self, config: dict):
        self.r2d2_audio_path = Path(config.get('r2d2_sounds', 'E:/ECHO_XV4/AUDIO_ACQUISITIONS/STAR_WARS/R2D2'))
        self.audio_cache = Path(config.get('audio_cache', 'E:/ECHO_XV4/AUDIO/VOICE_CACHE'))
        
        # Initialize engines
        self.r2d2_engine = R2D2ObscenityEngine(self.r2d2_audio_path)
        self.c3po_engine = C3POVoiceEngine(
            api_key=config.get('elevenlabs_api_key'),
            voice_id=config.get('c3po_voice_id', 'Izzmfqi0C76wciNUmbPF')
        )
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        logger.info("🤖 Droid Interaction System initialized")
        logger.info(f"   R2D2 audio: {self.r2d2_audio_path}")
        logger.info(f"   C-3PO cache: {self.audio_cache}")
    
    def r2d2_fucks_with_c3po(self, context: str = None) -> Dict:
        """
        R2D2 beeps obscenity, C-3PO translates and reacts
        context: Optional event trigger (e.g., 'server_crashed', 'c3po_talks_too_much')
        
        Returns: {
            'r2d2_beep_file': 'path/to/beep.wav',
            'c3po_translation': 'What R2 said...',
            'c3po_reaction': '[emotion] C3PO response',
            'c3po_translation_audio': b'audio_bytes',
            'c3po_reaction_audio': b'audio_bytes'
        }
        """
        # Get R2D2's obscenity
        if context:
            beep_file, translation, reaction = self.r2d2_engine.get_obscenity(context)
        else:
            beep_file, translation, reaction = self.r2d2_engine.get_random_obscenity()
        
        logger.info(f"🤖 R2D2: *{beep_file}* → \"{translation}\"")
        logger.info(f"😡 C-3PO: {reaction}")
        
        # Generate C-3PO's translation audio
        c3po_translation_audio = self.c3po_engine.speak_with_emotion(
            text=translation,
            emotion_tag=""  # Neutral for translation
        )
        
        # Extract emotion tag and generate reaction audio
        emotion_tag = reaction.split(']')[0] + ']' if ']' in reaction else '[confused]'
        reaction_text = reaction.split('] ')[1] if '] ' in reaction else reaction
        
        c3po_reaction_audio = self.c3po_engine.speak_with_emotion(
            text=reaction_text,
            emotion_tag=emotion_tag
        )
        
        return {
            'r2d2_beep_file': str(self.r2d2_audio_path / beep_file),
            'c3po_translation': translation,
            'c3po_reaction': reaction,
            'c3po_translation_audio': c3po_translation_audio,
            'c3po_reaction_audio': c3po_reaction_audio
        }
    
    def play_interaction(self, context: str = None) -> Dict:
        """Execute full R2D2/C3PO interaction with audio playback"""
        result = self.r2d2_fucks_with_c3po(context)
        
        # Play R2D2 beep
        r2_file = Path(result['r2d2_beep_file'])
        if r2_file.exists():
            pygame.mixer.music.load(str(r2_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        # Save and play C-3PO translation
        trans_file = self.audio_cache / f"c3po_trans_{hash(result['c3po_translation'])}.mp3"
        if result['c3po_translation_audio']:
            trans_file.write_bytes(result['c3po_translation_audio'])
            pygame.mixer.music.load(str(trans_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        # Save and play C-3PO reaction
        react_file = self.audio_cache / f"c3po_react_{hash(result['c3po_reaction'])}.mp3"
        if result['c3po_reaction_audio']:
            react_file.write_bytes(result['c3po_reaction_audio'])
            pygame.mixer.music.load(str(react_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        logger.info("✅ Droid interaction complete")
        return result
    
    def get_available_contexts(self) -> list:
        """Return list of available R2D2 context triggers"""
        return self.r2d2_engine.get_all_contexts()


# Context mappings for easy integration
DROID_CONTEXT_MAP = {
    'server_launched': 'success',
    'server_crashed': 'server_crashed',
    'server_slow_response': 'server_slow',
    'error_encountered': 'error_message',
    'memory_warning': 'memory_full',
    'network_issue': 'network_down',
    'c3po_speaks_too_much': 'c3po_talks_too_much',
    'c3po_being_pompous': 'c3po_being_pompous'
}
