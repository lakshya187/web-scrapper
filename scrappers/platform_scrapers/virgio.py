import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrappers.base import BaseScraper
from bs4 import BeautifulSoup
import requests
from settings.logger import logger


class VirgioScrapper(BaseScraper):
    PRODUCT_PATTERNS = ["/products/", "/collections/all"]

    def scrape(self):
        html = self.fetch_page()
        all_products = self.extract_product_links(html)
        return list(all_products)

    def fetch_page(self):
        """Scrolls and clicks 'Load More' button until all products are loaded."""
        self.retry(lambda: self.driver.get(f"{self.url}collections/all"))
        wait = WebDriverWait(self.driver, 10)

        while True:
            try:
                # Find 'Load More' button and click it
                logger("🔄 Clicking 'Load More' button...")
                load_more_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'Load more products')]")
                    )
                )
                self.retry(
                    lambda: self.driver.execute_script(
                        "arguments[0].click();", load_more_button
                    )
                )
                time.sleep(3)  # Wait for new products to load
            except Exception:
                # Stop if 'Load More' button is no longer found
                logger("No more 'Load More' button found. All products loaded.")
                break

        # Now scrape the fully loaded page
        html = self.driver.page_source
        self.driver.quit()
        logger(f"Fetching data for {self.url}...")
        return html

    def extract_product_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        unique_links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if any(pattern in href for pattern in self.PRODUCT_PATTERNS):
                unique_links.add(requests.compat.urljoin(self.url, href))
        logger(f"Found {len(unique_links)} unique product links. On {self.url}")
        return unique_links
