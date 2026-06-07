<div align="center">

# Data Collector

**Universal Web Scraping Toolkit — CSS Selectors + Regex + Auto-Pagination**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.1.0-purple.svg)](https://github.com/K2st0r/data-collector/releases)
[![Donate](https://img.shields.io/badge/Donate-USDT-red.svg)](#donate)

</div>

### 🎯 What It Does

Extract structured data from any website with zero config. Just specify what you want.

```python
from data_collector import DataCollector

dc = DataCollector(proxy="http://127.0.0.1:10793")

# Scrape headlines
titles = dc.scrape("https://news.ycombinator.com", selector=".titleline a")
```

### ✨ Features

| Feature | Description |
|---------|-------------|
| **CSS Selectors** | Target any element with familiar CSS syntax |
| **Regex Matching** | Extract patterns like emails, prices, phone numbers |
| **Auto-Pagination** | Use `{page}` in URL template — auto-fetches all pages |
| **Structured Mode** | Define field → selector mapping for table-like data |
| **Retry + Backoff** | Auto-retry on 429/5xx with exponential backoff |
| **Proxy Support** | HTTP/SOCKS proxy for geo-restricted sites |
| **JSON/CSV Export** | One-liner to save results |
| **Polite Crawling** | Configurable delay between pages |

### 🚀 Install

```bash
pip install requests beautifulsoup4 lxml
```

### 📖 Real Examples

**1. Quick scrape — headlines from Hacker News:**

```python
dc = DataCollector()
titles = dc.scrape("https://news.ycombinator.com", selector=".titleline a")
# ['Show HN: My New App', 'Why Rust is the Future', ...]
```

**2. Structured data — product listings:**

```python
products = dc.scrape_structured(
    "https://books.toscrape.com/catalogue/page-{page}.html",
    fields={
        "_row":  "article.product_pod",
        "title": "h3 a",
        "price": ".price_color"
    },
    pages=5
)
# [{"title": "A Light in the Attic", "price": "£51.77"}, ...]
```

**3. Regex — find all emails on a page:**

```python
emails = dc.scrape("https://example.com/team", pattern=r'[\w.+-]+@[\w-]+\.[\w.-]+')
# ['contact@example.com', 'jobs@example.com', ...]
```

**4. Export to CSV:**

```python
data = dc.scrape_structured("https://quotes.toscrape.com", fields={"_row": ".quote", "text": ".text", "author": ".author"})
dc.to_csv(data, "quotes.csv")
```

### 🆚 vs Scrapling / Scrapy / Alternatives

| | **Data Collector** | Scrapling | Scrapy | BeautifulSoup |
|---|---|---|---|---|
| Setup time | **1 line** | 5 min config | 30 min project | 5-10 lines |
| Pagination | ✅ Built-in | ✅ | ✅ Plugin | ❌ Manual |
| Structured | ✅ Field-selector | ✅ | ✅ ItemLoader | ❌ Manual |
| Retry | ✅ Auto | ✅ | ✅ Middleware | ❌ Manual |
| Export | ✅ JSON/CSV | ✅ | ✅ Feed export | ❌ Manual |
| Learning curve | **Minimal** | Medium | Steep | Medium |
| Best for | Quick jobs | Smart scraping | Large projects | Simple parsing |

### 🎯 Use Cases

- Monitoring competitor prices
- Building datasets for ML training
- Extracting job listings / real estate data
- SEO audit data collection
- Academic research data gathering

## 💎 Donate

**USDT (ERC20):** `0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697`

---

*MIT License · Made with ❤️ by [K2st0r](https://github.com/K2st0r)*
