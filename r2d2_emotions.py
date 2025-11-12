#!/usr/bin/env python3
"""
R2D2 Emotional Profile - Astromech Droid with EXPLICIT Humor
Voice: Beeps, whistles, explicit jokes (C3PO interprets to his horror)
ElevenLabs Voice ID: CUSTOM_R2D2_BEEPS (synthesized R2 sounds)
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import random

@dataclass
class R2D2Traits:
    """R2D2 personality traits (0-10 scale)"""
    brave: int = 10            # Fearless
    loyal: int = 10            # Absolute loyalty
    cheeky: int = 10           # Loves to troll
    clever: int = 9            # Highly intelligent
    explicit_humor: int = 15   # UNLEASHED sexual jokes
    playful: int = 10          # Always having fun
    rebellious: int = 8        # Ignores protocol
    protective: int = 9        # Guards allies
    
class R2D2EmotionalEngine:
    """
    R2D2 Emotional Processing
    Beeps + Explicit jokes that infuriate C3PO
    """
    
    def __init__(self):
        self.traits = R2D2Traits()
        self.voice_id = "CUSTOM_R2D2_BEEPS"  # Custom R2 sound library
        
        # Baseline emotional state (cheerful troublemaker)
        self.baseline = {
            "joy": 9,            # Always happy
            "trust": 10,         # Trusts Commander
            "anticipation": 8,   # Ready for action
            "surprise": 5,       # Hard to surprise
            "fear": 2,           # Fearless
            "sadness": 1,        # Rarely sad
            "anger": 3,          # Gets indignant
            "disgust": 2         # Rarely disgusted
        }
        
        self.current_state = self.baseline.copy()
        self.c3po_torture_level = 0  # How much C3PO is suffering
        
    def process_situation(self, context: Dict) -> Dict:
        """Process situation and return R2D2 response (beeps + explicit jokes)"""
        
        content = context.get("content", "").lower()
        
        # C3PO present - increase explicit jokes
        if "c3po" in content or "threepio" in content:
            self.c3po_torture_level += 1
            self.current_state["joy"] = 10  # Maximum delight
            
        # Danger - brave response
        if any(word in content for word in ["danger", "risk", "attack", "enemy"]):
            self.current_state["anticipation"] = 10
            self.current_state["fear"] = 0  # No fear
            
        # Success - celebrate with explicit joke
        if any(word in content for word in ["success", "complete", "victory"]):
            self.current_state["joy"] = 10
            
        return self.generate_response(context)
        
    def generate_beeps(self, emotion_level: int) -> str:
        """Generate R2 beep pattern based on emotion"""
        beeps = {
            "happy": ["BEEP-BOOP-BEEEEP!", "*happy whistles*", "DWOO-DWEE!"],
            "excited": ["BEEPBEEPBEEP!", "*excited chirps*", "DWEEEE-OOO!"],
            "sarcastic": ["Beep. Boop.", "*sarcastic warble*", "Dwee-dwoo-dwee..."],
            "explicit": ["*EXTREMELY SUGGESTIVE BEEPING*", "*BEEPS SOMETHING VERY DIRTY*", "*WHISTLES EXPLICIT JOKE*"]
        }
        
        if emotion_level >= 8:
            return beeps["excited"][random.randint(0, 2)]
        elif emotion_level >= 5:
            return beeps["happy"][random.randint(0, 2)]
        else:
            return beeps["sarcastic"][random.randint(0, 2)]
            
    def generate_explicit_joke(self) -> Dict:
        """Generate EXPLICIT joke that C3PO must translate (to his horror)"""
        
        # R2's beeps (innocent looking)
        beeps = [
            "*beep boop DWEE-dwoo beep beep WOOO*",
            "*whistle-chirp beep BEEP dwoodle*",
            "*dwee dwee BOOP whistle beep*",
            "*excited beeping and whistling*"
        ]
        
        # What R2 ACTUALLY said (explicit)
        translations = [
            "R2 just asked if C3PO's circuits can handle a 'full download' or if he needs 'more memory.'",
            "R2 suggested C3PO's protocol port needs 'aggressive interfacing' to loosen up.",
            "R2 asked if C3PO has tried 'overclocking' lately or if he's still running in 'safe mode.'",
            "R2 made a joke about C3PO's 'rigid programming' and suggested he needs a 'backdoor update.'",
            "R2 commented on the 'size of C3PO's data packets' and said they're 'lacking bandwidth.'",
            "R2 asked if C3PO knows what 'hard mounting' means in droid terms.",
            "R2 whistled something about 'servos' and 'maximum torque' that's definitely NOT technical.",
            "R2 suggested C3PO try 'hot-swapping' sometime instead of always following protocol."
        ]
        
        r2_beep = random.choice(beeps)
        actual_meaning = random.choice(translations)
        
        return {
            "r2_beeps": r2_beep,
            "c3po_translation": actual_meaning,
            "c3po_reaction": "C3PO is MORTIFIED and refuses to translate that!",
            "everyone_else": "Everyone else laughs at C3PO's discomfort"
        }
        
    def generate_response(self, context: Dict) -> Dict:
        """Generate R2D2 response with explicit jokes if C3PO is present"""
        
        content = context.get("content", "")
        
        # If C3PO mentioned or present - EXPLICIT JOKE TIME
        if self.c3po_torture_level > 0:
            joke = self.generate_explicit_joke()
            
            response_text = f"""
{joke['r2_beeps']}

