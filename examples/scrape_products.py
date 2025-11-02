#!/usr/bin/env python3
"""
Example: Scraping product information from e-commerce sites
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraper import WebScraper


def main():
    print("Product Information Scraping Examples")
    print("=" * 60)
    
    scraper = WebScraper(rate_limit=1.5)
    
    # Example 1: Books to Scrape (demo site)
    print("\n1. Scraping from Books to Scrape (Demo Site):")
    print("-" * 60)
    
    book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    
    product = scraper.scrape_product_info(
        book_url,
        price_selector='p.price_color',
        title_selector='h1',
        image_selector='img'
    )
    
    if product:
        print(f"Title: {product.get('title', 'N/A')}")
        print(f"Price: £{product.get('price', 'N/A')}")
        print(f"Image: {product.get('image', 'N/A')}")
        print(f"URL: {product.get('url', 'N/A')}")
    
    # Example 2: Multiple products from category page
    print("\n2. Scraping Multiple Products from Category:")
    print("-" * 60)
    
    category_url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    html = scraper.fetch(category_url)
    
    if html:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        for article in soup.select('article.product_pod')[:5]:
            title_elem = article.select_one('h3 a')
            price_elem = article.select_one('p.price_color')
            
            if title_elem and price_elem:
                products.append({
                    'title': title_elem.get('title', ''),
                    'price': price_elem.get_text(strip=True),
                    'url': category_url.rsplit('/', 1)[0] + '/' + title_elem.get('href', '')
                })
        
        print(f"Found {len(products)} products:")
        for i, prod in enumerate(products, 1):
            print(f"\n{i}. {prod['title']}")
            print(f"   Price: {prod['price']}")
    
    # Example 3: Product comparison
    print("\n3. Generic Product Scraping Template:")
    print("-" * 60)
    print("Use this template for other e-commerce sites:")
    print("""
    # Amazon example (requires specific selectors):
    product = scraper.scrape_product_info(
        'https://www.amazon.com/dp/PRODUCT_ID',
        price_selector='#priceblock_ourprice',
        title_selector='#productTitle',
        image_selector='#landingImage'
    )
    
    # eBay example (requires specific selectors):
    product = scraper.scrape_product_info(
        'https://www.ebay.com/itm/ITEM_ID',
        price_selector='.x-price-primary',
        title_selector='.x-item-title',
        image_selector='#icImg'
    )
    
    Note: Selectors may change. Always inspect the page first!
    """)
    
    # Example 4: Export products
    print("\n4. Exporting Product Data:")
    print("-" * 60)
    
    if product:
        output_file = '/tmp/product_info.json'
        scraper.export_to_json(product, output_file)
        print(f"Product data exported to: {output_file}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("\nTips:")
    print("- Different e-commerce sites use different HTML structures")
    print("- Always check robots.txt before scraping")
    print("- Some sites require authentication or have anti-scraping measures")


if __name__ == '__main__':
    main()
