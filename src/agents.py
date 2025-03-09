import httpx
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool

from constants import GEMINI_2_FLASH_MODEL_ID
from prompts import (
    SYSTEM_PROMPT_ORCHESTRATOR,
    SYSTEM_PROMPT_QUESTION,
    SYSTEM_PROMPT_SUMMARY,
)
from tools import (
    choose_category,
    get_article,
    retrieve_recent_articles,
    search_articles,
)

# TODO remove useless pydntic models


class GeneralResponse(BaseModel):
    response: str = Field(description="The response to the query or question asked")
    article_list: list[str] = Field(
        description="The list of articles urls you used to answer to the question."
    )


class Category(BaseModel):
    category_id: str = Field(description="The category ID of the topic requested.")
    category_name: str = Field(description="The category name of the topic requested.")


class CategoryResponse(BaseModel):
    category_id: Category = Field(description="The category id of the topic requested.")
    category_name: Category = Field(
        description="The category name of the topic requested."
    )
    article_list: list[str] = Field(
        description="The list of articles responding to the request."
    )


class PaperInfo(BaseModel):
    title: str = Field(description="Title of the paper")
    summary: str = Field(description="Summary of the paper, in 3 lines")
    examples: list[str] = Field(
        description="Relevant examples aiding comprehension, taken from the paper, if there are."
    )
    topic: str = Field(description="Topic of the paper")


class PapersResponse(BaseModel):
    category_id: Category = Field(description="The category requested.")
    papers: list[PaperInfo] = Field(
        description="List of papers retrieved with all the info"
    )


class Context(BaseModel):
    # no input required
    pass


summary_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_SUMMARY,
    result_type=PapersResponse,
    tools=[
        Tool(choose_category, takes_ctx=False),
        Tool(retrieve_recent_articles, takes_ctx=False),
        Tool(get_article, takes_ctx=False),
    ],
)

question_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_QUESTION,
    result_type=GeneralResponse,
    tools=[
        Tool(search_articles, takes_ctx=False),
        Tool(get_article, takes_ctx=False),
    ],
)

orchestrator_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_ORCHESTRATOR,
    result_type=PapersResponse | GeneralResponse,
)


@orchestrator_agent.tool
async def summarise_latest_papers(ctx: RunContext[Context], prompt: str) -> list[str]:
    r = await summary_agent.run(prompt)
    return r


@orchestrator_agent.tool
async def answer_question(ctx: RunContext[Context], prompt: str) -> list[str]:
    r = await question_agent.run(prompt)
    return r
