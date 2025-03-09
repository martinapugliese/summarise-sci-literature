from agents import question_agent, summary_agent

prompt = """Find the most recent papers about AI."""
prompt = """What are the most recent papers published about reinforcement learning?"""
prompt = """What are the most recent papers published about the neutrinos?"""
prompt = """What is the relation betweene context length and accuracy for large language models?"""


def main():

    result = summary_agent.run_sync(prompt)
    # result = question_agent.run_sync(prompt)
    print(result)

    return result


if __name__ == "__main__":
    main()
