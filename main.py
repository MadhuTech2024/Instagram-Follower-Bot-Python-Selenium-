from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv
load_dotenv()


class InstaFollower:
    def __init__(self):
        # Setup Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def login(self, username, password):
        self.driver.get("https://www.instagram.com/")
        time.sleep(3)

        # Enter username
        user_input = self.driver.find_element(By.NAME, "username")
        user_input.send_keys(username)

        # Enter password
        pass_input = self.driver.find_element(By.NAME, "password")
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def find_followers(self, account):
        # Go to target account page
        self.driver.get(f"https://www.instagram.com/{account}/")
        time.sleep(3)

        # Click followers link
        followers_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_link.click()
        time.sleep(5)

        # Scroll through followers modal
        modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']//ul/div")
        for i in range(5):  # Scroll 5 times (can increase as needed)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        # Click all visible "Follow" buttons
        follow_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Follow']")
        for button in follow_buttons:
            try:
                button.click()
                time.sleep(2)  # Pause to avoid being blocked
            except Exception as e:
                print("Error while clicking follow button:", e)


# ---------- RUNNING THE BOT ----------
USERNAME = os.getenv("INSTA_USERNAME")  # Load from .env or replace with your username
PASSWORD = os.getenv("INSTA_PASSWORD")  # Load from .env or replace with your password
TARGET_ACCOUNT = "chefsteps"

bot = InstaFollower()
bot.login(USERNAME, PASSWORD)
bot.find_followers(TARGET_ACCOUNT)
bot.follow()