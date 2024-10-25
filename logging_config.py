import logging


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(
                "nfa_generation.log", encoding="utf-8"
            ),  # Set encoding to UTF-8 for file output
            logging.StreamHandler(),  # Console output
        ],
    )
    return logging.getLogger(__name__)
