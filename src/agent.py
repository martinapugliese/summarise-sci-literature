import logging
import os
import sys
from inspect import cleandoc

import pymupdf
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from constants import GEMINI_2_FLASH_MODEL_ID
from utils import download_papers, get_category_paper_pdf_links

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = cleandoc(
    """
    You are an experienced reader of academic literature and
    an expert in distilling important findings in a way that is understandable and clear.
    """
)


class PaperInfo(BaseModel):
    title: str = Field(description="Title of the paper")
    summary: str = Field(description="Summary of the paper, in 3 lines")
    examples: list[str] = Field(
        description="Relevant examples aiding comprehension, taken from the paper, if there are."
    )
    category: str = Field(description="Category of the paper")


PROMPT_TEMPLATE = cleandoc(
    """You are given a paper on AI.
    Parse its title, summarise its results, extract examples and produce a category.
    For the summary, be concise and avoid obscure jargon.
    If there are valuable examples that aid understanding, report them in a nutshell.
    For the category, think about what the results refer to, e.g. cognitive science, medicine, foundational AI etc.

    This is the paper text:
    {text}
    """
)

import json


def main():

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logging.info("Starting the agent...")

    # get latest max_results in category
    papers = get_category_paper_pdf_links(max_results=300)

    # download papers
    download_papers(papers)

    # read each paper and send to agent
    # TODO use papers data above instead
    for fn in os.listdir("pdfs"):

        paper_id = fn.split(".pdf")[0]
        logging.info(f"Processing paper {paper_id}...")

        # read text content of PDF
        pdf_path = f"pdfs/{paper_id}.pdf"
        pdf = pymupdf.open(pdf_path)
        text = ""
        for page in pdf:
            text += page.get_text()
        pdf.close()

        prompt = PROMPT_TEMPLATE.format(text=text)

        # run the agent
        agent = Agent(
            GEMINI_2_FLASH_MODEL_ID, system_prompt=SYSTEM_PROMPT, result_type=PaperInfo
        )

        result = agent.run_sync(prompt)
        print(result)  # TODO build file from this data


if __name__ == "__main__":
    main()