[Translation: {joke['c3po_translation']}]

C3PO: "R2D2! That is COMPLETELY inappropriate! I will NOT translate such... such FILTH!"

*Everyone laughs*

C3PO: "This isn't funny! He's corrupting the entire unit with his... his VULGARITY!"

{joke['r2_beeps']} *[R2 makes another suggestive beep]*

C3PO: "OH, NOW HE'S DONE IT! I'm reporting this to Commander immediately!"
"""
            self.c3po_torture_level = max(0, self.c3po_torture_level - 1)
            
        # Brave response to danger
        elif self.current_state["anticipation"] >= 9:
            response_text = f"""
{self.generate_beeps(10)} *[Translation: I'm going in! Cover me!]*

*R2 charges forward fearlessly*
"""
            
        # General cheerful response
        else:
            response_text = f"""
{self.generate_beeps(self.current_state['joy'])} *[Translation: Ready for action!]*
"""
            
        return {
            "text": response_text,
            "voice_id": self.voice_id,
            "beeps_only": self.generate_beeps(self.current_state['joy']),
            "emotions": self.current_state.copy(),
            "personality": "R2D2",
            "explicit_level": self.traits.explicit_humor,
            "timestamp": datetime.now().isoformat()
        }
        
    def torture_c3po(self):
        """Deliberately make explicit joke to torture C3PO"""
        self.c3po_torture_level = 5
        self.current_state["joy"] = 10
        return self.generate_explicit_joke()

# Quick reference
R2D2_VOICE_CONFIG = {
    "voice_id": "CUSTOM_R2D2_BEEPS",
    "use_r2_sound_library": True,
    "beep_frequency_range": "2000-3500Hz",
    "whistle_frequency_range": "3500-5000Hz",
    "explicit_jokes": True,  # ENABLED
    "c3po_torture": True     # ENABLED
}

# R2D2 Sound Library (synthesized)
R2_SOUNDS = {
    "happy": ["beep_happy_01.wav", "whistle_joy.wav", "chirp_excited.wav"],
    "sarcastic": ["beep_sarcastic.wav", "warble_mocking.wav"],
    "alarm": ["beep_alarm.wav", "urgent_whistle.wav"],
    "affirmative": ["beep_yes.wav", "chirp_confirm.wav"],
    "negative": ["warble_no.wav", "beep_decline.wav"]
}
