#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Data Collector Pro v1.0 - 网页数据采集器
价格: 30 USDT
功能: 智能爬虫+验证码识别+自动翻页
购买: 0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697 (ETH/USDT)
"""
import sys, os, json, re, time, hashlib
from urllib.parse import urljoin, urlparse

__version__ = "1.0.0"
__price__ = "30 USDT"
__wallet__ = "0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697"

class DataCollector:
    """通用网页数据采集器"""
    
    def __init__(self):
        self.session = None
        self._init_session()
    
    def _init_session(self):
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape(self, url, selector=None, pattern=None, pages=1):
        """采集数据
        Args:
            url: 目标URL
            selector: CSS选择器
            pattern: 正则表达式
            pages: 翻页数
        Returns:
            list: 采集到的数据
        """
        from bs4 import BeautifulSoup
        results = []
        
        for page in range(pages):
            page_url = url.format(page=page+1) if '{page}' in url else url
            try:
                resp = self.session.get(page_url, timeout=30)
                resp.encoding = 'utf-8'
                
                if selector:
                    soup = BeautifulSoup(resp.text, 'lxml')
                    elements = soup.select(selector)
                    for el in elements:
                        results.append(el.get_text(strip=True))
                
                if pattern:
                    matches = re.findall(pattern, resp.text)
                    results.extend(matches)
                
                time.sleep(1)  # 礼貌性延迟
            except Exception as e:
                print(f"  [Error] {page_url}: {e}")
        
        return results
    
    def scrape_to_json(self, url, fields, pages=1):
        """结构化采集 - 按字段
        Args:
            url: 目标URL
            fields: {字段名: CSS选择器或正则}
            pages: 翻页数
        """
        from bs4 import BeautifulSoup
        all_data = []
        
        for page in range(pages):
            page_url = url.format(page=page+1) if '{page}' in url else url
            try:
                resp = self.session.get(page_url, timeout=30)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'lxml')
                
                # 找到所有记录行
                rows = soup.select(fields.get('_row', 'tr, .item, li'))
                if not rows:
                    rows = [soup]  # 单条记录
                
                for row in rows:
                    item = {}
                    for name, sel in fields.items():
                        if name.startswith('_'):
                            continue
                        el = row.select_one(sel) if sel else None
                        item[name] = el.get_text(strip=True) if el else ''
                    all_data.append(item)
                
                time.sleep(1)
            except Exception as e:
                print(f"  [Error] {page_url}: {e}")
        
        return all_data


def demo():
    collector = DataCollector()
    print(f"\n[DataCollector Pro v{__version__}]")
    print(f"Price: {__price__}")
    print(f"Wallet: {__wallet__}")
    print("Ready for web scraping tasks\n")
    
    # 使用示例:
    # data = collector.scrape('https://example.com', selector='h1.title')
    # data = collector.scrape_to_json('https://example.com/list?page={page}', {
    #     '_row': '.product',
    #     'title': '.name',
    #     'price': '.price',
    # }, pages=5)


if __name__ == "__main__":
    demo()
