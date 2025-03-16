import pyautogui
import time

print("Move your mouse to the position you want to capture.")
while True:
    x, y = pyautogui.position()  # Get the current mouse position
    print(f"Mouse position: x={x}, y={y}")
    time.sleep(0.1)  # Update every 100ms
