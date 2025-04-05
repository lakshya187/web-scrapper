import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrappers.platform_scrapers.base_scrapper import BaseScraper
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




class TataCliqScraper(BaseScraper):
    
    def __init__(self, url, max_products=1000, products_per_category=50):
        super().__init__(url)
        self.max_products = max_products
        self.products_per_category = products_per_category
        self.driver = None
        self.all_products = set()

    def fetch_page(self):
        """Initialize headless Chrome with user-agent and extract category links from the sitemap."""
        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  # Reduce loading time by not waiting for full page load

        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.url)
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
    
        print("[Info] Clicking 'Show More Products' until all products are loaded or ceiling is hit...")
    
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
                    print(f"[Info] Reached product limit ({max_links}). Stopping load.")
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
                print("[Info] No clickable 'Show More Products' button found or timeout.")
                break
            
        print(f"[Info] Total product links extracted: {len(product_links)}")
        return set(list(product_links)[:max_links])  # just in case

    def scrape(self):
     """Main method to orchestrate the scraping process."""
     print(f'Starting scrapping for {self.url}...')
     all_categories = self.fetch_page()


     for category_url in all_categories:
         if len(self.all_products) >= self.max_products:
             break

         print(f"\n[Scraping Category] {category_url}")
         self.driver.get(category_url)
         time.sleep(3)

         # Extract all products (with internal logic to click "Show More")
         product_links = self.extract_product_links()
         total_found = len(product_links)

         print(f"[Info] Found {total_found} products in category.")

         if total_found == 0:
             print("[Warning] No products found in this category, skipping.")
             continue

         # Limit to products_per_category and remaining max limit
         allowed_links = list(product_links)[:min(self.products_per_category, self.max_products - len(self.all_products))]
         self.all_products.update(allowed_links)

         print(f"[Done] Added {len(allowed_links)} products from this category. Total so far: {len(self.all_products)}")

     self.driver.quit()
     return list(self.all_products)[:self.max_products]
