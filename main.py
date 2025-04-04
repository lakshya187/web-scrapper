from rq import Queue
from rq.job import Job
from settings.redis import redis_client
import json
import time
from scrappers.platform_scrapper_factory import ScraperFactory
from task import scrape_and_store

# Connect to Redis & Create Queue
queue = Queue(connection=redis_client)

def save_to_json(data, filename="./output/scraped_data.json"):
    """Saves scraped data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"📂 Data saved to {filename}")

def start_crawler(domains):
    """Enqueues scraping jobs and waits for results."""
    jobs = []

    # Enqueue each job in Redis Queue
    for domain in domains:
        job = queue.enqueue(scrape_and_store, domain)  # ✅ Queue scrapper.scrape()
        jobs.append((domain['url'], job.id))  # Store job ID with URL
        print(f"🚀 Enqueued job {job.id} for {domain['url']}")

    # Wait for all jobs to finish and collect results
    all_data = {}
    for domain_url, job_id in jobs:
        while True:
            job = Job.fetch(job_id, connection=redis_client)
            if job.is_finished:
                break  # ✅ Job completed
            print(f"⏳ Waiting for job {job_id} ({domain_url})...")
            time.sleep(2)

        # Fetch results from Redis
        product_links = json.loads(redis_client.get(domain_url))
        all_data[domain_url] = product_links

    # Save results to JSON
    save_to_json(all_data, "scraped_data.json")


if __name__ == '__main__':
    start_crawler([
        {'url': 'https://www.virgio.com/collections/all', 'platform': 'virgio'},
        {'url': 'https://www.westside.com/', 'platform': 'westside'},
    ])
