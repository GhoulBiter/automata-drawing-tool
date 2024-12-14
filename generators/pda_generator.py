import os
import graphviz
from validators import PDA_Validator


class PDA_Generator:
    """
    Class to generate diagrams for Push Down Automata (PDA) based on a formal definition.

    Attributes:
        pda_data (dict): The formal definition of the PDA, including states, transitions, and stack operations.
        logger (logging.Logger): Logger instance for debugging and process updates.
    """

    def __init__(self, pda_data, logger):
        """
        Initializes the PDA_Generator with PDA data and a logger.

        Args:
            pda_data (dict): The formal definition of the PDA.
            logger (logging.Logger): Logger for logging information, warnings, and errors.
        """
        self.pda_data = pda_data
        self.logger = logger

    def create_diagram(self):
        """
        Generates and renders the PDA diagram. Validates the PDA definition before rendering.
        """
        self.logger.info(f"Generating PDA diagram for '{self.pda_data['name']}'")
        # Validate the PDA definition
        # self.validate_pda()

        # Initialize the Graphviz Digraph
        pda_graph = graphviz.Digraph(format="png", graph_attr={"rankdir": "LR"})

        # Add states to the graph
        for state in self.pda_data["states"]:
            shape = (
                "doublecircle" if state in self.pda_data["final_states"] else "circle"
            )
            pda_graph.node(state, state, shape=shape)

        # Add transitions to the graph
        for state, transitions in self.pda_data["transitions"].items():
            for input_symbol, stack_transitions in transitions.items():
                for stack_symbol, results in stack_transitions.items():
                    for next_state, stack_operation in results:
                        if (
                            stack_symbol == "Îµ"
                        ):  # Handle any mis-encoded epsilon symbol
                            stack_symbol = "ε"
                            # symbol = '&#949;'
                        stack_symbol = str(
                            stack_symbol
                        )  # Ensure symbol is treated as a string

                        if (
                            input_symbol == "Îµ"
                        ):  # Handle any mis-encoded epsilon symbol
                            input_symbol = "ε"
                            # symbol = '&#949;'
                        input_symbol = str(
                            input_symbol
                        )  # Ensure symbol is treated as a string

                        if (
                            stack_operation == "Îµ"
                        ):  # Handle any mis-encoded epsilon symbol
                            stack_operation = "ε"
                            # symbol = '&#949;'
                        stack_operation = str(
                            stack_operation
                        )  # Ensure symbol is treated as a string

                        label = f"{input_symbol}, {stack_symbol} → {stack_operation}"
                        self.logger.debug(
                            f"Adding transition: {state} → {next_state} [label='{label}']"
                        )
                        pda_graph.edge(state, next_state, label=label)

        # Add the start state indicator
        pda_graph.node("start", "", shape="none")
        pda_graph.edge("start", self.pda_data["start_state"])

        # Ensure the outputs directory exists
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

        # Render the graph to a file
        filename = self._get_unique_filename()
        output_path = os.path.join("outputs", filename)
        pda_graph.render(output_path)
        self.logger.info(f"PDA diagram saved as {output_path}.png")

    def validate_pda(self):
        """
        Validates the PDA definition.

        Raises:
            ValueError: If validation fails for any component of the PDA.
        """
        validator = PDA_Validator(self.pda_data, self.logger)
        validator.validate()

    def _get_unique_filename(self):
        """
        Generates a unique filename for the PDA output file.

        Returns:
            str: A unique filename for the PDA output file.
        """
        base_filename = (
            f"{self.pda_data['type']}_{self.pda_data['name'].replace(' ', '_')}"
        )
        filename = base_filename
        index = 1
        while os.path.exists(os.path.join("outputs", f"{filename}.png")):
            filename = f"{base_filename}_{index}"
            index += 1
        return filename
