# Web Scraper Tool 🚀

A fast, easy-to-use, and technologically advanced web scraping tool for extracting specific information from websites. Perfect for scraping news headlines, product prices, weather data, and much more!

## Features ✨

- **Fast HTTP Requests**: Session-based requests with connection pooling
- **Intelligent Caching**: Automatic caching with configurable TTL to speed up repeated requests
- **Rate Limiting**: Built-in rate limiting to be respectful to websites
- **Multiple Scraping Modes**: 
  - Generic CSS selector-based scraping
  - News headline extraction
  - Product information scraping
  - Table data extraction
  - Link extraction
  - Metadata extraction
- **Error Handling**: Automatic retry logic with exponential backoff
- **Export Options**: JSON and CSV export support
- **Quick Scrapers**: Pre-configured scrapers for popular sites
- **Easy CLI**: Simple command-line interface for quick scraping tasks

## Installation 📦

1. Clone this repository:
```bash
git clone https://github.com/Sushree1j/Web_Scrapper-v1.git
cd Web_Scrapper-v1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start 🚀

### Using the Python Module

```python
from web_scraper import WebScraper, QuickScrapers

# Initialize scraper
scraper = WebScraper(rate_limit=1.0, cache_ttl=300)

# Example 1: Scrape using CSS selector
title = scraper.scrape('https://example.com', 'h1')
print(f"Title: {title}")

# Example 2: Scrape multiple elements
paragraphs = scraper.scrape('https://example.com', 'p', multiple=True)
for p in paragraphs:
    print(p)

# Example 3: Scrape news headlines
headlines = scraper.scrape_news_headlines(
    'https://news.ycombinator.com',
    max_headlines=10
)
for headline in headlines:
    print(f"{headline['title']} - {headline['url']}")

# Example 4: Scrape product information
product = scraper.scrape_product_info(
    'https://example.com/product',
    price_selector='.price',
    title_selector='h1.product-title',
    image_selector='img.product-image'
)
print(f"Product: {product['title']} - ${product['price']}")

# Example 5: Use quick scrapers
hn_news = QuickScrapers.hacker_news_headlines(max_items=20)
quotes = QuickScrapers.quotes_to_scrape()
wiki_summary = QuickScrapers.wikipedia_summary('Web_scraping')
```

### Using the CLI

```bash
# Make CLI executable
chmod +x scraper_cli.py

# Scrape text from a CSS selector
python scraper_cli.py --url https://example.com --selector "h1"

# Scrape multiple elements and save to JSON
python scraper_cli.py --url https://example.com --selector "p" --multiple --output paragraphs.json

# Scrape news headlines
python scraper_cli.py --news --url https://news.ycombinator.com --max 10 --output news.json

# Scrape product information
python scraper_cli.py --product --url https://example.com/product \
    --price-selector ".price" \
    --title-selector "h1" \
    --output product.json

# Scrape table data to CSV
python scraper_cli.py --table --url https://example.com/data \
    --table-selector "table.data" \
    --output data.csv

# Extract all links
python scraper_cli.py --links --url https://example.com --output links.json

# Extract only internal links
python scraper_cli.py --links --url https://example.com --internal-only

# Extract metadata
python scraper_cli.py --metadata --url https://example.com

