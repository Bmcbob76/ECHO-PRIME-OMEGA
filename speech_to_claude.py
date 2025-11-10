"""
Speech-to-Text Claude Interface
Commander Bobby Don McWilliams II
Press SPACE to talk, ESC to quit
"""
import speech_recognition as sr
import anthropic
import os
import sys
from pynput import keyboard
import threading
import queue

class STTClaude:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.listening = False
        self.audio_queue = queue.Queue()
        self.running = True
        
        # Adjust for ambient noise
        print("🎤 Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Ready. Press SPACE to talk, ESC to quit\n")
    
    def listen_audio(self):
        """Continuous audio capture thread"""
        with self.microphone as source:
            while self.running:
                if self.listening:
                    try:
                        print("🔴 Listening...")
                        audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                        self.audio_queue.put(audio)
                        self.listening = False
                    except sr.WaitTimeoutError:
                        print("⏱️ No speech detected")
                        self.listening = False
                    except Exception as e:
                        print(f"❌ Audio error: {e}")
                        self.listening = False
    
    def process_audio(self):
        """Process audio queue and convert to text"""
        while self.running:
            try:
                audio = self.audio_queue.get(timeout=1)
                print("🔄 Processing speech...")
                
                # Convert speech to text
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"\n📝 You said: {text}\n")
                    
                    # Send to Claude
                    self.send_to_claude(text)
                    
                except sr.UnknownValueError:
                    print("❌ Could not understand audio")
                except sr.RequestError as e:
                    print(f"❌ Recognition error: {e}")
                    
            except queue.Empty:
                continue
    
    def send_to_claude(self, text):
        """Send text to Claude and display response"""
        try:
            print("💭 Claude thinking...")
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": text}]
            )
            
            response = message.content[0].text
            print(f"🤖 Claude: {response}\n")
            print("─" * 60)
            print("Press SPACE to talk again\n")
            
        except Exception as e:
            print(f"❌ Claude error: {e}")
    
    def on_press(self, key):
        """Handle keyboard input"""
        try:
            if key == keyboard.Key.space and not self.listening:
                self.listening = True
            elif key == keyboard.Key.esc:
                print("\n👋 Shutting down...")
                self.running = False
                return False
        except AttributeError:
            pass
    
    def run(self):
        """Main run loop"""
        # Start threads
        audio_thread = threading.Thread(target=self.listen_audio, daemon=True)
        process_thread = threading.Thread(target=self.process_audio, daemon=True)
        
        audio_thread.start()
        process_thread.start()
        
        # Keyboard listener
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
        
        # Wait for threads
        audio_thread.join(timeout=2)
        process_thread.join(timeout=2)

if __name__ == "__main__":
    print("=" * 60)
    print("SPEECH-TO-TEXT CLAUDE INTERFACE")
    print("Commander Bobby Don McWilliams II")
    print("=" * 60 + "\n")
    
    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set!")
        print("Set it with: set ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)
    
    try:
        app = STTClaude()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Interrupted")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
