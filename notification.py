import time
import json
from datetime import datetime
from plyer import notification
import threading

def notify(message):
    notification.notify(
        title="Reminder",
        message=message,
        app_name="Smart Reminder App",
        timeout=10  # Duration in seconds
    )

def check_reminders(data):
    reminders = data.get('reminders', [])
    
    while True:
        now = datetime.now().time()
        for rem in reminders:
            # Adjust the parsing to handle both HH:MM and HH:MM:SS formats
            try:
                reminder_time = datetime.strptime(rem['time'], "%H:%M").time()
            except ValueError:
                reminder_time = datetime.strptime(rem['time'], "%H:%M:%S").time()
            
            if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
                notify(rem['message'])
                reminders.remove(rem)
                break  # Break to avoid modifying the list while iterating
        time.sleep(60)  # Check every minute

def check_reminders_thread(data):
    thread = threading.Thread(target=check_reminders, args=(data,))
    thread.daemon = True  # Allows the program to exit even if the thread is running
    thread.start()


