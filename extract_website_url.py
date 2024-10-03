import requests
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm
# URLs of the sitemaps
with open("./all_sitemap.json", "r") as f:
    sitemap_urls = json.load(f)

all_data = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to fetch and parse XML
def fetch_sitemap(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        root = ET.fromstring(response.content)
        
        # Create a mapping of URLs to images
        for url_element in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            # Attempt to find the associated image
            image = url_element.find('{http://www.google.com/schemas/sitemap-image/1.1}image:loc')
            image_loc = image.text if image is not None else None
            
            # Append to the list as a dictionary
            all_data.append({'url': loc, 'image': image_loc})
    except Exception as e:
        print(f"Error fetching or parsing {url}: {e}")

# Fetch and parse both sitemaps
for sitemap_url in tqdm(sitemap_urls):
    fetch_sitemap(sitemap_url)

# Write the URLs and images to a JSON file
with open('./all_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print(f"Extracted {len(all_data)} URLs and images.")

