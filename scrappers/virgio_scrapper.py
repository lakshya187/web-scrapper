
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrappers.platform_scrapers.base_scrapper import BaseScraper
from bs4 import BeautifulSoup
import requests

class VirgioScrapper(BaseScraper):
    
    PRODUCT_PATTERNS = ["/products/", "/collections/all"]

    """Shopify scraper that supports lazy loading."""
    def scrape(self):
        """Main method to scrape the page."""
        html =  self.fetch_page()
        all_products = self.extract_product_links(html)
        return list(all_products)
    

    def fetch_page(self):
        print(f'Fetching data for {self.url}...')
        """Scrolls and clicks 'Load More' button until all products are loaded."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(f"{self.url}collections/all")
        wait = WebDriverWait(driver, 10)

        while True:
            try:
                # Find 'Load More' button and click it
                load_more_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load more products')]"))
                )
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)  # Wait for new products to load
            except Exception:
                # Stop if 'Load More' button is no longer found
                print("No more 'Load More' button found. All products loaded.")
                break  

        # Now scrape the fully loaded page
        html = driver.page_source
        driver.quit()
        print(f'Fetching data for {self.url}...')
        return html
        
    def extract_product_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        unique_links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if any(pattern in href for pattern in self.PRODUCT_PATTERNS):
                unique_links.add(requests.compat.urljoin(self.url, href))
        print(f"Found {len(unique_links)} unique product links. On {self.url}")    
        return unique_links
  


