# Web Scraper Tool 🚀

A fast, easy-to-use, and user-friendly web scraping tool for extracting information from websites. Perfect for scraping news headlines, product prices, table data, and much more!

## ✨ Features

- **🎯 Two Usage Modes**: Interactive auto mode OR manual command-line mode
- **⚡ Fast Performance**: Session-based requests with connection pooling
- **🧠 Intelligent Caching**: Automatic caching with configurable TTL
- **🛡️ Rate Limiting**: Built-in rate limiting to be respectful to websites
- **📊 Multiple Scraping Types**: 
  - Generic CSS selector-based scraping
  - News headline extraction
  - Product information scraping
  - Table data extraction
  - Link extraction
  - Metadata extraction
  - Full text extraction
- **🔄 Error Handling**: Automatic retry logic with exponential backoff
- **💾 Export Options**: JSON and CSV export support
- **🚀 Quick Scrapers**: Pre-configured scrapers for popular sites (Hacker News, Wikipedia, etc.)

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/Sushree1j/Web_Scrapper-v1.git
cd Web_Scrapper-v1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Option 1: Interactive Auto Mode (Easiest!)

The **auto_scraper.py** script guides you through the scraping process with simple questions:

```bash
python auto_scraper.py
```

It will ask you:
1. What type of scraping do you want to do?
2. What is the URL?
3. What elements to extract (with helpful prompts)
4. Where to save the results

**Perfect for beginners and quick tasks!**

### Option 2: Manual Command-Line Mode (Advanced)

The **manual_scraper.py** script gives you full control with command-line arguments:

```bash
# Scrape text from a CSS selector
python manual_scraper.py --url https://example.com --selector "h1"

# Scrape multiple elements and save to JSON
python manual_scraper.py --url https://example.com --selector "p" --multiple --output paragraphs.json

# Scrape news headlines
python manual_scraper.py --news --url https://news.ycombinator.com --max 10 --output news.json

# Use quick scrapers (no URL needed!)
python manual_scraper.py --quick hacker-news --max 20 --output hn.json
```

**Perfect for automation and scripting!**

### Option 3: Python Module (For Developers)

Use the web scraper in your own Python code:

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

# Example 4: Use quick scrapers
hn_news = QuickScrapers.hacker_news_headlines(max_items=20)
quotes = QuickScrapers.quotes_to_scrape()
wiki_summary = QuickScrapers.wikipedia_summary('Web_scraping')
```

## 📖 Usage Examples

### Interactive Auto Mode Examples

1. **Scrape News Headlines**:
   - Run: `python auto_scraper.py`
   - Choose option 3 (News Headlines)
   - Enter the news website URL
   - Specify how many headlines to extract
   - Save results to file

2. **Extract Product Information**:
   - Run: `python auto_scraper.py`
   - Choose option 4 (Product Information)
   - Enter the product page URL
   - Provide CSS selectors for price, title, image
   - Results are automatically saved

3. **Extract Full Text from Article**:
   - Run: `python auto_scraper.py`
   - Choose option 8 (Full Text Extraction)
   - Enter the article URL
   - Choose extraction scope (paragraphs, main content, or custom)
   - Get complete text content

### Manual Mode Examples

1. **Scrape News Headlines**:
```bash
python manual_scraper.py --news --url https://news.ycombinator.com --max 10 --output news.json
```

2. **Scrape Product Information**:
```bash
python manual_scraper.py --product --url https://example.com/product \
    --price-selector ".price" \
    --title-selector "h1" \
    --output product.json
```

3. **Scrape Table Data to CSV**:
```bash
python manual_scraper.py --table --url https://example.com/data \
    --table-selector "table.data" \
    --output data.csv
