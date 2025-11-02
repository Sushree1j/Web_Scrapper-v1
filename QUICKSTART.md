# Getting Started with Web Scraper Tool

This is a 5-minute quick start guide to get you scraping websites immediately!

## Step 1: Install (1 minute)

```bash
# Clone and install
git clone https://github.com/Sushree1j/Web_Scrapper-v1.git
cd Web_Scrapper-v1
pip install -r requirements.txt
```

## Step 2: Your First Scrape (2 minutes)

### Option A: Use the CLI

```bash
# Scrape using quick scrapers (pre-configured, no setup needed!)
python scraper_cli.py --quick hacker-news --max 5

# Scrape a custom site
python scraper_cli.py --url https://example.com --selector "h1"
```

### Option B: Use Python

Create a file `my_scraper.py`:

```python
from web_scraper import WebScraper

# Initialize
scraper = WebScraper()

# Scrape!
title = scraper.scrape('https://example.com', 'h1')
print(f"Title: {title}")
```

Run it:
```bash
python my_scraper.py
```

## Step 3: Try Common Tasks (2 minutes)

### Extract Multiple Elements

```bash
# Get all paragraph text
python scraper_cli.py --url https://example.com --selector "p" --multiple --output paragraphs.json
```

### Extract Links

```bash
# Get all links from a page
python scraper_cli.py --links --url https://example.com --output links.json
```

### Extract Table Data

```bash
# Extract table to CSV
python scraper_cli.py --table --url https://example.com --output data.csv
```

### Monitor Product Prices

```python
from web_scraper import WebScraper

scraper = WebScraper()
product = scraper.scrape_product_info(
    'https://example.com/product',
    price_selector='.price',  # Adjust selector for your site
    title_selector='h1'
)

print(f"{product['title']}: ${product['price']}")
```

## Next Steps

- 📖 Read the [Full Documentation](README.md)
- 📝 Check out [Usage Examples](USAGE_GUIDE.md)
- 🎯 Run example scripts in `examples/` folder
- 🔧 Customize for your specific needs

## Common CSS Selectors

| What to scrape | Common selectors to try |
|----------------|------------------------|
| Headlines | `h1`, `h2`, `.headline`, `.title` |
| Prices | `.price`, `.amount`, `span.price` |
| Links | `a`, `a.link`, `.nav a` |
| Images | `img`, `.image img`, `.gallery img` |
| Paragraphs | `p`, `.content p`, `article p` |
| Tables | `table`, `.data-table`, `#results` |

## Pro Tips 💡

1. **Find selectors**: Right-click element → Inspect → Copy selector
2. **Test selectors**: Use browser console: `document.querySelector('selector')`
3. **Start simple**: Get one element working, then scale up
4. **Use caching**: Reduces requests while testing
5. **Respect limits**: Set `rate_limit` appropriately

## Need Help?

- The tool prints helpful error messages
- Check if the selector is correct in browser DevTools
- Verify the URL is accessible
- Look at the [examples](examples/) folder for inspiration

## Ready for More?

See [USAGE_GUIDE.md](USAGE_GUIDE.md) for advanced features:
- Custom rate limiting
- Cache configuration  
- Multiple output formats
- Error handling
- And much more!

---

**Happy Scraping! 🚀**
