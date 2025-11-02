#!/usr/bin/env python3
"""
Interactive demonstration of the Web Scraper Tool capabilities
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_scraper import WebScraper, QuickScrapers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text):
    """Print a formatted section"""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print("─" * 70)


def demo_basic_scraping():
    """Demonstrate basic scraping capabilities"""
    print_header("WEB SCRAPER TOOL - FEATURE DEMONSTRATION")
    
    scraper = WebScraper()
    
    print("\n✨ Welcome to the Web Scraper Tool!")
    print("This demonstration showcases the tool's capabilities.\n")
    
    # Feature 1: Intelligent Caching
    print_section("Feature 1: Intelligent Caching System")
    print("✓ Automatic caching of requests (default: 5 minutes)")
    print("✓ Reduces redundant network calls")
    print("✓ Configurable cache TTL")
    print("\nExample:")
    print("  scraper = WebScraper(cache_ttl=600)  # 10 minute cache")
    
    # Feature 2: Rate Limiting
    print_section("Feature 2: Rate Limiting")
    print("✓ Per-domain rate limiting")
    print("✓ Prevents overloading servers")
    print("✓ Configurable delays")
    print("\nExample:")
    print("  scraper = WebScraper(rate_limit=2.0)  # 2 seconds between requests")
    
    # Feature 3: Error Handling
    print_section("Feature 3: Automatic Error Handling")
    print("✓ Retry logic with exponential backoff")
    print("✓ Graceful failure handling")
    print("✓ Detailed error logging")
    print("\nExample:")
    print("  data = scraper.fetch(url, max_retries=5)")
    
    # Feature 4: Multiple Scraping Modes
    print_section("Feature 4: Multiple Scraping Modes")
    modes = [
        ("Generic", "Use CSS selectors for any element"),
        ("News", "Optimized for news headlines"),
        ("Products", "Extract price, title, images"),
        ("Tables", "Parse HTML tables to structured data"),
        ("Links", "Collect all links with filtering"),
        ("Metadata", "Extract meta tags and page info")
    ]
    
    for mode, description in modes:
        print(f"  • {mode:12s} - {description}")
    
    # Feature 5: Export Capabilities
    print_section("Feature 5: Export Capabilities")
    print("✓ JSON export for nested data")
    print("✓ CSV export for tabular data")
    print("✓ UTF-8 encoding support")
    print("\nExample:")
    print("  scraper.export_to_json(data, 'output.json')")
    print("  scraper.export_to_csv(data, 'output.csv')")
    
    # Feature 6: CLI Interface
    print_section("Feature 6: Easy-to-Use CLI")
    print("Complete command-line interface for quick tasks:")
    print("\nExamples:")
    print("  python scraper_cli.py --url https://example.com --selector 'h1'")
    print("  python scraper_cli.py --news --url https://news.site.com --max 10")
    print("  python scraper_cli.py --quick hacker-news --output news.json")
    
    # Feature 7: Pre-configured Scrapers
    print_section("Feature 7: Quick Scrapers")
    print("Pre-configured scrapers for popular sites:")
    print("  • Hacker News headlines")
    print("  • Quotes (demo site)")
    print("  • Wikipedia summaries")
    print("\nNo configuration needed - just use and go!")
    
    # Performance Features
    print_section("Feature 8: Performance Optimizations")
    print("✓ Session-based requests (connection pooling)")
    print("✓ Intelligent caching")
    print("✓ Minimal memory footprint")
    print("✓ Fast HTML parsing with BeautifulSoup")
    
    # Code Example
    print_section("Quick Code Example")
    print("""
from web_scraper import WebScraper

# Initialize
scraper = WebScraper()

# Scrape a single element
title = scraper.scrape('https://example.com', 'h1')

# Scrape multiple elements
links = scraper.scrape('https://example.com', 'a', attr='href', multiple=True)

# Scrape news headlines
headlines = scraper.scrape_news_headlines('https://news.site.com', max_headlines=10)

# Export results
scraper.export_to_json(headlines, 'headlines.json')
    """)
    
    # Summary
    print_header("KEY BENEFITS")
    benefits = [
        "🚀 Fast: Session pooling and intelligent caching",
        "🎯 Easy: Simple API and comprehensive CLI",
        "🛡️ Safe: Rate limiting and retry logic built-in",
        "📦 Flexible: Multiple modes for different use cases",
        "📝 Well-documented: Examples and guides included",
        "🔧 Customizable: Configure every aspect of scraping",
        "✅ Tested: Unit tests included",
        "🔒 Secure: No vulnerabilities in dependencies"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    # Next Steps
    print_section("Next Steps")
    print("1. Try the examples:")
    print("   python examples/scrape_news.py")
    print("   python examples/scrape_products.py")
    print("   python examples/scrape_data.py")
    print("\n2. Read the documentation:")
    print("   - QUICKSTART.md  (5-minute guide)")
    print("   - USAGE_GUIDE.md (detailed examples)")
    print("   - README.md      (complete reference)")
    print("\n3. Run your first scrape:")
    print("   python scraper_cli.py --quick hacker-news --max 5")
    
    print("\n" + "=" * 70)
    print("  Ready to scrape the web! 🌐")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    demo_basic_scraping()