```

4. **Extract All Links**:
```bash
python manual_scraper.py --links --url https://example.com --output links.json
```

5. **Extract Only Internal Links**:
```bash
python manual_scraper.py --links --url https://example.com --internal-only
```

6. **Extract Metadata**:
```bash
python manual_scraper.py --metadata --url https://example.com
```

7. **Use Quick Scrapers**:
```bash
python manual_scraper.py --quick hacker-news --max 20 --output hn.json
python manual_scraper.py --quick quotes --output quotes.json
python manual_scraper.py --quick wikipedia --topic "Python_(programming_language)"
```

## 🎯 Scraping Types Explained

### 1. Generic Scraping
Use CSS selectors to extract any element:
```python
# Single element
title = scraper.scrape('https://example.com', 'h1')

# Multiple elements
links = scraper.scrape('https://example.com', 'a', attr='href', multiple=True)
```

### 2. News Headlines
Optimized for extracting headlines with their links:
```python
headlines = scraper.scrape_news_headlines(
    'https://news.site.com',
    headline_selector='h2.headline',
    max_headlines=20
)
```

### 3. Product Information
Extract price, title, and images from e-commerce pages:
```python
product = scraper.scrape_product_info(
    'https://shop.com/product',
    price_selector='.price',
    title_selector='h1.product-title',
    image_selector='img.main-image'
)
```

### 4. Table Data
Parse HTML tables into structured data:
```python
data = scraper.scrape_table('https://example.com/data', 'table#results')
scraper.export_to_csv(data, 'output.csv')
```

### 5. Link Extraction
Collect all links with optional filtering:
```python
# All internal links
internal_links = scraper.scrape_links('https://example.com', internal_only=True)

# Links matching a pattern (e.g., PDFs)
pdf_links = scraper.scrape_links('https://example.com', filter_pattern=r'\.pdf$')
```

### 6. Metadata Extraction
Extract page metadata (title, description, keywords):
```python
metadata = scraper.scrape_metadata('https://example.com')
```

### 7. Full Text Extraction
Extract complete text content from pages:
```python
# Extract all paragraphs
paragraphs = scraper.scrape('https://example.com', 'p', multiple=True)

# Extract main content
content = scraper.scrape('https://example.com', 'article, main, .content')
```

## ⚙️ Configuration Options

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
scraper = WebScraper(user_agent='MyBot/1.0 (contact@example.com)')
```

## 🔍 How to Find CSS Selectors

1. **Open Developer Tools**: Right-click on the element and select "Inspect"
2. **Find the element**: Look at the HTML structure
3. **Common selectors**:
   - `h1`, `h2`, `p` - Tag names
   - `.classname` - Class names
   - `#idname` - ID names
   - `div.class > p` - Nested elements
   - `[href]` - Elements with attributes

**Common CSS Selectors:**

| What to scrape | Common selectors |
|----------------|------------------|
| Headlines | `h1`, `h2`, `.headline`, `.title` |
| Prices | `.price`, `.amount`, `span.price` |
| Links | `a`, `a.link`, `.nav a` |
| Images | `img`, `.image img`, `.gallery img` |
| Paragraphs | `p`, `.content p`, `article p` |
| Tables | `table`, `.data-table`, `#results` |

## 🚀 Quick Scrapers

Pre-configured scrapers for popular sites (no configuration needed!):

```python
from web_scraper import QuickScrapers

# Hacker News headlines
news = QuickScrapers.hacker_news_headlines(max_items=30)

# Quotes from demo site
quotes = QuickScrapers.quotes_to_scrape()

# Wikipedia article summaries
wiki = QuickScrapers.wikipedia_summary('Web_scraping')
```

## 💡 Best Practices

1. ✅ **Be Respectful**: Always respect robots.txt and website terms of service
2. ✅ **Rate Limiting**: Use appropriate rate limits to avoid overloading servers
3. ✅ **Error Handling**: The scraper includes retry logic, but always handle None returns
4. ✅ **Caching**: Use caching to reduce unnecessary requests
5. ✅ **User Agent**: Consider setting a custom user agent that identifies your bot
6. ✅ **Legal Compliance**: Ensure you have permission to scrape the target website

## 🔧 Troubleshooting

### Common Issues

