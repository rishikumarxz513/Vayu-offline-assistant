import subprocess
import time
class TTSHandler:
    def __init__(self, engine="com.google.android.tts", language="en_IN", rate=1.0, pitch=1.0):
        self.engine = engine
        self.language = language
        self.rate = rate
        self.pitch = pitch
        if not self._test_tts():
            print("⚠️ Warning: Termux:API TTS not available")
            print("   Install Termux:API app from F-Droid")
            self.available = False
        else:
            self.available = True
            print("✓ TTS handler initialized")
    def _test_tts(self):
        """Test if TTS is available"""
        try:
            result = subprocess.run(
                ["which", "termux-tts-speak"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    def speak(self, text, rate=None, pitch=None, stream=None):
        if not self.available:
            print(f"TTS not available. Text was: {text}")
            return False
        
        if not text or not text.strip():
            print("⚠️ No text to speak")
            return False
        speech_rate = rate if rate is not None else self.rate
        speech_pitch = pitch if pitch is not None else self.pitch
        cmd = [
            "termux-tts-speak",
            "-e", self.engine,
            "-l", self.language,
            "-r", str(speech_rate),
            "-p", str(speech_pitch)
        ]
        if stream:
            cmd.extend(["-s", stream])
        cmd.append(text)  
        try:
            print(f"🔊 Speaking: {text[:50]}..." if len(text) > 50 else f"🔊 Speaking: {text}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                estimated_duration = len(text.split()) * 0.5 / speech_rate
                time.sleep(min(estimated_duration, 10)) 
                return True
            else:
                print(f"❌ TTS error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ TTS timeout")
            return False
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return False
    def speak_blocking(self, text, rate=None, pitch=None):
        return self.speak(text, rate, pitch)
    
    def speak_async(self, text, rate=None, pitch=None):
        if not self.available:
            print(f"TTS not available. Text was: {text}")
            return
        speech_rate = rate if rate is not None else self.rate
        speech_pitch = pitch if pitch is not None else self.pitch
        cmd = [
            "termux-tts-speak",
            "-e", self.engine,
            "-l", self.language,
            "-r", str(speech_rate),
            "-p", str(speech_pitch),
            text
        ]
        try:
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"🔊 Speaking (async): {text[:50]}..." if len(text) > 50 else f"🔊 Speaking: {text}")
        except Exception as e:
            print(f"❌ TTS error: {e}")
    def set_language(self, language):
        self.language = language
        print(f"✓ Language set to: {language}")
    def set_rate(self, rate):
        self.rate = max(0.5, min(2.0, rate))
        print(f"✓ Speech rate set to: {self.rate}")
    def set_pitch(self, pitch):
        self.pitch = max(0.5, min(2.0, pitch))
        print(f"✓ Speech pitch set to: {self.pitch}")
    def list_engines(self):
        try:
            result = subprocess.run(
                ["termux-tts-engines"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("Available TTS engines:")
                print(result.stdout)
            else:
                print("❌ Could not list engines")
        except Exception as e:
            print(f"❌ Error listing engines: {e}")
def speak(text, language="en_IN", rate=1.0):
    tts = TTSHandler(language=language, rate=rate)
    tts.speak(text)
if __name__ == "__main__":
    print("=== Testing TTS Handler ===\n")
    tts = TTSHandler(language="en_IN", rate=1.0)
    print("\n--- Test 1: Basic Speech ---")
    tts.speak("Hello! This is a test of the offline text to speech system.")
    print("\n--- Test 2: Speech Rates ---")
    tts.speak("This is slow speech", rate=0.7)
    time.sleep(1)
    tts.speak("This is fast speech", rate=1.5)
    print("\n--- Test 3: US English ---")
    tts.set_language("en_US")
    tts.speak("This is US English pronunciation")
    print("\n--- Test 4: Async Speech ---")
    tts.speak_async("This is non-blocking speech")
    print("Code continues immediately while speaking...")
    time.sleep(3)
    print("\n✓ TTS module test complete")





    