# Data Collector 网页数据采集器

> Universal web data collector with CSS selectors, regex, auto-pagination & export

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0.0-purple)

[English](#english) | [中文](#chinese)

---

## <a name="chinese">🇨🇳 中文说明</a>

### 概述

Data Collector 是一个通用的网页数据采集器，支持 CSS 选择器和正则表达式提取、自动翻页、JSON/CSV 导出，内置重试策略和反反爬机制。

### 功能特性

- **CSS 选择器采集**：精确提取指定网页元素
- **正则表达式匹配**：从页面源代码中提取结构化数据
- **结构化采集**：按字段定义采集，支持一行多字段
- **自动翻页**：通过 URL 模板 `{page}` 自动翻页
- **JSON/CSV 导出**：直接输出为可分析的数据文件
- **重试策略**：自动重试 429/5xx 错误，指数退避
- **反爬处理**：真实浏览器 User-Agent 和请求头
- **代理支持**：通过 HTTP/SOCKS5 代理访问
- **编码自动识别**：自动检测网页编码

### 快速开始

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml

# 使用
python data_collector.py
```

### 使用示例

```python
from data_collector import DataCollector

# 创建采集器
collector = DataCollector()

# 方式1：CSS选择器采集
titles = collector.scrape(
    "https://example.com/articles",
    selector="h2.title"
)
print(f"采集到 {len(titles)} 条标题")

# 方式2：正则采集
emails = collector.scrape(
    "https://example.com/contact",
    pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

# 方式3：结构化采集（最常用）
products = collector.scrape_structured(
    "https://shop.example.com/products?page={page}",
    fields={
        "_row": ".product-card",      # 每条数据的容器选择器
        "name": ".product-name",       # 商品名
        "price": ".price",             # 价格
        "rating": ".rating .score",    # 评分
        "description": ".desc"         # 描述
    },
    pages=5,    # 采集5页
    delay=1.5   # 每页间隔1.5秒
)

print(f"采集到 {len(products)} 件商品")
# 第1件商品：{"name": "...", "price": "...", "rating": "...", "description": "..."}

# 导出数据
collector.to_json(products, "products.json")
collector.to_csv(products, "products.csv")
```

### 代理设置

```python
# 国内用户通过代理访问外网
collector = DataCollector(proxy="http://127.0.0.1:10793")

# 自定义 User-Agent
collector = DataCollector(
    user_agent="Googlebot/2.1 (+http://www.google.com/bot.html)"
)
```

### 完整字段说明

`scrape_structured` 的 `fields` 参数：

| 字段 | 说明 | 示例 |
|------|------|------|
| `_row` | 每条数据行的CSS选择器 | `".product-card"`, `"tr"`, `"li.item"` |
| `字段名` | 自定义字段的CSS选择器 | `".title"`, `".price"`, `"span.author"` |

如果 `_row` 为空或未匹配到任何元素，则整页作为一条记录。

---

## <a name="english">🇬🇧 English</a>

### Overview

Data Collector is a universal web data extraction tool with CSS selector and regex support, automatic pagination, JSON/CSV export, built-in retry strategy, and anti-scraping countermeasures.

### Features

- **CSS selector extraction**: Precisely extract specific page elements
- **Regex pattern matching**: Extract structured data from page source
- **Structured scraping**: Multi-field extraction per row
- **Auto pagination**: URL template `{page}` for automatic page iteration
- **JSON/CSV export**: Output as analyzable data files
- **Retry strategy**: Automatic retry for 429/5xx with exponential backoff
- **Anti-scraping**: Real browser User-Agent and request headers
- **Proxy support**: HTTP/SOCKS5 proxy access
- **Auto encoding detection**: Automatic charset detection

### Quick Start

```bash
pip install requests beautifulsoup4 lxml
python data_collector.py
```

### Usage

```python
from data_collector import DataCollector

collector = DataCollector()

# CSS selector
results = collector.scrape("https://example.com", selector="h1")

# Regex
emails = collector.scrape("https://example.com", pattern=r"[\w.+-]+@[\w-]+\.[\w.]+")

# Structured (most useful)
data = collector.scrape_structured(
    "https://example.com/list?page={page}",
    fields={
        "_row": ".item",
        "title": ".title",
        "price": ".price",
        "date": ".date"
    },
    pages=3
)

# Export
collector.to_json(data, "output.json")
collector.to_csv(data, "output.csv")
```

### API Reference

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `scrape(url, selector, pattern, pages, delay)` | url, css selector, regex, page count, delay | list | Text extraction |
| `scrape_structured(url, fields, pages, delay)` | url, field definitions, page count, delay | list of dicts | Structured extraction |
| `to_csv(data, filepath)` | data list, output path | bool | Export to CSV |
| `to_json(data, filepath)` | data list, output path | bool | Export to JSON |

---

## 打赏 / Donate

如果这个项目帮到了您，欢迎打赏支持持续开发！

If this project helps you, consider supporting continued development!

![WeChat Pay](https://raw.githubusercontent.com/K2st0r/data-collector/main/static/zan.png)

📱 微信扫码赞赏 / WeChat Pay QR Code

**USDT (ERC20):** `0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697`

---

Open Source · MIT License · Made with ❤️