**Problem: Empty results**
- ❓ **Solution**: The CSS selector might be incorrect. Inspect the HTML to verify
- Use browser DevTools to test selectors: `document.querySelector('your-selector')`

**Problem: Connection errors**
- ❓ **Solution**: Check your internet connection and verify the URL is correct

**Problem: Being blocked by website**
- ❓ **Solution**: Increase the `rate_limit` parameter or use a respectful user agent

**Problem: Stale cached data**
- ❓ **Solution**: Use `use_cache=False` or reduce `cache_ttl`

**Problem: ImportError**
- ❓ **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

## 📊 API Reference

### WebScraper Class

#### Constructor
```python
WebScraper(rate_limit=1.0, cache_ttl=300, user_agent=None)
```
- `rate_limit`: Minimum time (seconds) between requests to same domain (default: 1.0)
- `cache_ttl`: Cache time-to-live in seconds (default: 300)
- `user_agent`: Custom user agent string (optional)

#### Methods

##### `scrape(url, selector, selector_type='css', attr=None, multiple=False)`
Generic scraping using CSS selectors.
- **url**: URL to scrape
- **selector**: CSS selector
- **attr**: HTML attribute to extract (None for text)
- **multiple**: Return multiple results (default: False)
- **Returns**: Single value, list of values, or None

##### `scrape_news_headlines(url, headline_selector='h1, h2, h3', max_headlines=10)`
Extract news headlines from a webpage.
- **Returns**: List of dictionaries with 'title' and 'url'

##### `scrape_product_info(url, price_selector, title_selector=None, image_selector=None)`
Scrape product information from e-commerce pages.
- **Returns**: Dictionary with product details

##### `scrape_table(url, table_selector='table', has_header=True)`
Extract data from HTML tables.
- **Returns**: List of dictionaries representing table rows

##### `scrape_links(url, filter_pattern=None, internal_only=False)`
Extract all links from a webpage.
- **Returns**: List of dictionaries with 'text' and 'url'

##### `scrape_metadata(url)`
Extract page metadata (title, description, etc.).
- **Returns**: Dictionary with metadata

##### `export_to_json(data, filename)`
Export data to JSON file.

##### `export_to_csv(data, filename)`
Export data to CSV file.

### QuickScrapers Class

Pre-configured scrapers for common use cases:

- `hacker_news_headlines(max_items=30)`: Scrape Hacker News front page
- `quotes_to_scrape()`: Scrape quotes from quotes.toscrape.com
- `wikipedia_summary(topic)`: Get Wikipedia article summary

## 📁 Project Structure

```
Web_Scrapper-v1/
├── auto_scraper.py        # Interactive auto mode (user-friendly!)
├── manual_scraper.py      # Manual command-line mode (advanced)
├── web_scraper.py         # Core scraping library
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # Apache License 2.0
└── .gitignore            # Git ignore rules
```

## 🎓 Learning Path

### For Beginners:
1. Start with **auto_scraper.py** - it guides you through everything
2. Try the quick scrapers (option 1 in auto mode)
3. Practice with simple websites like example.com
4. Learn basic CSS selectors

### For Intermediate Users:
1. Use **manual_scraper.py** for faster workflows
2. Create custom scraping scripts using the Python module
3. Learn advanced CSS selectors
4. Experiment with different scraping types

### For Advanced Users:
1. Import `WebScraper` class into your own applications
2. Customize rate limiting and caching for your needs
3. Build scheduled scrapers for monitoring
4. Combine multiple scraping techniques

## ⚡ Performance Tips

- ✅ Enable caching for repeated requests to same URLs
- ✅ Use session-based requests (already built-in)
- ✅ Adjust rate limiting based on website responsiveness
- ✅ Use specific selectors to reduce parsing time
- ✅ Export to appropriate format (JSON for nested data, CSV for tables)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational purposes. Always ensure you have permission to scrape websites and comply with their terms of service and robots.txt. The authors are not responsible for any misuse of this tool.

## 💬 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for the web scraping community**

**Happy Scraping! 🎉**