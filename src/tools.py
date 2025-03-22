import logging
import time
from io import BytesIO

import feedparser
import pandas as pd
import pymupdf
import requests

from utils import get_arxiv_categories

logger = logging.getLogger(__name__)


def choose_category(topic: str):
    categories = get_arxiv_categories()

    return categories


def identify_latest_day(category: str = "cs.AI"):
    """
    Identify the latest day available on the arXiv API in the given category
    """

    base_url = "http://export.arxiv.org/api/query?"

    search_query = f"cat:{category}"
    url = f"{base_url}search_query={search_query}&start=0&max_results=1"
    url += f"&sortBy=submittedDate&sortOrder=descending"

    print("*** DAY url:", url)

    res = requests.get(url, timeout=360)
    if not res.ok:
        latest_day = "Not Found"
    else:
        # remove the time part
        latest_day = feedparser.parse(res.content)["entries"][0]["published"].split(
            "T"
        )[0]

    print("*** latest day:", latest_day)

    return latest_day


def search_papers(
    query: str = "cs.AI",
    sortby: str = "submittedDate",
    prefix: str = "cat",
    start: int = 0,
    max_results: int = 20,
):
    """
    Search papers on arXiv according to the query value.
    It returns a markdown table with 20 papers and the following values:
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

    # TODO not sure this uses anything more than cat search

    time.sleep(0.5)

    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"{prefix}:{query}"

    # TODO this can keep searching forever, handle this
    url = (
        f"{base_url}search_query={search_query}&start={start}&max_results={max_results}"
    )
    url += f"&sortBy={sortby}&sortOrder=descending"
    print("*** url:", url)

    res = requests.get(url, timeout=360)
    if not res.ok:
        papers = "No Results"
    else:
        papers = feedparser.parse(res.content)["entries"]
        papers = pd.DataFrame(papers)[
            ["id", "updated", "published", "title", "summary"]
        ]
        papers = papers.rename(columns={"summary": "abstract"})
        papers.id = papers.id.apply(lambda s: s.replace("/abs/", "/pdf/"))
        papers = papers.to_markdown(index=False)

    markdown = f"""
        ---{query}-{sortby}----
        {papers}
        ------------------------
    """

    return markdown


def retrieve_recent_papers(
    category: str = "cs.AI",
    latest_day: str = "2022-01-01",
):
    base_url = "http://export.arxiv.org/api/query?"

    search_query = f"cat:{category}"
    url = f"{base_url}search_query={search_query}&start=0&max_results=300"
    url += f"&sortBy=submittedDate&sortOrder=descending"
    print("*** url:", url)

    response = requests.get(url, timeout=360)
    if not response.ok:
        df_papers = pd.DataFrame()  # no results, TODO needs to be handled
    else:
        papers_list = feedparser.parse(response.content)["entries"]
        df_papers = pd.DataFrame(papers_list)[
            ["id", "published", "title", "summary"]
        ]  # cols are from the Atom feed
        df_papers = df_papers.rename(columns={"summary": "abstract"})

    # remove time part from published and cut to latest day (string)
    df_papers["published"] = df_papers["published"].apply(lambda s: s.split("T")[0])
    df_papers = df_papers[df_papers["published"] == latest_day]

    return df_papers.to_markdown(index=False)


async def get_article(url: str) -> str:
    """
    Opens an article using its URL (PDF version) and returns its text content.
    Args:
        url: the article arXiv URL
    """

    print("**** article url:", url)

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
