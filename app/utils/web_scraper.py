import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urlparse, urljoin
from fastapi.exceptions import HTTPException

from urllib.parse import urlparse

def normalize_and_validate_domain_url(url_string: str):
    try:
        url = url_string.strip()
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        parsed = urlparse(url)
        if not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        base_url = f"{parsed.scheme}://{domain}/"
        response = requests.head(base_url, allow_redirects=True, timeout=5)
        if response.status_code >= 400:
            raise ValueError(f"Invalid Domain: {base_url}")
        return base_url
    except requests.RequestException:
        raise HTTPException(status_code=400, detail=f"Invalid domain: {url_string}")


def get_name_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    print(domain)
    name = domain.split('.')[0]
    return name


def web_scrape_logo(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check <meta> tags (OpenGraph, Twitter Card, etc.)
        meta_logo = (
            soup.find("meta", property="og:image") or
            soup.find("meta", attrs={"name": "twitter:image"}) or
            soup.find("meta", attrs={"itemprop": "image"}) or
            soup.find("link", rel="icon") or
            soup.find("link", rel="shortcut icon") or
            soup.find("link", rel="apple-touch-icon")
        )
        if meta_logo and meta_logo.get("content"):
            return meta_logo["content"]
        elif meta_logo and meta_logo.get("href"):
            return meta_logo["href"]

        # Check <img> tags with common logo-related attributes
        logo_keywords = ["logo", "brand", "site-logo", "header-logo", "icon"]
        logo_tags = soup.find_all("img", class_=lambda x: x and any(keyword in x.lower() for keyword in logo_keywords))
        if not logo_tags:
            logo_tags = soup.find_all("img", id=lambda x: x and any(keyword in x.lower() for keyword in logo_keywords))
        if not logo_tags:
            logo_tags = soup.find_all("img", alt=lambda x: x and any(keyword in x.lower() for keyword in logo_keywords))

        # Check <svg> tags (for inline SVGs)
        if not logo_tags:
            logo_tags = soup.find_all("svg", class_=lambda x: x and any(keyword in x.lower() for keyword in logo_keywords))

        # Check <div> or <a> tags with background images (CSS)
        if not logo_tags:
            logo_tags = soup.find_all("div", class_=lambda x: x and any(keyword in x.lower() for keyword in logo_keywords))
        if not logo_tags:
            logo_tags = soup.find_all("a", class_=lambda x: x and any(keyword in x.lower() for keyword in logo_keywords))

        # Check the first <img> or <svg> tag if no specific logo is found
        if not logo_tags:
            logo_tags = soup.find_all("img") + soup.find_all("svg")

        if logo_tags:
            logo = logo_tags[0]
            if logo.name == "img":
                logo_url = logo.get("src")
            elif logo.name == "svg":
                logo_url = "data:image/svg+xml;base64,"
                logo_url += logo.encode("utf-8").decode("utf-8")
            else:
                logo_url = logo.get("style")

            if logo_url and not logo_url.startswith(("http", "https", "data:")):
                logo_url = requests.compat.urljoin(url, logo_url)
            return logo_url

        return None

    except Exception as e:
        print(f"Error scraping logo: {e}")
        return None


def get_logo(url):
    """ Attempt to fetch a brand's logo from a given URL """
    try:
        url = normalize_and_validate_domain_url(url)
    except ValueError as e:
        return None
    logo_url = web_scrape_logo(url)

    return logo_url

def is_relative_url(url: str) -> bool:
    parsed = urlparse(url)
    return not parsed.scheme and not parsed.netloc

def resolve_image_url(base_url: str, image_url: str) -> str:
    if is_relative_url(image_url):
        return urljoin(base_url, image_url)
    return image_url
