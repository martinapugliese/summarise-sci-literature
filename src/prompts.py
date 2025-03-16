from inspect import cleandoc

GENERAL_SYSTEM_PROMPT = cleandoc(
    """
    You are an expert in understanding academic topics, using the arXiv API
    and distilling key information from papers in a way that is understandable and clear.
    """
)

SYSTEM_PROMPT_ORCHESTRATOR = cleandoc(
    """
   You are an orchestrator agent, you choose the best agent to delegate a request to
   based on its nature.

   * When receiving a request about summarising the latest papers,
   use the "summarise_latest_papers" tool;
   * When the request is about searching for papers based on a question,
   use the question as an argument for the "answer_question" tool and wait for its response.
    """
)

USER_PROMPT_SUMMARY_TEMPLATE = cleandoc(
    """
    Given the following request:
    '{request}'

    Answer it by first finding the best matching arXiv category for the request
    and then retrieving the most recent papers published in that category.

    After that, read the content of each paper.

    For each paper, return its title, a summary of the key findings, some examples
    (if present in the text and relevant to aid understanding) and a topic.

    For the summary, be concise and avoid obscure jargon.

    If there are valuable examples that aid understanding, report them in a nutshell.
    For the topic, think about what the results refer to,
    e.g. cognitive science, medicine, foundational AI etc.
    """
)

# USER_PROMPT_QUESTION = cleandoc(
#     """
#     Given this question:
#     '{question}'

#     Answer it by first performing the most relevant search via the arXiv API and
#     reading the abstracts of the papers found.

#     If the some (or all) the abstracts respond to the question, return the answer.
#     Otherwise, select only the most promising papers from the list access
#     and their whole content to search for the answer within.

#     Quote the papers you used to answer.

#     If you don't find the answer, say you did not find relevant information
#     and terminate your generation.

#     **Do not try to answer the question yourself.**

#     **Always privilege looking for an answer in the abstracts if possible,
#     do not read the whole papers' content unless necessary.**
#     """
# )


USER_PROMPT_QUESTION_TEMPLATE = cleandoc(
    """
    Answer the following question or request:

    '{question}'

    Follow these steps when creating the answer:
    1. Use the search_papers tool multiple times to collect a list of relevant papers.
    Perform as many searches as you need; you will not be allowed to search further after this step.
    2. Generate an answer reading the paper abstract.
        - End the process here if the answer is exahstive.
        - End the process if none of the papers answer the question/request.
    3. If you need more specific information, access up to 5 papers with the get_article tool.
    4. Refine the answer question with the paper information you collected.
    5. State if you have not found any relevant information or the information you have found is not exhaustive.
    6. End the process without searching further.
    """
)
