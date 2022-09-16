import re

import requests
from bs4 import BeautifulSoup

n = 51
urls = [f"https://www.aquanliang.com/blog/page/{page}" for page in range(1, n)]


def craw(url: str):
    r = requests.get(url)
    content = r.text
    return content