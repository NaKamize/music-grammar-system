from grammar.parser import Parser
from grammar.generator import Generator
from midi.midi_writer import MidiWriter
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj) 

class Commands:
    def execute_command(self, command_name, *args):
        if command_name == "generate":
            if len(args) < 1:
                print("Error: Missing grammar file argument for generate command.")
                return
            
            repetitions = int(args[1]) if len(args) > 1 else 1
            outfile = args[2] if len(args) > 2 else "output.mid"
            self.generate_music(args[0], outfile, repetitions)  
        elif command_name == "list":
            self.list_commands()
        elif command_name == "instruments":
            instrument_map = {
            "Violin": 40,
            "Cello": 42,
            "Flute": 73,
            "Piano": 0,
            "Guitar": 24,
            "Trumpet": 56,
            "Saxophone": 65,
            "Clarinet": 71,
            "Trombone": 57,
            "Accordion": 21,
            "Bass": 32
            }
            print("Available instruments:")
            for instrument, program_number in instrument_map.items():
                print(f"  {instrument}: Program Number {program_number}")
        else:
            print(f"Unknown command: {command_name}")

    def list_commands(self):
        print("Available commands:")
        print("  generate <infile> <number> <outfile> Generate MIDI music from grammar and specify the number of possible repetitions")
        print("                               and the name of the output file.")
        print("  list - List available commands.")
        print("  instruments - List available instruments and their program numbers.")

    def generate_music(self, grammar_file, outfile, repetitions=1):
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
            print(json.dumps(result['final_string'], cls=CustomJSONEncoder))
            print("  Steps:")
            for step in result["steps"]:
                if isinstance(step, dict):
                    print(f"    Applied tone rule {step['left']} -> {step['right']}")
                else:
                    print(f"    {step}")
        
        # Write the multi_string to a MIDI file
        midi_writer = MidiWriter(multi_string)
        midi_writer.write_to_midi(outfile)