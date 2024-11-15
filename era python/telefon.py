import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

# Function to fetch the webpage content
def fetch_page(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print("Failed to retrieve the page.")
        return None

# Function to extract product details
def extract_telephone_data(products):
    telephones = []
    for product in products[:10]:  # Limit to first 10 products
        title_element = product.find('a', class_='product-title')
        price_element = product.find('span', class_='ty-list-price')
        discount_price_element = product.find('span', class_='ty-price-update')

        title = title_element.text.strip() if title_element else 'N/A'
        price = price_element.text.strip().replace('€', '').replace(',', '') if price_element else 'N/A'
        discount_price = discount_price_element.text.strip().replace('€', '').replace(',', '') if discount_price_element else 'N/A'

        price = try_convert_to_float(price)
        discount_price = try_convert_to_float(discount_price)

        telephones.append({
            'Title': title,
            'Price': price,
            'Discount Price': discount_price
        })
    return telephones

# Helper function to safely convert values to float
def try_convert_to_float(value):
    try:
        return float(value) / 100 if value else None
    except ValueError:
        return None

# Function to create DataFrame and plot the data as a pie chart
def create_dataframe_and_plot(telephones):
    df = pd.DataFrame(telephones)
    print(df)

    # Create a pie chart visualization
    fig = px.pie(df, names='Title', values='Price',
                 hover_data=['Discount Price'],
                 title='Telephone Price Distribution')
    fig.show()

# Main function to scrape telephone data
def scrape_telephones():
    url = "https://www.75mall.com/telefone-and-ora-te-mencura/telefone-mobil-al/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    soup = fetch_page(url, headers)
    if soup:
        products = soup.find_all('div', class_='ty-column4')
        telephones = extract_telephone_data(products)
        create_dataframe_and_plot(telephones)

# Call the function to scrape data
scrape_telephones()