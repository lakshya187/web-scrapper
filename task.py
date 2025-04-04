from scrappers.platform_scrapper_factory import ScraperFactory
from settings.redis import redis_client 
import json

def scrape_and_store(domain):
    """Scrapes a website and stores results in Redis."""
    scrapper = ScraperFactory.get_scraper(domain['platform'], domain['url'])
    if scrapper:
        product_links = scrapper.scrape()
        redis_client.set(domain['url'], json.dumps(list(product_links)))  # Store result in Redis
        print(f"✅ Scraped {len(product_links)} products from {domain['url']}")
    else:
        print(f"❌ No scraper found for {domain['url']}")
