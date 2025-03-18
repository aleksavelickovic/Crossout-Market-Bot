import pyautogui
import pytesseract
from PIL import Image
import time
import threading
import keyboard  # To listen for key presses
import re  # Regular expressions to clean and extract valid numbers
import cv2
import numpy as np

# Set the path to Tesseract (if necessary for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define constants
MIN_PROFIT = 0.1  # Minimum profit in coins to continue buying/selling
MARKET_FEE = 0.10  # 10% market fee on the sell price

# Coordinates for UI elements (to be adjusted based on your screen layout)
ITEM_CONTEXT_MENU_COORDS = (1722, 360)  # Coordinates of the item in "My Offers" (right-click to open context menu)
TRADE_BUTTON_COORDS = (1725, 412)  # Coordinates of the "Trade" button (adjust accordingly)
PRICE_FIELD_COORDS = (1078, 445)  # Coordinates of the price field in price adjusting tab (adjust accordingly)
GO_BACK_BUTTON_COORDS = (50, 111)  # Coordinates of the back button (adjust accordingly)
BUY_BUTTON_COORDS = (154, 983)
SELL_BUTTON_COORDS = (734, 963)
LONG_PRESS_COORDS = (802, 776)
MARKET_TAB_COORDS = (396, 41)

# OCR regions for BUY and SELL price fields
SELL_PRICE_REGION = (182, 899, 110, 41)  # Sell price field coordinates
BUY_PRICE_REGION = (751, 899, 110, 41)   # Buy price field coordinates
MY_OFFERS_SALE_PRICE_REGION = (974, 369, 175, 45)
MY_OFFERS_PURCHASE_PRICE_REGION = (1395, 369, 175, 45)
LAST_PURCHASE_PRICE_REGION = (797, 405, 110, 41)

# Global flag to check if we should stop the script
stop_script = False

# Function to capture a screenshot of the region and use OCR to read it
def read_price_from_screen(region=None):
    # Capture screenshot of the specified region
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("screenshot.png")  # Save for debugging

    # Use pytesseract to extract text (numbers) from the image
    extracted_text = pytesseract.image_to_string(screenshot, config='--psm 6')

    print(f"Extracted text: {extracted_text}")

    # Preprocess the extracted text to remove unwanted characters (like spaces or non-numeric symbols)
    extracted_text = re.sub(r'[^0-9.,]', '', extracted_text)  # Keep only numbers, commas, or periods

    print(f"Processed text: {extracted_text}")

    # Try to extract the first valid number from the OCR output
    try:
        # Replace commas with dots (for decimal points), if needed
        extracted_text = extracted_text.replace(",", ".")

        # Convert the cleaned-up text into a float
        price = float(extracted_text.strip())  # Convert extracted text to a float
        return price
    except ValueError:
        return None  # Return None if OCR didn't find a valid number

# Function to adjust buy orders
def adjust_buy_order(current_price, item_coords):
    
    while True:
        if stop_script:  # Check if the script should stop
            print("Stopping script.")
            return

        # Read the current highest buy price from the screen
        market_buy_price = read_price_from_screen(region=BUY_PRICE_REGION)
        market_sell_price = read_price_from_screen(region=SELL_PRICE_REGION)

        if ((market_sell_price * 0.90) - market_buy_price) < 5:
            print("Profit would be too small to raise the price!")
            keyboard.press_and_release("esc")
            break

        if market_buy_price is None:
            print("Could not read market price. Skipping adjustment.")
            keyboard.press_and_release("esc")
            break

        print(f"Current market price: {market_buy_price}")

        if market_buy_price > current_price:
            # Calculate the new buy price (add 0.01 coins)
            new_price = market_buy_price + 0.01

            # Move to the price input field and update the price
            time.sleep(2)
            pyautogui.moveTo(GO_BACK_BUTTON_COORDS, duration=1)
            pyautogui.click()
            
            pyautogui.moveTo(item_coords, duration=1)
            pyautogui.click()

            pyautogui.moveTo(PRICE_FIELD_COORDS, duration=1)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')  # Select all text in price field
            pyautogui.press('backspace')  # Clear the text
            pyautogui.write(str(new_price))  # Write the new price
            #pyautogui.press('enter')  # Confirm the new price
            pyautogui.moveTo(LONG_PRESS_COORDS, duration=1)
            pyautogui.mouseDown()
            time.sleep(1)
            pyautogui.mouseUp()
            time.sleep(4)
            keyboard.press_and_release("esc")

            print(f"Buy order adjusted to {new_price} coins.")

        else:
            print(f"No higher bid found. Skipping buy order adjustment.")
            keyboard.press_and_release("esc")
            break

        # Wait a bit before making another adjustment (to avoid too many rapid clicks)
        time.sleep(2)
        break

