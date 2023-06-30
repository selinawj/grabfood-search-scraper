from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import ssl
import urllib
import pandas as pd
from selenium import webdriver
import time


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    "Content-Type": "application/x-www-form-urlencoded"} # set the headers
ssl._create_default_https_context = ssl._create_unverified_context

data = {}
city = "New-York-City"
# url = "https://www.ubereats.com/city/" + city.lower()
url = "https://www.ubereats.com/_p/api/getFeedV1"
# url = "https://www.ubereats.com/search?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk5vLiUyMDMzMyUyQyUyMER1bkh1YSUyME4lMjBSZCUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpIOVd6dk8tclFqUVJNNTY2bFVpVmRtOCUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wNTk1Njg3JTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjU1MDE0NTglN0Q%3D&q=tea&sc=SEARCH_SUGGESTION&vertical=ALL"
req = Request(url, headers=headers)
page = urlopen(req).read()
soup = BeautifulSoup(page, 'html.parser')

vendornames = []
vendorimages = []
vendorurls = []

for x in soup.findAll("div", {"class": "af cx cu f9 eq er es et"}):
    print (x)
    for y in x:
        print (y.text)
for x in soup.select("h3[class^=be]"): # find the name of the restaurant
    vendor_name = x.text
    vendornames.append(vendor_name)

print (len(vendornames))

for x in soup.findAll('a', {"class": "al ak br c8 iq bs am fz g8 ir gt"}):
for x in soup.select("a[class^=al][data-test^=store-link]"): # find vendor url of restaurant
    base_url = "https://www.ubereats.com"
    vendor_url = base_url + x.get('href')
    vendorurls.append(vendor_url)

print(len(vendorurls))
# for x in soup.findAll('a', {"class": "al ak br c8 iq bs am fz g8 ir gt"}):
# for x in soup.findAll('div', {"class": "al br is it"}):
#     vendor_img = x.find('img').attrs['src']
#     vendorimages.append(vendor_img)

print (vendornames)
output_df = pd.DataFrame({'vendor_names': vendornames, 'vendor_urls': vendorurls})

output_df.to_csv("ubereats_res.csv", index=False)
print ("output saved")