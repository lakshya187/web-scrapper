from tasks import crawl_page  # ✅ Explicitly import the function
from rq import Queue
from rq.job import Job
import redis
# from tasks import crawl_page
from scrappers.platform_scrapper_factory import ScraperFactory
# Redis setup
redis_client = redis.Redis()
queue = Queue(connection=redis_client)
import json

def save_to_json(data, filename="scraped_data.json"):
        """Saves scraped data to a JSON file."""
        if isinstance(data, set):  # Convert set to list
            data = list(data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")
   
def start_crawler(domains):
    
    jobs = []  # Store job objects
    data = {}
    for domain in domains:
        # crawl_page(domain)
        scrapper = ScraperFactory.get_scraper(domain['platform'], domain['url'])   
        if scrapper:
         product_links = scrapper.scrape()
         data[domain['url']] = product_links

         
         print(f"Total product links: {len(product_links)}")
        
        # job = queue.enqueue(crawl_page, domain)  # ✅ Enqueue job correctly
        # print(f"Enqueued job {job.id} for {domain}")  
        # jobs.append(job.id)  # Store job ID

    save_to_json(data, "scraped_data.json")

    # return jobs  # Return list of job IDs

if __name__ == '__main__':
    job_ids = start_crawler([
        {'url': 'https://www.virgio.com/collections/all', 'platform': 'virgio'},

        # {'url': 'https://www.tatacliq.com/', 'platform': 'tatacliq'},
        # {'url': 'https://nykaafashion.com/', 'platform': 'shopify'},
        {'url': 'https://www.westside.com/', 'platform': 'westside'},

        # 'https://www.tatacliq.com/',
        # 'https://nykaafashion.com/',
        # 'https://www.westside.com/'
    ])

    # Fetch and check job results
    # for job_id in job_ids:
    #     job = Job.fetch(job_id, connection=redis_client)  # ✅ Fetch dynamically
    #     print(f"Job {job_id} status: {job.get_status()}")  # Show status


