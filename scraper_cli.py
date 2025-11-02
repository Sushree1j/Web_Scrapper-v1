#!/usr/bin/env python3
"""
Command-line interface for the Web Scraper Tool
"""

import argparse
import sys
import json
from web_scraper import WebScraper, QuickScrapers


def main():
    parser = argparse.ArgumentParser(
        description='Advanced Web Scraper Tool - Fast, easy-to-use web scraping',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape text from a CSS selector
  python scraper_cli.py --url https://example.com --selector "h1" --output titles.json
  
  # Scrape multiple elements
  python scraper_cli.py --url https://example.com --selector "p" --multiple --output paragraphs.json
  
  # Scrape news headlines
  python scraper_cli.py --news --url https://news.ycombinator.com --max 10
  
  # Scrape product price
  python scraper_cli.py --product --url https://example.com/product --price-selector ".price"
  
  # Scrape table data
  python scraper_cli.py --table --url https://example.com --table-selector "table" --output data.csv
  
  # Quick scrapers
  python scraper_cli.py --quick hacker-news --max 20
  python scraper_cli.py --quick quotes
  python scraper_cli.py --quick wikipedia --topic "Web_scraping"
        """
    )
    
    # Main options
    parser.add_argument('--url', help='URL to scrape')
    parser.add_argument('--output', help='Output file (JSON or CSV)')
    parser.add_argument('--rate-limit', type=float, default=1.0,
                       help='Rate limit in seconds between requests (default: 1.0)')
    parser.add_argument('--no-cache', action='store_true',
                       help='Disable caching')
    
    # Scraping modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--news', action='store_true',
                           help='News headline scraping mode')
    mode_group.add_argument('--product', action='store_true',
                           help='Product information scraping mode')
    mode_group.add_argument('--table', action='store_true',
                           help='Table scraping mode')
    mode_group.add_argument('--links', action='store_true',
                           help='Link extraction mode')
    mode_group.add_argument('--metadata', action='store_true',
                           help='Metadata extraction mode')
    mode_group.add_argument('--quick', choices=['hacker-news', 'quotes', 'wikipedia'],
                           help='Use pre-configured quick scraper')
    
    # Generic scraping options
    parser.add_argument('--selector', help='CSS selector for element(s)')
    parser.add_argument('--attr', help='HTML attribute to extract (default: text)')
    parser.add_argument('--multiple', action='store_true',
                       help='Extract multiple elements')
    
    # News scraping options
    parser.add_argument('--headline-selector', default='h1, h2, h3',
                       help='CSS selector for headlines (default: "h1, h2, h3")')
    parser.add_argument('--max', type=int, default=10,
                       help='Maximum items to scrape (default: 10)')
    
    # Product scraping options
    parser.add_argument('--price-selector', help='CSS selector for product price')
    parser.add_argument('--title-selector', help='CSS selector for product title')
    parser.add_argument('--image-selector', help='CSS selector for product image')
    
    # Table scraping options
    parser.add_argument('--table-selector', default='table',
                       help='CSS selector for table (default: "table")')
    parser.add_argument('--no-header', action='store_true',
                       help='Table has no header row')
    
    # Link scraping options
    parser.add_argument('--filter-pattern', help='Regex pattern to filter links')
    parser.add_argument('--internal-only', action='store_true',
                       help='Only extract internal links')
    
    # Quick scraper options
    parser.add_argument('--topic', help='Wikipedia topic for quick scraper')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.quick and not args.url:
        parser.error('--url is required unless using --quick')
    
    # Initialize scraper
    scraper = WebScraper(rate_limit=args.rate_limit)
    result = None
    
    try:
        # Quick scrapers
        if args.quick:
            if args.quick == 'hacker-news':
                result = QuickScrapers.hacker_news_headlines(max_items=args.max)
                print(f"Scraped {len(result)} headlines from Hacker News")
            elif args.quick == 'quotes':
                result = QuickScrapers.quotes_to_scrape()
                print(f"Scraped {len(result)} quotes")
            elif args.quick == 'wikipedia':
                if not args.topic:
                    parser.error('--topic is required for wikipedia quick scraper')
                result = QuickScrapers.wikipedia_summary(args.topic)
                print(f"Scraped Wikipedia summary for: {args.topic}")
        
        # News scraping
        elif args.news:
            result = scraper.scrape_news_headlines(
                args.url,
                headline_selector=args.headline_selector,
                max_headlines=args.max
            )
            print(f"Scraped {len(result)} headlines from {args.url}")
        
        # Product scraping
        elif args.product:
            if not args.price_selector:
                parser.error('--price-selector is required for product scraping')
            result = scraper.scrape_product_info(
                args.url,
                price_selector=args.price_selector,
                title_selector=args.title_selector,
                image_selector=args.image_selector
            )
            print(f"Scraped product information from {args.url}")
        
        # Table scraping
        elif args.table:
            result = scraper.scrape_table(
                args.url,
                table_selector=args.table_selector,
                has_header=not args.no_header
            )
            print(f"Scraped {len(result)} rows from table")
        
        # Link extraction
        elif args.links:
            result = scraper.scrape_links(
                args.url,
                filter_pattern=args.filter_pattern,
                internal_only=args.internal_only
            )
            print(f"Extracted {len(result)} links from {args.url}")
        
        # Metadata extraction
        elif args.metadata:
            result = scraper.scrape_metadata(args.url)
            print(f"Extracted metadata from {args.url}")
        
        # Generic scraping
        elif args.selector:
            result = scraper.scrape(
                args.url,
                selector=args.selector,
                attr=args.attr,
                multiple=args.multiple
            )
            print(f"Scraped data from {args.url}")
        
        else:
            parser.error('Please specify a scraping mode or selector')
        
        # Output results
        if result is not None:
            if args.output:
                if args.output.endswith('.csv') and isinstance(result, list):
                    scraper.export_to_csv(result, args.output)
                else:
                    scraper.export_to_json(result, args.output)
            else:
                # Print to stdout
                print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("No data scraped", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
