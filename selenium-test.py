from selenium import webdriver
import time

# Chrome Session
driver = webdriver.Chrome('/Applications/chromedriver')
driver.get('https://www.google.com')
time.sleep(5)
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)
driver.quit()
