# Web Scraper Tool - Usage Guide

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Sushree1j/Web_Scrapper-v1.git
cd Web_Scrapper-v1

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

#### As a Python Module

```python
from web_scraper import WebScraper

# Create scraper instance
scraper = WebScraper()

# Scrape a single element
title = scraper.scrape('https://example.com', 'h1')
print(f"Title: {title}")

# Scrape multiple elements
links = scraper.scrape('https://example.com', 'a', attr='href', multiple=True)
print(f"Found {len(links)} links")
```

#### Using the CLI

```bash
# Simple text extraction
python scraper_cli.py --url https://example.com --selector "h1"

# Save to file
python scraper_cli.py --url https://example.com --selector "p" --multiple --output data.json
```

## Feature Highlights

### 🚀 Fast Performance
- Session-based HTTP requests with connection pooling
- Intelligent caching system (default: 5 minutes TTL)
- Configurable rate limiting to respect servers

### 🎯 Multiple Scraping Modes

1. **Generic Scraping** - Use CSS selectors for any element
2. **News Headlines** - Optimized for news websites
3. **Product Information** - Extract price, title, images from e-commerce
4. **Table Data** - Parse HTML tables into structured data
5. **Link Extraction** - Collect all links with filtering options
6. **Metadata Extraction** - Get meta tags, title, descriptions

### 🛠️ Advanced Features

- **Automatic Retry Logic** - Exponential backoff on failures
- **Cache Management** - Reduce redundant requests
- **Rate Limiting** - Per-domain request throttling
- **Export Options** - JSON and CSV output formats
- **Custom User Agents** - Configurable browser identification

## Use Cases

### News Scraping

```python
from web_scraper import WebScraper

scraper = WebScraper()
headlines = scraper.scrape_news_headlines(
    'https://news.ycombinator.com',
    max_headlines=20
)

for h in headlines:
    print(f"{h['title']}\n  {h['url']}\n")
```

**CLI:**
```bash
python scraper_cli.py --news --url https://news.ycombinator.com --max 20 --output news.json
```

### Product Price Monitoring

```python
product = scraper.scrape_product_info(
    'https://example.com/product/12345',
    price_selector='.price',
    title_selector='h1.product-name',
    image_selector='img.main-image'
)

print(f"{product['title']}: ${product['price']}")
```

**CLI:**
```bash
python scraper_cli.py --product \
    --url https://example.com/product/12345 \
    --price-selector ".price" \
    --title-selector "h1.product-name" \
    --output product.json
```

### Data Extraction from Tables

```python
table_data = scraper.scrape_table(
    'https://example.com/data-page',
    table_selector='table.data-table',
    has_header=True
)

# Export to CSV
scraper.export_to_csv(table_data, 'output.csv')
```

**CLI:**
```bash
python scraper_cli.py --table \
    --url https://example.com/data-page \
    --table-selector "table.data-table" \
    --output data.csv
```

### Link Collection

```python
# Get all internal links
links = scraper.scrape_links(
    'https://example.com',
    internal_only=True
)

# Get links matching a pattern (e.g., PDFs)
pdf_links = scraper.scrape_links(
    'https://example.com',
    filter_pattern=r'\.pdf$'
)
```

**CLI:**
```bash
# Internal links only
python scraper_cli.py --links --url https://example.com --internal-only

# Filter by pattern
python scraper_cli.py --links --url https://example.com --filter-pattern "\.pdf$"
```

## Configuration Options

### Rate Limiting

```python
# Conservative (2 seconds between requests)
scraper = WebScraper(rate_limit=2.0)

# Aggressive (0.5 seconds - use responsibly!)
scraper = WebScraper(rate_limit=0.5)
```

### Cache Configuration

```python
# 10 minute cache
scraper = WebScraper(cache_ttl=600)

# Disable cache for specific request
html = scraper.fetch('https://example.com', use_cache=False)
```

### Custom User Agent

```python
scraper = WebScraper(
    user_agent='MyBot/1.0 (contact@example.com)'
)
```

## Quick Scrapers

Pre-configured scrapers for popular sites:

```python
from web_scraper import QuickScrapers

# Hacker News
news = QuickScrapers.hacker_news_headlines(max_items=30)

# Quotes (demo site)
quotes = QuickScrapers.quotes_to_scrape()

# Wikipedia summaries
wiki = QuickScrapers.wikipedia_summary('Web_scraping')
```

**CLI:**
```bash
python scraper_cli.py --quick hacker-news --max 30
python scraper_cli.py --quick quotes
python scraper_cli.py --quick wikipedia --topic "Web_scraping"
```

## Best Practices

1. ✅ **Check robots.txt** - Respect website policies
2. ✅ **Use rate limiting** - Don't overload servers
3. ✅ **Handle errors** - Always check for None returns
4. ✅ **Cache wisely** - Reduce unnecessary requests
5. ✅ **Identify yourself** - Use descriptive user agents
6. ✅ **Legal compliance** - Ensure you have permission to scrape

## Examples

Run the included examples:

```bash
# News scraping examples
python examples/scrape_news.py

# Product scraping examples
python examples/scrape_products.py

# Data extraction examples
python examples/scrape_data.py
```

## Troubleshooting

**Problem: Empty results**
- Solution: Verify CSS selectors using browser DevTools

**Problem: Connection errors**
- Solution: Check URL and internet connection

**Problem: Being blocked**
- Solution: Increase rate_limit, use respectful user agent

**Problem: Stale cached data**
- Solution: Use `use_cache=False` or reduce `cache_ttl`

## Performance Tips

1. **Enable caching** for repeated requests to same URLs
2. **Batch requests** with appropriate delays
3. **Use specific selectors** to reduce parsing time
4. **Export to appropriate format** (JSON for nested, CSV for tabular)

## API Reference

See README.md for complete API documentation.

## Contributing

Contributions welcome! Please:
- Follow existing code style
- Add tests for new features
- Update documentation
- Respect web scraping ethics

## Support

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/Sushree1j/Web_Scrapper-v1/issues)
- 💬 [Discussions](https://github.com/Sushree1j/Web_Scrapper-v1/discussions)

---

**Remember**: Always scrape responsibly and ethically!
