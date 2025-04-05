import json
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import os

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

    def backup_data(self, data, filename):
        """Saves data to JSON file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure directory exists
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(list(data), file, indent=4, ensure_ascii=False)
        print(f"📂 Data saved to {filename}")

        

   
