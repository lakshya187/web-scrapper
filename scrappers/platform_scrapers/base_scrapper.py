import json
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    """Abstract base class for web scrapers."""

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def fetch_page(self):
        """Fetches a webpage using requests."""
        pass

    @abstractmethod
    def extract_product_links(self, html):
        """Extract product links (must be implemented by subclasses)."""
        pass

    @abstractmethod
    def scrape(self):
        pass
        

   
