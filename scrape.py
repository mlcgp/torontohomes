from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from data_helper import get_data
import os
from secret import key

base_url = 'https://www.zolo.ca/index.php?sarea=Toronto&ptype_house=1&ptype_townhouse=1&filter=1'

# Start session
options = Options()
options.add_argument(
    "user-agent=Chrome/80.0.3987.149 Safari/537.36 RuxitSynthetic/1.0 v320195424 t18859")
driver = webdriver.Chrome('/Applications/chromedriver', options=options)
driver.get(base_url)
time.sleep(2)

# Sign in
key_ = key
driver.find_element_by_xpath(
    "//button[@class='button button--transparent button--small bold xs-hide md-block signup-btn']").click()
email = driver.find_element_by_name("emailaddress")
email.send_keys(key)
driver.find_element_by_xpath("//button[@id='submitEmail']").click()

# Wait for a little
time.sleep(2)

# Create a function to crawl


def spider():
    num_pages = int(driver.find_element_by_css_selector("body.home.gallery.logged-in:nth-child(2) div.wrapper:nth-child(1) main.transition-after-load.gut section.supplementary-nav.xs-mt5.xs-mb6.sm-mt5.sm-mb6.xs-flex.xs-flex-column.xs-flex-align-center:nth-child(3) nav.md-inline-block.xs-hide.md-block > a.button.button--mono.button--large.shadow-1.xs-mr05:nth-child(7)").text)
    # Iterate through all pages for search results (base_url)
    for i in range(num_pages - 1):
        num_listings = list(range(1, len(driver.find_elements_by_class_name("street"))+1))
        listings = [
            f"//li[{num_listing}]//article[1]//div[1]//div[1]//a[1]//h3[1]" for num_listing in num_listings]
        all_data = []
        for listing in listings:
            driver.find_element_by_xpath(listing).click()
            # Avoid 404 errors
            try:
                r = requests.head(driver.current_url)
                status = r.status_code
                if status == 404:
                    driver.back()
                    continue
            except requests.ConnectionError:
                print("failed to connect")
            # Try expandable toggle element before click
            # Wait if element is not found and return to main listings page
            try:
                element_present = EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='button button--large button--white-black link-green pill xs-full-width shadow-1 expandable-toggle']"))
                WebDriverWait(driver, 30).until(element_present)
                driver.find_element_by_xpath(
                    "//button[@class='button button--large button--white-black link-green pill xs-full-width shadow-1 expandable-toggle']").click()
            except TimeoutException:
                print("Couldn't find element")
                driver.back()
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # Get the listing data
            listing_data = get_data(soup, driver)
            all_data.append(listing_data)
            driver.back()
            # Go to the next page if at the last item of listings
            if listing == listings[-1]:
                time.sleep(2)
                driver.find_element_by_class_name("icon-keyboard-arrow-right").click()
    driver.quit()
    return pd.DataFrame(all_data)


if __name__ == '__main__':
    cwd = os.getcwd()
    filename = f"{cwd}/toronto_home_data.csv"
    data = spider()
    data.to_csv(filename)
