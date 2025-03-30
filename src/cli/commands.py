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

        # Print the grammar system using the parser's method
        parser.print_grammar_system(grammar_system)