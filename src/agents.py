from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool

from constants import GEMINI_2_FLASH_MODEL_ID
from prompts import (
    SYSTEM_PROMPT_ABSTRACTS,
    SYSTEM_PROMPT_ORCHESTRATOR_QUESTION,
    SYSTEM_PROMPT_PAPERS,
)
from tools import (
    choose_category,
    get_articles,
    retrieve_recent_articles,
    search_articles_new,
)


class GeneralResponse(BaseModel):
    response: str = Field(description="The response to the query or question asked")
    article_list: list[str] = Field(
        description="The list of articles urls you used to answer to the question."
    )


class GeneralQuestionResponse(BaseModel):
    response: str = Field(description="The response to the question asked")
    query_string: str = Field(
        description="The query string used to search for the articles in the API"
    )
    found_relevant_info: bool = Field(
        description="Whether you found relevant information or not"
    )
    reason: str = Field(
        description="The reason why you found relevant information or not"
    )
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


# summary_agent = Agent(
#     GEMINI_2_FLASH_MODEL_ID,
#     system_prompt=SYSTEM_PROMPT_SUMMARY,
#     result_type=PapersResponse,
#     tools=[
#         Tool(choose_category, takes_ctx=False),
#         Tool(retrieve_recent_articles, takes_ctx=False),
#         Tool(get_article, takes_ctx=False),
#     ],
# )

# abstract_researcher_agent = Agent(
#     GEMINI_2_FLASH_MODEL_ID,
#     system_prompt=SYSTEM_PROMPT_GENERAL_QUESTION,
#     model_settings={"max_tokens": 200, "temperature": 0},
#     result_type=GeneralQuestionResponse,
#     tools=[Tool(search_articles, takes_ctx=False)],
# )

# deeper_agent = Agent(
#     GEMINI_2_FLASH_MODEL_ID,
#     system_prompt=SYSTEM_PROMPT_QUESTION,
#     model_settings={"max_tokens": 200, "temperature": 0},
#     result_type=GeneralResponse,
#     tools=[
#         Tool(search_articles, takes_ctx=False),
#         Tool(get_article, takes_ctx=False),
#     ],
# )

# orchestrator_agent = Agent(
#     GEMINI_2_FLASH_MODEL_ID,
#     system_prompt=SYSTEM_PROMPT_ORCHESTRATOR,
#     model_settings={"max_tokens": 200, "temperature": 0},
#     result_type=PapersResponse | GeneralResponse,
# )


# @orchestrator_agent.tool
# async def summarise_latest_papers(ctx: RunContext[Context], prompt: str) -> list[str]:
#     r = await summary_agent.run(prompt)
#     return r


# @orchestrator_agent.tool
# async def answer_question(ctx: RunContext[Context], prompt: str) -> list[str]:
#     r = await deeper_agent.run(prompt)
#     return r


class Answer(BaseModel):
    question: str = Field(description="The question asked")
    answer: str = Field(description="The answer to question", default=None)
    source: Literal["abstracts", "papers"] = Field(
        description="The source of the answer, either abstracts or papers", default=None
    )
    api_query: str = Field(
        description="The query string used to search for papers via the arXiv API",
        default=None,
    )
    article_urls: list[str] = Field(
        description="The list of papers URLs whose abstract you used to answer to the question.",
        default=[],
    )


question_orchestrator_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_ORCHESTRATOR_QUESTION,
    model_settings={"max_tokens": 1000, "temperature": 0},
    result_type=Answer,
)


abstract_researcher_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_ABSTRACTS,
    model_settings={"max_tokens": 200, "temperature": 0},
    result_type=Answer,
    tools=[Tool(search_articles_new, takes_ctx=False)],
)

paper_researcher_agent = Agent(
    GEMINI_2_FLASH_MODEL_ID,
    system_prompt=SYSTEM_PROMPT_PAPERS,
    model_settings={"max_tokens": 200, "temperature": 0},
    result_type=Answer,
    tools=[
        Tool(get_articles, takes_ctx=False),
    ],
)


@question_orchestrator_agent.tool
async def get_response_from_abstracts(
    ctx: RunContext[Context], prompt: str
) -> list[str]:
    r = await abstract_researcher_agent.run(prompt)
    return r


@question_orchestrator_agent.tool
async def gen_response_from_papers(ctx: RunContext[Context], prompt: str) -> list[str]:
    r = await paper_researcher_agent.run(prompt)
    return r
