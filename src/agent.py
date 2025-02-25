from pydantic import BaseModel, Field
from pydantic_ai import Agent
from inspect import cleandoc

from constants import GEMINI_2_FLASH_MODEL_ID
from utils import get_latest_day_papers, download_papers, get_category_papers


SYSTEM_PROMPT = cleandoc(
    """
    You are an experienced reader of academic literature and
    an expert in distilling important findings in a way that is understandable and clear.
    """)


class PaperInfo(BaseModel):
    title: str = Field(description="Title of the paper")
    summary: str = Field(description="Summary of the paper, in 3 lines")
    examples: list[str] = Field(description="Relevant examples aiding comprehension, taken from the paper, if there are.")
    category: str = Field(description='Category of the paper')


prompt = cleandoc(
    """This is a paper on AI.
    Parse its title, summarise its results, extract examples and produce a category.
    For the summary, be concise and avoid obscure jargon.
    If there are valuable examples that aid understanding, report them in a nutshell.
    For the category, think about what the results refer to, e.g. cognitive science, medicine, foundational AI etc.
    """)


def main():

    # # retrieve latest day papers info
    # paper_metadata = get_latest_day_papers()

    # if paper_metadata is not None:

    #     # download papers locally
    #     download_papers(paper_metadata)

    #     # run the agent
    #     agent = Agent(  
    #         GEMINI_2_FLASH_MODEL_ID,
    #         system_prompt=SYSTEM_PROMPT,
    #         result_type=PaperInfo
    #     )

    #     result = agent.run_sync(prompt)
    #     print(result)

    #     return result

    content = get_category_papers('cs.AI')
    print(content)
                

if __name__ == "__main__":
    main()