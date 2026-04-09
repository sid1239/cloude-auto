"""
Leofame Instagram Automation
- Runs on 4 services: views, likes, saves, shares
- Uses same Instagram reel link
- Uses website default selected values
- Case-insensitive button detection (fixes Get Free Shares)
- Takes screenshot immediately after click
- Waits 1 minute
- Takes another screenshot
- Sends both screenshots to Telegram
- Skips failed pages and continues
- GitHub Actions ready
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URLS = [
    "https://leofame.com/free-instagram-views",
    "https://leofame.com/free-instagram-likes",
    "https://leofame.com/free-instagram-saves",
    "https://leofame.com/free-instagram-shares",
]

INSTAGRAM_LINK = "https://www.instagram.com/reel/DU07x-mDx8e/?igsh=dGtkMjNmbGpncG83"

TELEGRAM_BOT_TOKEN = "8793923431:AAH5eX0CGpos4v6u1XEMO8LTLxPm-QcH3rA"
TELEGRAM_CHAT_ID = "1814769108"


def send_to_telegram(image_path, caption=""):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        requests.post(
            api_url,
            data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
            files={"photo": img},
            timeout=60,
        )


def submit_all_services():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    wait = WebDriverWait(driver, 25)

    try:
        for url in URLS:
            try:
                print(f"Opening {url}")
                driver.get(url)

                # Find Instagram link input
                link_box = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder*='instagram.com']")
                    )
                )
                link_box.clear()
                link_box.send_keys(INSTAGRAM_LINK)

                # Case-insensitive Get Free button
                button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'get free')]",
                        )
                    )
                )
                button.click()
                print(f"Submitted successfully for: {url}")

                page_name = url.split("/")[-1]

                # Screenshot immediately after click
                shot1 = f"{page_name}_after_click.png"
                driver.save_screenshot(shot1)
                send_to_telegram(shot1, f"{page_name} - immediately after click")

                # Wait 1 minute
                time.sleep(60)

                # Screenshot after 1 minute
                shot2 = f"{page_name}_after_1min.png"
                driver.save_screenshot(shot2)
                send_to_telegram(shot2, f"{page_name} - after 1 minute")

            except Exception as page_error:
                print(f"Failed on {url}: {page_error}")
                continue

    finally:
        driver.quit()


if __name__ == "__main__":
    submit_all_services()
