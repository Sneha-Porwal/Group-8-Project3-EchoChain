import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import HEADERS
def fetch_page(url):
    """
    Download a webpage and return BeautifulSoup object.
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_next_page(soup, current_url):
    """
    Find the next page URL.
    """
    next_button = soup.find("a", rel="next")

    if next_button:
        next_url = urljoin(current_url, next_button["href"])
        return next_url

    return None