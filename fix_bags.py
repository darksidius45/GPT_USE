from googlesearch import search
# import re
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException
import openpyxl
# import json
# import subprocess
import requests
import random
# from bs4 import BeautifulSoup
# import zipfile
# from config import promt
import pandas as pd


PROXY_PORT = 5500
PROXY_USER = "5vWk59"
PROXY_PASSWORD = "tXQt5fnHW9"

def get_random_proxy():
    proxies = [
        "45.11.21.124",
        "213.226.101.147",
        "94.158.190.16",
        "109.248.128.64",
        "188.130.218.160",
        "46.8.15.51",
        "46.8.23.126",
        "188.130.129.246",
        "188.130.128.66",
        "46.8.106.76",
        "46.8.111.80",
        "109.248.142.228",
        "46.8.222.147",
        "109.248.204.170"
    ]
    return random.choice(proxies)

def find_website(name):
    query = f"{name} site"
    proxy = get_random_proxy()
    proxy_url = f"http://{PROXY_USER}:{PROXY_PASSWORD}@{proxy}:{PROXY_PORT}"

    try:
        for result in search(query, num_results=10):
            if all(exclusion not in result for exclusion in ['youtube.com', 'facebook.com', 'wikipedia.org', 'linkedin.com']):
                return result
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    return None



# def get_site_text(website):
#     chrome_options = Options()
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")
#     service = Service("C:/webdrivers/chromedriver.exe")
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     try:
#         driver.get(website)
#         time.sleep(3)
#         site_element = driver.page_source
#         soup = BeautifulSoup(site_element, "html.parser")
#         hrefs = []
#         main_page_text = [site_element.get_text(separator=" ", strip=True)]

#         for a_tag in soup.find_all('a', href=True):
#             href = a_tag['href']
#             if not any(exclusion in href for exclusion in ['youtube.com', 'wikipedia.org', 'facebook.com', 'instagram.com']):
#                 if not any(ext in href for ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov']):
#                     hrefs.append(href)

#         for href in hrefs:
#             try:
#                 driver.get(href)
#                 time.sleep(3)
#                 href_page_source = driver.page_source
#                 href_soup = BeautifulSoup(href_page_source, "html.parser")
#                 main_page_text.append(href_soup.get_text(separator=" ", strip=True))

#             except requests.exceptions.RequestException as e:
#                 print(f"Error fetching {href}: {e}")
        
#         print(main_page_text)
#         driver.quit()
#     except WebDriverException as e:
#         print(main_page_text)
#         print(f"WebDriverException occurred: {e}")
#     finally:
#         driver.quit()






df = openpyxl.load_workbook("out.xlsx")
sheet = df.active
company_data = []
for row in sheet.iter_rows(min_row=2):
    name = row[0].value
    website = row[1].value
    categories = row[4].value
    description = row[5].value
    if not website or website == "error":
        website = find_website(name)
        row[1].value = website  # Save the website in the Excel sheet
    company_data.append((name, website, categories, description))
df.save("out.xlsx")  # Save the changes to the Excel file

for data in company_data:
    print(f"Company Name: {data[0]}")
    print(f"Company Website: {data[1]}")
    print(f"Company Categories: {data[2]}")
    print(f"Company Description: {data[3]}")
    print("\n")
