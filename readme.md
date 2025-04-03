Approach
Seed URLs – Start crawling from given domains.
HTML Parsing – Extract all <a> tags and filter product URLs.
URL Deduplication – Use Redis to avoid duplicate crawling.
Asynchronous Processing – Use RQ workers for parallel execution.
JavaScript Handling – Use Playwright for dynamic pages.
Output Storage – Save results in a structured JSON file.

Components
Component Choice Purpose
Web Scraping requests + BeautifulSoup Fetch and parse HTML pages
JavaScript Handling playwright Fetch dynamically loaded pages
Task Queue RQ (Redis Queue) Distributed crawling and async execution
Storage Redis Caching visited URLs
Concurrency Multiple RQ Workers Parallel execution for speed
Output Format JSON file Store discovered product URLs

Edgecases
Edge Case Solution
Duplicate URLs Use Redis to track visited URLs.
Infinite Crawling Restrict crawling within a given domain.
Dynamic Content Use Playwright for JavaScript-rendered pages.
Rate Limiting / Blocking Implement delays and rotate User-Agents.
Different URL structures Use regex-based patterns for product URLs.

Explanation of Each Folder & File
File/Folder Purpose
crawler/ Contains the main crawling logic
crawler.py Handles URL fetching, parsing, and queueing
url_extractor.py Extracts and filters valid product URLs
playwright_fetcher.py Fetches JS-rendered pages if needed
storage.py Manages Redis caching and JSON output
config/ Stores configuration files
settings.py Defines Redis settings, headers, timeouts
scripts/ Contains runnable scripts
run_crawler.py Main script to start the crawling process
output/ Stores final results
results.json JSON output of discovered product URLs
tests/ Contains unit tests
test_crawler.py Unit tests for core crawling functions
requirements.txt Lists dependencies
README.md Documentation on the approach, setup, and execution
.gitignore Excludes unnecessary files (e.g., cache, logs)
