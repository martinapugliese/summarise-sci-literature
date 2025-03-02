import logging
import os
import urllib.request as urllib_req
from io import BytesIO

import feedparser
import pandas as pd
import pymupdf
import requests

logger = logging.getLogger(__name__)


def query_articles_list(
    query: str = "cs.AI",
    sortby: str = "submittedDate",
    prefix: str = "cat",
    start: int = 0,
    max_results: int = 20,
):
    """
    Search articles on arvix according to the query value.
    It returns a markdown table with 20 articles and the following values:
    - pdf: the url to the article pdf
    - updated: the last time the article was updated
    - published: the date when the article was published
    - title: the article title
    - summary: a summary of the article content
    Args:
        query: the query used for the search
        sortby: how to sort the results. Possible values:
            - relevance (most relevant on the top)
            - lastUpdatedDate (most recently updated on the top)
            - submittedDate (most recently submitted on top)
        prefix: how to interpret the query. Possible values:
            - ti (saarch by title)
            - au (search by author)
            - abs (search in the abstracts)
            - co (search in the comments)
            - jr (search by journal reference)
            - cat (search by subject category)
            - rn (seach by report number)
            - all (use all the above)
        start: the index of the ranking where the table starts, add +20 to get the next table chunk
        max_results: the total number of papers to retrieve. Default value is 20.
    """

    base_url = "http://export.arxiv.org/api/query?"

    search_query = f"{prefix}:{query}"

    url = (
        f"{base_url}search_query={search_query}&start={start}&max_results={max_results}"
    )
    url += f"&sortBy={sortby}&sortOrder=descending"

    res = requests.get(url, timeout=360)

    if not res.ok:
        articles = "No Results"
    else:
        articles = feedparser.parse(res.content)["entries"]
        articles = pd.DataFrame(articles)[
            ["id", "updated", "published", "title", "summary"]
        ]
        articles.id = articles.id.apply(lambda s: s.replace("/abs/", "/pdf/"))
        articles = articles.to_markdown(index=False)

    markdown = f"""
---{query}-{sortby}----
{articles}
------------------------
    """

    return markdown


async def get_article(url: str) -> str:
    """
    Opens an article using its pdf url and reads its content.

    Args:
        url: the arxiv url on the article
    """

    res = requests.get(url, timeout=360)
    if not res.ok:
        article = "Not Found"

    else:
        bytes_stream = BytesIO(res.content)
        try:
            with pymupdf.open(stream=bytes_stream) as doc:
                article = chr(12).join([page.get_text() for page in doc])
        except pymupdf.FileDataError:
            article = "Not Found"

    article = f"""
-------{url}------------
{article}
------END----------------
    """

    return article


async def download_papers(paper_metadata, output_dir="pdfs"):
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
