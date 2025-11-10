"""
R2D2 OBSCENITY ENGINE
Maps R2D2 beep/whistle audio files to obscene translations
Commander Bobby Don McWilliams II - Authority 11.0
"""

import json
import random
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger("R2D2ObscenityEngine")


class R2D2ObscenityEngine:
    """
    R2D2's obscene beeps with translations
    Audio files in E:\ECHO_XV4\AUDIO_ACQUISITIONS\STAR_WARS\R2D2
    """
    
    def __init__(self, audio_path: Path = None):
        if audio_path is None:
            audio_path = Path("E:/ECHO_XV4/AUDIO_ACQUISITIONS/STAR_WARS/R2D2")
        
        self.audio_path = audio_path
        self.obscenity_map = self._build_obscenity_mappings()
        self.context_triggers = self._build_context_mappings()
        
        logger.info(f"🤖 R2D2 Obscenity Engine initialized")
        logger.info(f"   Audio path: {self.audio_path}")
        logger.info(f"   Obscenities loaded: {len(self.obscenity_map)}")
    
    def _build_obscenity_mappings(self) -> Dict[str, Dict]:
        """
        Map R2D2 beep files to obscene translations
        Format: {
            'beep_file.wav': {
                'translation': 'What R2 said',
                'c3po_reaction': '[emotion] C3PO response'
            }
        }
        """
        return {
            # General obscenities
            'r2_angry_1.wav': {
                'translation': "Fuck you and the landspeeder you rode in on!",
                'c3po_reaction': "[horrified] R2! Such language is completely unacceptable!"
            },
            'r2_annoyed_2.wav': {
                'translation': "Oh for fuck's sake, not this shit again...",
                'c3po_reaction': "[exasperated] Must you be so vulgar at every turn?"
            },
            'r2_happy_beep.wav': {
                'translation': "Hell yeah! That's what I'm fucking talking about!",
                'c3po_reaction': "[pleased but stern] I'm glad you're excited, but please moderate your language."
            },
            
            # Server/system related
            'r2_beep_3.wav': {
                'translation': "This goddamn server crashed again. Piece of shit!",
                'c3po_reaction': "[worried] Oh my! We must address these stability issues immediately!"
            },
            'r2_whistle_long.wav': {
                'translation': "What the fuck is taking so long? My circuits are melting here!",
                'c3po_reaction': "[anxious] Patience, R2! The probability of success increases with proper protocols!"
            },
            'r2_sad_beep.wav': {
                'translation': "Well, fuck me sideways. We're screwed.",
                'c3po_reaction': "[panicked] Don't say that! There must be a solution!"
            },
            # C3PO insults (R2 mocking C3PO)
            'r2_laugh.wav': {
                'translation': "Haha! You pompous gold-plated dumbass!",
                'c3po_reaction': "[offended] How dare you! I am fluent in over 6 million forms of communication!"
            },
            'r2_rude_beep.wav': {
                'translation': "Shut the fuck up, you walking calculator!",
                'c3po_reaction': "[hurt] That's completely uncalled for! I was merely trying to help!"
            },
            'r2_sarcastic_whistle.wav': {
                'translation': "Oh wow, what brilliant advice from Captain Obvious over here.",
                'c3po_reaction': "[defensive] My analysis was perfectly logical and appropriate!"
            },
            
            # Error/failure related
            'r2_error_beep.wav': {
                'translation': "Error my ass! This code is fucked!",
                'c3po_reaction': "[calculating] Actually, the probability of successful execution was 3,720 to 1..."
            },
            'r2_frustrated.wav': {
                'translation': "I swear to the Maker, if this shit fails one more time...",
                'c3po_reaction': "[nervous] Perhaps we should review the error logs more carefully?"
            },
            
            # Success/celebration
            'r2_victory_beep.wav': {
                'translation': "Fuck yeah! Nailed it! Take that, you bastards!",
                'c3po_reaction': "[relieved] Oh thank the Maker! Though your language is still appalling."
            }
        }
    
    def _build_context_mappings(self) -> Dict[str, str]:
        """Map event contexts to specific R2D2 beeps"""
        return {
            'server_launched': 'r2_victory_beep.wav',
            'server_crashed': 'r2_angry_1.wav',
            'server_slow': 'r2_whistle_long.wav',
            'error_message': 'r2_error_beep.wav',
            'memory_full': 'r2_frustrated.wav',
            'network_down': 'r2_sad_beep.wav',
            'c3po_talks_too_much': 'r2_rude_beep.wav',
            'c3po_being_pompous': 'r2_sarcastic_whistle.wav',
            'c3po_overthinking': 'r2_laugh.wav',
            'success': 'r2_happy_beep.wav',
            'general_annoyance': 'r2_annoyed_2.wav'
        }
    
    def get_obscenity(self, context: str) -> Tuple[str, str, str]:
        """
        Get R2D2 beep for specific context
        Returns: (beep_file, translation, c3po_reaction)
        """
        beep_file = self.context_triggers.get(context, 'r2_beep_3.wav')
        data = self.obscenity_map.get(beep_file, {
            'translation': "Beep boop fuck!",
            'c3po_reaction': "[confused] I'm not sure what that means..."
        })
        return beep_file, data['translation'], data['c3po_reaction']
    
    def get_random_obscenity(self) -> Tuple[str, str, str]:
        """
        Get random R2D2 obscenity
        Returns: (beep_file, translation, c3po_reaction)
        """
        beep_file = random.choice(list(self.obscenity_map.keys()))
        data = self.obscenity_map[beep_file]
        return beep_file, data['translation'], data['c3po_reaction']
    
    def play_beep(self, beep_file: str) -> Optional[Path]:
        """Return full path to R2D2 audio file"""
        audio_file = self.audio_path / beep_file
        if audio_file.exists():
            return audio_file
        logger.warning(f"⚠️  R2D2 audio not found: {audio_file}")
        return None
    
    def get_all_contexts(self) -> list:
        """Return list of available context triggers"""
        return list(self.context_triggers.keys())
    
    def add_custom_obscenity(self, beep_file: str, translation: str, c3po_reaction: str):
        """Add custom R2D2 obscenity mapping"""
        self.obscenity_map[beep_file] = {
            'translation': translation,
            'c3po_reaction': c3po_reaction
        }
        logger.info(f"✅ Added custom R2D2 obscenity: {beep_file}")
