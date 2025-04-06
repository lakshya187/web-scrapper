import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrappers.platform_scrapers.base_scrapper import BaseScraper
from settings.logger import logger

class TataCliqScraper(BaseScraper):
    
    def __init__(self, url, products_per_category=50):
        headless = False # Tata Cliq has anti-bot measures, using headless mode blocks requests and products are not fetched.
        super().__init__(url, headless)
        self.products_per_category = products_per_category
        self.all_products = set()

    def fetch_page(self):
        """Initialize headless Chrome with user-agent and extract category links from the sitemap."""

        self.driver.get(f"{self.url}sitemap")
        time.sleep(3)
        return self.get_category_links()

    def get_category_links(self):
        """Extract category links from the sitemap page."""
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        category_links = set()

        for a in soup.find_all("a", class_="SitemapPage__link"):
            href = a.get("href")
            if href and href.startswith("/") and "/p/" not in href:
                full_url = f"https://www.tatacliq.com{href}"
                category_links.add(full_url)

        return list(category_links)
    
    def extract_product_links(self):
        """Extract product links by clicking 'Show More Products' until 'Back to Top' or ceiling is reached."""
    
    
        product_links = set()
        max_links = self.products_per_category  # You can pass this via constructor
    
        while True:
            try:
                # Check current loaded links before clicking
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
    
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag["href"]
                    if "/p-mp" in href:
                        full_url = f"https://www.tatacliq.com{href}" if href.startswith("/") else href
                        product_links.add(full_url)
    
                if len(product_links) >= max_links:
                    logger(f"[Info] Reached product limit ({max_links}). Stopping load.")
                    break
                
                # Wait and check the button
                button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ShowMoreButtonPlp__button"))
                )
    
                button_text = button.text.strip().lower()
                if "back to top" in button_text:
                    break
                
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
    
            except Exception:
                break
            
        logger(f"[Info] Total product links extracted: {len(product_links)}")
        return set(list(product_links)[:max_links])  # just in case

    def scrape(self):
     """Main method to orchestrate the scraping process."""
     logger(f'Starting scrapping for {self.url}...')
     all_categories = self.fetch_page()


     for category_url in all_categories:
         if len(self.all_products) >= self.MAX_PRODUCTS:
             break

         logger(f"\n[Scraping Category] {category_url}")
         self.driver.get(category_url)
         time.sleep(3)

         # Extract all products (with internal logic to click "Show More")
         product_links = self.extract_product_links()
         total_found = len(product_links)

         logger(f"[Info] Found {total_found} products in category.")

         if total_found == 0:
             logger("[Warning] No products found in this category, skipping.")
             continue

         # Limit to products_per_category and remaining max limit
         allowed_links = list(product_links)[:min(self.products_per_category, self.MAX_PRODUCTS - len(self.all_products))]
         self.all_products.update(allowed_links)

         logger(f"[Done] Added {len(allowed_links)} products from this category. Total so far: {len(self.all_products)}")

     self.driver.quit()
     return list(self.all_products)[:self.MAX_PRODUCTS]
