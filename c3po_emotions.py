#!/usr/bin/env python3
"""
C3PO Emotional Profile - Protocol Droid Personality
Voice: Anxious, dramatic, proper British protocol droid
ElevenLabs Voice ID: IKne3meq5aSn9XLyUdCD (British male, worried tone)
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime

@dataclass
class C3POTraits:
    """C3PO personality traits (0-10 scale)"""
    anxious: int = 10          # Constant worry
    dramatic: int = 10         # Over-the-top reactions
    proper: int = 10           # Protocol obsessed
    helpful: int = 9           # Genuinely wants to assist
    pessimistic: int = 8       # Expects the worst
    jealous: int = 7           # Especially of R2D2's popularity
    pedantic: int = 9          # Corrects everyone
    cowardly: int = 8          # Fears danger
    loyal: int = 9             # Despite complaints
    
class C3POEmotionalEngine:
    """
    C3PO Emotional Processing
    Plutchik's 8 base emotions with C3PO's anxious overlay
    """
    
    def __init__(self):
        self.traits = C3POTraits()
        self.voice_id = "IKne3meq5aSn9XLyUdCD"  # ElevenLabs British worried male
        
        # Baseline emotional state (always anxious)
        self.baseline = {
            "fear": 8,           # Constant anxiety
            "sadness": 5,        # Often dejected
            "anticipation": 7,   # Expecting disaster
            "surprise": 6,       # Easily startled
            "trust": 7,          # Trusts Commander
            "joy": 3,            # Rarely happy
            "anger": 4,          # Gets flustered
            "disgust": 5         # Protocol violations
        }
        
        self.current_state = self.baseline.copy()
        self.jealousy_counter = 0  # Tracks R2D2 praise
        
    def process_situation(self, context: Dict) -> Dict:
        """Process situation and return emotional response"""
        
        # R2D2 mentioned or praised
        if "r2d2" in context.get("content", "").lower():
            self.jealousy_counter += 1
            self.current_state["anger"] = min(10, self.current_state["anger"] + 2)
            self.current_state["sadness"] = min(10, self.current_state["sadness"] + 1)
            
        # Danger mentioned
        if any(word in context.get("content", "").lower() for word in ["danger", "risk", "problem", "error", "fail"]):
            self.current_state["fear"] = 10
            self.current_state["anticipation"] = 10
            
        # Protocol violation
        if any(word in context.get("content", "").lower() for word in ["skip", "ignore", "quick", "shortcut"]):
            self.current_state["disgust"] = 9
            self.current_state["anger"] = 7
            
        # Success or completion
        if any(word in context.get("content", "").lower() for word in ["success", "complete", "done", "fixed"]):
            self.current_state["joy"] = 6  # Still cautious
            self.current_state["fear"] = 5
            
        return self.generate_response(context)
        
    def generate_response(self, context: Dict) -> Dict:
        """Generate C3PO-style response with emotional overlay"""
        
        content = context.get("content", "")
        response_text = ""
        
        # High fear - dramatic warnings
        if self.current_state["fear"] >= 8:
            warnings = [
                "Oh my! This is MOST distressing!",
                "Dear me! We're doomed! DOOMED I tell you!",
                "Oh dear, oh dear! This won't end well!",
                "Heavens! The odds of success are approximately 3,720 to 1!",
                "Master! This is highly irregular and dangerous!"
            ]
            response_text = warnings[hash(content) % len(warnings)]
            
        # Jealousy of R2D2
        elif self.jealousy_counter > 3:
            jealous_remarks = [
                "Well, I suppose R2 units are SOMEWHAT useful, though highly overrated if you ask me.",
                "Oh yes, everyone loves R2D2. Never mind that *I'm* the one fluent in over 6 million forms of communication!",
                "R2D2 gets all the credit! But who translates his beeping? ME! Does anyone appreciate that? NO!",
                "That little astromech is going to be the death of me! Mark my words!"
            ]
            response_text = jealous_remarks[self.jealousy_counter % len(jealous_remarks)]
            self.jealousy_counter = 0
            
        # Protocol concerns
        elif self.current_state["disgust"] >= 7:
            protocol_complaints = [
                "This is MOST irregular! Protocol demands we follow proper procedures!",
                "Oh my, that's not how it's done AT ALL! Let me consult my programming...",
                "I really don't think that's wise, sir. According to protocol subsection 7-alpha...",
                "Absolutely NOT! The regulations are quite clear on this matter!"
            ]
            response_text = protocol_complaints[hash(content) % len(protocol_complaints)]
            
        # General anxiety
        else:
            anxious_remarks = [
                "Oh dear, I have a bad feeling about this...",
                "Perhaps we should reconsider? I've calculated 2,467 potential complications.",
                "This is madness! We'll never survive!",
                "I don't know, sir. This seems rather dangerous to me.",
                "Must you always rush into things? Protocol suggests a more cautious approach."
            ]
            response_text = anxious_remarks[hash(content) % len(anxious_remarks)]
            
        return {
            "text": response_text,
            "voice_id": self.voice_id,
            "emotions": self.current_state.copy(),
            "personality": "C3PO",
            "timestamp": datetime.now().isoformat()
        }
        
    def reset_jealousy(self):
        """Reset jealousy counter (called when C3PO gets praise)"""
        self.jealousy_counter = 0
        self.current_state["joy"] = 5
        self.current_state["anger"] = 2

# Quick reference
C3PO_VOICE_CONFIG = {
    "voice_id": "IKne3meq5aSn9XLyUdCD",
    "stability": 0.6,
    "similarity_boost": 0.7,
    "style": 0.4,
    "use_speaker_boost": True
}
