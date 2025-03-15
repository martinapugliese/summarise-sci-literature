from typing import Literal

import httpx
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool

from constants import GEMINI_2_FLASH_MODEL_ID
from prompts import (
    PROMPT_QUESTION,
    SYSTEM_PROMPT_ORCHESTRATOR,
    SYSTEM_PROMPT_QUESTION,
    SYSTEM_PROMPT_SUMMARY,
)
from tools import choose_category, get_article, retrieve_recent_papers, search_papers

# TODO remove useless pydntic models


class QuestionAnswerResponse(BaseModel):
    response: str = Field(description="The response to the question")
    papers_list: list[str] = Field(
        description="The list of papers urls you used to answer to the question."
    )
    source: Literal["abstracts", "papers"] = Field(
        description="Whether you found the answer in the abstracts or in the whole papers."
    )


class Category(BaseModel):
    category_id: str = Field(description="The category ID of the topic requested.")
    category_name: str = Field(description="The category name of the topic requested.")


class CategoryResponse(BaseModel):
    category_id: Category = Field(description="The category id of the topic requested.")
    category_name: Category = Field(
        description="The category name of the topic requested."
    )
    PapersListResponse_list: list[str] = Field(
        description="The list of papers responding to the request."
    )


class PaperInfo(BaseModel):
    title: str = Field(description="Title of the paper")
    summary: str = Field(description="Summary of the paper, in 3 lines")
    examples: list[str] = Field(
        description="Relevant examples aiding comprehension, taken from the paper, if there are."
    )
    topic: str = Field(description="Topic of the paper")


class PapersListResponse(BaseModel):
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
    result_type=PapersListResponse,
    tools=[
        Tool(choose_category, takes_ctx=False),
        Tool(retrieve_recent_papers, takes_ctx=False),
        Tool(get_article, takes_ctx=False),
    ],
    model_settings={"max_tokens": 1000, "temperature": 0},
)

question_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_QUESTION,
    result_type=QuestionAnswerResponse,
    tools=[
        Tool(search_papers, takes_ctx=False),
        Tool(get_article, takes_ctx=False),
    ],
    model_settings={"max_tokens": 1000, "temperature": 0},
)

orchestrator_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_ORCHESTRATOR,
    result_type=PapersListResponse | QuestionAnswerResponse,
    model_settings={"max_tokens": 1000, "temperature": 0},
)


@orchestrator_agent.tool
async def summarise_latest_papers(ctx: RunContext[Context], request: str) -> list[str]:
    """
    Make a request to an agent about the most recent paper in a specific field.

    Args:
        ctx: the context
        request: the request
    """
    r = await summary_agent.run(request)
    return r


@orchestrator_agent.tool
async def answer_question(ctx: RunContext[Context], question: str) -> list[str]:
    """
    Ask an agent to search on Arxiv and access some papers to answer a question.

    Args:
        ctx: the context
        question: the question
    """

    prompt = PROMPT_QUESTION.format(question=question)
    r = await question_agent.run(prompt)
    return r
