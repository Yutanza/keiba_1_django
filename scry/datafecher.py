import os
import csv
import requests
import time
from bs4 import BeautifulSoup
import re
import logging

import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/85.0.4341.72",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/85.0.4341.72",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/5.3.2679.55",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/5.3.2679.55",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Brave/1.40.107",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Brave/1.40.107",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# class DataFetcher:
#     def __init__(self, base_url, sleep_time=1):
#         self.base_url = base_url
#         self.sleep_time = sleep_time

#     def fetch(self, url):
#         try:
#             user_agent=random.choice(USER_AGENTS)
#             headers = {
#             "User-Agent":user_agent
#             }
#             response = requests.get(url,headers=headers)
#             response.raise_for_status()
#             time.sleep(self.sleep_time)
#             return response.content
#         except requests.RequestException as e:
#             logging.error(f"Failed to fetch {url}: {e}")
#             return None
        
class DataFetcher:
    def __init__(self, sleep_time=0.7):
        self.sleep_time = sleep_time
        self.html_encoding=""

    def fetch(self, url):
        try:
            user_agent=random.choice(USER_AGENTS)
            headers = {
            "User-Agent":user_agent
            }
            response = requests.get(url,headers=headers)
            # print(response.content[:1000])
            self.html_encoding=response.apparent_encoding
            return_str=response.content.decode(self.html_encoding)
            
            response.raise_for_status()
            print(f"Done fetch {url}")
            print(self.html_encoding)
            # logging.info(f"Detected encoding: {response.apparent_encoding}")
            time.sleep(self.sleep_time)
            return return_str
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None