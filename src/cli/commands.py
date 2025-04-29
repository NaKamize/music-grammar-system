from grammar.parser import Parser
from grammar.generator import Generator
from midi.midi_writer import MidiWriter

class Commands:
    def execute_command(self, command_name, *args):
        if command_name == "generate":
            if len(args) < 1:
                print("Error: Missing grammar file argument for 'generate' command.")
                return
            # Check if the number of iterations is provided, otherwise use a default value
            iterations = int(args[1]) if len(args) > 1 else 1
            self.generate_music(args[0], iterations)  # Pass the grammar file
        elif command_name == "list":
            self.list_commands()
        else:
            print(f"Unknown command: {command_name}")

    def list_commands(self):
        print("Available commands:")
        print("  generate - Generate MIDI music from grammar")
        print("  list - List available commands")

    def generate_music(self, grammar_file, iterations=0):
        # Parse the grammar file
        parser = Parser()
        grammar_system = parser.parse_grammar(grammar_file)

        if grammar_system is None:
            print("Failed to parse the grammar file.")
            return

        # Print the grammar system using the parser's method
        #parser.print_grammar_system(grammar_system)
        
        # Generate music
        generator = Generator(grammar_system, iterations=iterations)
        multi_string = generator.generate_music()

        # Print the generated multi-string
        for instrument_name, result in multi_string.items():
            print(f"Instrument: {instrument_name}")
            print("  Final String:")
            print(f"    {result['final_string']}")# ' '.join(result['final_string'])
            print("  Steps:")
            for step in result["steps"]:
                print(f"    {step}")
        
        # Write the multi_string to a MIDI file
        midi_writer = MidiWriter(multi_string)
        midi_writer.write_to_midi("output.mid")