# Function to adjust sell orders
def adjust_sell_order(current_price, item_coords):
    
    while True:
        if stop_script:  # Check if the script should stop
            print("Stopping script.")
            return

        # Read the current highest buy price from the screen
        market_price = read_price_from_screen(region=SELL_PRICE_REGION)
        last_purchased_price = read_price_from_screen(region=LAST_PURCHASE_PRICE_REGION)
        if market_price is None:
            print("Could not read market price. Skipping adjustment.")
            keyboard.press_and_release("esc")
            break

        print(f"Current market price: {market_price}")

        if ((market_price * 0.90) - last_purchased_price) < 5:
            print("PROFITS WOULD BE TOO SMALL IF WE DECREASE THE PRICE FURTHER!!!!!!!!")
            keyboard.press_and_release("esc")
            break

        if market_price < current_price:
            # Calculate the new buy price (add 0.01 coins)
            new_price = market_price - 0.01

            # Move to the price input field and update the price
            time.sleep(2)
            pyautogui.moveTo(GO_BACK_BUTTON_COORDS, duration=1)
            pyautogui.click()
            
            pyautogui.moveTo(item_coords, duration=1)
            pyautogui.click()

            pyautogui.moveTo(PRICE_FIELD_COORDS, duration=1)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')  # Select all text in price field
            pyautogui.press('backspace')  # Clear the text
            pyautogui.write(str(new_price))  # Write the new price
            #pyautogui.press('enter')  # Confirm the new price
            pyautogui.moveTo(LONG_PRESS_COORDS, duration=1)
            pyautogui.mouseDown()
            time.sleep(1)
            pyautogui.mouseUp()
            time.sleep(2)
            keyboard.press_and_release("esc")

            print(f"Buy order adjusted to {new_price} coins.")

        else:
            print(f"No lower bid found. Skipping sell order adjustment.")
            keyboard.press_and_release("esc")
            break

        # Wait a bit before making another adjustment (to avoid too many rapid clicks)
        time.sleep(5)
        break

    

# Function to cancel the order (simulates a click on the cancel button)
def cancel_order():
    pyautogui.moveTo(GO_BACK_BUTTON_COORDS, duration=1)
    pyautogui.click()
    print("Order cancelled.")

