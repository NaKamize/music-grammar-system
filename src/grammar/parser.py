import json


class GrammarSystem:
    def __init__(self, instruments, states):
        self.instruments = instruments  # Dictionary of Instrument objects
        self.states = states  # List of dictionaries representing states


class Instrument:
    def __init__(self, nonterminals, terminals, start, structure_rules, tone_rules):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.start = start
        self.structure_rules = structure_rules
        self.tone_rules = tone_rules


class ToneRule:
    def __init__(self, tone=None, length=None, octave=None, dynamics=None, variation=None, chord=None, operations=None):
        self.tone = tone
        self.length = length
        self.octave = octave
        self.dynamics = dynamics
        self.variation = variation
        self.chord = chord
        self.operations = operations
        
    def set_tone_name(self, tone_name):
        self.tone = tone_name
        
    def to_dict(self):
        """
        Converts the ToneRule object into a dictionary for JSON serialization.
        """
        return {
            "tone": self.tone,
            "length": self.length,
            "octave": self.octave,
            "dynamics": self.dynamics,
            "variation": self.variation,
            "chord": self.chord,
            "operations": self.operations
        }


class Parser:
    
    def parse_tone_or_nonterminal(self, tone):
        """
        Parses an element from the 'right' list. If it's a dictionary, it creates a ToneRule.
        If it's a string, it treats it as a nonterminal.
        """
        if isinstance(tone, dict):
            # Parse as a ToneRule
            return ToneRule(
                tone=tone.get("tone"),
                length=tone.get("length"),
                octave=tone.get("octave"),
                dynamics=tone.get("dynamics"),
                variation=tone.get("variation"),
                chord=tone.get("chord"),
                operations=tone.get("operation")
            )
        elif isinstance(tone, str):
            # Parse as a nonterminal
            return tone  # Return the nonterminal as-is
        else:
            # Handle invalid cases
            raise ValueError(f"Invalid tone or nonterminal: {tone}")
        
    def parse_grammar(self, file_path):
        """
        Parses the JSON grammar file and returns a GrammarSystem object.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Parse instruments
            instruments = {}
            for instrument_name, instrument_data in data["instruments"].items():
                # Preprocess terminals: Convert nested lists to tuples
                terminals = set(
                    tuple(item) if isinstance(item, list) else item
                    for item in instrument_data["terminals"]
                )
                nonterminals = set(instrument_data["nonterminals"])

                # Validate that nonterminals and terminals do not overlap
                overlap = nonterminals.intersection(terminals)
                if overlap:
                    raise ValueError(
                        f"Error in instrument '{instrument_name}': "
                        f"Symbols found in both nonterminals and terminals: {overlap}"
                    )
                # Parse tone rules
                tone_rules = []
                for rule in instrument_data["tone_rules"]:
                    parsed_rule = {
                        "left": rule["left"],
                        "right": [
                            [
                                self.parse_tone_or_nonterminal(tone)
                                for tone in tones
                            ]
                            for tones in rule["right"]
                        ]
                    }
                    tone_rules.append(parsed_rule)

                instruments[instrument_name] = Instrument(
                    nonterminals=instrument_data["nonterminals"],
                    terminals=instrument_data["terminals"],
                    start=instrument_data["start"],
                    structure_rules=instrument_data["structure_rules"],
                    tone_rules=tone_rules
                )

            # Parse states (Q)
            states = data["Q"]

            # Return GrammarSystem object
            return GrammarSystem(instruments=instruments, states=states)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading grammar file: {e}")
            return None

    def print_grammar_system(self, grammar_system):
        """
        Prints the grammar system in a readable format.
        """
        print("Grammar System:")
        for instrument_name, instrument in grammar_system.instruments.items():
            print(f"Instrument: {instrument_name}")
            
            # Print structure rules
            print("  Structure Rules:")
            for rule in instrument.structure_rules:
                print(f"    Rule Left: {rule['left']}, Rule Right: {rule['right']}")
            
            # Print tone rules
            print("  Tone Rules:")
            for rule in instrument.tone_rules:
                print(f"    Rule Left: {rule['left']}")
                for tones in rule["right"]:
                    for tone in tones:
                        print(f"      Tone: {tone.tone}, Length: {tone.length}, Octave: {tone.octave}, Dynamics: {tone.dynamics}, Variation: {tone.variation}, Chord: {tone.chord}")
        
        # Print states
        print("States (Q):")
        for state in grammar_system.states:
            print(f"  {state}")