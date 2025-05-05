from grammar.parser import Parser
from grammar.generator import Generator
from midi.midi_writer import MidiWriter

class Commands:
    def execute_command(self, command_name, *args):
        if command_name == "generate":
            if len(args) < 1:
                print("Error: Missing grammar file argument for 'generate' command.")
                return
            
            repetitions = int(args[1]) if len(args) > 1 else 1
            self.generate_music(args[0], repetitions)  
        elif command_name == "list":
            self.list_commands()
        else:
            print(f"Unknown command: {command_name}")

    def list_commands(self):
        print("Available commands:")
        print("  generate <number>- Generate MIDI music from grammar and specify the number of possible repetitions")
        print("  list - List available commands")

    def generate_music(self, grammar_file, repetitions=1):
        # Parse the grammar file
        parser = Parser()
        grammar_system = parser.parse_grammar(grammar_file)

        if grammar_system is None:
            print("Failed to parse the grammar file.")
            return
        
        # Generate music
        generator = Generator(grammar_system, repetitions=repetitions)
        multi_string = generator.generate_music()

        # Print the generated multi-string
        for instrument_name, result in multi_string.items():
            print(f"Instrument: {instrument_name}")
            print("  Final String:")
            print(f"    {result['final_string']}")
            print("  Steps:")
            for step in result["steps"]:
                print(f"    {step}")
        
        # Write the multi_string to a MIDI file
        midi_writer = MidiWriter(multi_string)
        midi_writer.write_to_midi("output.mid")