import yaml
from logging_config import setup_logger
from generators import NFA_Generator, PDA_Generator


def load_automata_data(filename="input.yaml"):
    """
    Loads automata data (NFAs and PDAs) from the specified YAML file.

    Args:
        filename (str): The path to the YAML file.

    Returns:
        dict: Parsed YAML data containing NFAs and/or PDAs.
    """
    with open(filename, "r") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Starting automaton generation process.")

    try:
        automata_data = load_automata_data()

        # Generate NFAs
        if "nfas" in automata_data:
            logger.info("Processing NFAs...")
            for nfa in automata_data["nfas"]:
                try:
                    generator = NFA_Generator(nfa, logger)
                    generator.create_graph()
                except Exception as e:
                    logger.error(f"Error generating NFA '{nfa['name']}': {str(e)}")

        # Generate PDAs
        if "pdas" in automata_data:
            logger.info("Processing PDAs...")
            for pda in automata_data["pdas"]:
                try:
                    generator = PDA_Generator(pda, logger)
                    generator.create_diagram()
                except Exception as e:
                    logger.error(f"Error generating PDA '{pda['name']}': {str(e)}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

    logger.info("Automaton generation process completed.")
