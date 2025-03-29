import json

class GrammarSystem:
    def __init__(self, instruments, Q):
        self.instruments = instruments
        self.Q = Q

class Instrument:
    def __init__(self, nonterminals, terminals, start, structure_rules, tone_rules):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.start = start
        self.structure_rules = structure_rules
        self.tone_rules = tone_rules

class Parser:
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
                instruments[instrument_name] = Instrument(
                    nonterminals=instrument_data["nonterminals"],
                    terminals=instrument_data["terminals"],
                    start=instrument_data["start"],
                    structure_rules=instrument_data["structure_rules"],
                    tone_rules=instrument_data["tone_rules"]
                )
            
            # Parse Q
            Q = data["Q"]

            # Return GrammarSystem object
            return GrammarSystem(instruments=instruments, Q=Q)
        
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading grammar file: {e}")
            return None

    def validate_grammar(self, grammar_system):
        """
        Validates the structure of the GrammarSystem object.
        """
        if not isinstance(grammar_system, GrammarSystem):
            raise ValueError("Invalid grammar system object.")

        for instrument_name, instrument in grammar_system.instruments.items():
            if not instrument.nonterminals or not instrument.terminals:
                raise ValueError(f"Instrument '{instrument_name}' must have nonterminals and terminals.")
            if not instrument.start:
                raise ValueError(f"Instrument '{instrument_name}' must have a start symbol.")
            if not instrument.structure_rules or not instrument.tone_rules:
                raise ValueError(f"Instrument '{instrument_name}' must have structure and tone rules.")
        
        print("Grammar system is valid.")