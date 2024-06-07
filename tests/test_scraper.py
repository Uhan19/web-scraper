import unittest
from src.website_oos_scraper import check_product_availability

class TestScraper(unittest.TestCase):

  def test_product_availability(self):
    url = "https://www.bestbuy.com/site/apple-airpods-with-charging-case-2nd-generation-white/6084400.p?skuId=6084400" # Specifies the URL to scrape (should be replaced with the actual target URL).
    product_name = "AirPods" # Specifies the product name to check.
    self.assertTrue(check_product_availability(url, product_name))

  def test_product_availability_2(self):
    url = "https://www.bestbuy.com/site/lenovo-loq-15-6-gaming-laptop-fhd-amd-ryzen-7-7435hs-with-16gb-memory-nvidia-geforce-rtx-4060-8gb-512gb-ssd-luna-grey/6578511.p?skuId=6578511&irclickid=yIfxa-xaexyKTxL0-0RvfWmtUkHVfkwNA3SQTI0&irgwc=1&ref=198&loc=PricePP%20LLC&acampID=0&mpid=56357&affgroup=%22Deals%22&intl=nosplash"
    product_name = "Lenovo laptop"
    self.assertFalse(check_product_availability(url, product_name))


if __name__ == "__main__":
  unittest.main()
