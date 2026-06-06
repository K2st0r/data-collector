#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================
Data Collector v2.1 — Universal Web Data Extraction Toolkit
   通用网页数据采集工具
=============================================================
Category:   Python Library + CLI Tool
License:    MIT
Donate:     0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697 (ETH/USDT)
=============================================================
Features:
  - CSS selector & regex extraction
  - Structured multi-field scraping
  - Auto pagination via URL templates
  - JSON & CSV export
  - Automatic retry with exponential backoff
  - Proxy & custom User-Agent support
=============================================================
"""
import argparse
import csv
import json
import re
import sys
import time
from io import StringIO
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

sys.stdout.reconfigure(encoding="utf-8")

__version__ = "2.1.0"
__wallet__  = "0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697"

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class DataCollector:
    """
    Universal web data collector.

    Usage::

        collector = DataCollector(proxy="http://127.0.0.1:10793")
        data = collector.scrape("https://example.com", selector="h1")
        collector.to_json(data, "output.json")

    Parameters:
        proxy:      HTTP proxy URL.
        user_agent: Custom User-Agent header.
        timeout:    Request timeout in seconds (default 30).
        retries:    Number of retry attempts (default 3).
    """

    def __init__(self, proxy: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 timeout: int = 30,
                 retries: int = 3) -> None:
        self.session = requests.Session()

        # Retry strategy: 429, 5xx → exponential backoff
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update({
            "User-Agent": user_agent or (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        self.timeout = timeout

        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    # ── Core scraping ──────────────────────────────────

    def scrape(self, url: str, selector: Optional[str] = None,
               pattern: Optional[str] = None,
               pages: int = 1, delay: float = 1.0) -> List[str]:
        """
        Extract text from web pages.

        Args:
            url:      Target URL. Use ``{page}`` placeholder for pagination.
            selector: CSS selector to extract.
            pattern:  Regex pattern to match in page source.
            pages:    Number of pages to fetch.
            delay:    Seconds between page requests (polite crawling).

        Returns:
            List of extracted text strings.
        """
        results: List[str] = []
        for page_num in range(pages):
            page_url = url.format(page=page_num + 1) if "{page}" in url else url
            try:
                resp = self.session.get(page_url, timeout=self.timeout)
                resp.encoding = resp.apparent_encoding or "utf-8"

                if selector:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(resp.text, "lxml")
                    for el in soup.select(selector):
                        results.append(el.get_text(strip=True))

                if pattern:
                    results.extend(re.findall(pattern, resp.text))

                if pages > 1:
                    time.sleep(delay)
            except Exception as exc:
                print(f"  [Error] Page {page_num + 1}: {exc}", file=sys.stderr)

        return results

    def scrape_structured(self, url: str,
                          fields: Dict[str, str],
                          pages: int = 1,
                          delay: float = 1.0) -> List[Dict[str, Any]]:
        """
        Extract structured data by field definitions.

        Args:
            url:    Target URL. Use ``{page}`` for pagination.
            fields: Mapping of ``field_name -> CSS selector``.
                    Special key ``_row`` defines the container selector.
            pages:  Number of pages.
            delay:  Delay between pages.

        Returns:
            List of dicts, each representing one row/item.

        Example::

            collector.scrape_structured(
                "https://shop.example.com?page={page}",
                fields={
                    "_row":  ".product-card",
                    "name":  ".product-name",
                    "price": ".price"
                },
                pages=5
            )
        """
        from bs4 import BeautifulSoup
        all_data: List[Dict[str, Any]] = []

        for page_num in range(pages):
            page_url = url.format(page=page_num + 1) if "{page}" in url else url
            try:
                resp = self.session.get(page_url, timeout=self.timeout)
                resp.encoding = resp.apparent_encoding or "utf-8"
                soup = BeautifulSoup(resp.text, "lxml")

                rows = soup.select(fields.get("_row", "tr, .item, li, .card"))
                if not rows:
                    rows = [soup]

                for row in rows:
                    item: Dict[str, Any] = {}
                    for name, sel in fields.items():
                        if name.startswith("_"):
                            continue
                        els = row.select(sel) if sel else []
                        if len(els) == 1:
                            item[name] = els[0].get_text(strip=True)
                        elif len(els) > 1:
                            item[name] = [e.get_text(strip=True) for e in els]
                        else:
                            item[name] = ""
                    if item:
                        all_data.append(item)

                if pages > 1:
                    time.sleep(delay)
            except Exception as exc:
                print(f"  [Error] Page {page_num + 1}: {exc}", file=sys.stderr)

        return all_data

    # ── Export ─────────────────────────────────────────

    @staticmethod
    def to_json(data: List[Dict], filepath: str) -> bool:
        """Export data to JSON file. Returns ``True`` on success."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    @staticmethod
    def to_csv(data: List[Dict], filepath: str) -> bool:
        """Export data to CSV file. Returns ``True`` on success."""
        if not data:
            return False
        try:
            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception:
            return False


# ─── CLI Interface ──────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="data_collector",
        description=f"Data Collector v{__version__} — Universal web data extraction toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  data_collector.py --url https://example.com --selector h1
  data_collector.py -u "https://news.ycombinator.com" -s ".titleline > a"
  data_collector.py -u "https://example.com?page={page}" -s ".title" -p 5 -o out.json
        """
    )
    p.add_argument("-u", "--url", required=True, help="Target URL (use {page} for pagination)")
    p.add_argument("-s", "--selector", help="CSS selector")
    p.add_argument("-r", "--regex", help="Regex pattern")
    p.add_argument("-p", "--pages", type=int, default=1, help="Number of pages (default: 1)")
    p.add_argument("-d", "--delay", type=float, default=1.0, help="Delay between pages in seconds (default: 1.0)")
    p.add_argument("-o", "--output", help="Output file (.json or .csv)")
    p.add_argument("--proxy", help="HTTP proxy URL")
    p.add_argument("--user-agent", help="Custom User-Agent string")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main() -> None:
    args = build_parser().parse_args()
    collector = DataCollector(proxy=args.proxy, user_agent=args.user_agent)

    print(f"\n  Data Collector v{__version__}")
    print(f"  URL: {args.url}")

    results = collector.scrape(
        url=args.url,
        selector=args.selector,
        pattern=args.regex,
        pages=args.pages,
        delay=args.delay,
    )

    print(f"  Found: {len(results)} items")

    if args.output:
        # Transform to list-of-dicts for export if simple text results
        export_data = [{"text": r} for r in results]
        if args.output.endswith(".json"):
            collector.to_json(export_data, args.output)
        elif args.output.endswith(".csv"):
            collector.to_csv(export_data, args.output)
        print(f"  Saved to: {args.output}")
    else:
        for i, r in enumerate(results[:50]):
            print(f"  [{i + 1}] {r[:120]}")
        if len(results) > 50:
            print(f"  ... and {len(results) - 50} more")

    print(f"  Donate: {__wallet__} (USDT/ERC20)\n")


if __name__ == "__main__":
    main()