# Use quick scrapers
python scraper_cli.py --quick hacker-news --max 20 --output hn.json
python scraper_cli.py --quick quotes --output quotes.json
python scraper_cli.py --quick wikipedia --topic "Python_(programming_language)"
```

## API Reference 📚

### WebScraper Class

#### Constructor
```python
WebScraper(rate_limit=1.0, cache_ttl=300, user_agent=None)
```
- `rate_limit`: Minimum time (seconds) between requests to same domain
- `cache_ttl`: Cache time-to-live in seconds
- `user_agent`: Custom user agent string

#### Methods

##### `scrape(url, selector, selector_type='css', attr=None, multiple=False)`
Generic scraping using CSS selectors.
- `url`: URL to scrape
- `selector`: CSS selector
- `attr`: HTML attribute to extract (None for text)
- `multiple`: Return multiple results

##### `scrape_news_headlines(url, headline_selector='h1, h2, h3', max_headlines=10)`
Extract news headlines from a webpage.

##### `scrape_product_info(url, price_selector, title_selector=None, image_selector=None)`
Scrape product information from e-commerce pages.

##### `scrape_table(url, table_selector='table', has_header=True)`
Extract data from HTML tables.

##### `scrape_links(url, filter_pattern=None, internal_only=False)`
Extract all links from a webpage.

##### `scrape_metadata(url)`
Extract page metadata (title, description, etc.).

##### `export_to_json(data, filename)`
Export data to JSON file.

##### `export_to_csv(data, filename)`
Export data to CSV file.

### QuickScrapers Class

Pre-configured scrapers for common use cases:

- `hacker_news_headlines(max_items=30)`: Scrape Hacker News
- `quotes_to_scrape()`: Scrape quotes from quotes.toscrape.com
- `wikipedia_summary(topic)`: Get Wikipedia article summary

## Advanced Usage 🎯

### Custom Scraping with CSS Selectors

```python
scraper = WebScraper()

# Scrape with attribute extraction
image_url = scraper.scrape('https://example.com', 'img.main', attr='src')

# Scrape multiple elements with attributes
all_links = scraper.scrape('https://example.com', 'a', attr='href', multiple=True)

# Complex CSS selectors
specific_data = scraper.scrape('https://example.com', 'div.container > p.highlight')
```

### Table Scraping

```python
# Scrape table with headers
data = scraper.scrape_table('https://example.com/data', 'table#results')

# Scrape table without headers
data = scraper.scrape_table(
    'https://example.com/data',
    'table.no-header',
    has_header=False
)

# Export to CSV
scraper.export_to_csv(data, 'output.csv')
```

### Link Extraction with Filters

```python
# Extract all internal links
internal_links = scraper.scrape_links(
    'https://example.com',
    internal_only=True
)

# Extract links matching a pattern
pdf_links = scraper.scrape_links(
    'https://example.com',
    filter_pattern=r'\.pdf$'
)
```

### Custom Rate Limiting and Caching

```python
# Aggressive scraping (use responsibly!)
fast_scraper = WebScraper(rate_limit=0.5, cache_ttl=600)

# Conservative scraping
slow_scraper = WebScraper(rate_limit=2.0, cache_ttl=1800)

# Disable cache for specific request
data = scraper.fetch('https://example.com', use_cache=False)
```

## Examples 📝

See the `examples/` directory for more detailed examples:

- `scrape_news.py`: News headline scraping examples
- `scrape_products.py`: E-commerce scraping examples
- `scrape_data.py`: Data extraction examples

## Best Practices 💡

1. **Be Respectful**: Always respect robots.txt and website terms of service
2. **Rate Limiting**: Use appropriate rate limits to avoid overloading servers
3. **Error Handling**: The scraper includes retry logic, but always handle None returns
4. **Caching**: Use caching to reduce unnecessary requests
5. **User Agent**: Consider setting a custom user agent that identifies your bot
6. **Legal Compliance**: Ensure you have permission to scrape the target website

## Troubleshooting 🔧

### Common Issues

1. **ImportError**: Make sure all dependencies are installed: `pip install -r requirements.txt`
2. **Connection Errors**: Check your internet connection and verify the URL
3. **Empty Results**: The CSS selector might be incorrect. Inspect the HTML to verify
4. **Rate Limiting**: Increase the `rate_limit` parameter if you're being blocked

## Performance Tips ⚡

- Enable caching for repeated requests
- Use session-based requests (already built-in)
- Scrape in parallel for multiple URLs (use with caution)
- Adjust rate limiting based on website responsiveness

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Disclaimer ⚠️

This tool is for educational purposes. Always ensure you have permission to scrape websites and comply with their terms of service and robots.txt. The authors are not responsible for any misuse of this tool.

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ for the web scraping community