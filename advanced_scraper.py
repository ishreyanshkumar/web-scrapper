import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import logging
import argparse
from typing import List, Dict, Optional
from datetime import datetime


class WebScraper:
    """Advanced web scraper with enhanced error handling and features."""
    
    def __init__(self, base_url: str, delay: int = 2, max_retries: int = 3):
        """
        Initialize the web scraper.
        
        Args:
            base_url: Base URL for scraping
            delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url
        self.delay = delay
        self.max_retries = max_retries
        self.session = requests.Session()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML content with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string or None if failed
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Fetching URL (Attempt {attempt + 1}/{self.max_retries}): {url}")
                response = self.session.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                time.sleep(self.delay)
                return response.text
            except requests.RequestException as e:
                self.logger.error(f"Error fetching URL: {e}")
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    self.logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Failed to fetch URL after {self.max_retries} attempts")
                    return None
    
    def extract_products(self, html: str) -> List[Dict[str, str]]:
        """
        Extract product details from HTML.
        
        Args:
            html: HTML content as string            
        Returns:
            List of product dictionaries
        """
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        # Find all products
        product_containers = soup.find_all('div', class_='tUxRFH')
        self.logger.info(f"Found {len(product_containers)} product containers")
        
        for idx, product in enumerate(product_containers, 1):
            try:
                # Extract product name
                name_elem = product.find('div', class_='KzDlHZ')
                name = name_elem.text.strip() if name_elem else "N/A"
                
                # Extract product price
                price_elem = product.find('div', class_='Nx9bqj _4b5DiR')
                price = price_elem.text.strip() if price_elem else "N/A"
                
                # Extract product rating
                rating_elem = product.find('div', class_='XQDdHH')
                rating = rating_elem.text.strip() if rating_elem else "N/A"
                
                # Extract product link
                link_elem = product.find('a', class_='CGtC98')
                link = f"https://www.flipkart.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else "N/A"
                
                product_data = {
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'Link': link,
                    'Scraped_At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                products.append(product_data)
                self.logger.debug(f"Extracted product {idx}: {name}")
                
            except Exception as e:
                self.logger.error(f"Error extracting product {idx}: {e}")
                continue
        
        return products
    
    def save_to_csv(self, products: List[Dict], filename: str = 'products.csv'):
        """
        Save products to CSV file.
        
        Args:
            products: List of product dictionaries
            filename: Output filename
        """
        if not products:
            self.logger.warning("No products to save")
            return
        
        try:
            fieldnames = ['Name', 'Price', 'Rating', 'Link', 'Scraped_At']
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            self.logger.info(f"Successfully saved {len(products)} products to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
    
    def save_to_json(self, products: List[Dict], filename: str = 'products.json'):
        """
        Save products to JSON file.
        
        Args:
            products: List of product dictionaries
            filename: Output filename
        """
        if not products:
            self.logger.warning("No products to save")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(products, file, indent=2, ensure_ascii=False)
            self.logger.info(f"Successfully saved {len(products)} products to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")
    
    def scrape(self, search_query: str, output_format: str = 'csv', output_filename: str = None):
        """
        Main scraping function.
        
        Args:
            search_query: Product search query
            output_format: Output format ('csv' or 'json')
            output_filename: Custom output filename (without extension)
        """
        url = f"{self.base_url}?q={search_query.replace(' ', '+'')}"
        
        self.logger.info(f"Starting scrape for query: {search_query}")
        html = self.fetch(url)
        
        if not html:
            self.logger.error("Failed to fetch HTML content")
            return
        
        products = self.extract_products(html)
        
        if not products:
            self.logger.warning("No products found")
            return
        
        # Generate filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"flipkart_{search_query.replace(' ', '_')}_{timestamp}"
        
        # Save based on format
        if output_format.lower() == 'json':
            self.save_to_json(products, f"{output_filename}.json")
        else:
            self.save_to_csv(products, f"{output_filename}.csv")
        
        self.logger.info(f"Scraping completed. Found {len(products)} products")


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(description='Advanced Flipkart Web Scraper')
    parser.add_argument('--query', '-q', type=str, default='laptops',
                        help='Search query for products (default: laptops)')
    parser.add_argument('--format', '-f', type=str, choices=['csv', 'json'], default='csv',
                        help='Output format: csv or json (default: csv)')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Output filename without extension')
    parser.add_argument('--delay', '-d', type=int, default=2,
                        help='Delay between requests in seconds (default: 2)')
    parser.add_argument('--retries', '-r', type=int, default=3,
                        help='Maximum retry attempts (default: 3)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize scraper
    base_url = "https://www.flipkart.com/search"
    scraper = WebScraper(base_url, delay=args.delay, max_retries=args.retries)
    
    # Run scraper
    scraper.scrape(args.query, output_format=args.format, output_filename=args.output)


if __name__ == "__main__":
    main()
