import requests # For making HTTP requests to fetch web pages
from bs4 import BeautifulSoup # For parsing HTML and extracting data

# For automating web browser interactions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from webdriver_manager.chrome import ChromeDriverManager # Automatically manages the ChromeDriver binary
import time # For adding delays

def check_product_availability(url, product_name):
  # Creates a 'ChromeOptions' object to configure the browser options
  options = Options()
  # Set the browser to run in headless mode (no browser UI)
  options.headless = True
  # Initializes a Chrome WebDriver with thte specified options and managed by 'ChromeDriverManager'
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

  driver.get(url)

  try:
      # Use explicit wait to wait for the button to be present
      wait = WebDriverWait(driver, 10)
      pickup_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/main/div[5]/div/div/div/div/div/div/div[7]/div[2]/div/div[11]/div/div/div/div/div[1]/fieldset/button[1]/p')))

      print("Pickup Element HTML:", pickup_element.get_attribute('outerHTML'))
      # Check the text inside the button to see if it contains "Ready within"
      if "Ready within" in pickup_element.text:
          driver.quit()
          return True
  except Exception as e:
      print(e)
      # Extract and print relevant part of the page source
      page_source = driver.page_source
      start_index = page_source.find('<p')
      end_index = page_source.find('</p>', start_index) + len('</p>')
      relevant_snippet = page_source[start_index:end_index]

      print("Relevant snippet of the page source:", relevant_snippet)

  driver.quit()
  return False



# Example usage
if __name__ == "__main__": # Ensures that the following code block runs only if the script is executed directly, not when imported as a module.
  url = "https://www.bestbuy.com/site/lenovo-loq-15-6-gaming-laptop-fhd-amd-ryzen-7-7435hs-with-16gb-memory-nvidia-geforce-rtx-4060-8gb-512gb-ssd-luna-grey/6578511.p?skuId=6578511&irclickid=yIfxa-xaexyKTxL0-0RvfWmtUkHVfkwNA3SQTI0&irgwc=1&ref=198&loc=PricePP%20LLC&acampID=0&mpid=56357&affgroup=%22Deals%22&intl=nosplash" # Specifies the URL to scrape (should be replaced with the actual target URL).
  product_name = "Lenovo laptop" # Specifies the product name to check.
  is_available = check_product_availability(url, product_name)
  print(f"Product available: {is_available}")