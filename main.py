import asyncio
import json
import time
from scrappers.platform_scrapper_factory import ScraperFactory

def save_to_json(data, filename="./output/scraped_data.json"):
    """Saves scraped data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"📂 Data saved to {filename}")

async def scrape_and_store_async(domain):
    """Asynchronously runs a scraper."""
    print(f"🚀 Starting scraper for {domain['url']}")
    
    # Run the blocking scraper in a separate thread
    scraper = ScraperFactory.get_scraper(domain["platform"], domain["url"])
    scraped_data = await asyncio.to_thread(scraper.scrape)  # Runs scraper in a thread

    return {domain["url"]: scraped_data}  # Store result

async def start_crawler(domains):
    """Runs all scrapers asynchronously."""
    tasks = [scrape_and_store_async(domain) for domain in domains]  
    results = await asyncio.gather(*tasks)  # Wait for all scrapers

    # Combine results into a single dictionary
    all_data = {url: data for result in results for url, data in result.items()}

    # Save results
    save_to_json(all_data, "./output/scraped_data.json")

if __name__ == '__main__':
    domains = [
        # {'url': 'https://www.virgio.com/collections/all', 'platform': 'virgio'},
        # {'url': 'https://www.westside.com/', 'platform': 'westside'},
        # {'url': "https://www.nykaafashion.com/", 'platform': 'nykaafashion'},
         {'url': "https://www.tatacliq.com/sitemap", 'platform': 'tatacliq'},
    ]
    asyncio.run(start_crawler(domains))
    print("🛑 Scraping completed."  )
