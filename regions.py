import cv2
import numpy as np
import pyautogui

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
draw_regions_on_screen()