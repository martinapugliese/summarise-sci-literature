from pydantic_ai.usage import UsageLimits

from agents import orchestrator_agent, question_agent, summary_agent

# THIS IS ONLY FOR LOCAL TESTING

# TMP - prmpt fpr summaries
question = """Find the most recent papers about AI"""
# question = """What are the most recent papers published about reinforcement learning?"""
# question = """What are the most recent papers published about neutrinos?"""

# TMP - prpmpt for questions
# question= """What is the relation between context length and accuracy for large language models?"""
# question = "How good is AI at playing chess?"
question = "Has anyone solved the Goldbach conjecture?"
# question = "What is reinforcement learning?"
# question = "Tell me about the needle-in-a-haystack method to investigate capabilities of LLMs"
# question = "Is Gemini better than other LLMs?"
# question="what happens when you account for electron interference in Josephson junctions?"

question_list = [
    "What is reinforcement learning?",
    "What is the relation between context length and accuracy for large language models?",
    "How good is AI at playing chess?",
    "Has anyone solved the Goldbach conjecture?",
    "Tell me about the needle-in-a-haystack method to investigate capabilities of LLMs",
    "Is Gemini better than other LLMs?",
    "what happens when you account for electron interference in Josephson junctions?",
]


def main():
    import time

    # result = summary_agent.run_sync(prompt)
    # result = question_agent.run_sync(prompt)
    for question in question_list:
        result = orchestrator_agent.run_sync(
            question,
            usage_limits=UsageLimits(request_limit=20),  # limit to 10 requests
        )
        print(result)
        time.sleep(60)

    # print(result.all_messages())   # doesn't look like you can print the messages one at a time, only at the end

    return result


if __name__ == "__main__":
    main()
