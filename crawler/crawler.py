import requests

from bs4 import BeautifulSoup

from urllib.parse import (
    urljoin,
    urlparse
)


def extract_page_data(url):

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

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "Missing"
        )

        meta_tag = soup.find(
            "meta",
            attrs={
                "name": "description"
            }
        )

        meta_description = (
            meta_tag.get("content")
            if meta_tag
            else "Missing"
        )

        h1_tag = soup.find("h1")

        h1_text = (
            h1_tag.get_text(strip=True)
            if h1_tag
            else "Missing"
        )

        page_data = {
            "url": url,
            "status_code": response.status_code,
            "title": title,
            "meta_description": meta_description,
            "h1": h1_text
        }

        return page_data, soup

    except Exception as e:

        return {
            "url": url,
            "status_code": "Error",
            "title": str(e),
            "meta_description": "-",
            "h1": "-"
        }, None


def crawl_website(
    start_url,
    max_pages=20
):

    queue = [start_url]

    visited = set()

    results = []

    root_domain = urlparse(
        start_url
    ).netloc

    while queue and len(visited) < max_pages:

        current_url = queue.pop(0)

        if current_url in visited:
            continue

        page_data, soup = extract_page_data(
            current_url
        )

        results.append(page_data)

        visited.add(current_url)

        if not soup:
            continue

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link["href"]

            full_url = urljoin(
                current_url,
                href
            )

            parsed = urlparse(
                full_url
            )

            if parsed.netloc != root_domain:
                continue

            clean_url = (
                parsed.scheme
                + "://"
                + parsed.netloc
                + parsed.path
            )

            if (
                clean_url not in visited
                and clean_url not in queue
            ):
                queue.append(
                    clean_url
                )

    return results