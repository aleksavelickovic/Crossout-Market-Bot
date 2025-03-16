import pyautogui
import time

# Move the mouse to the position (x=100, y=200) and click
pyautogui.moveTo(100, 200, duration=1)  # Move to position over 1 second
pyautogui.click()  # Click the mouse

# Alternatively, you can use screen coordinates for the "Buy" button in the game
# For example, you can also click after moving the mouse
pyautogui.moveTo(500, 300, duration=1)  # X and Y coordinates of the "Buy" button
pyautogui.click()

# After clicking, wait for some time (e.g., 2 seconds) to simulate human behavior
time.sleep(2)

# You can also type in text (e.g., set the price or confirm an order)
pyautogui.write('100.01')  # Example price
pyautogui.press('enter')  # Press Enter to confirm
