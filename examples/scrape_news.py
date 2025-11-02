#!/usr/bin/env python3
"""
Example: Scraping news headlines from various sources
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraper import WebScraper, QuickScrapers


def main():
    print("News Headline Scraping Examples")
    print("=" * 60)
    
    scraper = WebScraper(rate_limit=1.5)
    
    # Example 1: Hacker News (using QuickScraper)
    print("\n1. Hacker News Headlines (Top 10):")
    print("-" * 60)
    hn_headlines = QuickScrapers.hacker_news_headlines(max_items=10)
    for i, headline in enumerate(hn_headlines, 1):
        print(f"{i:2d}. {headline['title']}")
        print(f"    URL: {headline['url']}")
    
    # Example 2: Generic news site scraping
    print("\n2. Generic News Scraping:")
    print("-" * 60)
    print("This example shows how to scrape any news site by")
    print("specifying the appropriate CSS selectors.")
    print("\nExample code:")
    print("""
    # For BBC News:
    headlines = scraper.scrape_news_headlines(
        'https://www.bbc.com/news',
        headline_selector='h3',
        max_headlines=15
    )
    
    # For CNN:
    headlines = scraper.scrape_news_headlines(
        'https://www.cnn.com',
        headline_selector='span.cd__headline-text',
        max_headlines=15
    )
    
    # For The Guardian:
    headlines = scraper.scrape_news_headlines(
        'https://www.theguardian.com',
        headline_selector='a.dcr-lv2v9o',
        max_headlines=15
    )
    """)
    
    # Example 3: Export to file
    print("\n3. Exporting Headlines to JSON:")
    print("-" * 60)
    output_file = '/tmp/hacker_news_headlines.json'
    scraper.export_to_json(hn_headlines, output_file)
    print(f"Headlines exported to: {output_file}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("\nTips:")
    print("- Use browser DevTools to inspect elements and find selectors")
    print("- Different news sites require different selectors")
    print("- Respect rate limits to avoid being blocked")


if __name__ == '__main__':
    main()
