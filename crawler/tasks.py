import requests
from bs4 import BeautifulSoup
import redis
from rq import Queue

# Redis setup
redis_client = redis.Redis()
queue = Queue('crawlerQueue', connection=redis_client)

PRODUCT_PATTERNS = ['/product/', '/p/', '/item/']

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
        links = set()
        
        # for a_tag in soup.find_all('a', href=True):
        #     href = a_tag['href']
        #     if any(pattern in href for pattern in PRODUCT_PATTERNS):
        #         links.add(requests.compat.urljoin(url, href))
        
        # for link in links:
        #     redis_client.set(link, 'visited')
        #     queue.enqueue(crawl_page, link)  
        
    except requests.exceptions.RequestException as e:
        print(f'Error crawling {url}: {e}')
