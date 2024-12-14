class PDA_Validator:
    """
    Class to validate the structure and transitions of a Push Down Automaton (PDA).

    Attributes:
        pda_data (dict): The formal definition of the PDA.
        logger (logging.Logger): Logger instance for debugging and error messages.
    """

    def __init__(self, pda_data, logger):
        """
        Initializes the PDA_Validator with PDA data and a logger.

        Args:
            pda_data (dict): The formal definition of the PDA.
            logger (logging.Logger): Logger instance for logging validation details.
        """
        self.pda_data = pda_data
        self.logger = logger

    def validate(self):
        """
        Validates the PDA structure and transitions.

        Raises:
            ValueError: If the PDA definition is invalid.
        """
        self.logger.info(f"Validating PDA '{self.pda_data['name']}'")
        self._validate_structure()
        self._validate_states()
        self._validate_stack_operations()
        self.logger.info(f"PDA '{self.pda_data['name']}' validation successful.")

    def _validate_structure(self):
        """
        Validates the basic structure of the PDA definition, ensuring required fields are present.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        required_fields = [
            "states",
            "input_alphabet",
            "stack_alphabet",
            "start_state",
            "initial_stack",
            "final_states",
            "transitions",
        ]
        for field in required_fields:
            if field not in self.pda_data or not self.pda_data[field]:
                self.logger.error(
                    f"Missing or empty required field '{field}' in PDA '{self.pda_data['name']}'"
                )
                raise ValueError(f"'{field}' is a required field for PDA definitions.")

        # Ensure the start state is valid
        if self.pda_data["start_state"] not in self.pda_data["states"]:
            self.logger.error(
                f"Invalid start state '{self.pda_data['start_state']}' in PDA '{self.pda_data['name']}'"
            )
            raise ValueError(f"Start state must be one of the defined states.")

        # Ensure the initial stack symbol is valid
        if self.pda_data["initial_stack"] not in self.pda_data["stack_alphabet"]:
            self.logger.error(
                f"Invalid initial stack symbol '{self.pda_data['initial_stack']}' in PDA '{self.pda_data['name']}'"
            )
            raise ValueError(
                f"Initial stack symbol must be part of the stack alphabet."
            )

    def _validate_states(self):
        """
        Validates that all states, transitions, and final states are consistent with the PDA definition.

        Raises:
            ValueError: If transitions refer to undefined states or final states are invalid.
        """
        states = self.pda_data["states"]

        # Validate final states
        for final_state in self.pda_data["final_states"]:
            if final_state not in states:
                self.logger.error(
                    f"Invalid final state '{final_state}' in PDA '{self.pda_data['name']}'"
                )
                raise ValueError(f"Final states must be part of the defined states.")

        # Validate transitions reference valid states
        for current_state, transitions in self.pda_data["transitions"].items():
            if current_state not in states:
                self.logger.error(
                    f"Undefined state '{current_state}' in transitions of PDA '{self.pda_data['name']}'"
                )
                raise ValueError(
                    f"Transition references undefined state '{current_state}'."
                )

            for input_symbol, stack_transitions in transitions.items():
                for stack_symbol, results in stack_transitions.items():
                    for next_state, _ in results:
                        if next_state not in states:
                            self.logger.error(
                                f"Transition to undefined state '{next_state}' from '{current_state}' in PDA '{self.pda_data['name']}'"
                            )
                            raise ValueError(
                                f"Transition references undefined state '{next_state}'."
                            )

    def _validate_stack_operations(self):
        """
        Validates the stack operations in the PDA transitions.

        Raises:
            ValueError: If stack operations are invalid.
        """
        stack_alphabet = self.pda_data["stack_alphabet"]
        input_alphabet = self.pda_data["input_alphabet"] + [
            "ε",
            "Îµ",
        ]  # Include epsilon transitions

        # Validate transitions for stack consistency
        for current_state, transitions in self.pda_data["transitions"].items():
            for input_symbol, stack_transitions in transitions.items():
                # Ensure input symbols are valid
                if input_symbol not in input_alphabet:
                    self.logger.error(
                        f"Invalid input symbol '{input_symbol}' in PDA '{self.pda_data['name']}'"
                    )
                    raise ValueError(
                        f"Input symbols in transitions must be part of the input alphabet or 'ε'."
                    )

                for stack_symbol, results in stack_transitions.items():
                    # Ensure stack symbols are valid
                    if stack_symbol not in stack_alphabet:
                        self.logger.error(
                            f"Invalid stack symbol '{stack_symbol}' in PDA '{self.pda_data['name']}'"
                        )
                        raise ValueError(
                            f"Stack symbols in transitions must be part of the stack alphabet."
                        )

                    for _, stack_operation in results:
                        # Ensure stack operation uses valid stack symbols
                        for symbol in stack_operation:
                            if symbol == "Îµ":
                                continue

                            if symbol not in stack_alphabet and (
                                symbol != "ε" or symbol != "Îµ"
                            ):
                                self.logger.error(
                                    f"Invalid stack operation '{stack_operation}' in PDA '{self.pda_data['name']}'"
                                )
                                raise ValueError(
                                    f"Stack operations must use valid stack symbols or 'ε'."
                                )
