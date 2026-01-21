# Web Scraper - Automated Data Extraction Tool

A powerful and flexible Python-based web scraper designed for automated data extraction from e-commerce websites. Currently supports Flipkart product scraping with extensible architecture for additional platforms.

## 🚀 Features

- **Automated Data Extraction**: Scrape product details including name, price, and ratings
- **CSV Export**: Save scraped data in CSV format for easy analysis
- **Smart Request Handling**: Built-in rate limiting and user-agent headers to avoid blocking
- **Error Handling**: Robust error handling for network and parsing issues
- **Extensible Design**: Easy to add support for additional websites

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🔧 Installation

1. Clone the repository:
```bash
   git clone https://github.com/ishreyanshkumar/web-scrapper.git
   cd web-scrapper
```

2. Install required dependencies:
```bash
   pip install requests beautifulsoup4
```

Or use the requirements file (if available):
```bash
   pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage

Run the scraper with default settings:
```bash
   python "Web Scrapper.py"
```

This will:
- Scrape laptop listings from Flipkart
- Extract product name, price, and rating
- Save results to `flipkart_products.csv`

### Output Format

The scraper generates a CSV file with the following columns:
- **Name**: Product name/title
- **Price**: Product price in INR
- **Rating**: Product rating (out of 5)

## 📁 Project Structure

```
web-scrapper/
│
├── Web Scrapper.py           # Main scraper script
├── Script Workflow.pdf       # Workflow documentation
├── flipkart_products.csv     # Sample output file
└── README.md                 # Project documentation
```

## 🔍 How It Works

1. **Fetch**: Sends HTTP request with proper headers to avoid blocking
2. **Parse**: Uses BeautifulSoup to parse HTML and locate product elements
3. **Extract**: Extracts relevant data (name, price, rating) from parsed HTML
4. **Save**: Writes extracted data to CSV file

## 🛠️ Technical Details

### Libraries Used

- **requests**: HTTP library for making web requests
- **BeautifulSoup4**: HTML parsing and navigation
- **csv**: CSV file operations (built-in)
- **time**: Rate limiting delays (built-in)

### Key Functions

- `fetch(url)`: Fetches HTML content with proper headers
- `extract(html)`: Parses HTML and extracts product data
- `save(products, filename)`: Saves data to CSV file
- `main()`: Orchestrates the scraping workflow

## ⚙️ Configuration

### Modifying Search Query

To search for different products, edit the URL in `main()`:
```python
url = "https://www.flipkart.com/search?q=YOUR_SEARCH_TERM"
```

### Adjusting Rate Limiting

Modify the sleep duration in `fetch()` to change request delay:
```python
time.sleep(2)  # Wait 2 seconds between requests
```

## 🚨 Important Notes

### Legal and Ethical Considerations

- **Respect robots.txt**: Check the website's robots.txt file
- **Rate Limiting**: Don't overload servers with too many requests
- **Terms of Service**: Review and comply with website ToS
- **Personal Use**: This scraper is intended for educational and personal use

### Common Issues

1. **Empty Results**: Website structure may have changed; CSS selectors need updating
2. **Blocked Requests**: Try adjusting headers or increasing delay between requests
3. **Import Errors**: Ensure all dependencies are installed

## 🔄 Future Enhancements

Potential improvements for this project:

- [ ] Multi-threaded scraping for better performance
- [ ] Support for multiple e-commerce platforms
- [ ] Database integration (SQLite, PostgreSQL)
- [ ] JSON export option
- [ ] Command-line arguments for flexible configuration
- [ ] Logging system for debugging
- [ ] Proxy support for avoiding IP blocks
- [ ] Product comparison features
- [ ] Price tracking and alerts
- [ ] Web UI dashboard

## 📝 Example Output

```csv
Name,Price,Rating
"Dell Inspiron 15 Laptop",₹45,990,4.3
"HP Pavilion Gaming Laptop",₹67,999,4.5
"Lenovo IdeaPad Slim 3",₹38,990,4.2
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

**ishreyanshkumar**
- GitHub: [@ishreyanshkumar](https://github.com/ishreyanshkumar)

## ⚠️ Disclaimer

This tool is provided for educational purposes only. Users are responsible for ensuring their use complies with applicable laws and website terms of service. The author is not responsible for any misuse of this tool.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note**: Web scraping may be against the terms of service of some websites. Always verify that you have permission to scrape a website before doing so.