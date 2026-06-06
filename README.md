<div align="center">

# Data Collector

**Universal Web Data Extraction Toolkit**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.1.0-purple.svg)](https://github.com/K2st0r/data-collector/releases)
[![Donate](https://img.shields.io/badge/Donate-USDT-red.svg)](#donate)

</div>

---

## Table of Contents

- [English](#english)
- [中文](#chinese)
- [Donate / 打赏](#donate--打赏)

---

## English

### What is Data Collector?

Data Collector is a **Python library and CLI tool** for extracting structured data from web pages. It supports CSS selectors, regex patterns, automatic pagination, and JSON/CSV export — like a lightweight, no-config alternative to Scrapy for common scraping tasks.

### Features

| Category | Description |
|----------|-------------|
| **CSS Selectors** | Extract elements using CSS syntax (h1, .class, #id) |
| **Regex Extraction** | Pattern-matching on raw page source |
| **Structured Scraping** | Multi-field extraction with row/container selectors |
| **Auto Pagination** | `{page}` placeholder in URL for automatic page iteration |
| **JSON/CSV Export** | Save results directly to file |
| **Retry Strategy** | Auto-retry on 429/5xx with exponential backoff |
| **Proxy Support** | Route requests through HTTP/SOCKS proxy |
| **Custom Headers** | Full User-Agent and header customization |
| **Politeness** | Configurable inter-request delay |

### Installation

```bash
git clone https://github.com/K2st0r/data-collector.git
cd data-collector
pip install requests beautifulsoup4 lxml
```

### CLI Usage

```bash
# Extract all H1 texts
python data_collector.py --url https://example.com --selector h1

# Extract titles from Hacker News
python data_collector.py -u "https://news.ycombinator.com" -s ".titleline > a"

# Multi-page scraping
python data_collector.py -u "https://example.com?page={page}" -s ".title" -p 5

# Save results
python data_collector.py -u https://example.com -s "h2.title" -o results.json
python data_collector.py -u https://example.com -s "h2.title" -o results.csv

# Via proxy
python data_collector.py --url https://github.com --selector ".repo" --proxy http://127.0.0.1:10793
```

### Python API

```python
from data_collector import DataCollector

# Initialize
collector = DataCollector(proxy="http://127.0.0.1:10793")

# Simple text extraction
titles = collector.scrape("https://example.com/articles", selector="h2.title")

# Regex extraction
emails = collector.scrape("https://example.com/contact",
                          pattern=r"[\w.+-]+@[\w-]+\.[\w.]+")

# Structured extraction (most powerful)
products = collector.scrape_structured(
    "https://shop.example.com/products?page={page}",
    fields={
        "_row":  ".product-card",   # container for each item
        "name":  ".product-name",
        "price": ".price",
        "rating": ".stars",
    },
    pages=5,  delay=1.5
)
# -> [{"name": "...", "price": "...", "rating": "..."}, ...]

# Export
collector.to_json(products, "products.json")
collector.to_csv(products, "products.csv")
```

---

## 中文

### 概述

Data Collector 是一个 **Python 库 + CLI 工具**，用于网页结构化数据采集。支持 CSS 选择器、正则匹配、自动翻页、JSON/CSV 导出。

### 安装

```bash
git clone https://github.com/K2st0r/data-collector.git
cd data-collector
pip install requests beautifulsoup4 lxml
```

### CLI 命令

```bash
python data_collector.py --url https://example.com --selector h1
python data_collector.py -u "https://example.com?page={page}" -s ".title" -p 5
python data_collector.py -u https://example.com -s ".title" -o results.json
python data_collector.py --url https://github.com --selector ".repo" --proxy http://127.0.0.1:10793
```

### Python API

```python
from data_collector import DataCollector

collector = DataCollector()

# CSS选择器提取
titles = collector.scrape("https://example.com", selector="h1")

# 结构化采集
data = collector.scrape_structured(
    "https://shop.com/list?page={page}",
    fields={"_row": ".card", "title": ".name", "price": ".price"},
    pages=5
)

# 导出
collector.to_json(data, "output.json")
collector.to_csv(data, "output.csv")
```

---

## Donate / 打赏

<div align="center">
<img src="https://raw.githubusercontent.com/K2st0r/data-collector/main/static/zan.png" width="200" alt="WeChat Pay">

📱 微信扫码赞赏

**USDT (ERC20):** `0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697`

</div>

---

MIT License · Made with ❤️ by [K2st0r](https://github.com/K2st0r)
