from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

from constants import GEMINI_2_FLASH_MODEL_ID
from prompts import SYSTEM_PROMPT_QUESTION, SYSTEM_PROMPT_SUMMARY
from tools import (
    choose_category,
    get_article,
    query_articles_list,
    query_recent_articles,
)


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


question_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_QUESTION,
    result_type=GeneralResponse,
    tools=[
        Tool(query_articles_list, takes_ctx=False),
        Tool(get_article, takes_ctx=False),
    ],
)

summary_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_SUMMARY,
    result_type=CategoryResponse,
    tools=[
        Tool(choose_category, takes_ctx=False),
        Tool(query_recent_articles, takes_ctx=False),
    ],
)