# Function to differentiate and interact with each item in the "My Offers" tab
def interact_with_my_offers():
    # Assuming there are 7 items, but adjust this number based on the actual number of items you have
    num_items = 7
    
    while True:
        for i in range(num_items): 
            if stop_script:  # Check if the script should stop
                print("Stopping script.")
                return  # Exit the function instead of breaking the loop

            print(f"Processing item {i + 1}...")

            # Adjust the regions for each iteration
            sale_price_region = (MY_OFFERS_SALE_PRICE_REGION[0], MY_OFFERS_SALE_PRICE_REGION[1] + i * 83, MY_OFFERS_SALE_PRICE_REGION[2], MY_OFFERS_SALE_PRICE_REGION[3])
            purchase_price_region = (MY_OFFERS_PURCHASE_PRICE_REGION[0], MY_OFFERS_PURCHASE_PRICE_REGION[1] + i * 83, MY_OFFERS_PURCHASE_PRICE_REGION[2], MY_OFFERS_PURCHASE_PRICE_REGION[3])

            sale_price = read_price_from_screen(sale_price_region)
            purchase_price = read_price_from_screen(purchase_price_region)

            while isinstance(sale_price, float) and isinstance(purchase_price, float):
                print("RESCANING THE PRICES!")
                sale_price = read_price_from_screen(sale_price_region)
                purchase_price = read_price_from_screen(purchase_price_region)

            if sale_price is None and purchase_price is None:
                keyboard.press_and_release("esc")
                print("RESTARTING INTERACTIONS")
                pyautogui.moveTo(MARKET_TAB_COORDS, duration=1)
                pyautogui.click()
                time.sleep(2)
                #interact_with_my_offers() // Breaking the loop instead of calling the function recursively to aviod a memory leak and reaching maximum recursion depth
                break

            if sale_price is None or not isinstance(sale_price, float):
                print("ITEM IS BEING BOUGHT")
                # Calculate the Y position based on the index (adjusting for offset of 50px between items)
                item_y_position = ITEM_CONTEXT_MENU_COORDS[1] + i * 83

                # Step 1: Right-click on the item to open the context menu
                pyautogui.moveTo(ITEM_CONTEXT_MENU_COORDS[0], item_y_position, duration=1)
                pyautogui.rightClick()
                print(f"Right-clicking on item {i + 1} at Y={item_y_position}...")

                # Step 2: Click the "Trade" button to view the item's price
                pyautogui.moveTo(TRADE_BUTTON_COORDS[0], TRADE_BUTTON_COORDS[1] + i * 83, duration=1)
                pyautogui.click()
                print(f"Clicked on 'Trade' for item {i + 1}...")

                time.sleep(2)  # Give time for the trade screen to load

                # Step 3: Read the price of the item (using different regions for sell and buy)
                current_sell_price = read_price_from_screen(region=SELL_PRICE_REGION)
                current_buy_price = read_price_from_screen(region=BUY_PRICE_REGION)

                if current_sell_price is None or current_buy_price is None:
                    print(f"Couldn't read price for item {i + 1}. Skipping item.")
                    keyboard.press_and_release("esc")
                    continue

                print(f"Item {i + 1} sell price: {current_sell_price}, buy price: {current_buy_price}")

                # if current_buy_price != purchase_price:
                time.sleep(2)
                adjust_buy_order(purchase_price, (ITEM_CONTEXT_MENU_COORDS[0], ITEM_CONTEXT_MENU_COORDS[1] + i * 83))  # Adjust buy price based on the sell price

            elif purchase_price is None or not isinstance(purchase_price, float):
                print("ITEM IS BEING SOLD")
                # Calculate the Y position based on the index (adjusting for offset of 83px between items)
                item_y_position = ITEM_CONTEXT_MENU_COORDS[1] + i * 83

                # Step 1: Right-click on the item to open the context menu
                pyautogui.moveTo(ITEM_CONTEXT_MENU_COORDS[0], item_y_position, duration=1)
                pyautogui.rightClick()
                print(f"Right-clicking on item {i + 1} at Y={item_y_position}...")

                # Step 2: Click the "Trade" button to view the item's price
                pyautogui.moveTo(TRADE_BUTTON_COORDS[0], TRADE_BUTTON_COORDS[1] + i * 83, duration=1)
                pyautogui.click()
                print(f"Clicked on 'Trade' for item {i + 1}...")

                time.sleep(2)  # Give time for the trade screen to load

                # Step 3: Read the price of the item (using different regions for sell and buy)
                current_sell_price = read_price_from_screen(region=SELL_PRICE_REGION)
                current_buy_price = read_price_from_screen(region=BUY_PRICE_REGION)

                if current_sell_price is None or current_buy_price is None:
                    print(f"Couldn't read price for item {i + 1}. Skipping item.")
                    keyboard.press_and_release("esc")
                    continue

                print(f"Item {i + 1} sell price: {current_sell_price}, buy price: {current_buy_price}")

                # if current_sell_price != sale_price:
                time.sleep(2)
                adjust_sell_order(sale_price, (ITEM_CONTEXT_MENU_COORDS[0], ITEM_CONTEXT_MENU_COORDS[1] + i * 83))  # Adjust sell price based on the sell price

            time.sleep(1)  # Wait before moving to the next item

# Function to listen for the stop button (Esc key)
def listen_for_stop():
    global stop_script
    print("Press 'Esc' to stop the script.")
    while True:
        if keyboard.is_pressed("esc"):  # Check if 'Esc' is pressed
            stop_script = True
            break
        time.sleep(0.1)  # Check every 0.1 seconds

# Run the stop listening in a separate thread
stop_thread = threading.Thread(target=listen_for_stop)
stop_thread.start()
def draw_regions_on_screen():
    # Capture a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Define the regions
    regions = {
        "SELL_PRICE_REGION": SELL_PRICE_REGION,
        "BUY_PRICE_REGION": BUY_PRICE_REGION,
        "MY_OFFERS_SALE_PRICE_REGION": MY_OFFERS_SALE_PRICE_REGION,
        "MY_OFFERS_PURCHASE_PRICE_REGION": MY_OFFERS_PURCHASE_PRICE_REGION
    }

    # Draw rectangles for each region
    for name, region in regions.items():
        x, y, w, h = region
        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(screenshot, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the screenshot with the drawn regions
    cv2.imshow("Regions", screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Call the function to draw regions on the screen
# draw_regions_on_screen()
# Start interacting with offers
interact_with_my_offers()
