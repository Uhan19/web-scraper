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
import smtplib # For sending emails
from email.mime.multipart import MIMEMultipart # For creating email messages
from email.mime.text import MIMEText # For adding text to email messages
from dotenv import load_dotenv # For loading environment variables from a .env file
import os # For accessing environment variables

load_dotenv() # Load environment variables from the .env file

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS") # Get the email address from the environment variables
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # Get the email password from the environment variables
TO_EMAILS = os.getenv("TO_EMAILS").split(',') # Get the recipient email address from the environment variables

def send_email(product_name, url):
  msg = MIMEMultipart()
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = ", ".join(TO_EMAILS)
  msg['Subject'] = f"{product_name} is available!"

  body = f"The product {product_name} is now available for pickup. Check it out here: {url}"
  msg.attach(MIMEText(body, 'plain'))

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
  text = msg.as_string()
  server.sendmail(EMAIL_ADDRESS, TO_EMAILS, text)
  server.quit()
  print("Email sent successfully.")

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
      shipping_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/main/div[5]/div/div/div/div/div/div/div[7]/div[2]/div/div[11]/div/div/div/div/div[1]/fieldset/button[2]/p')))

      print("Pickup Element HTML:", pickup_element.get_attribute('outerHTML'))
      print("Shipping Element HTML:", shipping_element.get_attribute('outerHTML'))
      # Check the text inside the button to see if it contains "Ready within"
      if "Ready within" in pickup_element.text:
          driver.quit()
          return True
      if "Get it by" in shipping_element.text:
          driver.quit()
          return True

  except Exception as e:
      print(e)

  driver.quit()
  return False



# Example usage
if __name__ == "__main__": # Ensures that the following code block runs only if the script is executed directly, not when imported as a module.
  url = "https://www.bestbuy.com/site/apple-11-inch-ipad-pro-4th-generation-m2-chip-wi-fi-128gb-silver/5498402.p?skuId=5498402" # Specifies the URL to scrape.
  # url = "https://www.bestbuy.com/site/apple-airpods-with-charging-case-2nd-generation-white/6084400.p?skuId=6084400"
  product_name = "Apple - 11-Inch iPad Pro (4th Generation) M2 chip Wi-Fi - 128GB - Silver" # Specifies the product name to check.
  # product_name = "Apple - AirPods with Charging Case (2nd Generation) - White"

  while True:
    is_available = check_product_availability(url, product_name)
    print(f"Product available: {is_available}")

    if is_available:
      send_email(product_name, url)
      break # Exit the loop if the product is available

    # Wait for 5 minutes before checking again
    time.sleep(300)