________________________________________
Offline Voice Assistant for Android (Termux)
Overview
This project is a fully offline, privacy-respecting voice assistant for Android, designed to handle everyday device automation and utility tasks. It uses open-source modules for speech-to-text (Vosk), text-to-speech (Termux TTS), and device control via Termux API. No cloud or AI model is involved: the assistant executes direct system commands and reads responses aloud. It’s tested on Poco M2 Pro running Termux under Android 11.
________________________________________
Features
•	Offline voice and text command support
•	Device automation: Launch apps, toggle brightness, control volume, vibrate, etc.
•	Battery, time, and date status reporting (spoken output)
•	Clipboard, SMS, and telephony operations
•	Custom hourly water reminder notifications
•	Easy extension for new commands
________________________________________
Requirements
•	Android device with Termux installed (Tested on Poco M2 Pro)
•	Vosk STT model (vosk-model-en-in-0.5 preferred)
•	Python 3.8 or newer (apt install python)
•	Termux:API app (from Play Store) and Termux:API package (pkg install termux-api)
•	Required Termux permissions (Audio, Storage, etc.)
________________________________________
 
Install Steps
1.	Install Termux from Play Store
2.	Install Python and Termux API
text
pkg update
pkg install python termux-api
3.	Clone the Project and Install Dependencies
text
git clone <your-repo-url>
cd offline-assistant
pip install vosk
4.	Download the Vosk Speech Recognition Model
o	Put your model folder (e.g., vosk-model-en-in-0.5) in the location specified by MODEL_PATH in assistant.py.
5.	Install Termux:API App from Play Store
o	Ensure Termux:API has all the required Android permissions.
6.	Test Termux:API
text
termux-battery-status
termux-tts-speak "Setup is complete"
________________________________________
 
Files Structure
text
offline-assistant/
├── assistant.py                # Main entry script
├── assistant_handler_vayu.py   # Command handler (edit for new commands)
├── audio_handler_vayu.py       # Speech-to-text using Vosk
├── tts_handler_vayu.py         # Text-to-speech handler
└── vosk-model-en-in-0.5/       # Vosk STT model directory

________________________________________
How to Run
1.	Start Termux and cd into your project directory:
text
cd offline-assistant
python assistant.py
2.	Select mode:
o	1 = Voice input (records and transcribes)
o	2 = Text command input
o	3 = Exit
3.	Speak or type your command (see examples below).
________________________________________
 
Supported Commands
| Example Keywords   | Function               | Output/Action              |
| ------------------ | ---------------------- | -------------------------- |
| camera             | Open Camera app        | App opens                  |
| chrome, web        | Open Chrome browser    | App opens                  |
| brightness maximum | Set screen brightness  | "Task completed."          |
| volume full        | Set music volume max   | "Task completed."          |
| battery status     | Spoken battery details | "Battery health is ...etc" |
| time / date        | Spoken time/date       | "The current time is ..."  |
| water reminder on  | Start hourly reminder  | Notification every hour    |
| water reminder off | Stop hourly reminder   | Reminder stops             |
________________________________________
Water Reminder
•	To start: Say/type "water reminder" or "water on"
•	To stop: Say/type "water reminder off" or "water off"
•	Every hour, a Termux notification reminds you to drink water.
________________________________________
Troubleshooting
•	Permissions errors: Make sure Termux:API app has microphone, storage, notification, and phone permissions.
•	Speech recognition not working: Check Vosk model path and installation.
•	Some apps not launching: Command syntax may differ by device; edit assistant_handler_vayu.py for your phone’s package names if needed.
•	TTS issues: Test with termux-tts-speak "Hello world" and check device TTS settings.
•	Custom commands: Add more keywords and shell commands in assistant_handler_vayu.py.
________________________________________
 
Extending
•	Edit the command_map dictionary in assistant_handler_vayu.py to add more device actions.
•	Integrate new Termux:API features or Android intent commands as desired.
________________________________________
License
This project is released under the MIT License.
________________________________________
Credits
•	Vosk Speech Recognition (https://alphacephei.com/vosk/)
•	Termux and Termux:API (https://termux.com/)
•	Community contributions on GitHub
________________________________________

