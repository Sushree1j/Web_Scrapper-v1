#!/usr/bin/env python3
"""
Interactive Auto Web Scraper
A user-friendly, interactive script that guides you through web scraping tasks.
"""

import sys
import os
from web_scraper import WebScraper, QuickScrapers
import json

# Default selectors
DEFAULT_HEADLINE_SELECTOR = 'h1, h2, h3'
DEFAULT_CONTENT_SELECTOR = 'article, main, .content'
DEFAULT_TABLE_SELECTOR = 'table'

def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("  🚀 INTERACTIVE WEB SCRAPER - AUTO MODE")
    print("=" * 70)
    print("  This tool will guide you through scraping a website.")
    print("  Just answer a few simple questions!\n")

def get_input(prompt, default=None, options=None):
    """Get user input with optional default and validation"""
    if default:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "
    
    while True:
        user_input = input(prompt).strip()
        
        if not user_input and default:
            return default
        
        if options and user_input and user_input not in options:
            print(f"  ⚠️  Please choose from: {', '.join(options)}")
            continue
        
        if user_input or default:
            return user_input if user_input else default
        
        print("  ⚠️  This field is required. Please enter a value.")

def get_yes_no(prompt, default='n'):
    """Get yes/no input from user"""
    response = get_input(f"{prompt} (y/n)", default=default, options=['y', 'n', 'yes', 'no'])
    return response.lower() in ['y', 'yes']

