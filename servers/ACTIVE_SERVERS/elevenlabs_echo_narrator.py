"""
ECHO XV4 - ELEVENLABS TTS V3 NARRATOR
Voice: Echo | Model: eleven_turbo_v2_5 | Full Emotion Range
Seamless segment playback with pygame
Authority Level: 11.0
"""

import os
import sys
import time
import re
from pathlib import Path
import pygame
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from openai import OpenAI

# API Keys
ELEVENLABS_API_KEY = "sk_2c0f0020651d25cc93485dfabfe000b7d3355f930ad44ea5"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Initialize clients
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Voice IDs
ECHO_PRIME_VOICE_ID = "keDMh3sQlEXKM4EQxvvi"  # Echo Prime - Command Authority
BREE_VOICE_ID = "ru5RIm1Wp637zVrUbYeu"       # Bree - Intelligence Analyst
OPENAI_ECHO_VOICE = "echo"                    # OpenAI fallback

# Audio configuration
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024

class EchoNarrator:
    """ElevenLabs TTS v3 Narrator with Echo Prime voice and OpenAI fallback"""
    
    def __init__(self, input_file, output_dir="audio_segments", use_openai_fallback=False):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.segments = []
        self.audio_files = []
        self.use_openai = use_openai_fallback
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
        
    def load_document(self):
        """Load and read the markdown document"""
        print(f"[ECHO] Loading document: {self.input_file}")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def segment_text(self, text, max_chars=2000):
        """
        Break text into segments suitable for TTS
        Breaks at sentence boundaries for natural speech
        """
        print(f"[ECHO] Segmenting text (max {max_chars} chars per segment)")
        
        # Split by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        segments = []
        current_segment = ""
        
        for para in paragraphs:
            # Skip empty paragraphs
            para = para.strip()
            if not para:
                continue
                
            # If paragraph alone exceeds max, split by sentences
            if len(para) > max_chars:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    if len(current_segment) + len(sentence) + 1 <= max_chars:
                        current_segment += sentence + " "
                    else:
                        if current_segment:
                            segments.append(current_segment.strip())
                        current_segment = sentence + " "
            else:
                # Try to add paragraph to current segment
                if len(current_segment) + len(para) + 2 <= max_chars:
                    current_segment += para + "\n\n"
                else:
                    if current_segment:
                        segments.append(current_segment.strip())
                    current_segment = para + "\n\n"
        
        # Add remaining segment
        if current_segment:
            segments.append(current_segment.strip())
        
        print(f"[ECHO] Created {len(segments)} segments")
        self.segments = segments
        return segments
    
    def generate_audio(self):
        """Generate audio for all segments using ElevenLabs TTS v3 or OpenAI TTS fallback"""
        if self.use_openai:
            print(f"\n[ECHO] Generating audio with OpenAI TTS (Fallback Mode)")
            print(f"[ECHO] Voice: echo | Model: tts-1-hd")
        else:
            print(f"\n[ECHO] Generating audio with ElevenLabs TTS v3")
            print(f"[ECHO] Voice: Echo Prime | Model: eleven_turbo_v2_5")
        print(f"[ECHO] Emotion: Full range enabled\n")
        
        for i, segment in enumerate(self.segments, 1):
            print(f"[ECHO] Segment {i}/{len(self.segments)}: {len(segment)} chars")
            
            try:
                output_path = self.output_dir / f"segment_{i:03d}.mp3"
                
                if self.use_openai:
                    # OpenAI TTS fallback
                    response = openai_client.audio.speech.create(
                        model="tts-1-hd",
                        voice=OPENAI_ECHO_VOICE,
                        input=segment
                    )
                    response.stream_to_file(output_path)
                    
                else:
                    # ElevenLabs TTS v3 (primary)
                    audio = elevenlabs_client.generate(
                        text=segment,
                        voice=ECHO_PRIME_VOICE_ID,
                        model="eleven_turbo_v2_5",
                        voice_settings=VoiceSettings(
                            stability=0.5,
                            similarity_boost=0.75,
                            style=0.5,
                            use_speaker_boost=True
                        )
                    )
                    
                    # Write audio stream to file
                    with open(output_path, 'wb') as f:
                        for chunk in audio:
                            if chunk:
                                f.write(chunk)
                
                self.audio_files.append(output_path)
                print(f"[ECHO] ✓ Saved: {output_path.name}")
                
            except Exception as e:
                print(f"[ECHO] ✗ ERROR generating segment {i}: {e}")
                # Try OpenAI fallback if ElevenLabs fails
                if not self.use_openai:
                    print(f"[ECHO] → Attempting OpenAI fallback...")
                    try:
                        response = openai_client.audio.speech.create(
                            model="tts-1-hd",
                            voice=OPENAI_ECHO_VOICE,
                            input=segment
                        )
                        response.stream_to_file(output_path)
                        self.audio_files.append(output_path)
                        print(f"[ECHO] ✓ Fallback successful: {output_path.name}")
                    except Exception as fallback_error:
                        print(f"[ECHO] ✗ Fallback failed: {fallback_error}")
                        continue
                else:
                    continue
        
        print(f"\n[ECHO] Generated {len(self.audio_files)} audio files")
    
    def play_seamless(self):
        """Play all audio segments with NO delay between them using pygame"""
        print(f"\n[ECHO] Starting seamless playback")
        print(f"[ECHO] Total segments: {len(self.audio_files)}")
        print(f"[ECHO] Engine: pygame mixer\n")
        
        for i, audio_file in enumerate(self.audio_files, 1):
            print(f"[ECHO] ▶ Playing segment {i}/{len(self.audio_files)}: {audio_file.name}")
            
            try:
                # Load and play audio
                pygame.mixer.music.load(str(audio_file))
                pygame.mixer.music.play()
                
                # Wait for audio to finish (no delay)
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Immediately continue to next segment (NO delay)
                
            except Exception as e:
                print(f"[ECHO] ✗ ERROR playing {audio_file.name}: {e}")
                continue
        
        print(f"\n[ECHO] ✓ Playback complete")
    
    def execute(self):
        """Main execution flow"""
        print("=" * 70)
        print("ECHO XV4 - ELEVENLABS TTS V3 NARRATOR")
        print("=" * 70)
        
        # Load document
        text = self.load_document()
        print(f"[ECHO] Document loaded: {len(text)} characters\n")
        
        # Segment text
        self.segment_text(text)
        
        # Generate audio
        self.generate_audio()
        
        # Play seamlessly
        self.play_seamless()
        
        print("\n" + "=" * 70)
        print("ECHO NARRATOR - MISSION COMPLETE")
        print("=" * 70)


def main():
    """Entry point"""
    # Input file
    input_file = r"C:\Users\bobmc\Downloads\compass_artifact_wf-1e4f961d-8cef-41ac-9215-c2723a88b3aa_text_markdown.md"
    
    # Create narrator with ElevenLabs (primary)
    print("[ECHO] Initializing Echo Prime narrator with ElevenLabs TTS v3")
    narrator = EchoNarrator(input_file, use_openai_fallback=False)
    
    # Execute
    narrator.execute()


if __name__ == "__main__":
    main()
