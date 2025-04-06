import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from scrappers.platform_scrapers.base_scrapper import BaseScraper
from settings.logger import logger


class WestsideScraper(BaseScraper):
    """Scraper for Westside platform with data saving and timeout handling."""

    def __init__(self, url):
        super().__init__(url)
        self.all_products = set()  # Store all product links
        self.MAX_NUMBER_OF_CATEGORIES = 5

    def scrape(self):
        """Main scraping function"""
        self.fetch_page()
        return list(self.all_products)

    def fetch_page(self):
        try:
            self.retry(lambda: self.driver.get(self.url))
            collection_links = self.retry(lambda: self.get_collection_links())
            logger(f"🔗 Found {len(collection_links)} collections.")

            for i, collection in enumerate(
                collection_links[: self.MAX_NUMBER_OF_CATEGORIES]
            ):
                logger(f"📦 Scraping collection: {collection}")
                self.retry(lambda: self.scrape_collection(collection))

                if len(self.all_products) >= self.MAX_PRODUCTS:
                    logger("🚨 Reached global product limit, stopping early.")
                    break

        except Exception as e:
            logger(f"❌ Scraper failed: {e}")

        finally:
            self.driver.quit()  # Ensure WebDriver quits

    def get_collection_links(self):
        """Extracts collection links from navbar."""
        try:
            wait = WebDriverWait(self.driver, 15)  # Increased timeout
            nav_links = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "nav a[href*='/collections/']")
                )
            )
            return list(
                set(link.get_attribute("href") for link in nav_links)
            )  # Unique links only
        except TimeoutException:
            logger("⚠ Timeout while fetching collection links.")
            return []

    def scrape_collection(self, collection_url):
        """Scrapes products from a given collection page."""

        self.driver.get(collection_url)
        time.sleep(2)  # Allow page to load
        # Scroll and load all products
        self.retry(lambda: self.scroll_to_load_products())
        # Extract product links
        page_source = self.driver.page_source
        product_links = self.extract_product_links(page_source)
        self.all_products.update(product_links)
        logger(f"✅ Scraped {len(product_links)} products from {collection_url}")
        return

    def scroll_to_load_products(self):
        """Scrolls to load lazy-loaded products."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break  # Stop scrolling if no new content is loaded
            last_height = new_height

        # Handle "Load More" button
        while True:
            try:
                load_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'Load more products')]")
                    )
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
