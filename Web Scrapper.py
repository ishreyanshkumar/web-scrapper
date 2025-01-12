import requests
from bs4 import BeautifulSoup
import csv
import time

# Function to fetch HTML content
def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }

    response = requests.get(url, headers=headers)
    time.sleep(2)
    response.raise_for_status()
    return response.text

# Function to extract product details
def extract(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    # Find all products
    pl = soup.find_all('div', class_='tUxRFH')  # Outer product container

    for product in pl:

        # Extract product name
        name = product.find('div', class_='KzDlHZ').text.strip()

        # Extract product price
        price = product.find('div', class_='Nx9bqj _4b5DiR').text.strip()

        # Extract product rating
        rating = product.find('div', class_='XQDdHH').text.strip()

        # Append the product data
        products.append({'Name': name, 'Price': price, 'Rating': rating})

    return products

# Function to save data to CSV
def save(products, filename='flipkart_products.csv'):
    if not products:
        print("No products found to save.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Name', 'Price', 'Rating'])
            writer.writeheader()
            writer.writerows(products)
        print(f"Data saved to {filename}")
    except:
        print(f"Error saving data")

# Main function
def main():
    # Flipkart search URL laptops here
    url = "https://www.flipkart.com/search?q=laptops"

    print("Fetching data from Flipkart...")
    html = fetch(url)


    print("Extracting product details...")
    products = extract(html)

    if products:
        print(f"Found {len(products)} products. Saving to CSV...")
        save(products)
    else:
        print("No products found")


if __name__ == "__main__":
    main()
