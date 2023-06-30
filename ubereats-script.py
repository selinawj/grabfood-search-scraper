import time
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


### Setup Driver ###
url = "https://food.grab.com/sg/en/restaurants?search=wings&lng=en&support-deeplink=true&searchParameter=wings"
chrome_options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

### Accept Cookies ###
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))).click()
except TimeoutException:
    pass

### Scroll to bottom ###
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

### Extract Restaurant Data ###
layout_div = driver.find_element(By.CSS_SELECTOR, '.ant-layout')
# container = driver.find_elements(By.CSS_SELECTOR, '.ant-col-24')

restaurant_names = layout_div.find_elements(By.CSS_SELECTOR, '.name___2epcT')
cuisine_names = layout_div.find_elements(By.CSS_SELECTOR, '.basicInfoRow___UZM8d.cuisine___T2tCh')

image_elements = driver.find_elements(By.XPATH, "//img[contains(@class, 'realImage___2TyNE')]")
img_url_list = []
for img in image_elements:
    img_url = img.get_attribute("src")
    # if img_url is not None:
        # if img_url.endswith('.webp'):
    img_url_list.append(img_url)
# print(len(img_url_list))


vendor_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/sg/en/restaurant')]")
url_elements_list = []
for url_element in vendor_url:
    url_elements_list.append(url_element.get_attribute("href"))
# url_elements_list = url_elements_list[10:]

# for item in container:


### Convert to lists ###
names = [name.text for name in restaurant_names]
cuisines = [cuisines_name.text for cuisines_name in cuisine_names]


#select first 100 results
names = names[:100]
cuisines = cuisines[:100]
url_elements_list = url_elements_list[:100]
img_url_list = img_url_list[:100]
print(len(names))
print(len(cuisines))
print(len(img_url_list))
print(len(url_elements_list))
# resto_names = pd.DataFrame({'restaurant_names': names})
# resto_url = pd.DataFrame({'restaurant_urls': url_elements_list})
# resto_img = pd.DataFrame({'restaurant_img': img_url_list})

# resto_names.to_csv("resto_names.csv", index=False)
# resto_url.to_csv("resto_url.csv", index=False)
# resto_img.to_csv("resto_img.csv", index=False)

grab_resto = pd.DataFrame({
'restaurant_names': names, 'cuisine_names': cuisines, 'vendor_urls': url_elements_list, 'vendor_img': img_url_list})
grab_resto.to_csv("test_grab_res.csv", index=False)
