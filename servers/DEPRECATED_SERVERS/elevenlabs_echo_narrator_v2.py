"""
ECHO XV4 - ELEVENLABS TTS V3 ECHO NARRATOR
Production-Ready Audio Narration System
Voice: Echo | Model: eleven_turbo_v2_5 | Seamless Pygame Playback
Authority Level: 11.0
"""

import os
import sys
import time
import re
from pathlib import Path
import pygame
from elevenlabs import VoiceSettings, play
from elevenlabs.client import ElevenLabs
import io
from pydub import AudioSegment
from pydub.playback import play as pydub_play

# Initialize ElevenLabs client
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    print("❌ ERROR: ELEVENLABS_API_KEY not set")
    print("Set with: $env:ELEVENLABS_API_KEY='your-key-here'")
    sys.exit(1)

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Echo voice ID - ElevenLabs preset
ECHO_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Echo voice

# Voice settings for full emotional range
VOICE_SETTINGS = VoiceSettings(
    stability=0.5,          # Medium stability for natural variation
    similarity_boost=0.75,  # High similarity to original voice
    style=0.5,              # Full emotional expressiveness  
    use_speaker_boost=True  # Enhanced clarity
)

# TTS Model - v3 turbo
TTS_MODEL = "eleven_turbo_v2_5"

# Initialize pygame mixer for playback
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

class EchoNarrator:
    """Production TTS narrator with seamless playback"""
    
    def __init__(self, document_path):
        self.document_path = Path(document_path)
        self.segments = []
        self.current_segment = 0
        
    def load_document(self):
        """Load and segment the document"""
        print(f"📄 Loading: {self.document_path.name}")
        with open(self.document_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean markdown formatting
        content = self._clean_markdown(content)
        
        # Split into sentences for natural pacing
        self.segments = self._segment_text(content)
        print(f"✅ Loaded {len(self.segments)} segments")
        
        return len(self.segments)
    
    def _clean_markdown(self, text):
        """Remove markdown formatting for TTS"""
        # Remove headers markers but keep text
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Remove bold/italic markers
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)  # Bold+italic
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)      # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)          # Italic
        
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove horizontal rules
        text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
        
        # Remove emoji/special markers
        text = re.sub(r'[⭐🚩✅❌📄💰]', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _segment_text(self, text):
        """Break text into speakable segments"""
        # Split by sentences, keeping some context
        sentences = re.split(r'([.!?])\s+', text)
        
        segments = []
        current = ""
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
            sentence = sentence.strip()
            
            if not sentence:
                continue
                
            # Skip very short segments (likely formatting artifacts)
            if len(sentence) < 10:
                continue
            
            # Add to segments (target ~300 chars per segment for natural pacing)
            if len(current) + len(sentence) < 300:
                current += " " + sentence
            else:
                if current:
                    segments.append(current.strip())
                current = sentence
        
        if current:
            segments.append(current.strip())
        
        return segments
    
    def generate_audio_segment(self, text, segment_num):
        """Generate audio for a single text segment"""
        try:
            # Generate with ElevenLabs
            audio_generator = client.text_to_speech.convert(
                voice_id=ECHO_VOICE_ID,
                model_id=TTS_MODEL,
                text=text,
                voice_settings=VOICE_SETTINGS
            )
            
            # Collect audio bytes
            audio_bytes = b""
            for chunk in audio_generator:
                audio_bytes += chunk
            
            return audio_bytes
            
        except Exception as e:
            print(f"❌ Error generating segment {segment_num}: {e}")
            return None
    
    def play_segment_pygame(self, audio_bytes):
        """Play audio using pygame with no gaps"""
        if not audio_bytes:
            return False
            
        try:
            # Load audio into pygame
            audio_buffer = io.BytesIO(audio_bytes)
            pygame.mixer.music.load(audio_buffer)
            
            # Play
            pygame.mixer.music.play()
            
            # Wait for completion
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            return True
            
        except Exception as e:
            print(f"❌ Playback error: {e}")
            return False
    
    def narrate(self, start_segment=0, max_segments=None):
        """Narrate the document with seamless playback"""
        if not self.segments:
            print("❌ No segments loaded. Call load_document() first.")
            return
        
        total = len(self.segments)
        end_segment = min(start_segment + max_segments, total) if max_segments else total
        
        print(f"\n🎙️  ECHO NARRATOR ACTIVATED")
        print(f"📊 Segments: {start_segment+1} - {end_segment} of {total}")
        print(f"🔊 Voice: Echo | Model: {TTS_MODEL}")
        print(f"━" * 60)
        
        for i in range(start_segment, end_segment):
            segment_text = self.segments[i]
            
            # Show progress
            progress = ((i - start_segment + 1) / (end_segment - start_segment)) * 100
            print(f"\n[{i+1}/{total}] ({progress:.1f}%)")
            print(f"📝 {segment_text[:80]}...")
            
            # Generate audio
            print("🎵 Generating audio...", end=" ")
            audio_bytes = self.generate_audio_segment(segment_text, i+1)
            
            if audio_bytes:
                print(f"✓ ({len(audio_bytes)} bytes)")
                
                # Play immediately
                print("🔊 Playing...", end=" ")
                if self.play_segment_pygame(audio_bytes):
                    print("✓")
                else:
                    print("❌ Playback failed")
            else:
                print("❌ Generation failed")
                continue
        
        print(f"\n━" * 60)
        print(f"✅ NARRATION COMPLETE")
        print(f"📊 Played {end_segment - start_segment} segments")


def main():
    """Main execution"""
    # Target document
    doc_path = r"C:\Users\bobmc\Downloads\compass_artifact_wf-1e4f961d-8cef-41ac-9215-c2723a88b3aa_text_markdown.md"
    
    if not Path(doc_path).exists():
        print(f"❌ Document not found: {doc_path}")
        return 1
    
    # Create narrator
    narrator = EchoNarrator(doc_path)
    
    # Load document
    num_segments = narrator.load_document()
    
    # Show options
    print(f"\n📋 NARRATION OPTIONS:")
    print(f"1. Full document ({num_segments} segments)")
    print(f"2. First 10 segments (test)")
    print(f"3. Custom range")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        narrator.narrate()
    elif choice == "2":
        narrator.narrate(max_segments=10)
    elif choice == "3":
        start = int(input("Start segment (1-based): ")) - 1
        count = int(input("Number of segments: "))
        narrator.narrate(start_segment=start, max_segments=count)
    else:
        print("Invalid choice")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
