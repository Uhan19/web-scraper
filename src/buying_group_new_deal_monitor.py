import os
import time
import hashlib
import smtplib
from dotenv import load_dotenv
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Configurations
LOGIN_URL = "https://www.buyinggroup.com/login"
DEALS_URL = "https://buyinggroup.com/deals/active"
USERNAME = os.getenv("BUYING_GROUP_USERNAME")
PASSWORD = os.getenv("BUYING_GROUP_PASSWORD")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SCREENSHOT_PATH = "/Users/yuehanduan/Documents/screenshot/scraper_screenshots/buying_group_deals"

# Ensure the screenshot directory exists
os.makedirs(SCREENSHOT_PATH, exist_ok=True)

def send_email(deal):
  msg = MIMEMultipart()
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = EMAIL_ADDRESS
  msg['Subject'] = f"New deal post at buyinggroup.com!"

  body = f"New deal found: {deal['description']} at {deal['price']}"
  msg.attach(MIMEText(body, 'plain'))

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
  text = msg.as_string()
  server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, text)
  server.quit()
  print("Email sent successfully.")

def login(driver):
  driver.get(LOGIN_URL)
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/section/section/section/main/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/form/label[1]")))

  username_input = driver.find_element(By.ID, "username")
  password_input = driver.find_element(By.ID, "password")
  login_button = driver.find_element(By.ID, "login-btn")

  username_input.send_keys(USERNAME)
  password_input.send_keys(PASSWORD)
  time.sleep(3) # There's an issue where the login button can't be clicked right away, only works have a delay
  login_button.click()

  WebDriverWait(driver, 10).until(EC.url_contains('dashboard'))
  print("Login successful.")

def generate_deal_id(description, price):
  return hashlib.md5(f"{description}{price}".encode()).hexdigest()

def get_deals(driver):
  driver.get(DEALS_URL)
  WebDriverWait(driver, 10).until(EC.url_contains('active'))

  # Ensure the page is fully loaded
  driver.execute_script("return document.readyState;")
  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#deals-list > div:nth-child(2) > div")))
  time.sleep(5) # Wait for the page to fully load

  deal_elements = driver.find_elements(By.ID, "deal-card-container") [:10] # Limit to first 4 items
  print(f"Found {len(deal_elements)} deal elements.")

  deals = []
  for deal in deal_elements:
    description = deal.find_element(By.ID, "deal-card-title").text
    price = deal.find_element(By.CLASS_NAME, "new-blue-color.bold20").text  # Adjust the class name based on your page
    deal_id = generate_deal_id(description, price)

    print(f"Found deal: {description} - {price}")
    deals.append({
      'id': deal_id,
      'description': description,
      'price': price,
      'element': deal
    })

  print(f"Found {len(deals)} deals.")
  return deals

def capture_screenshot(driver, deal_element, filename):
  deal_element.screenshot(filename)

def monitor_deals():
  options = Options()
  options.headless = True
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

  try:
    login(driver)
    existing_deals = set()

    while True:
      deals = get_deals(driver)
      current_deals = set(deal['id'] for deal in deals)

      new_deals = current_deals - existing_deals
      if new_deals:
        for deal in deals:
          screenshot_filename = os.path.join(SCREENSHOT_PATH, f"deal_{deal['id']}.png")
          capture_screenshot(driver, deal['element'], screenshot_filename)
          print(f"New deal found {deal['description']} at {deal['price']}. Screenshot saved to {screenshot_filename}")
          # TODO: send SMS notification
          send_email(deal)

      existing_deals = current_deals
      time.sleep(60) # Check every minute
  finally:
    driver.quit()

if __name__ == "__main__":
  monitor_deals()
