from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from scrappers.platform_scrapers.base_scrapper import BaseScraper

class WestsideScraper(BaseScraper):
    """Scraper for Westside platform."""

    def __init__(self, url):
        super().__init__(url)
        self.driver = None  # Initialize WebDriver in fetch_page()
    def scrape(self):
        return self.fetch_page()

        # self.save_to_json(all_products, "westside_products.json")

    def fetch_page(self):
        """Uses Selenium to navigate collections, trigger lazy loading, and extract product links."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 10)

        # Step 1: Extract all collection links from navbar
        collection_links = self.get_collection_links()

        all_products = set()

        for collection in collection_links:
            print(f"Scraping collection: {collection}")
            self.driver.get(collection)
            time.sleep(3)  # Wait for page to load

            # Step 2: Scroll and load all products
            self.scroll_to_load_products()

            # Step 3: Extract product links from loaded page
            page_source = self.driver.page_source
            product_links = self.extract_product_links(page_source)
            all_products.update(product_links)  # Add unique links

        self.driver.quit()
        return all_products

    def get_collection_links(self):
        """Extracts all collection links from the navbar."""
        wait = WebDriverWait(self.driver, 10)
        nav_links = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav a[href*='/collections/']"))
        )
        return list(set(link.get_attribute("href") for link in nav_links))  # Unique links only

    def scroll_to_load_products(self):
        """Scrolls to the bottom multiple times to trigger lazy loading."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for lazy loading
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Stop scrolling if no new content is loaded
            if new_height == last_height:
                break
            last_height = new_height
        
        # Click "Load More" buttons if present
        while True:
            try:
                load_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load more products')]"))
                )
                self.driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)  # Wait for more products to load
            except Exception:
                break  # No more "Load More" button

    def extract_product_links(self, html):
        """Extract product links from the HTML content."""
        soup = BeautifulSoup(html, "html.parser")
        product_links = set()

        for a in soup.select("a[href*='/products/']"):
            link = a["href"]
            if link.startswith("/"):
                link = f"https://www.westside.com{link}"  # Convert relative to absolute URL
            product_links.add(link)

        return product_links
