# Multigenerative Grammar CLI

This project implements a command line application that utilizes a multigenerative grammar system with scattered context grammars to parse grammar examples and produce MIDI music files.

## Project Structure

```
multigenerative-grammar-cli
├── src
│   ├── main.py               # Entry point of the application
│   ├── grammar               # Module for grammar parsing and generation
│   │   ├── parser.py         # Contains the Parser class
│   │   ├── generator.py      # Contains the Generator class
│   │   └── __init__.py       # Initializes the grammar module
│   ├── midi                  # Module for MIDI file handling
│   │   ├── midi_writer.py     # Contains the MidiWriter class
│   │   └── __init__.py       # Initializes the midi module
│   ├── cli                   # Module for command line interface
│   │   ├── commands.py       # Contains the Commands class
│   │   └── __init__.py       # Initializes the cli module
│   └── utils                 # Module for utility functions
│       ├── file_utils.py     # Contains utility functions for file handling
│       └── __init__.py       # Initializes the utils module
├── tests                     # Directory for unit tests
│   ├── test_grammar          # Tests for grammar module
│   │   ├── test_parser.py    # Unit tests for the Parser class
│   │   ├── test_generator.py  # Unit tests for the Generator class
│   │   └── __init__.py       # Initializes the test_grammar module
│   ├── test_midi             # Tests for MIDI module
│   │   ├── test_midi_writer.py # Unit tests for the MidiWriter class
│   │   └── __init__.py       # Initializes the test_midi module
│   └── test_cli              # Tests for CLI module
│       ├── test_commands.py   # Unit tests for the Commands class
│       └── __init__.py       # Initializes the test_cli module
├── requirements.txt          # Project dependencies
├── setup.py                  # Setup script for the project
└── README.md                 # Project documentation
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the application, use the following command:

```
python src/main.py [options]
```

Replace `[options]` with the desired command line options.

## Examples

1. **Parsing a Grammar File**: 
   ```
   python src/main.py parse --file path/to/grammar.txt
   ```

2. **Generating MIDI Music**:
   ```
   python src/main.py generate --grammar path/to/grammar.txt --output path/to/output.mid
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.