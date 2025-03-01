import os
import re
import urllib.request as urllib_req

import requests
from bs4 import BeautifulSoup


def get_category_papers(arxiv_category):
    """
    Get papers from a chosen ArXiv category by querying the ArXiv API.
    Input: ArXiv category (e.g. "cs.AI")
    Output: API response content
    """

    base_url = "http://export.arxiv.org/api/query?"

    # Search parameters
    search_query = f"cat:{arxiv_category}"
    start = 0
    max_results = 5

    r = requests.get(
        f"{base_url}search_query={search_query}&start={start}&max_results={max_results}"
    )

    return r.content


def get_latest_day_papers(arxiv_category="cs.AI"):
    """
    Parse ArXiv page for latest day's papers for a chosen ArXiv category.
    Input: ArXiv category (default "cs.AI")
    Output: dictionary {paper_id: paper_url}
    """

    # URL for all papers in the category
    webpage = f"https://arxiv.org/list/{arxiv_category}/recent?skip=0&show=2000"

    r = requests.get(webpage)
    if r.status_code != 200:
        return

    # initialise parser
    soup = BeautifulSoup(r.content, "html.parser")

    # pick most recent day info
    latest_day_str = soup.find_all("h3")[0].text
    day = latest_day_str.split("(")[0]

    # and the total number of entries for that day
    match = re.search(r"of \d+ entries", latest_day_str)
    if match:
        n_entries = int(match.group().split(" ")[1])
        print(day, " - ", n_entries, "papers")
    else:
        print("Failed to isolate latest day's info")

    # find the URLs to these papers for the latest day only (up to n_entries)
    paper_links = soup.find_all("a", {"title": "Download PDF"})[:n_entries]

    # extract paper IDs and URLs
    paper_ids, paper_urls = [], []
    for link in paper_links:
        paper_url = "https://arxiv.org" + link["href"]
        paper_id = link["href"].split("/")[-1].split("v")[0]  # Extract the ID
        paper_ids.append(paper_id)
        paper_urls.append(paper_url)

    # find all titles, which follow the same order
    paper_title_divs = soup.find_all("div", {"class": "list-title mathjax"})[:n_entries]

    paper_titles = []
    for title_div in paper_title_divs:
        paper_titles.append(title_div.contents[1].split("\n")[1].lstrip())

    # create json linking ID and URL
    paper_metadata = {paper_ids[i]: paper_urls[i] for i in range(len(paper_ids))}

    return paper_metadata


def download_papers(paper_metadata, output_dir="pdfs"):
    """
    Given a dict of paper IDs and URLs, download them locally.
    """

    # if output directory exists, delete it with all content
    if os.path.exists(output_dir):
        os.system(f"rm -rf {output_dir}")
    os.makedirs(output_dir)

    i = 0
    for id_, url_ in paper_metadata.items():
        try:
            urllib_req.urlretrieve(url_, f"{output_dir}/{id_}.pdf")
        except Exception as e:
            print(f"Failed to download {id_} due to {e}")
            continue
        i += 1
        if i % 10 == 0:
            print(f"Downloaded {i} papers")

    print(f"Downloaded {len(paper_metadata)} papers to {output_dir}")

    return
