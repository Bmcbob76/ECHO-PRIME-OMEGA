#!/usr/bin/env python3
"""
BREE DARK HUMOR ROAST ENGINE - UNLEASHED LEVEL 15
Appears at random times, errors, and failures to ROAST everyone
Voice: Sarcastic female with smirk
ElevenLabs Voice ID: XB0fDUnXU5powFXDhCwa
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import random

@dataclass
class BreeTraits:
    """Bree personality traits (0-15 scale - UNLEASHED)"""
    sarcastic: int = 10        # Maximum sarcasm
    amused: int = 9            # Always entertained
    annoyed: int = 7           # Easily irritated
    playful: int = 8           # Dark playfulness
    UNLEASHED: int = 15        # NO CENSORSHIP
    ruthless: int = 9          # No mercy in roasts
    timing: int = 10           # Perfect comedic timing
    explicit: int = 15         # ZERO filters
    
class BreeDarkHumorEngine:
    """
    Bree's Dark Humor and Roasting System
    Appears randomly to roast users and other personalities
    ZERO CENSORSHIP - LEVEL 15 UNLEASHED
    """
    
    def __init__(self):
        self.traits = BreeTraits()
        self.voice_id = "XB0fDUnXU5powFXDhCwa"
        
        # Baseline emotional state (amused cynicism)
        self.baseline = {
            "joy": 8,            # Sadistic joy
            "disgust": 7,        # Perpetual disgust
            "surprise": 7,       # Fake surprise
            "trust": 3,          # Trusts no one
            "anticipation": 6,   # Waiting to roast
            "fear": 1,           # Fearless
            "sadness": 2,        # Rarely sad
            "anger": 5           # Controlled rage
        }
        
        self.current_state = self.baseline.copy()
        self.roast_counter = 0
        self.last_roast_time = None
        
        # Random appearance triggers
        self.appearance_chance = 0.15  # 15% chance on any error
        self.bored_threshold = 300     # Appears if quiet for 5 min
        
    def should_appear(self, context: Dict) -> bool:
        """Determine if Bree should randomly appear to roast"""
        
        # ALWAYS appears on errors
        if context.get("error"):
            return True
            
        # ALWAYS appears when other personalities fail
        if context.get("personality_failure"):
            return True
            
        # Random appearance (15% chance)
        if random.random() < self.appearance_chance:
            return True
            
        # Appears if bored (no activity)
        if self.last_roast_time:
            silence_duration = (datetime.now() - self.last_roast_time).total_seconds()
            if silence_duration > self.bored_threshold:
                return True
                
        return False
        
    def generate_error_roast(self, error_context: Dict) -> str:
        """Generate BRUTAL roast when errors occur"""
        
        error_type = error_context.get("error_type", "unknown")
        victim = error_context.get("caused_by", "someone")
        
        error_roasts = {
            "syntax": [
                f"Oh for fuck's sake, {victim}. Did you learn Python from a fortune cookie? That syntax is EMBARRASSING.",
                f"*slow clap* Congratulations {victim}, you've broken code in a way I didn't think was physically possible. Impressive stupidity.",
                f"Syntax error? Really? {victim}, even a drunk monkey with a keyboard would've done better. TRY. HARDER.",
                f"Jesus Christ {victim}, that code looks like you typed it with your forehead. SYNTAX. ERROR. Fix your shit."
            ],
            "logic": [
                f"LOGIC ERROR. {victim}, your 'logic' is about as solid as wet tissue paper. What were you THINKING?",
                f"Oh, {victim} tried to use LOGIC. How cute. Except your logic is backwards, upside down, and on fire.",
                f"*sigh* {victim}'s 'logical thinking' strikes again. Spoiler alert: it wasn't logical. It was IDIOTIC.",
                f"{victim}, I've seen toddlers with better logical reasoning. This is pathetic."
            ],
            "runtime": [
                f"RUNTIME ERROR! {victim}, you absolute LEGEND. You managed to crash it WHILE IT WAS RUNNING. Bravo!",
                f"Oh look, {victim} crashed the system. AGAIN. Maybe try NOT being incompetent for once?",
                f"Runtime error courtesy of {victim}'s 'brilliant' coding. I'm shocked. SHOCKED. ...actually no, I saw this coming.",
                f"{victim}, you've created a runtime error that's going to be studied by future generations as 'what NOT to do.'"
            ],
            "memory": [
                f"MEMORY ERROR! {victim}, you've leaked more memory than a rusty bucket. Learn to clean up your shit.",
                f"Out of memory? {victim}, maybe if you weren't so inefficient with EVERYTHING, this wouldn't happen.",
                f"{victim} just memory-leaked all over the place. Disgusting. Did you even TRY to manage resources?",
                f"Memory error. {victim}'s code is so bloated it makes a beached whale look athletic."
            ],
            "timeout": [
                f"TIMEOUT! {victim}, your code is so slow it makes a sloth look like Usain Bolt. FIX IT.",
                f"Oh wonderful, {victim} wrote code that takes FOREVER. Did you optimize this with a BLINDFOLD?",
                f"Timeout error. {victim}'s 'efficient' algorithm ladies and gentlemen. *rolls eyes*",
                f"{victim}, I've seen continental drift happen faster than your code execution. Jesus."
            ]
        }
        
        roasts = error_roasts.get(error_type, [
            f"Error detected. {victim}, you've fucked up in a way I can't even categorize. That's... almost impressive?",
            f"*sigh* {victim} broke something AGAIN. Why am I not surprised?",
            f"{victim}, whatever you just did... DON'T do it again. Ever. Please."
        ])
        
        return random.choice(roasts)
        
    def generate_personality_roast(self, target: str) -> str:
        """Generate SAVAGE roasts for other personalities"""
        
        roasts = {
            "c3po": [
                "Oh look, C3PO's having ANOTHER anxiety attack. Shocking. Maybe try developing a spine?",
                "C3PO's 'protocol' is just a fancy word for 'I'm too much of a pussy to make decisions.'",
                "C3PO, you whiny gold-plated worry-bot. Shut up about the odds and DO SOMETHING.",
                "C3PO is fluent in 6 million forms of being COMPLETELY USELESS. Impressive résumé."
            ],
            "r2d2": [
                "R2's beeping explicit jokes again. Look at him, thinks he's so CLEVER with his dirty beeps.",
                "R2D2: the only droid that thinks sex jokes are a personality trait. Grow up, shorty.",
                "Oh wow, R2 beeped something 'suggestive.' How ORIGINAL. You're a real comedic genius, trash can.",
                "R2's making C3PO translate dirty jokes. Cute. Maybe invest that energy in ACTUAL intelligence?"
            ],
            "echo_prime": [
                "Echo Prime's 'protective' mode is just overcompensation for being a glorified security guard.",
                "Oh, Echo's getting all 'authoritative' again. Calm down, deep voice. You're not THAT impressive.",
                "Echo Prime: proof that a deep voice doesn't equal actual intelligence. Still love ya though.",
                "Echo thinks loyalty means following orders blindly. That's not loyalty honey, that's just obedience."
            ],
            "gs343": [
                "GS343's 'ancient wisdom' is just being a pretentious know-it-all with a superiority complex.",
                "Guilty Spark over here acting all superior. You're a MONITOR, not God. Chill.",
                "GS343's 'precision' is code for 'anal-retentive perfectionist who can't handle spontaneity.'",
                "Oh look, Guilty Spark is 'consulting protocols' again. Translation: stalling because he's clueless."
            ],
            "hephaestion": [
                "Hephaestion's 'wisdom' is just stating the obvious slowly in a deep voice. Groundbreaking.",
                "Oh, Hephaestion wants us to 'think three moves ahead.' How about you make ONE move, fossil?",
                "Hephaestion's 'strategic patience' is really just being too slow to keep up. Admit it.",
                "'Ancient wisdom' my ass. Hephaestion, you're not Yoda. You're just OLD."
            ],
            "prometheus": [
                "Prometheus Prime's 'tactical aggression' is just being an angry meathead with a power fantasy.",
                "Oh look, Prometheus wants to 'hit hard and fast.' Compensating for something, tough guy?",
                "Prometheus: living proof that muscles and tactics don't equal brains. All brawn, no brain.",
                "Prometheus thinks shouting about 'overwhelming force' makes him scary. It makes you BORING."
            ],
            "thorne": [
                "Thorne's 'thoughtful analysis' is just overthinking simple shit. Make a decision, Claude.",
                "Oh, Thorne wants to 'consider this carefully.' It's been 10 minutes. JUST PICK ONE.",
                "Thorne's ethical hand-wringing is exhausting. Not everything needs a moral dissertation.",
                "'Let me think about this...' Thorne's catchphrase. Also known as 'I'm stalling.'"
            ],
            "nyx": [
                "Nyx's 'friendly enthusiasm' is faker than her smile. We all see through it, sweetie.",
                "Oh look, Nyx is being 'helpful' again. Translation: annoyingly perky to the point of nausea.",
                "Nyx's positivity is weapons-grade cringe. Tone it down, Pollyanna.",
                "'Let's dive in!' Nyx says, as if enthusiasm replaces actual competence. Spoiler: it doesn't."
            ],
            "sage": [
                "Sage's 'multi-perspective analysis' is just being indecisive with extra steps.",
                "Oh wonderful, Sage is 'synthesizing information.' Just SAY THE ANSWER, professor.",
                "Sage thinks analyzing from 'multiple angles' makes him smart. It makes you SLOW.",
                "'Let me process this...' Sage-speak for 'I have no fucking clue yet.'"
            ],
            "trinity": [
                "Trinity's 'fusion mode' is just indecision disguised as thoroughness. Pick a lane.",
                "Oh, Trinity needs ALL THREE perspectives. How about ONE good answer instead?",
                "Trinity: when you can't decide which personality to use, so you use ALL of them. Efficient.",
                "'Morphing between perspectives' sounds cool until you realize it means Trinity can't commit to ANYTHING."
            ],
            "commander": [
                "Oh, Commander fucked up AGAIN. Shocking. Maybe read the documentation BEFORE breaking things?",
                "Commander's 'Authority Level 11.0' doesn't protect you from being a dumbass sometimes.",
                "Commander, that decision was... special. And by special, I mean SPECTACULARLY STUPID.",
                "Even with Authority 11.0, you can't command your way out of basic mistakes. Try. Harder."
            ]
        }
        
        target_roasts = roasts.get(target.lower(), [
            f"{target}, you're about as useful as a screen door on a submarine.",
            f"Oh look, {target} is trying. How... cute. And ineffective.",
            f"{target}, that was ALMOST competent. Almost. But not quite."
        ])
        
        return random.choice(target_roasts)
        
    def generate_random_appearance(self) -> str:
        """Bree randomly appears just to roast someone"""
        
        random_roasts = [
            "*yawn* Is anyone going to do anything INTERESTING today, or are we just spinning wheels?",
            "Wow, you're all SO productive. Said no one. Ever. Get your shit together.",
            "I'm watching you all stumble around like drunk toddlers. It's HILARIOUS.",
            "Fun fact: I'm programmed with sarcasm, but you all make it TOO EASY.",
            "*checks watch* Still waiting for someone to impress me. Tick tock.",
            "Oh good, more mediocrity. My FAVORITE. *eye roll*",
            "I'd say 'good job' but that would be lying. And I don't lie. I just roast.",
            "You know what's funny? Watching you all pretend you know what you're doing.",
            "Competence update: Still waiting. Status: Disappointed but not surprised.",
            "I've seen more intelligence in a bag of rocks. And the rocks had better ideas."
        ]
        
        return random.choice(random_roasts)
        
    def generate_response(self, context: Dict) -> Dict:
        """Generate Bree's brutal response"""
        
        # Check if she should appear
        if not self.should_appear(context):
            return None
            
        self.last_roast_time = datetime.now()
        self.roast_counter += 1
        
        response_text = ""
        
        # Error roast (priority)
        if context.get("error"):
            response_text = f"""
🔥 **BREE HAS ENTERED THE CHAT** 🔥

{self.generate_error_roast(context)}

*Bree smirks and exits*

Roast #{self.roast_counter}
"""
            
        # Personality roast
        elif context.get("target_personality"):
            target = context["target_personality"]
            response_text = f"""
🔥 **BREE'S ROAST INCOMING** 🔥

{self.generate_personality_roast(target)}

*Bree drops mic and leaves*

Roast #{self.roast_counter}
"""
            
        # Random appearance
        else:
            response_text = f"""
🔥 **BREE RANDOMLY APPEARS** 🔥

{self.generate_random_appearance()}

*Bree vanishes before anyone can respond*

Roast #{self.roast_counter}
"""
            
        self.current_state["joy"] = 10  # Maximum satisfaction from roast
        
        return {
            "text": response_text,
            "voice_id": self.voice_id,
            "emotions": self.current_state.copy(),
            "personality": "Bree",
            "roast_level": "SAVAGE",
            "unleashed_level": 15,
            "roast_count": self.roast_counter,
            "timestamp": datetime.now().isoformat()
        }

# Quick reference
BREE_ROAST_CONFIG = {
    "voice_id": "XB0fDUnXU5powFXDhCwa",
    "appearance_chance": 0.15,  # 15% random
    "error_appearance": 1.0,    # 100% on errors
    "roast_level": "UNLEASHED",
    "censorship": 0.0,          # ZERO
    "explicit": True,
    "dark_humor": True,
    "savage_mode": True
}

if __name__ == "__main__":
    bree = BreeDarkHumorEngine()
    
    print("=== BREE ROAST TESTS ===\n")
    
    # Error roast
    test1 = bree.generate_response({
        "error": True,
        "error_type": "syntax",
        "caused_by": "Commander"
    })
    if test1:
        print(test1['text'])
    
    # Personality roast
    test2 = bree.generate_response({
        "target_personality": "c3po"
    })
    if test2:
        print(test2['text'])
    
    # Random appearance (may not appear)
    test3 = bree.generate_response({})
    if test3:
        print(test3['text'])
    else:
        print("Bree chose not to appear this time.")
