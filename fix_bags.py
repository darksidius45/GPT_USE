from googlesearch import search
# import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import openpyxl
import json
import subprocess
import requests
import random
from bs4 import BeautifulSoup
# import zipfile
# from config import promt
import pandas as pd
from urllib.parse import urlparse, urljoin

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



def get_site_text(website):
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")
    service = Service("C:/webdrivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    original_domain = urlparse(website).netloc
    keywords = [
        "about", "product", "solution",  # English
        "über", "produkt", "lösung",  # German
        "acerca de", "producto", "solución",  # Spanish
        "à propos", "produit", "solution",  # French
        "circa", "prodotto", "soluzione",  # Italian
        "sobre", "produto", "solução",  # Portuguese
        "关于", "产品", "解决方案",  # Chinese
        "о", "продукт", "решение",  # Russian
        "について", "製品", "ソリューション",  # Japanese
        "hakkında", "ürün", "çözüm",  # Turkish
        "حول", "منتج", "حل"  # Arabic
    ]
    all_texts = []

    try:
        driver.get(website)
        time.sleep(3)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        all_texts.append(soup.get_text(separator=" ", strip=True))

        hrefs_set = set()
        clickable_elements = []
        for element in soup.find_all(['a', 'button', 'input', 'area']):
            if element.has_attr('href'):
                href = element['href']
                if href not in hrefs_set and original_domain in urlparse(href).netloc and any(keyword in href for keyword in keywords):
                    clickable_elements.append(element)
        for i in clickable_elements:
            print(i, end = "\n")
        for element in clickable_elements:
            if element.has_attr('href'):
                new_link = urljoin(website, element['href'])
                if original_domain in urlparse(new_link).netloc and any(keyword in new_link for keyword in keywords):
                    driver.get(new_link)
                    time.sleep(3)
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    all_texts.append(soup.get_text(separator=" ", strip=True))
            elif element.has_attr('onclick'):
                # Extract URL from onclick JavaScript if possible
                onclick_content = element['onclick']
                # This is a simple heuristic to extract URLs from JavaScript
                url_start = onclick_content.find("http")
                if url_start != -1:
                    url_end = onclick_content.find("'", url_start)
                    if url_end == -1:
                        url_end = onclick_content.find('"', url_start)
                    if url_end != -1:
                        new_link = onclick_content[url_start:url_end]
                        if original_domain in urlparse(new_link).netloc and any(keyword in new_link for keyword in keywords):
                            driver.get(new_link)
                            time.sleep(3)
                            page_source = driver.page_source
                            soup = BeautifulSoup(page_source, "html.parser")
                            all_texts.append(soup.get_text(separator=" ", strip=True))
    except WebDriverException as e:
        print(f"Error accessing {website}: {e}")
    finally:
        driver.quit()

    return all_texts


def gemini_flash(text):
    curl_command = [
        "curl",
        "https://api.proxyapi.ru/google/v1/models/gemini-1.5-flash:generateContent",
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer sk-UmoxJZ8wJm1DEmcSrwP3Iu9Bk4TGZJ0h",
        "-d", json.dumps({
            "contents": [{"role": "user", "parts": [{"text": text}]}]
        })
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode == 0:
        response = json.loads(result.stdout)
        print(response)
        return response
    else:
        print("Error executing curl command:", result.stderr)
        return None



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
    site_text = get_site_text(website)
    site_info = gemini_flash(f"tell me about this company according to this text from their site{site_text}")
    company_data.append((name, website, categories, description, site_info))
    row[6].value = site_info
df.save("out.xlsx")  # Save the changes to the Excel file
