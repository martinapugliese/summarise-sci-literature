from pydantic_ai.usage import UsageLimits

from agents import orchestrator_agent, question_agent, summary_agent

# THIS IS ONLY FOR LOCAL TESTING

# TMP - prmpt fpr summaries
question = """Find the most recent papers about AI"""
# question = """What are the most recent papers published about reinforcement learning?"""
# question = """What are the most recent papers published about neutrinos?"""

# TMP - prpmpt for questions
# question= """What is the relation between context length and accuracy for large language models?"""
# prompt = "How good is AI at playing chess?"
# prompt = "Has anyone solved the Goldbach conjecture?"
# prompt = "What is reinforcement learning?"
# question = "Tell me about the needle-in-a-haystack method to investigate capabilities of LLMs"
question = "Is Gemini better than other LLMs?"


def main():

    # result = summary_agent.run_sync(prompt)
    # result = question_agent.run_sync(prompt)
    result = orchestrator_agent.run_sync(
        question,
        usage_limits=UsageLimits(request_limit=10),  # limit to 10 requests
    )
    print(result)
    # print(result.all_messages())   # doesn't look like you can print the messages one at a time, only at the end

    return result


if __name__ == "__main__":
    main()
