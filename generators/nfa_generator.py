import graphviz
import os
from validators import (
    validate_nfa_structure,
    validate_nfa_states,
    validate_transitions,
    validate_nfa_symbols,
)


class NFAGenerator:
    """
    NFAGenerator is responsible for creating and rendering NFAs using Graphviz.

    Attributes:
        nfa_data (dict): A dictionary containing the NFA's structure and transitions.
        logger (logging.Logger): A logger instance for logging actions and events.
    """

    def __init__(self, nfa_data, logger):
        """
        Initializes NFAGenerator with the NFA data and a logger.

        Args:
            nfa_data (dict): The structure of the NFA including states, transitions, and alphabet.
            logger (logging.Logger): Logger for logging information, warnings, and errors.
        """
        self.nfa_data = nfa_data
        self.logger = logger

    def create_graph(self):
        """
        Creates and renders the NFA graph in landscape orientation. Validates the NFA structure
        before rendering and saves the output file in the 'outputs' directory.
        """
        self.validate_nfa()

        # Create a Graphviz Digraph with landscape orientation
        nfa_graph = graphviz.Digraph(format="png", graph_attr={"rankdir": "LR"})

        # Add nodes (states)
        for state in self.nfa_data["states"]:
            shape = (
                "doublecircle" if state in self.nfa_data["final_states"] else "circle"
            )
            nfa_graph.node(state, state, shape=shape)

        # Add transitions
        for state, transitions_dict in self.nfa_data["transitions"].items():
            for symbol, next_states in transitions_dict.items():
                if symbol == "Îµ":  # Handle any misencoded epsilon symbol
                    symbol = "ε"
                    # symbol = '&#949;'
                symbol = str(symbol)  # Ensure symbol is treated as a string
                for next_state in next_states:
                    self.logger.debug(
                        f"Adding transition from '{state}' to '{next_state}' on symbol '{symbol}'"
                    )
                    nfa_graph.edge(state, next_state, label=symbol)

        # Start state
        nfa_graph.node("start", "", shape="none")
        nfa_graph.edge("start", self.nfa_data["start_state"])

        # Ensure outputs directory exists
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

        # Save the graph
        filename = self._get_unique_filename()
        output_path = os.path.join("outputs", filename)
        nfa_graph.render(output_path)
        self.logger.info(f"Graph saved as {output_path}.png")

    def validate_nfa(self):
        """
        Validates the NFA structure, states, transitions, and symbols.

        Raises:
            ValueError: If validation fails for any component of the NFA.
        """
        validate_nfa_structure(self.nfa_data, self.logger)
        validate_nfa_states(self.nfa_data, self.logger)
        validate_transitions(self.nfa_data, self.logger)
        validate_nfa_symbols(self.nfa_data, self.logger)

    def _get_unique_filename(self):
        """
        Generates a unique filename for the output file by appending an index if needed.

        Returns:
            str: A unique filename for the NFA output file.
        """
        index = 1
        base_filename = (
            f"{self.nfa_data['type']}_{self.nfa_data['name'].replace(' ', '_')}"
        )
        filename = base_filename
        while os.path.exists(os.path.join("outputs", f"{filename}.png")):
            filename = f"{base_filename}_{index}"
            index += 1
        return filename
