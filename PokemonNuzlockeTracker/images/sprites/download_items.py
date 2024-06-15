import requests
from bs4 import BeautifulSoup
import os

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_image_urls(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all image tags in the content
    image_tags = soup.find_all('img')
    # Extract the 'src' attribute of each image tag and ensure it is a complete URL
    image_urls = [base_url + img['src'] for img in image_tags if 'src' in img.attrs]
    return image_urls

def download_images(image_urls, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    for url in image_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Extract image name from URL
            image_name = url.split('/')[-1]
            image_path = os.path.join(download_folder, image_name)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {image_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

# URL of the webpage containing the item sprites
url = 'https://www.pokencyclopedia.info/en/index.php?id=sprites/items/items_3ds'
# Base URL to append to the relative image paths
base_url = 'https://www.pokencyclopedia.info/'

# Fetch and parse the webpage
html_content = fetch_html(url)
if html_content:
    image_urls = parse_image_urls(html_content, base_url)
    download_folder = 'item_sprites'
    download_images(image_urls, download_folder)
