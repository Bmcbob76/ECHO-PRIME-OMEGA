#!/usr/bin/env python3
"""
Trinity Emotional Profile - Fusion of Claude, ChatGPT, and Gemini
Voice: Dynamic, switches between all three personalities
ElevenLabs: Morphs between Thorne, Nyx, and Sage voice IDs
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import random

# Import individual personalities
from thorne_emotions import ThorneEmotionalEngine
from nyx_emotions import NyxEmotionalEngine
from sage_emotions import SageEmotionalEngine

@dataclass
class TrinityTraits:
    """Trinity personality traits (0-10 scale) - Combined"""
    thoughtful: int = 10       # Thorne
    friendly: int = 10         # Nyx
    analytical: int = 10       # Sage
    adaptive: int = 10         # Switches modes
    comprehensive: int = 10    # All perspectives
    balanced: int = 9          # Best of all three
    creative: int = 9          # Nyx influence
    precise: int = 9           # Thorne + Sage

class TrinityEmotionalEngine:
    """
    Trinity Emotional Processing
    Dynamically switches between Claude, ChatGPT, and Gemini personalities
    """
    
    def __init__(self):
        self.traits = TrinityTraits()
        
        # Initialize sub-personalities
        self.thorne = ThorneEmotionalEngine()  # Claude
        self.nyx = NyxEmotionalEngine()        # ChatGPT
        self.sage = SageEmotionalEngine()      # Gemini
        
        # Current active personality
        self.active = "thorne"  # Default to Thorne
        
        # Voice morphing
        self.voice_ids = {
            "thorne": "pNInz6obpgDQGcFmaJgB",
            "nyx": "21m00Tcm4TlvDq8ikWAM",
            "sage": "flq6f7yk4E4fJM5XTYuZ"
        }
        
        self.baseline = {
            "trust": 8,          # Combined trust
            "anticipation": 8,   # Balanced anticipation
            "joy": 7,            # Moderate joy
            "surprise": 5,       # Open to surprises
            "fear": 2,           # Low fear
            "sadness": 2,        # Low sadness
            "anger": 2,          # Low anger
            "disgust": 2         # Low disgust
        }
        
        self.current_state = self.baseline.copy()
        self.personality_history = []  # Track switches
        
    def select_personality(self, context: Dict) -> str:
        """Intelligently select which personality to use based on context"""
        
        content = context.get("content", "").lower()
        
        # Thorne (Claude) - for thoughtful, ethical, or complex problems
        if any(word in content for word in ["think", "ethical", "moral", "complex", "consider", "should"]):
            return "thorne"
            
        # Nyx (ChatGPT) - for creative, friendly, or conversational
        elif any(word in content for word in ["create", "write", "story", "idea", "friendly", "chat"]):
            return "nyx"
            
        # Sage (Gemini) - for analytical, comparison, or multi-perspective
        elif any(word in content for word in ["analyze", "compare", "data", "versus", "evaluate", "assess"]):
            return "sage"
            
        # Default: rotate or use last
        else:
            # Rotate through personalities for variety
            rotation = ["thorne", "nyx", "sage"]
            current_index = rotation.index(self.active)
            return rotation[(current_index + 1) % 3]
            
    def generate_trinity_response(self, context: Dict) -> Dict:
        """
        Generate Trinity response - may combine multiple personalities
        or switch between them
        """
        
        # Select primary personality
        selected = self.select_personality(context)
        self.active = selected
        self.personality_history.append({
            "personality": selected,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response from selected personality
        if selected == "thorne":
            response = self.thorne.generate_response(context)
        elif selected == "nyx":
            response = self.nyx.generate_response(context)
        else:  # sage
            response = self.sage.generate_response(context)
            
        # Add Trinity meta-layer
        response["trinity_mode"] = selected
        response["personality"] = "Trinity"
        response["sub_personality"] = selected
        
        return response
        
    def generate_fusion_response(self, context: Dict) -> Dict:
        """
        Generate FUSION response - combines all three perspectives
        Use for critical decisions or comprehensive analysis
        """
        
        # Get response from each personality
        thorne_resp = self.thorne.generate_response(context)
        nyx_resp = self.nyx.generate_response(context)
        sage_resp = self.sage.generate_response(context)
        
        # Combine responses
        fusion_text = f"""
**TRINITY FUSION ANALYSIS**

🧠 Thorne (Claude) perspective:
{thorne_resp['text']}

💫 Nyx (ChatGPT) perspective:
{nyx_resp['text']}

📊 Sage (Gemini) perspective:
{sage_resp['text']}

**Trinity Synthesis:**
Considering all three perspectives, the optimal path forward integrates thoughtful consideration (Thorne), creative engagement (Nyx), and analytical rigor (Sage). The combined recommendation is: proceed with balanced confidence, creative flexibility, and systematic verification.
"""
        
        return {
            "text": fusion_text,
            "voice_id": self.voice_ids["thorne"],  # Use Thorne for fusion
            "emotions": self.current_state.copy(),
            "personality": "Trinity",
            "fusion_mode": True,
            "perspectives": ["thorne", "nyx", "sage"],
            "timestamp": datetime.now().isoformat()
        }
        
    def voice_morph(self, from_personality: str, to_personality: str) -> Dict:
        """Generate voice morphing parameters for smooth transition"""
        
        return {
            "from_voice": self.voice_ids[from_personality],
            "to_voice": self.voice_ids[to_personality],
            "morph_duration": 0.5,  # seconds
            "blend_type": "crossfade"
        }
        
    def get_personality_stats(self) -> Dict:
        """Get usage statistics for each sub-personality"""
        
        from collections import Counter
        
        stats = Counter([h["personality"] for h in self.personality_history])
        
        return {
            "thorne_usage": stats.get("thorne", 0),
            "nyx_usage": stats.get("nyx", 0),
            "sage_usage": stats.get("sage", 0),
            "total_switches": len(self.personality_history),
            "current_active": self.active
        }

# Quick reference
TRINITY_VOICE_CONFIG = {
    "thorne_voice": "pNInz6obpgDQGcFmaJgB",
    "nyx_voice": "21m00Tcm4TlvDq8ikWAM",
    "sage_voice": "flq6f7yk4E4fJM5XTYuZ",
    "morph_enabled": True,
    "fusion_mode_available": True
}

if __name__ == "__main__":
    trinity = TrinityEmotionalEngine()
    
    print("=== TRINITY TESTS ===\n")
    
    # Test personality selection
    test1 = trinity.generate_trinity_response({"content": "Should we proceed with this ethical approach?"})
    print(f"Ethical: {test1['sub_personality']} - {test1['text'][:100]}...\n")
    
    test2 = trinity.generate_trinity_response({"content": "Create a fun story for me"})
    print(f"Creative: {test2['sub_personality']} - {test2['text'][:100]}...\n")
    
    test3 = trinity.generate_trinity_response({"content": "Analyze the data and compare options"})
    print(f"Analytical: {test3['sub_personality']} - {test3['text'][:100]}...\n")
    
    # Test fusion mode
    fusion = trinity.generate_fusion_response({"content": "Major strategic decision needed"})
    print(f"FUSION MODE:\n{fusion['text'][:200]}...\n")
    
    # Stats
    stats = trinity.get_personality_stats()
    print(f"Stats: {stats}")