def main():
    """Main interactive function"""
    print_banner()
    
    # Step 1: Choose scraping mode
    print("\n📋 STEP 1: Choose Scraping Type")
    print("-" * 70)
    print("  1. Quick Scraper (pre-configured for popular sites)")
    print("  2. Generic Scraping (CSS selector)")
    print("  3. News Headlines")
    print("  4. Product Information")
    print("  5. Table Data")
    print("  6. Extract Links")
    print("  7. Extract Metadata")
    print("  8. Full Text Extraction")
    
    scrape_type = get_input("\nEnter your choice (1-8)", default="1", 
                            options=['1', '2', '3', '4', '5', '6', '7', '8'])
    
    scraper = WebScraper()
    result = None
    output_file = None
    
    try:
        # Quick Scraper Mode
        if scrape_type == '1':
            print("\n📋 STEP 2: Choose Quick Scraper")
            print("-" * 70)
            print("  1. Hacker News Headlines")
            print("  2. Quotes (demo site)")
            print("  3. Wikipedia Summary")
            
            quick_choice = get_input("\nEnter your choice (1-3)", default="1", 
                                    options=['1', '2', '3'])
            
            if quick_choice == '1':
                max_items = int(get_input("\nHow many headlines to scrape?", default="10"))
                print("\n⏳ Scraping Hacker News headlines...")
                result = QuickScrapers.hacker_news_headlines(max_items=max_items)
                print(f"✅ Scraped {len(result)} headlines!")
                
            elif quick_choice == '2':
                print("\n⏳ Scraping quotes...")
                result = QuickScrapers.quotes_to_scrape()
                print(f"✅ Scraped {len(result)} quotes!")
                
            elif quick_choice == '3':
                topic = get_input("\nEnter Wikipedia topic (e.g., 'Python_(programming_language)')")
                print(f"\n⏳ Scraping Wikipedia summary for '{topic}'...")
                result = QuickScrapers.wikipedia_summary(topic)
                print("✅ Summary extracted!")
        
        # Generic Scraping
        elif scrape_type == '2':
            print("\n📋 STEP 2: Enter Scraping Details")
            print("-" * 70)
            url = get_input("Enter the URL to scrape")
            selector = get_input("Enter CSS selector (e.g., 'h1', '.title', '#content')")
            
            extract_attr = get_yes_no("Do you want to extract an HTML attribute (like 'href' or 'src')?")
            attr = None
            if extract_attr:
                attr = get_input("Enter attribute name (e.g., 'href', 'src', 'alt')")
            
            multiple = get_yes_no("Extract multiple elements?", default='n')
            
            print(f"\n⏳ Scraping {url}...")
            result = scraper.scrape(url, selector, attr=attr, multiple=multiple)
            
            if result:
                if isinstance(result, list):
                    print(f"✅ Extracted {len(result)} elements!")
                else:
                    print(f"✅ Extracted: {result[:100]}..." if len(str(result)) > 100 else f"✅ Extracted: {result}")
            else:
                print("⚠️  No data found. Check your selector.")
        
        # News Headlines
        elif scrape_type == '3':
            print("\n📋 STEP 2: Enter News Site Details")
            print("-" * 70)
            url = get_input("Enter the news website URL")
            max_headlines = int(get_input("How many headlines to extract?", default="10"))
            custom_selector = get_yes_no("Use custom headline selector?", default='n')
            
            headline_selector = DEFAULT_HEADLINE_SELECTOR
            if custom_selector:
                headline_selector = get_input("Enter CSS selector for headlines", default=DEFAULT_HEADLINE_SELECTOR)
            
            print(f"\n⏳ Scraping news headlines from {url}...")
            result = scraper.scrape_news_headlines(url, headline_selector=headline_selector, 
                                                   max_headlines=max_headlines)
            print(f"✅ Extracted {len(result)} headlines!")
        
        # Product Information
        elif scrape_type == '4':
            print("\n📋 STEP 2: Enter Product Page Details")
            print("-" * 70)
            url = get_input("Enter the product page URL")
            price_selector = get_input("Enter CSS selector for price (e.g., '.price', '#price')")
            
            extract_title = get_yes_no("Extract product title?", default='y')
            title_selector = None
            if extract_title:
                title_selector = get_input("Enter CSS selector for title", default="h1")
            
            extract_image = get_yes_no("Extract product image?", default='n')
            image_selector = None
            if extract_image:
                image_selector = get_input("Enter CSS selector for image")
            
            print(f"\n⏳ Scraping product information from {url}...")
            result = scraper.scrape_product_info(url, price_selector=price_selector,
                                                title_selector=title_selector,
                                                image_selector=image_selector)
            print("✅ Product information extracted!")
        
        # Table Data
        elif scrape_type == '5':
            print("\n📋 STEP 2: Enter Table Details")
            print("-" * 70)
            url = get_input("Enter the URL containing the table")
            table_selector = get_input("Enter CSS selector for table", default=DEFAULT_TABLE_SELECTOR)
            has_header = get_yes_no("Does the table have a header row?", default='y')
            
            print(f"\n⏳ Scraping table data from {url}...")
            result = scraper.scrape_table(url, table_selector=table_selector, 
                                         has_header=has_header)
            print(f"✅ Extracted {len(result)} rows!")
        
        # Extract Links
        elif scrape_type == '6':
            print("\n📋 STEP 2: Enter Link Extraction Details")
            print("-" * 70)
            url = get_input("Enter the URL to extract links from")
            internal_only = get_yes_no("Extract only internal links?", default='n')
            
            use_filter = get_yes_no("Filter links by pattern (e.g., only PDFs)?", default='n')
            filter_pattern = None
            if use_filter:
                filter_pattern = get_input("Enter regex pattern (e.g., '\\.pdf$' for PDFs)")
            
            print(f"\n⏳ Extracting links from {url}...")
            result = scraper.scrape_links(url, filter_pattern=filter_pattern, 
                                         internal_only=internal_only)
            print(f"✅ Extracted {len(result)} links!")
        
        # Extract Metadata
        elif scrape_type == '7':
            print("\n📋 STEP 2: Enter URL for Metadata Extraction")
            print("-" * 70)
            url = get_input("Enter the URL")
            
            print(f"\n⏳ Extracting metadata from {url}...")
            result = scraper.scrape_metadata(url)
            print("✅ Metadata extracted!")
        
        # Full Text Extraction
        elif scrape_type == '8':
            print("\n📋 STEP 2: Enter URL for Full Text Extraction")
            print("-" * 70)
            url = get_input("Enter the URL")
            
            print("\n📋 STEP 3: Choose Text Extraction Scope")
            print("-" * 70)
            print("  1. All paragraph text (<p> tags)")
            print("  2. All text in main content area")
            print("  3. Custom selector")
            
            text_choice = get_input("Enter your choice (1-3)", default="1", 
                                   options=['1', '2', '3'])
            
            if text_choice == '1':
                print(f"\n⏳ Extracting all paragraph text from {url}...")
                result = scraper.scrape(url, 'p', multiple=True)
                if result:
                    result = {'url': url, 'paragraphs': result, 'full_text': '\n\n'.join(result)}
                    print(f"✅ Extracted {len(result['paragraphs'])} paragraphs!")
                
            elif text_choice == '2':
                content_selector = get_input("Enter selector for main content area", 
                                            default=DEFAULT_CONTENT_SELECTOR)
                print(f"\n⏳ Extracting text from content area...")
                result = scraper.scrape(url, content_selector, multiple=False)
                if result:
                    result = {'url': url, 'full_text': result}
                    print(f"✅ Extracted {len(result['full_text'])} characters!")
                
            elif text_choice == '3':
                selector = get_input("Enter CSS selector for text extraction")
                multiple = get_yes_no("Extract from multiple elements?", default='y')
                print(f"\n⏳ Extracting text from {url}...")
                text_result = scraper.scrape(url, selector, multiple=multiple)
                if text_result:
                    if isinstance(text_result, list):
                        result = {'url': url, 'texts': text_result, 'full_text': '\n\n'.join(text_result)}
                        print(f"✅ Extracted text from {len(text_result)} elements!")
                    else:
                        result = {'url': url, 'full_text': text_result}
                        print(f"✅ Extracted {len(text_result)} characters!")
        
        # Display results
        if result:
            print("\n📊 RESULTS PREVIEW")
            print("-" * 70)
            
            if isinstance(result, dict):
                for key, value in list(result.items())[:5]:  # Show first 5 items
                    if isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    elif isinstance(value, list) and len(value) > 3:
                        print(f"  {key}: [{len(value)} items]")
                    else:
                        print(f"  {key}: {value}")
            elif isinstance(result, list):
                for i, item in enumerate(result[:3], 1):  # Show first 3 items
                    if isinstance(item, dict):
                        print(f"\n  Item {i}:")
                        for key, value in list(item.items())[:3]:
                            if isinstance(value, str) and len(value) > 60:
                                print(f"    {key}: {value[:60]}...")
                            else:
                                print(f"    {key}: {value}")
                    else:
                        display_value = str(item)[:80]
                        print(f"  {i}. {display_value}..." if len(str(item)) > 80 else f"  {i}. {display_value}")
                if len(result) > 3:
                    print(f"\n  ... and {len(result) - 3} more items")
            else:
                display_value = str(result)[:200]
                print(f"  {display_value}..." if len(str(result)) > 200 else f"  {display_value}")
            
            # Save results
            print("\n💾 SAVE RESULTS")
            print("-" * 70)
            save_results = get_yes_no("Save results to file?", default='y')
            
            if save_results:
                default_name = "scraped_data"
                if scrape_type == '3':
                    default_name = "headlines"
                elif scrape_type == '4':
                    default_name = "product"
                elif scrape_type == '5':
                    default_name = "table_data"
                elif scrape_type == '6':
                    default_name = "links"
                elif scrape_type == '7':
                    default_name = "metadata"
                elif scrape_type == '8':
                    default_name = "full_text"
                
                # Determine format
                if scrape_type == '5' and isinstance(result, list):
                    format_choice = get_input("Save as CSV or JSON? (csv/json)", default="csv", 
                                             options=['csv', 'json'])
                    output_file = get_input(f"Enter filename (without extension)", 
                                          default=default_name) + f".{format_choice}"
                else:
                    output_file = get_input("Enter filename (without .json)", 
                                          default=default_name) + ".json"
                
                # Save the file
                if output_file.endswith('.csv') and isinstance(result, list):
                    scraper.export_to_csv(result, output_file)
                else:
                    scraper.export_to_json(result, output_file)
                
                print(f"✅ Results saved to: {output_file}")
            
            # Summary
            print("\n" + "=" * 70)
            print("  ✅ SCRAPING COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            if output_file:
                print(f"  📁 Output file: {output_file}")
            print("  🎉 Thank you for using the Interactive Web Scraper!\n")
        
        else:
            print("\n⚠️  No data was scraped. Please check:")
            print("  • The URL is correct and accessible")
            print("  • The CSS selectors match elements on the page")
            print("  • The website allows scraping (check robots.txt)")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("  Please check your inputs and try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
