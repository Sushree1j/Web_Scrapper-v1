#!/usr/bin/env python3
"""
Advanced Web Scraper Tool
A fast, easy-to-use, and technologically advanced web scraping tool
for extracting specific information from websites.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse
from functools import lru_cache
from datetime import datetime, timedelta
import hashlib


class WebScraper:
    """
    Main web scraper class with advanced features:
    - Fast HTTP requests with session management
    - Intelligent caching
    - Rate limiting
    - Multiple scraping modes
    - Error handling and retries
    """
    
    def __init__(self, rate_limit: float = 1.0, cache_ttl: int = 300, user_agent: Optional[str] = None):
        """
        Initialize the web scraper.
        
        Args:
            rate_limit: Minimum time (seconds) between requests to same domain
            cache_ttl: Cache time-to-live in seconds
            user_agent: Custom user agent string
        """
        self.session = requests.Session()
        self.rate_limit = rate_limit
        self.cache_ttl = cache_ttl
        self.last_request_time = {}
        self.cache = {}
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key for URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key].get('timestamp')
        if not cached_time:
            return False
        
        return (datetime.now() - cached_time).total_seconds() < self.cache_ttl
    
    def _enforce_rate_limit(self, domain: str):
        """Enforce rate limiting per domain."""
        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < self.rate_limit:
                time.sleep(self.rate_limit - elapsed)
        
        self.last_request_time[domain] = time.time()
    
    def fetch(self, url: str, use_cache: bool = True, max_retries: int = 3) -> Optional[str]:
        """
        Fetch HTML content from URL with caching and retry logic.
        
        Args:
            url: URL to fetch
            use_cache: Whether to use cached content
            max_retries: Maximum number of retry attempts
            
        Returns:
            HTML content as string, or None if failed
        """
        cache_key = self._get_cache_key(url)
        
        # Check cache
        if use_cache and self._is_cache_valid(cache_key):
            return self.cache[cache_key]['content']
        
        # Enforce rate limiting
        domain = urlparse(url).netloc
        self._enforce_rate_limit(domain)
        
        # Retry logic
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                content = response.text
                
                # Cache the result
                self.cache[cache_key] = {
                    'content': content,
                    'timestamp': datetime.now()
                }
                
                return content
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"Error fetching {url}: {e}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def scrape(self, url: str, selector: str, selector_type: str = 'css',
               attr: Optional[str] = None, multiple: bool = False) -> Union[str, List[str], None]:
        """
        Generic scraping method using CSS or XPath selectors.
        
        Args:
            url: URL to scrape
            selector: CSS selector or XPath expression
            selector_type: 'css' or 'xpath'
            attr: HTML attribute to extract (None for text)
            multiple: Whether to return multiple results
            
        Returns:
            Single value, list of values, or None
        """
        html = self.fetch(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        if selector_type == 'css':
            if multiple:
                elements = soup.select(selector)
            else:
                element = soup.select_one(selector)
                elements = [element] if element else []
        else:
            # XPath not directly supported by BeautifulSoup, use CSS as fallback
            print("XPath not supported, using CSS selector instead")
            if multiple:
                elements = soup.select(selector)
            else:
                element = soup.select_one(selector)
                elements = [element] if element else []
        
        # Extract values
        results = []
        for element in elements:
            if element:
                if attr:
                    value = element.get(attr, '')
                else:
                    value = element.get_text(strip=True)
                results.append(value)
        
        if not results:
            return None
        
        return results if multiple else results[0]
    
    def scrape_news_headlines(self, url: str, headline_selector: str = 'h1, h2, h3',
                              max_headlines: int = 10) -> List[Dict[str, str]]:
        """
        Scrape news headlines from a webpage.
        
        Args:
            url: URL of news website
            headline_selector: CSS selector for headlines
            max_headlines: Maximum number of headlines to extract
            
        Returns:
            List of dictionaries with headline and link
        """
        html = self.fetch(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        headlines = []
        
        for element in soup.select(headline_selector)[:max_headlines]:
            # Try to find parent link
            link_element = element.find_parent('a') or element.find('a')
            
            headline = {
                'title': element.get_text(strip=True),
                'url': urljoin(url, link_element['href']) if link_element and link_element.get('href') else ''
            }
            
            if headline['title']:
                headlines.append(headline)
        
        return headlines
    
    def scrape_product_info(self, url: str, price_selector: str,
                           title_selector: Optional[str] = None,
                           image_selector: Optional[str] = None) -> Dict[str, str]:
        """
        Scrape product information from an e-commerce page.
        
        Args:
            url: URL of product page
            price_selector: CSS selector for price
            title_selector: CSS selector for product title
            image_selector: CSS selector for product image
            
        Returns:
            Dictionary with product information
        """
        html = self.fetch(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        product = {'url': url}
        
        # Extract price
        price_element = soup.select_one(price_selector)
        if price_element:
            price_text = price_element.get_text(strip=True)
            # Extract numeric price
            price_match = re.search(r'[\d,]+\.?\d*', price_text)
            product['price'] = price_match.group(0) if price_match else price_text
        
        # Extract title
        if title_selector:
            title_element = soup.select_one(title_selector)
            if title_element:
                product['title'] = title_element.get_text(strip=True)
        
        # Extract image
        if image_selector:
            image_element = soup.select_one(image_selector)
            if image_element:
                product['image'] = urljoin(url, image_element.get('src', ''))
        
        return product
    
    def scrape_table(self, url: str, table_selector: str = 'table',
                     has_header: bool = True) -> List[Dict[str, str]]:
        """
        Scrape data from HTML tables.
        
        Args:
            url: URL containing table
            table_selector: CSS selector for table
            has_header: Whether table has header row
            
        Returns:
            List of dictionaries representing table rows
        """
        html = self.fetch(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select_one(table_selector)
        
        if not table:
            return []
        
        data = []
        rows = table.find_all('tr')
        
        if not rows:
            return []
        
        # Extract headers
        if has_header:
            headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
            data_rows = rows[1:]
        else:
            # Generate generic headers
            first_row = rows[0].find_all(['th', 'td'])
            headers = [f'column_{i}' for i in range(len(first_row))]
            data_rows = rows
        
        # Extract data
        for row in data_rows:
            cells = row.find_all(['td', 'th'])
            if cells:
                row_data = {
                    headers[i]: cell.get_text(strip=True)
                    for i, cell in enumerate(cells) if i < len(headers)
                }
                data.append(row_data)
        
        return data
    
    def scrape_links(self, url: str, filter_pattern: Optional[str] = None,
                     internal_only: bool = False) -> List[Dict[str, str]]:
        """
        Extract all links from a webpage.
        
        Args:
            url: URL to scrape
            filter_pattern: Regex pattern to filter links
            internal_only: Only return links within same domain
            
        Returns:
            List of dictionaries with link text and URL
        """
        html = self.fetch(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        base_domain = urlparse(url).netloc
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            link_url = urljoin(url, a_tag['href'])
            link_domain = urlparse(link_url).netloc
            
            # Apply filters
            if internal_only and link_domain != base_domain:
                continue
            
            if filter_pattern and not re.search(filter_pattern, link_url):
                continue
            
            links.append({
                'text': a_tag.get_text(strip=True),
                'url': link_url
            })
        
        return links
    
    def scrape_metadata(self, url: str) -> Dict[str, str]:
        """
        Extract metadata from webpage (title, description, keywords, etc.).
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with metadata
        """
        html = self.fetch(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        metadata = {'url': url}
        
        # Extract title
        if soup.title:
            metadata['title'] = soup.title.get_text(strip=True)
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            
            if name and content:
                metadata[name] = content
        
        return metadata
    
    def export_to_json(self, data: Union[Dict, List], filename: str):
        """
        Export scraped data to JSON file.
        
        Args:
            data: Data to export
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data exported to {filename}")
    
    def export_to_csv(self, data: List[Dict], filename: str):
        """
        Export scraped data to CSV file.
        
        Args:
            data: List of dictionaries to export
            filename: Output filename
        """
        import csv
        
        if not data:
            print("No data to export")
            return
        
        keys = list(data[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Data exported to {filename}")


class QuickScrapers:
    """Pre-configured scrapers for common use cases."""
    
    @staticmethod
    def hacker_news_headlines(max_items: int = 30) -> List[Dict[str, str]]:
        """Scrape Hacker News front page headlines."""
        scraper = WebScraper()
        html = scraper.fetch('https://news.ycombinator.com/')
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        headlines = []
        
        for item in soup.select('.athing')[:max_items]:
            title_link = item.select_one('.titleline > a')
            if title_link:
                headlines.append({
                    'title': title_link.get_text(strip=True),
                    'url': title_link.get('href', ''),
                    'id': item.get('id', '')
                })
        
        return headlines
    
    @staticmethod
    def quotes_to_scrape() -> List[Dict[str, str]]:
        """Scrape quotes from quotes.toscrape.com (demo site)."""
        scraper = WebScraper()
        quotes = []
        
        for page in range(1, 3):  # First 2 pages
            html = scraper.fetch(f'http://quotes.toscrape.com/page/{page}/')
            if not html:
                break
            
            soup = BeautifulSoup(html, 'html.parser')
            
            for quote_div in soup.select('.quote'):
                quote = {
                    'text': quote_div.select_one('.text').get_text(strip=True),
                    'author': quote_div.select_one('.author').get_text(strip=True),
                    'tags': [tag.get_text(strip=True) for tag in quote_div.select('.tag')]
                }
                quotes.append(quote)
        
        return quotes
    
    @staticmethod
    def wikipedia_summary(topic: str) -> Dict[str, str]:
        """Get Wikipedia article summary for a topic."""
        scraper = WebScraper()
        url = f'https://en.wikipedia.org/wiki/{topic.replace(" ", "_")}'
        
        html = scraper.fetch(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get first paragraph
        content_div = soup.select_one('#mw-content-text')
        if not content_div:
            return {}
        
        paragraphs = content_div.find_all('p', recursive=False)
        summary = ''
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 50:
                summary = text
                break
        
        return {
            'topic': topic,
            'url': url,
            'summary': summary,
            'title': soup.title.get_text(strip=True) if soup.title else ''
        }


if __name__ == '__main__':
    # Example usage
    scraper = WebScraper()
    
    print("Web Scraper Tool - Demo")
    print("=" * 50)
    
    # Example 1: Scrape Hacker News
    print("\n1. Hacker News Headlines:")
    hn_headlines = QuickScrapers.hacker_news_headlines(max_items=5)
    for i, headline in enumerate(hn_headlines, 1):
        print(f"  {i}. {headline['title']}")
    
    # Example 2: Scrape quotes
    print("\n2. Quotes to Scrape:")
    quotes = QuickScrapers.quotes_to_scrape()
    for i, quote in enumerate(quotes[:3], 1):
        print(f"  {i}. \"{quote['text']}\" - {quote['author']}")
    
    # Example 3: Wikipedia summary
    print("\n3. Wikipedia Summary (Python):")
    wiki_info = QuickScrapers.wikipedia_summary('Python_(programming_language)')
    if wiki_info:
        print(f"  {wiki_info.get('summary', '')[:200]}...")
    
    print("\n" + "=" * 50)
    print("Demo completed!")
