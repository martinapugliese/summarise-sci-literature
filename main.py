import logging
import os
import sys

from src.agent import agent

logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logging.info("Starting the agent...")

    result1 = agent.run_sync(
        "What is the relation between context length and accuracy for large language models?"
    )

    print(result1)


if __name__ == "__main__":
    main()
