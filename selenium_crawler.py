import os
import time
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Set up MongoDB connection
mongo_client = MongoClient(os.environ["MONGO_URI"])
db = mongo_client["crawl"]
collection = db["bachhoaxanh"]

def crawl_urls(url_batch):
    # Create a single instance of the browser for the batch
    driver = webdriver.Chrome()

    for item in tqdm(url_batch):
        url = item.get("url")
        if not url:
            continue
        
        try:
            driver.get(url)
            time.sleep(3)  # Wait for the page to load
            
            # Extract data
            title = driver.find_element(By.TAG_NAME, "h1").text
            
            flagPrice = False
            try:
                price = driver.find_element(By.CSS_SELECTOR, "div.text-20.text-red-price").text
            except Exception as e:
                flagPrice = True
            if flagPrice:
                price = driver.find_element(By.CSS_SELECTOR, "div.swiper-list-cate-search div.swiper-slide-active div.flex.flex-col div:nth-child(1)").text
                
            description = driver.find_element(By.CSS_SELECTOR, "div.detail-style").text
            
            # Store data in MongoDB
            new_data = {
                "title": title,
                "price": price,
                "description": description,
                "image": item.get("image")
            }
            collection.insert_one(new_data)
        
        except Exception as e:
            with open("error.txt", "a") as f:
                f.write(f"ERROR crawling {url}\n")
    
    # Close the browser once the batch is processed
    driver.quit()

def chunkify(lst, n):
    """Divide the list into chunks of size n."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def main():
    # Load all URLs
    with open("all_data.json", "r") as f:
        all_urls = json.load(f)

    # Number of processes (use the number of CPU cores)
    num_processes = 2

    # Divide URLs into batches, one for each worker
    url_batches = chunkify(all_urls, len(all_urls) // num_processes)

    # Use a pool of workers to parallelize the crawling
    with Pool(num_processes) as pool:
        pool.map(crawl_urls, url_batches)

if __name__ == "__main__":
    main()
