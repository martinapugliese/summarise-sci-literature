from inspect import cleandoc

from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

from .constants import GEMINI_2_FLASH_MODEL_ID
from .utils import get_article, query_articles_list


class GeneralResponse(BaseModel):
    response: str = Field(description="The response to the query or question asked")
    article_list: list[str] = Field(
        description="The list of articles urls you used to answer to the question."
    )


SYSTEM_PROMPT = cleandoc(
    """
    You are an experienced reader of academic literature and
    an expert in distilling important findings in a way that is understandable and clear.

    Answer any question by searching on axiv and looking at the articles information.
    If needed, access directly the articles you think are important to answer the question.
    Try to be smart in the way you query and access article and limit the number of article searches
    and article accesses.

    Quote the articles you used to answer.
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
