import subprocess
import os
import time
from vosk_stt import VoskSTT
class AudioHandler:
    def __init__(self, model_path, temp_audio_file="recording.wav"):
        self.model_path = model_path
        self.temp_audio_file = temp_audio_file
        self.stt = VoskSTT(model_path)
        print("✓ Audio handler initialized")
    def record_audio(self, duration=5):
        filename = self.temp_audio_file
        print(f"🎤 Recording for {duration} seconds...")
        print("Speak now!")
        if os.path.exists(filename):
            os.remove(filename)
        process = subprocess.Popen([
            "termux-microphone-record",
            "-f", filename,
            "-l", str(duration)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        max_wait = duration + 5
        start_time = time.time()
        last_size = 0
        stable_count = 0
        while time.time() - start_time < max_wait:
            if os.path.exists(filename):
                current_size = os.path.getsize(filename)               
                if current_size > 0:
                    if current_size == last_size:
                        stable_count += 1
                        if stable_count >= 2:
                            break
                    else:
                        stable_count = 0
                        last_size = current_size           
            time.sleep(1)      
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print("❌ Recording failed")
            return None
        print(f"✓ Recording complete ({os.path.getsize(filename)} bytes)")
        return self._convert_to_wav(filename)
    def _convert_to_wav(self, filename):
        temp_file = "temp_" + filename
        result = subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", filename,
            "-ac", "1",
            "-ar", "16000",
            "-acodec", "pcm_s16le",
            temp_file
        ], capture_output=True)
        if result.returncode == 0 and os.path.exists(temp_file):
            os.remove(filename)
            os.rename(temp_file, filename)
            print("✓ Converted to WAV format")
        return filename
    def transcribe(self, audio_file=None):
        if audio_file is None:
            audio_file = self.temp_audio_file
        
        if not os.path.exists(audio_file):
            print("❌ Audio file not found")
            return ""
        print("🔊 Transcribing audio...")
        text = self.stt.transcribe_file(audio_file)
        return text
    def record_and_transcribe(self, duration=5, cleanup=True):
        audio_file = self.record_audio(duration)
        if not audio_file:
            return ""
        text = self.transcribe(audio_file)
        if text:
            print(f"📝 You said: {text}")
        else:
            print("❌ No speech detected")
        if cleanup and os.path.exists(audio_file):
            os.remove(audio_file)
            print("✓ Cleaned up audio file")
        return text
    def cleanup(self):
        if os.path.exists(self.temp_audio_file):
            os.remove(self.temp_audio_file)
            print(f"✓ Deleted {self.temp_audio_file}")
def get_voice_input(model_path, duration=5):
    handler = AudioHandler(model_path)
    text = handler.record_and_transcribe(duration, cleanup=True)
    return text
if __name__ == "__main__":
    MODEL_PATH = "/data/data/com.termux/files/home/vosk-models/vosk-model-en-in-0.5"
    print("Testing Audio Handler\n")
    handler = AudioHandler(MODEL_PATH)  
    text = handler.record_and_transcribe(duration=5)
    print("\n Final Result")
    print(f"Transcribed: '{text}'")
