import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException
from scrappers.platform_scrapers.base_scrapper import BaseScraper



class WestsideScraper(BaseScraper):
    """Scraper for Westside platform with data saving and timeout handling."""

    def __init__(self, url):
        super().__init__(url)
        self.driver = None  
        self.all_products = set()  # Store all product links
        self.MAX_NUMBER_OF_CATEGORIES = 5
       

    def scrape(self):
        """Main scraping function"""
        self.fetch_page()
        return list(self.all_products)

    def fetch_page(self):
        """Fetches collections and extracts products."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)

        try:
            self.driver.get(self.url)
            collection_links = self.get_collection_links()
            print(f'🔗 Found {len(collection_links)} collections.')

            for i, collection in enumerate(collection_links[:self.MAX_NUMBER_OF_CATEGORIES]):
                print(f"📦 Scraping collection: {collection}")
                self.scrape_collection(collection)

                if len(self.all_products) >= self.MAX_PRODUCTS:
                    print("🚨 Reached global product limit, stopping early.")
                    break
                

        except Exception as e:
            print(f"❌ Scraper failed: {e}")

        finally:
            self.driver.quit()  # Ensure WebDriver quits
       

    def get_collection_links(self):
        """Extracts collection links from navbar."""
        try:
            wait = WebDriverWait(self.driver, 15)  # Increased timeout
            nav_links = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav a[href*='/collections/']"))
            )
            return list(set(link.get_attribute("href") for link in nav_links))  # Unique links only
        except TimeoutException:
            print("⚠ Timeout while fetching collection links.")
            return []

    def scrape_collection(self, collection_url):
        """Scrapes products from a given collection page."""
        retries = 3  # Retry up to 3 times
        for attempt in range(retries):
            try:
                self.driver.get(collection_url)
                time.sleep(2)  # Allow page to load

                # Scroll and load all products
                self.scroll_to_load_products()

                # Extract product links
                page_source = self.driver.page_source
                product_links = self.extract_product_links(page_source)
                self.all_products.update(product_links)

                print(f"✅ Scraped {len(product_links)} products from {collection_url}")
                return

            except TimeoutException:
                print(f"⏳ Timeout on attempt {attempt + 1} for {collection_url}. Retrying...")
                time.sleep(2)

        print(f"❌ Failed to scrape {collection_url} after {retries} retries.")

    def scroll_to_load_products(self):
        """Scrolls to load lazy-loaded products."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break  # Stop scrolling if no new content is loaded
            last_height = new_height

        # Handle "Load More" button
        while True:
            try:
                load_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load more products')]"))
                )
                self.driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)
            except TimeoutException:
                break  # No more buttons

    def extract_product_links(self, html):
        """Extracts product links from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        product_links = set()

        for a in soup.select("a[href*='/products/']"):
            link = a["href"]
            if link.startswith("/"):
                link = f"https://www.westside.com{link}"  
            product_links.add(link)

        return product_links
