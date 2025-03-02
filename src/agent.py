import logging
import sys
from inspect import cleandoc

from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

from constants import GEMINI_2_FLASH_MODEL_ID
from utils import get_article, query_articles_list

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = cleandoc(
    """
    You are an experienced reader of academic literature and
    an expert in distilling important findings in a way that is understandable and clear.
    """
)


class GeneralResponse(BaseModel):
    response: str = Field(description="The response to the query or question asked")
    article_list: list[str] = Field(
        description="The list of articles urls you used to answer to the question."
    )


PROMPT_TEMPLATE = cleandoc(
    """You are given a paper on AI.
    Answer the following question by search on axiv and looking at the articles information.
    If needed, access directly the articles you think are important to answer the question.
    Try to be smart in the way you query and access article and limit the number of article searches
    and article accesses.
    Be as concise as possible in the answer.

    This is the question:
    {question}
    """
)

agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT,
    result_type=GeneralResponse,
    tools=[
        Tool(query_articles_list, takes_ctx=False),
        Tool(get_article, takes_ctx=False),
    ],
)


def main():

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logging.info("Starting the agent...")

    result = agent.run_sync(
        PROMPT_TEMPLATE.format(
            question="What is the relation between context length and accuracy for large language models?"
        )
    )

    print(result)


if __name__ == "__main__":
    main()
