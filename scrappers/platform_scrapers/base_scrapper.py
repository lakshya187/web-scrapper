import json
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
class BaseScraper(ABC):
    """Abstract base class for web scrapers."""

    def __init__(self, url, headless=True, max_products= 1000):
        self.url = url
        self.MAX_PRODUCTS = max_products
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")  # Use new headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # **Set a random User-Agent**
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")

        # **Disable automation detection**
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # **Start Selenium WebDriver**
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # **Bypass Selenium detection**
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    @abstractmethod
    def fetch_page(self):
        """Fetches a webpage using requests."""
        pass

    @abstractmethod
    def extract_product_links(self, html):
        """Extract product links (must be implemented by subclasses)."""
        pass

    @abstractmethod
    def scrape(self):
        pass

    @staticmethod
    def backup_data(data, filename):
        """Saves data to JSON file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure directory exists
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(list(data), file, indent=4, ensure_ascii=False)
        print(f"📂 Data saved to {filename}")

    def retry(action, retries=3):
        for _ in range(retries):
            try:
                return action()
            except Exception:
                time.sleep(1)
        raise Exception("Failed after retries")


