from agents import orchestrator_agent, question_agent, summary_agent

# TMP - prmpt fpr summaries
# prompt = """Find the most recent papers about AI."""
prompt = """What are the most recent papers published about reinforcement learning?"""
# prompt = """What are the most recent papers published about neutrinos?"""

# TMP - prpmpt for questions
# prompt = """What is the relation between context length and accuracy for large language models?"""
# prompt = "How good is AI at playing chess?"
prompt = "Has anyone solved the Goldbach conjecture?"


def main():

    # result = summary_agent.run_sync(prompt)
    # result = question_agent.run_sync(prompt)
    result = orchestrator_agent.run_sync(prompt)
    print(result)

    return result


if __name__ == "__main__":
    main()
