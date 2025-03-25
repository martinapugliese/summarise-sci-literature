from pydantic_ai.usage import UsageLimits

from agents import orchestrator_agent, question_agent, summary_agent

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


def main():
    import time

    # result = summary_agent.run_sync(prompt)
    # result = question_agent.run_sync(prompt)
    for question in question_list:

        print("|-------------------------|")
        print("Question:", question)

        result = orchestrator_agent.run_sync(
            question,
            usage_limits=UsageLimits(request_limit=20),  # limit to 10 requests
        )
        print(result)
        time.sleep(15)

    # print(result.all_messages())   # doesn't look like you can print the messages one at a time, only at the end

    return result


if __name__ == "__main__":
    main()
