import asyncio
import time

import nest_asyncio
from pydantic_ai.usage import UsageLimits

from agents import orchestrator_agent, question_agent, summary_agent

nest_asyncio.apply()  # Allows nesting of event loops

# THIS IS ONLY FOR LOCAL TESTING

question_list = [
    "Find the most recent articles about AI",
    "What are the most recent articles published about reinforcement learning?",
    "What are the most recent articles published about neutrinos?",
    "What is reinforcement learning?",
    "What is the relation between context length and accuracy for large language models?",
    "How good is AI at playing chess?",
    "Has anyone solved the Goldbach conjecture?",
    "Tell me about the needle-in-a-haystack method to investigate capabilities of LLMs",
    "Is Gemini better than other LLMs?",
    "what happens when you account for electron interference in Josephson junctions?",
]


async def main():

    for question in question_list:

        print("|-------------------------|")
        print("Question:", question)

        result = await orchestrator_agent.run(
            question,
            usage_limits=UsageLimits(request_limit=20),  # limit to 10 requests
        )
        print(result)
        time.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
