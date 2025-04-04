
from bs4 import BeautifulSoup
from scrappers.platform_scrapers.base_scrapper import BaseScraper
import requests

class ShopifyScraper(BaseScraper):
    """Scraper for Shopify-based stores."""

    PRODUCT_PATTERNS = ["/products/", "/collections/all"]

    def fetch_page(self):
        """Fetches a webpage using requests."""
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    

    def extract_product_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        unique_links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if any(pattern in href for pattern in self.PRODUCT_PATTERNS):
                unique_links.add(requests.compat.urljoin(self.url, href))

        return unique_links
