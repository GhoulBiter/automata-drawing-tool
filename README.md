# Automata Drawing Tool

A Python application for generating and visualizing Nondeterministic Finite Automata (NFA) from a structured YAML file. This project is modularized to support future extensions like Deterministic Finite Automata (DFA) and regular expressions, as well as conversions between them. The generated automata are outputted as images in a landscape format, and detailed logs are maintained for troubleshooting.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using Conda](#using-conda)
  - [Using Pip](#using-pip)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Logging](#logging)
- [Known Issues](#known-issues)
- [Future Plans](#future-plans)
- [License](#license)

## Introduction

The NFA Drawer allows you to define NFAs in a YAML file, validate them, and generate corresponding visual diagrams. The tool is designed to support epsilon (`ε`) transitions and produces diagrams in landscape format. The modular design allows for future expansion to support Deterministic Finite Automata (DFA), regular expressions, and conversions between different automaton types.

## Features

- **Generate NFA diagrams**: Automatically create and save NFA visualizations based on the provided YAML definitions.
- **Support for epsilon transitions**: Properly handle `ε` transitions in the NFA.
- **Modular design**: Easily extendable to support DFAs and regular expressions.
- **Logging**: Detailed logs for validation, debugging, and error handling.
- **Landscape diagram generation**: Output diagrams are rendered in landscape mode for better readability.

## Prerequisites

- **Python 3.12.7**: This project uses Python 3.12.7. Please ensure that you have this or a compatible version installed.
- **Graphviz**: Install Graphviz for generating and rendering diagrams.

To install Graphviz:

- **On Windows**: Download the installer from [Graphviz official website](https://graphviz.org/download/).
- **On Linux**: Install via package manager:

    ```bash
    sudo apt-get install graphviz
    ```

- **On macOS**: Install via Homebrew:

    ```bash
    brew install graphviz
    ```

## Installation

### Using Conda

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/nfa-drawer.git
    cd nfa-drawer
    ```

2. **Create a new Conda environment** with Python 3.12.7:

    ```bash
    conda create -n nfa-drawer python=3.12.7
    conda activate nfa-drawer
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure Graphviz is installed** and added to your system’s PATH.

### Using Pip

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/nfa-drawer.git
    cd nfa-drawer
    ```

2. **Set up a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure Graphviz is installed** and added to your system’s PATH.

## Usage

1. **Edit the `input.yaml` file** to define your NFAs. Example YAML format:

    ```yaml
    nfas:
      - name: "NFA 1"
        type: "nfa"
        states: ['A', 'B', 'C', 'D', 'E']
        alphabet: ['0', '1', 'ε']
        transitions:
          A:
            '0': ['B']
            '0': ['C']
          B:
            '1': ['D']
          C:
            '0': ['E']
          D:
            'ε': ['C', 'E']
          E:
            '1': ['A']
        start_state: 'A'
        final_states: ['D', 'E']
    ```

2. **Run the application**:

    ```bash
    python app.py
    ```

3. The generated NFA diagrams will be saved as PNG files in the `outputs` directory.

## Folder Structure

The project is structured to allow easy extensions for DFA, regular expressions, and conversions:

``` text
nfa-drawer/
│
├── generators/                 # Modules for generating and rendering diagrams
│   ├── __init__.py
│   └── nfa_generator.py        # NFA-specific generator
│
├── validators/                 # Modules for validating automaton definitions
│   ├── __init__.py
│   └── nfa_validator.py        # NFA-specific validation logic
│
├── outputs/                    # Directory for storing generated diagram files
│   └── files.png
│
├── app.py                      # Main driver code to run the NFA generator
├── input.yaml                  # YAML file containing NFA definitions
├── logging_config.py           # Logger configuration for handling logs
├── nfa_generation.log          # Log file with details of the run
├── .gitignore                  # Git ignore file
└── requirements.txt            # Python dependencies
```

## Logging

Logs are maintained in the `nfa_generation.log` file located in the root directory. Logging details include:

- **INFO**: High-level process updates (e.g., starting graph generation, saving files).
- **DEBUG**: Detailed steps (e.g., adding states, transitions).
- **ERROR**: Any issues encountered during validation or graph creation.

Logs are also displayed in the console during execution.

### Common Issue: UnicodeEncodeError

If you encounter a `UnicodeEncodeError` due to the epsilon (`ε`) symbol, ensure that:

- Your terminal encoding is set to UTF-8 (`chcp 65001` on Windows).
- The log file is encoded as `utf-8` (already set in `logging_config.py`).

## Known Issues

- **Encoding Issues**: On some systems, Unicode characters like `ε` may not render correctly in the terminal. Ensure that UTF-8 encoding is enabled.

## Future Plans

- **Support for DFAs**: Add modules for generating and validating Deterministic Finite Automata (DFA).
- **Support for Regular Expressions**: Add functionality to generate automata from regular expressions.
- **Conversion Between Automata**: Implement conversion logic between NFA, DFA, and regular expressions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
