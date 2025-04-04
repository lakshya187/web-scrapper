
import time
from scrappers.platform_scrapers.base_scrapper import BaseScraper

class SeleniumScraper(BaseScraper):
    """Scraper that loads all products by clicking 'Load More' until all items are visible."""
