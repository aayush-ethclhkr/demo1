import pyautogui
import os
import time
from datetime import datetime

# Create a folder to save screenshots
folder_name = datetime.now().strftime("Screenshots_%Y%m%d_%H%M%S")
os.makedirs(folder_name, exist_ok=True)

# Time interval in seconds (1 minute)
interval = 60

print("[*] Silent screen monitoring started... (1 screenshot per minute)")

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(folder_name, f"screenshot_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        time.sleep(interval)

except KeyboardInterrupt:
    print("\n[!] Monitoring stopped by user.")
