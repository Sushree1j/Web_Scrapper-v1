#!/usr/bin/env python3
"""
Example: Scraping structured data from websites
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraper import WebScraper, QuickScrapers


def main():
    print("Data Extraction Examples")
    print("=" * 60)
    
    scraper = WebScraper(rate_limit=1.0)
    
    # Example 1: Scraping quotes
    print("\n1. Scraping Quotes (using QuickScraper):")
    print("-" * 60)
    quotes = QuickScrapers.quotes_to_scrape()
    
    print(f"Scraped {len(quotes)} quotes. Here are the first 5:")
    for i, quote in enumerate(quotes[:5], 1):
        print(f"\n{i}. \"{quote['text']}\"")
        print(f"   - {quote['author']}")
        print(f"   Tags: {', '.join(quote['tags'])}")
    
    # Example 2: Wikipedia summary
    print("\n2. Wikipedia Article Summary:")
    print("-" * 60)
    wiki_info = QuickScrapers.wikipedia_summary('Web_scraping')
    
    if wiki_info:
        print(f"Topic: {wiki_info.get('topic', 'N/A')}")
        print(f"URL: {wiki_info.get('url', 'N/A')}")
        print(f"\nSummary:")
        summary = wiki_info.get('summary', '')
        print(f"{summary[:300]}..." if len(summary) > 300 else summary)
    
    # Example 3: Scraping metadata
    print("\n3. Website Metadata Extraction:")
    print("-" * 60)
    metadata = scraper.scrape_metadata('https://quotes.toscrape.com')
    
    if metadata:
        print("Extracted metadata:")
        for key, value in list(metadata.items())[:10]:
            print(f"  {key}: {value}")
    
    # Example 4: Link extraction
    print("\n4. Link Extraction:")
    print("-" * 60)
    links = scraper.scrape_links(
        'https://quotes.toscrape.com',
        internal_only=True
    )
    
    print(f"Found {len(links)} internal links. First 5:")
    for i, link in enumerate(links[:5], 1):
        print(f"{i}. {link['text']} -> {link['url']}")
    
    # Example 5: Table scraping (example with Wikipedia)
    print("\n5. Table Data Scraping:")
    print("-" * 60)
    print("Example: Scraping a table from Wikipedia")
    print("""
    # Scrape a table with headers
    table_data = scraper.scrape_table(
        'https://en.wikipedia.org/wiki/List_of_countries_by_population',
        table_selector='table.wikitable',
        has_header=True
    )
    
    # Export to CSV
    scraper.export_to_csv(table_data, 'countries.csv')
    """)
    
    # Example 6: Custom scraping
    print("\n6. Custom CSS Selector Scraping:")
    print("-" * 60)
    
    # Get all author names from quotes site
    authors = scraper.scrape(
        'https://quotes.toscrape.com',
        selector='.author',
        multiple=True
    )
    
    if authors:
        unique_authors = list(set(authors))
        print(f"Found {len(unique_authors)} unique authors:")
        print(", ".join(sorted(unique_authors)[:10]))
    
    # Example 7: Export data
    print("\n7. Exporting Scraped Data:")
    print("-" * 60)
    
    # Export quotes to JSON
    json_file = '/tmp/quotes.json'
    scraper.export_to_json(quotes, json_file)
    print(f"Quotes exported to JSON: {json_file}")
    
    # Export links to CSV
    csv_file = '/tmp/links.csv'
    scraper.export_to_csv(links, csv_file)
    print(f"Links exported to CSV: {csv_file}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("\nTips:")
    print("- Use CSS selectors to target specific elements")
    print("- Combine multiple scraping methods for complex tasks")
    print("- Always validate scraped data before using it")
    print("- Export to JSON for nested data, CSV for tabular data")


if __name__ == '__main__':
    main()
