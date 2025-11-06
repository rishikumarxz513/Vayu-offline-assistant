import subprocess
import threading
import time
import json
from datetime import datetime
water_reminder_active = False
def get_current_time():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    return f"The current time is {time_str}."
def get_current_date():
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    return f"Today is {date_str}."
def get_time_and_date():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    return f"The current time is {time_str}. Today is {date_str}."
def execute_command(command):
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
def send_toast(message):
    execute_command(f'termux-toast "{message}"')
def start_water_reminder():
    global water_reminder_active
    water_reminder_active = True
    def reminder_loop():
        while water_reminder_active:
            subprocess.run(
                'termux-notification --title "💧 Water Reminder" '
                '--content "Time to drink a glass of water!" '
                '--sound --vibrate 1000,500,1000 --priority high',
                shell=True)
            time.sleep(3600)  
    threading.Thread(target=reminder_loop, daemon=True).start()
def stop_water_reminder():
    global water_reminder_active
    water_reminder_active = False
def parse_battery_status(json_output):
    try:
        data = json.loads(json_output)
        message = (
            f"Battery health is {data.get('health', 'unknown')}. "
            f"Battery percentage is {data.get('percentage', 0)} percent. "
            f"Status is {data.get('status', 'unknown')}. "
            f"Temperature is {data.get('temperature', 0)} degrees celsius."
        )
        return message
    except:
        return "Could not read battery status."
def assistant_handler(user_input):
    input_lower = user_input.lower().strip()

    if any(kw in input_lower for kw in ["time", "what time", "current time", "tell me the time"]):
        return get_current_time()
    

    if any(kw in input_lower for kw in ["date", "what date", "today's date", "tell me the date"]):
        return get_current_date()
    
    if any(kw in input_lower for kw in ["time and date", "date and time", "time date","tell date time","tell date and time"]):
        return get_time_and_date()

    if any(kw in input_lower for kw in ["battery", "battery status", "battery level", "check battery"]):
        success, output = execute_command("termux-battery-status")
        if success:
            readable = parse_battery_status(output)
            return readable
        else:
            return "I did not understand."
    command_map = {
        ("camera",): "am start -n com.android.camera/.Camera",
        ("chrome", "web", "web browser", "internet"): "am start -n com.android.chrome/com.google.android.apps.chrome.Main",
        ("youtube",): "am start -n com.google.android.youtube/.HomeActivity",
        ("notes",): "am start -n com.miui.notes/.ui.NotesListActivity",
        ("music",): "am start -n com.miui.player/.ui.MusicBrowserActivity",
        ("messages",): "am start -n com.android.mms/.ui.ConversationList",
        ("settings",): "am start -n com.android.settings/.Settings",
        ("phone",): "am start -a android.intent.action.DIAL",
        ("maps", "rishikesh map"): "am start -n com.google.android.apps.maps/com.google.android.maps.MapsActivity",
        ("whatsapp",): "am start -n com.whatsapp/.Main",
        ("photos",): "am start -n com.google.android.apps.photos/.home.HomeActivity",
        ("instagram",): "am start -n com.instagram.android/.activity.MainTabActivity",
        ("volume full", "volume max", "volume maximum", "max volume"): "termux-volume music 15",
        ("volume min", "volume minimum", "min volume"): "termux-volume music 1",
        ("volume mute", "mute volume", "mute"): "termux-volume music 0",
        ("volume medium", "volume half"): "termux-volume music 7",
        ("ring volume full", "ring max"): "termux-volume ring 7",
        ("ring mute", "mute ring"): "termux-volume ring 0",
        ("brightness maximum", "brightness 100", "brightness full"): "termux-brightness 100",
        ("vibrate",): "termux-vibrate -d 500",
        ("clipboard set",): 'termux-clipboard-set "Hello from Termux!"',
        ("clipboard get",): "termux-clipboard-get",
        ("message list",): "termux-sms-list",
        ("device info",): "termux-telephony-deviceinfo",
        ("toast test",): 'termux-toast "Hello world"'
    }
    if "water reminder" in input_lower or "water on" in input_lower:
        start_water_reminder()
        send_toast("Water reminder started.")
        return "Water reminder started."
    if "water off" in input_lower or "stop water" in input_lower:
        stop_water_reminder()
        send_toast("Water reminder stopped.")
        return "Water reminder stopped."
    for keywords, cmd in command_map.items():
        if any(kw in input_lower for kw in keywords):
            success, output = execute_command(cmd)
            if success:
                return "Task completed."
            else:
                return "I did not understand."
    return "I did not understand."
if __name__ == "__main__":
    while True:
        user_cmd = input("Enter your command: ")
        response = assistant_handler(user_cmd)
        print(response)

