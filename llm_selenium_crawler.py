import os
from dotenv import load_dotenv
load_dotenv()


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from llm_extractor.openai import OpenAIExtractor
from pydantic import BaseModel


class QuerySelectorResult(BaseModel):
    name_query_selector: str
    price_query_selector: str
    description_query_selector: str
    

list_extract_fields = """
1. Product name
2. Product price
3. Product description
"""

query_css_extractor = OpenAIExtractor(
    api_key=os.environ["OPENAI_API_KEY"],
    json_format=QuerySelectorResult,
    list_extract_fields=list_extract_fields
)

# Set up the webdriver (make sure you have the correct driver installed)
driver = webdriver.Chrome()  # You can also use Firefox or other browsers

# Navigate to the URL
url = 'https://www.bachhoaxanh.com/nuoc-tay-quan-ao/2-chai-tay-moc-quan-ao-mau-mori-500ml'
driver.get(url)

# Wait for the page to load
time.sleep(3)


website_body = driver.find_element(By.TAG_NAME, "body")
website_body = website_body.get_attribute("outerHTML")

query_selector_result = query_css_extractor.extract(website_body)

# Loop through the results and print the content of the corresponding elements
for key, selector in query_selector_result.items():
    try:
        new_selector = selector.replace("[", "\\[").replace("]", "\\]")
        print("# Selector: ", new_selector)
        # Use find_elements to get a list of matching elements
        elems = driver.find_elements(By.CSS_SELECTOR, new_selector)
        
        # Concatenate their text content
        combined_text = " ".join(elem.text for elem in elems)
        print(f"{key}: {combined_text}")
    except Exception as e:
        print(f"Error finding {key}: {e}")

driver.quit()

