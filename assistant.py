import os
from audio_handler_vayu import AudioHandler
from tts_handler_vayu import TTSHandler
from assistant_handler_vayu import assistant_handler
MODEL_PATH = "/data/data/com.termux/files/home/vosk-models/vosk-model-en-in-0.5"
def main():
    audio = AudioHandler(MODEL_PATH)
    tts = TTSHandler(language="en_IN", rate=1.0)
    print("\nOffline Assistant")
    print("1. Voice input")
    print("2. Text input")
    print("3. Exit\n")
    while True:
        choice = input("Select mode (1/2/3): ").strip()
        if choice == "1":
            print("\n--- Voice Mode ---")
            user_text = audio.record_and_transcribe(duration=5, cleanup=True)
            if user_text:
                print(f"📝 You said: {user_text}")
                response = assistant_handler(user_text)
                print(f"\n🤖 Assistant: {response}")
                tts.speak(response)
                print()
            else:
                msg = "Sorry, I didn't hear anything"
                print(msg)
                tts.speak(msg)
        elif choice == "2":
            print("\n--- Text Mode ---")
            user_text = input("Enter your question: ").strip()
            if user_text:
                response = assistant_handler(user_text)
                print(f"\n🤖 Assistant: {response}")
                tts.speak(response)
                print()
        elif choice == "3":
            tts.speak("Goodbye!")
            print("\nGoodbye! 👋")
            audio.cleanup()
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")
if __name__ == "__main__":
    main()


