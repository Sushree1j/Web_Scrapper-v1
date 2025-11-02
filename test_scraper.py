#!/usr/bin/env python3
"""
Unit tests for the web scraper (without network dependencies)
"""

import sys
import os
import logging

# Suppress logging during tests
logging.basicConfig(level=logging.CRITICAL)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraper import WebScraper
from bs4 import BeautifulSoup


def test_basic_parsing():
    """Test basic HTML parsing without network requests"""
    print("Testing basic HTML parsing...")
    
    # Create test HTML
    test_html = """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test description">
        </head>
        <body>
            <h1>Main Title</h1>
            <h2>Subtitle 1</h2>
            <h2>Subtitle 2</h2>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <table>
                <tr><th>Header 1</th><th>Header 2</th></tr>
                <tr><td>Data 1</td><td>Data 2</td></tr>
                <tr><td>Data 3</td><td>Data 4</td></tr>
            </table>
            <div class="product">
                <h3 class="title">Product Name</h3>
                <span class="price">$19.99</span>
                <img src="/image.jpg" alt="Product">
            </div>
        </body>
    </html>
    """
    
    soup = BeautifulSoup(test_html, 'html.parser')
    
    # Test 1: Extract single element
    h1 = soup.select_one('h1')
    assert h1 and h1.get_text(strip=True) == 'Main Title', "Failed to extract h1"
    print("✓ Single element extraction works")
    
    # Test 2: Extract multiple elements
    h2_elements = soup.select('h2')
    assert len(h2_elements) == 2, "Failed to extract multiple h2 elements"
    assert h2_elements[0].get_text(strip=True) == 'Subtitle 1', "Wrong h2 content"
    print("✓ Multiple element extraction works")
    
    # Test 3: Extract with attributes
    links = soup.select('a')
    assert len(links) == 2, "Failed to extract links"
    assert links[0].get('href') == '/link1', "Failed to extract href attribute"
    print("✓ Attribute extraction works")
    
    # Test 4: Table parsing
    table = soup.select_one('table')
    rows = table.find_all('tr')
    assert len(rows) == 3, "Failed to extract table rows"
    headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
    assert headers == ['Header 1', 'Header 2'], "Failed to extract headers"
    print("✓ Table parsing works")
    
    # Test 5: Product info extraction
    title = soup.select_one('.product .title')
    price = soup.select_one('.product .price')
    assert title and title.get_text(strip=True) == 'Product Name', "Failed to extract product title"
    assert price and price.get_text(strip=True) == '$19.99', "Failed to extract product price"
    print("✓ Product info extraction works")
    
    # Test 6: Metadata extraction
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    assert meta_desc and meta_desc.get('content') == 'Test description', "Failed to extract metadata"
    print("✓ Metadata extraction works")
    
    print("\nAll basic parsing tests passed! ✓")


def test_scraper_initialization():
    """Test scraper initialization"""
    print("\nTesting scraper initialization...")
    
    scraper = WebScraper(rate_limit=2.0, cache_ttl=600)
    assert scraper.rate_limit == 2.0, "Rate limit not set correctly"
    assert scraper.cache_ttl == 600, "Cache TTL not set correctly"
    assert scraper.session is not None, "Session not initialized"
    print("✓ Scraper initialization works")


def test_cache_key_generation():
    """Test cache key generation"""
    print("\nTesting cache functionality...")
    
    scraper = WebScraper()
    key1 = scraper._get_cache_key('https://example.com')
    key2 = scraper._get_cache_key('https://example.com')
    key3 = scraper._get_cache_key('https://different.com')
    
    assert key1 == key2, "Same URLs should generate same cache keys"
    assert key1 != key3, "Different URLs should generate different cache keys"
    print("✓ Cache key generation works")


def test_data_export():
    """Test data export functionality"""
    print("\nTesting data export...")
    
    import json
    import tempfile
    
    scraper = WebScraper()
    
    # Test JSON export
    test_data = {'key1': 'value1', 'key2': 'value2'}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json_file = f.name
    
    scraper.export_to_json(test_data, json_file)
    
    with open(json_file, 'r') as f:
        loaded_data = json.load(f)
    
    assert loaded_data == test_data, "JSON export/import failed"
    print("✓ JSON export works")
    
    # Test CSV export
    test_list = [
        {'col1': 'a', 'col2': 'b'},
        {'col1': 'c', 'col2': 'd'}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_file = f.name
    
    scraper.export_to_csv(test_list, csv_file)
    
    with open(csv_file, 'r') as f:
        content = f.read()
    
    assert 'col1,col2' in content, "CSV headers not written"
    assert 'a,b' in content, "CSV data not written"
    print("✓ CSV export works")
    
    # Cleanup
    os.unlink(json_file)
    os.unlink(csv_file)


def main():
    print("=" * 60)
    print("Web Scraper Tool - Unit Tests")
    print("=" * 60)
    
    try:
        test_basic_parsing()
        test_scraper_initialization()
        test_cache_key_generation()
        test_data_export()
        
        print("\n" + "=" * 60)
        print("All tests passed successfully! ✓✓✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
