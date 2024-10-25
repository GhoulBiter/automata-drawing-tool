import yaml
from logging_config import setup_logger
from generators import NFAGenerator


def load_nfa_data(filename="input.yaml"):
    with open(filename, "r") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Starting NFA generation process.")

    try:
        nfa_data = load_nfa_data()
        for nfa in nfa_data["nfas"]:
            generator = NFAGenerator(nfa, logger)
            generator.create_graph()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    logger.info("NFA generation process completed.")
