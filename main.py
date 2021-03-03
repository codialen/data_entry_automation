from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

# Input your HTTP Request Header
header = {
    "User-Agent": "[YOUR USER-AGENT HERE]",
    "Accept-Language": "[YOUR ACCEPT-LANGUAGE HERE]"
}

FORM_URL = "" # The form you want to populate
ZILLOW_URL = "" # The Zillow URL with the area you are searching

# Use BeautifulSoup/Requests to scrape all the listings from the Zillow web address.
response = requests.get(ZILLOW_URL, headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

# Create a list of links for all the listings you scraped.
all_link_elements = soup.select(".list-card-top a")
all_links = []
for link in all_link_elements:
    href = link["href"]
    # Some of the links you get back from Zillow may be incomplete.
    if "http" not in href:
        all_links.append(f"https://www.zillow.com/{href}")
    else:
        all_links.append(href)

# Create a list of prices for all the listings you scraped.
all_price_elements = soup.select(".list-card-heading")
all_prices = []
for element in all_price_elements:
    # Get the prices. Single and multiple listings have different tag & class structures
    try:
        # Price with only one listing
        price = element.select(".list-card-price")[0].contents[0]
    except IndexError:
        print("Multiple listings for the card.")
        # Price with multiple listings
        price = element.select(".list-card-details li")[0].contents[0]
    finally:
        all_prices.append(price)

# Create a list of addresses for all the listings you scraped.
all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

# Use Selenium to fill in the form you created. Each listing should have its price/address/link added to the form.
# You will need to fill in a new form for each new listing.
chrome_driver_path = "" # Your driver path here
driver = webdriver.Chrome(executable_path=chrome_driver_path)

for n in range(len(all_links)):
    driver.get(FORM_URL)

    time.sleep(2)
    address = driver.find_element_by_xpath(
        '') # The address xpath on your form
    price = driver.find_element_by_xpath(
        '') # The price xpath on your form
    link = driver.find_element_by_xpath(
        '') # The link xpath on your form
    submit_button = driver.find_element_by_xpath('') # The submit button xpath on your form

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()

