import logging
import os
import re
import urllib.request as urllib_req
from datetime import datetime

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_category_paper_pdf_links(arxiv_category="cs.AI", max_results=2000):
    """
    Get papers from a chosen ArXiv category by querying the ArXiv API.
    Input:
        - ArXiv category (default "cs.AI")
        - max number of results (default 2000 which is the max in pagination)
    Output: API response content
    """

    base_url = "http://export.arxiv.org/api/query?"

    search_query = f"cat:{arxiv_category}"
    start = 0

    url = (
        f"{base_url}search_query={search_query}&start={start}&max_results={max_results}"
    )
    url += f"&sortBy=submittedDate&sortOrder=descending"
    papers = feedparser.parse(requests.get(url).content)["entries"]

    # you can take link from "links" key but this is less cumbersome
    paper_metadata = {
        paper["id"].split("/")[-1]: paper["link"].replace("abs", "pdf")
        for paper in papers
    }

    return paper_metadata


def download_papers(paper_metadata, output_dir="pdfs"):
    """
    Given a dict of paper IDs and URLs, download them locally.
    """

    os.makedirs(output_dir, exist_ok=True)

    i = 0
    for id_, url_ in paper_metadata.items():
        try:
            urllib_req.urlretrieve(url_, f"{output_dir}/{id_}.pdf")
        except Exception as e:
            logging.error(f"Failed to download {id_} due to {e}")
            continue
        i += 1
        if i % 10 == 0:
            logging.info(f"Downloaded {i} papers")

    logging.info(f"Downloaded {len(paper_metadata)} papers to folder {output_dir}/")

    return
