from tasks import crawl_page  # ✅ Explicitly import the function
from rq import Queue
from rq.job import Job
import redis
from tasks import crawl_page
# Redis setup
redis_client = redis.Redis()
queue = Queue(connection=redis_client)

def start_crawler(domains):
    
    jobs = []  # Store job objects
    for domain in domains:
        crawl_page(domain)
        # job = queue.enqueue(crawl_page, domain)  # ✅ Enqueue job correctly
        # print(f"Enqueued job {job.id} for {domain}")  
        # jobs.append(job.id)  # Store job ID

    # return jobs  # Return list of job IDs

if __name__ == '__main__':
    job_ids = start_crawler([
        'https://www.virgio.com/',
        # 'https://www.tatacliq.com/',
        # 'https://nykaafashion.com/',
        # 'https://www.westside.com/'
    ])

    # Fetch and check job results
    for job_id in job_ids:
        job = Job.fetch(job_id, connection=redis_client)  # ✅ Fetch dynamically
        print(f"Job {job_id} status: {job.get_status()}")  # Show status
