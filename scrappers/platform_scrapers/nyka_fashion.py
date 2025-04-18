import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrappers.base import BaseScraper
from selenium.common.exceptions import TimeoutException
from settings.logger import logger


class NykaaScraper(BaseScraper):
    def __init__(
        self,
        url,
    ):
        super().__init__(url)
        self.all_products = set()

    def scrape(self):
        """Main method to start scraping."""
        self.retry(lambda: self.fetch_page())
        return list(self.all_products)

    def fetch_page(self):
        """Using Selenium to navigate categories, trigger lazy loading, and extract product links."""
        self.driver.get(self.url)
        time.sleep(3)
        # **Get category links**
        category_links = self.retry(lambda: self.get_category_links())
        for category in category_links[:2]:  # Testing on 2 categories
            logger(f"📦 Scraping category: {category}")
            self.scrape_category(category)
        self.driver.quit()

    def get_category_links(self):
        """Extracts category links from the navbar."""
        wait = WebDriverWait(self.driver, 15)
        try:
            nav_menu = self.retry(
                lambda: wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div[data-at='mega-menu']")
                    )
                )
            )
            category_elements = nav_menu.find_elements(By.CSS_SELECTOR, "a[href^='/']")
            category_links = set(
                el.get_attribute("href")
                for el in category_elements
                if "/c/" in el.get_attribute("href")
            )
            if not category_links:
                logger("⚠️ No categories found. The page structure might have changed.")

            return list(category_links) if category_links else []

        except TimeoutException:
            logger(
                "⏳ Timeout: Navbar categories not found. Retrying with page source..."
            )
            logger(self.driver.page_source)  # Debugging: logger HTML

    def scrape_category(self, category_url):
        """Scrapes products from a given category page."""
        self.retry(lambda: self.driver.get(category_url))
        time.sleep(3)
        self.retry(lambda: self.scroll_to_load_products())
        page_source = self.driver.page_source
        product_links = self.retry(lambda: self.extract_product_links(page_source))
        self.all_products.update(product_links)

        if len(self.all_products) >= self.MAX_PRODUCTS:
            logger("Reached product limit. Stopping scrape.")
            return

    def scroll_to_load_products(self):
        """Scrolls to trigger lazy loading but stops after collecting a fixed number of products."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Extract product links from the current page
            page_source = self.driver.page_source
            product_links = self.extract_product_links(page_source)
            self.all_products.update(product_links)
            # Stop scrolling when the limit is reached
            if len(self.all_products) >= self.MAX_PRODUCTS:
                logger(
                    f"✅ Collected {len(self.all_products)} products. Stopping scrolling."
                )
                break

            # Scroll down to load more products
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)  # Allow time for new products to load

            # Check if the page height changes (to detect end of page)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logger("⚠️ No more products loaded. Stopping scrolling.")
                break

            last_height = new_height

    def extract_product_links(self, html):
        """Extracts product links from HTML content."""
        soup = BeautifulSoup(html, "html.parser")
        product_links = set()

        # Select all <a> tags where href contains "/p/"
        for a in soup.select("a[href^='/'][href*='/p/']"):
            link = a["href"]
            if link.startswith("/"):
                link = f"https://www.nykaafashion.com{link}"
            product_links.add(link)

        logger(f"✅ Extracted {len(product_links)} product links")
        return product_links
