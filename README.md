# Assignment 6: Backend Engineer Role

## Problem Statement: Crawler for Discovering Product URLs on E-commerce Websites

### Objective

Design and implement a scalable, robust, and performant web crawler that discovers and extracts all product URLs from multiple e-commerce platforms. The crawler should support both the initially provided domains and scale to accommodate many more.

### Covered Domains

- https://www.virgio.com/
- https://www.tatacliq.com/
- https://www.nykaafashion.com/
- https://www.westside.com/

---

## Tech Stack

- **Python** (Primary language)
- **Selenium** (Web automation & dynamic content handling)
- **BeautifulSoup** (HTML parsing)
- **JSON** (Structured output)

---

## 📁 Repository Structure

```
project-root/
├── scrapers/
│   ├── base.py                      # BaseScraper with common scraping logic
│   ├── platform_factory.py         # Factory to initialize the correct scraper based on URL
│   └── platforms/                  # Platform-specific scraper implementations
│       ├── virgio.py
│       ├── tata_cliq.py
│       ├── nykaa_fashion.py
│       └── westside.py
├── data/                           # Output folder for scraped product URLs
│   └── <domain>.json
├── settings/
│   └── logger.py                   # Logger for info, warnings, errors
├── main.py                         # Entry point to orchestrate all scrapers
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation (problem statement, approach, usage)
```

---

## 🧐 Design & Approach

### 1. **Domain-Specific Scrapers (Strategy Pattern)**

Each domain has its own scraper class inheriting from `BaseScraper`. This allows custom handling for each site's HTML structure, lazy-loading, and anti-bot strategies.

### 2. **URL Discovery Strategy**

- **Category Links:** Start by discovering top-level category pages via sitemaps or navbar crawling.
- **Pagination & Lazy-Loading:** Scroll or click 'load more' buttons to fetch additional product items.
- **Product URL Extraction:** Product links typically follow patterns like `/p/`, `/product/`, or `/item/`.
- **De-duplication:** URLs are stored in sets to avoid duplicates.

### 3. **Performance Considerations**

- Scrapers run independently for each platform.
- Retry logic is added to ensure scraping reliability on flaky elements.
- `headless` mode is optional; non-headless mode used for JS-heavy sites like TataCliq.

### 4. **Scalability**

- Easily pluggable architecture — new scrapers can be added in `platforms/` folder.
- `platform_factory.py` dynamically instantiates the correct scraper class.
- Output for each domain is stored in a JSON file under `data/`.

---

## 📦 Output Format

Each scraper outputs product links in the following structure:

```json
{
  "domain": "https://www.example.com",
  "products": [
    "https://www.example.com/product/123",
    "https://www.example.com/product/456"
  ]
}
```

---

## 🔥 Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run all scrapers
python main.py
```

---

## ♻️ Retry Logic & Logging

Implemented a `retry` utility within `BaseScraper` to ensure flaky elements or timeouts don’t break scraping:

```python

    @staticmethod
    def retry(action, retries=3):
        for attempt in range(1, retries + 1):
            try:
                return action()
            except Exception as e:
                if attempt < retries:
                    logger(
                        f"⚠️ Attempt {attempt} failed with error: {e}. Retrying...",
                        level="warning",
                    )
                    time.sleep(1)
                else:
                    logger(
                        f"❌ All {retries} attempts failed. Last error: {e}",
                        level="error",
                    )
                    raise

```

The `logger.py` in `settings/` provides a centralized utility for logging info, warnings, and errors.

---

## ✅ Features Checklist

- [x] Handle 4 required domains
- [x] Extract only valid product URLs
- [x] Handle infinite scroll and pagination
- [x] Use retry logic for robustness
- [x] Logs with retry warnings and final errors
- [x] Modular, extensible scraper design
- [x] Output saved in structured JSON

---

## 📹 Video Demo

Loom recording explaining the approach, code structure, and results: [Insert Loom Link Here]

---

## 🚧 Limitations

- Some sites like TataCliq are resistant to headless browsers. For such sites, scraping works only in non-headless mode.
- Minor inconsistencies may arise from dynamic JS behavior, but retries handle most issues.

---

## 📌 Next Steps (Optional Enhancements)

- Convert all scrapers to run asynchronously
- Add retry limits & exponential backoff
- Save crawl stats (time taken, pages visited, failures)
- Add CLI to choose domains to run

---

## 🚀 Scaling Strategy & Product Vision

### 🌌 Technical Scaling & Deployment Strategy

#### 1. Horizontal Scaling with Microservices

- Deploy individual scrapers as microservices via Cloud Run or AWS Lambda.
- Each service handles a single platform and can scale independently.
- Use Cloud Tasks or Pub/Sub for job queuing.

#### 2. Central Controller API

- Build an orchestrator API to manage scraper jobs.
- Expose status, trigger schedules, and fetch output.

#### 3. Headless Browser Infrastructure

- Containerize Selenium + Chrome in Kubernetes pods.
- Autoscale based on job queue.
- Rotate anti-bot strategies dynamically.

#### 4. Data Storage

- Persist results in MongoDB or BigQuery.
- Add versioning, timestamps, and change detection hashes.

#### 5. Monitoring & Logging

- Use Prometheus/Grafana or Google Cloud Monitoring for metrics.
- Monitor job durations, failures, domain issues.

---

### 🔬 Product Features on Scraped Data

#### A. Market Intelligence Dashboard

- Compare prices across platforms.
- Track trending or out-of-stock items.
- Alert system for price drops.

#### B. Competitive Analysis

- Identify categories competitors push more.
- Compare frequency of specific SKUs across platforms.

#### C. Content Quality Analysis

- Use NLP to rate product titles & descriptions.
- Detect keyword stuffing or low-quality listings.

#### D. AI Catalog Tagging

- Use Vision + NLP models to auto-tag products.
- Extract missing attributes (material, color, fit).

---

### 🤖 AI Agentic Use Cases

#### 1. Autonomous Scraper Agent

- Input a domain URL.
- Agent auto-discovers category/product links.
- Generates site-specific scraping logic using LLMs.

#### 2. Chatbot for Product Discovery

- Index scraped data in a vector DB.
- User can ask: "Find red summer dresses under ₹1500 on Nykaa"

#### 3. Price Intelligence Agent

- Continuously track SKU prices across sites.
- Recommend optimal selling price.

#### 4. Listing Optimizer

- Suggest better product titles and descriptions.
- Tailor listings based on platform tone & SEO.
