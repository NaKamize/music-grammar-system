from grammar.parser import Parser

class Commands:
    def execute_command(self, command_name, *args):
        if command_name == "generate":
            if len(args) < 1:
                print("Error: Missing grammar file argument for 'generate' command.")
                return
            self.generate_music(args[0])  # Pass the grammar file
        elif command_name == "list":
            self.list_commands()
        else:
            print(f"Unknown command: {command_name}")

    def list_commands(self):
        print("Available commands:")
        print("  generate - Generate MIDI music from grammar")
        print("  list - List available commands")

    def generate_music(self, grammar_file):
        # Parse the grammar file
        parser = Parser()
        grammar_system = parser.parse_grammar(grammar_file)

        if grammar_system is None:
            print("Failed to parse the grammar file.")
            return

        # Placeholder for generating music logic
        print(f"Successfully parsed grammar file: {grammar_file}")
        # Print the grammar system in a readable format
        print("Successfully parsed grammar file:")
        print("Grammar System:")
        for instrument_name, instrument in grammar_system.instruments.items():
            print(f"  Instrument: {instrument_name}")
            print(f"    Nonterminals: {instrument.nonterminals}")
            print(f"    Terminals: {instrument.terminals}")
            print(f"    Start Symbol: {instrument.start}")
            print(f"    Structure Rules: {instrument.structure_rules}")
            print(f"    Tone Rules: {instrument.tone_rules}")
        print(f"Q (Sequence of Rules): {grammar_system.Q}")