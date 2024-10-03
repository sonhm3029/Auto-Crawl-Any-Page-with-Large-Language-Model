import requests
import xml.etree.ElementTree as ET
import json

# URLs of the sitemaps
sitemap_urls = [
  'https://www.bachhoaxanh.com/sitemapnew/sitemap-product'
]

all_urls = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to fetch and parse XML
def fetch_sitemap(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        root = ET.fromstring(response.content)
        # Extract all <loc> elements that contain the URLs
        for url_element in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            all_urls.append(url_element.text)
    except Exception as e:
        print(f"Error fetching or parsing {url}: {e}")

# Fetch and parse both sitemaps
for sitemap_url in sitemap_urls:
    fetch_sitemap(sitemap_url)

# Write the URLs to a JSON file
with open('./all_sitemap.json', 'w') as f:
    json.dump(all_urls, f, indent=4)

print(f"Extracted {len(all_urls)} sitemap url and saved to all_sitemap.json")
