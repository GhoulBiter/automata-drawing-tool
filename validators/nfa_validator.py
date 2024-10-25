def validate_nfa_structure(nfa, logger):
    """
    Validates that the NFA has the required structure.

    Args:
        nfa (dict): NFA data to validate.
        logger (logging.Logger): Logger instance for logging errors and warnings.

    Raises:
        ValueError: If required fields are missing in the NFA.
    """
    required_keys = [
        "name",
        "type",
        "states",
        "transitions",
        "start_state",
        "final_states",
    ]
    for key in required_keys:
        if key not in nfa:
            logger.error(f"Missing required key '{key}' in NFA definition: {nfa}")
            raise ValueError(f"Missing required key '{key}' in NFA definition.")


def validate_nfa_states(nfa, logger):
    """
    Validates the states in the NFA for presence and duplicates.

    Args:
        nfa (dict): NFA data containing states information.
        logger (logging.Logger): Logger instance for logging warnings and errors.

    Raises:
        ValueError: If states are missing or duplicate states are detected.
    """
    if not nfa["states"]:
        logger.error(f"NFA '{nfa['name']}' has no states.")
        raise ValueError(f"NFA '{nfa['name']}' has no states.")
    if len(nfa["states"]) != len(set(nfa["states"])):
        logger.warning(f"NFA '{nfa['name']}' contains duplicate states.")


def validate_transitions(nfa, logger):
    """
    Validates transitions to ensure they reference defined states only.

    Args:
        nfa (dict): NFA data containing transition details.
        logger (logging.Logger): Logger instance for logging errors.

    Raises:
        ValueError: If transitions reference undefined states.
    """
    for state, transitions_dict in nfa["transitions"].items():
        if state not in nfa["states"]:
            logger.error(
                f"State '{state}' in transitions is not defined in the list of states."
            )
            raise ValueError(
                f"State '{state}' in transitions is not defined in the list of states."
            )
        for next_states in transitions_dict.values():
            for next_state in next_states:
                if next_state not in nfa["states"]:
                    logger.error(
                        f"Transition to undefined state '{next_state}' in NFA '{nfa['name']}'."
                    )
                    raise ValueError(
                        f"Transition to undefined state '{next_state}' in NFA '{nfa['name']}'."
                    )


def validate_nfa_symbols(nfa, logger):
    """
    Validates that the NFA uses symbols defined in its alphabet and logs unused symbols.

    Args:
        nfa (dict): NFA data including the alphabet and transition symbols.
        logger (logging.Logger): Logger instance for logging information and errors.
    """
    used_symbols = set(
        str(symbol)
        for transitions_dict in nfa["transitions"].values()
        for symbol in transitions_dict.keys()
    )
    unused_symbols = set(str(symbol) for symbol in nfa["alphabet"]) - used_symbols
    if unused_symbols:
        logger.info(
            f"NFA '{nfa['name']}' has unused symbols in its alphabet: {', '.join(unused_symbols)}."
        )
