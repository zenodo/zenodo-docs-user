import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pagefind.index import IndexConfig, PagefindIndex

BASE_URL = "https://support.zenodo.org/help/"
CACHE_FILENAME = ".zammad-cache.json"


def fetch(url):
    time.sleep(0.5)
    content = requests.get(url).text
    return BeautifulSoup(content, "html.parser")


def scrape_zammad_answer(url, answers):
    print(f"Scraping answer: {url}")
    soup = fetch(url)

    soup_body = soup.select_one("main article .container")
    # Setting the attribute to `None` is the way to have the attribute added but without a value.
    soup_body["data-pagefind-body"] = None

    answer_soup_meta = soup_body.select_one(".article-meta")
    answer_soup_meta["data-pagefind-ignore"] = None

    answers.append(
        {
            "content": str(soup),
            "url": url,
        }
    )


def scrape_zammad_category(url, answers):
    print(f"Scraping category: {url}")
    soup = fetch(url)

    for category_link in soup.select(".sections--grid li.section a"):
        category_url = urljoin(BASE_URL, category_link["href"])
        scrape_zammad_category(category_url, answers)

    for answer_link in soup.select(".sections--list li.section a"):
        answer_url = urljoin(BASE_URL, answer_link["href"])
        scrape_zammad_answer(answer_url, answers)


def scrape_zammad():
    cache_path = Path(CACHE_FILENAME)
    if (
        cache_path.is_file()
        and datetime.fromtimestamp(cache_path.stat().st_mtime).date()
        == datetime.today().date()
    ):
        print("Using cache file modified today...")
        answers = json.loads(cache_path.read_text())
    else:
        answers = []
        scrape_zammad_category(BASE_URL, answers)
        cache_path.write_text(json.dumps(answers))
    return answers


async def main(path):
    print("Scraping...")
    zammad_answers = scrape_zammad()

    print("Indexing...")
    config = IndexConfig(
        output_path=os.path.join(path, "pagefind"),
        force_language="en",
    )
    async with PagefindIndex(config=config) as index:
        # Index the output of the static site.
        tasks = [index.add_directory(path)]

        # Index the Zammad answers.
        for answer in zammad_answers:
            tasks.append(
                index.add_html_file(
                    content=answer["content"],
                    url=answer["url"],
                )
            )

        await asyncio.gather(*tasks)

    print("Done")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pagefind_index.py path")
        sys.exit(1)

    path = sys.argv[1]

    asyncio.run(main(path))
