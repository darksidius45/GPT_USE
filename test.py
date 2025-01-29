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
import tempfile
import os


def gemini_flash(text):
    json_data = {
        "contents": [{"role": "user", "parts": [{"text": text}]}]
    }
    
    # Create a temporary file to store the JSON data
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(json_data, temp_file)
        temp_file.flush()  # Ensure the data is written

        # Get the name of the temporary file
        temp_file_name = temp_file.name

    try:
        # Simplified curl command using the temporary file
        curl_command = [
            "curl",
            "https://api.proxyapi.ru/google/v1/models/gemini-1.5-flash:generateContent",
            "-H", "Content-Type: application/json",
            "-H", "Authorization: Bearer sk-UmoxJZ8wJm1DEmcSrwP3Iu9Bk4TGZJ0h",
            "-d", f"@{temp_file_name}"  # Use the temp file
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print("API Response:", response)  # Print the full response for debugging
            text_response = response['candidates'][0]['content']['parts'][0]['text']
            return text_response
        else:
            print("Error executing curl command:", result.stderr)
            return None
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

print(gemini_flash("what i was asking in the previos message"))
