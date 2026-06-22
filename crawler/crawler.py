import requests
from bs4 import BeautifulSoup


def crawl_page(url):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        title = soup.title.string.strip() if soup.title else "Missing"

        meta_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        meta_description = (
            meta_tag.get("content")
            if meta_tag
            else "Missing"
        )

        h1 = soup.find("h1")

        h1_text = (
            h1.get_text(strip=True)
            if h1
            else "Missing"
        )

        return {
            "url": url,
            "status_code": response.status_code,
            "title": title,
            "meta_description": meta_description,
            "h1": h1_text
        }

    except Exception as e:

        return {
            "url": url,
            "status_code": "Error",
            "title": str(e),
            "meta_description": "-",
            "h1": "-"
        }