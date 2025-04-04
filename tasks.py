import requests
from bs4 import BeautifulSoup
import redis
from rq import Queue

# Redis setup
redis_client = redis.Redis()
queue = Queue('crawlerQueue', connection=redis_client)

PRODUCT_PATTERNS = ['collections/all']

def crawl_page(url):
    print(f'Crawling: {url}')
    
    if redis_client.exists(url):
        print(f'Skipping already visited URL: {url}')
        return
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        unique_links = set()
        all_links = soup.find_all('a', href=True)
        # print(all_links)
        for a_tag in all_links:
            href = a_tag['href']
            if any(pattern in href for pattern in PRODUCT_PATTERNS):
                unique_links.add(requests.compat.urljoin(url, href))
        
        for link in unique_links:
            print(link)
            # redis_client.set(link, 'visited')
            # queue.enqueue(crawl_page, link)  
        
    except requests.exceptions.RequestException as e:
        print(f'Error crawling {url}: {e}')
