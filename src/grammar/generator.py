class Generator:
    def __init__(self, grammar_system):
        self.grammar_system = grammar_system

    def generate_music(self):
        """
        Generates multi-string music representation based on the grammar system.
        """
        multi_string = {}

        # Iterate over instruments
        for instrument_name, instrument in self.grammar_system.instruments.items():
            print(f"Generating for instrument: {instrument_name}")
            current_string = [instrument.start]  # Start with the start symbol
            steps = []

            # Apply structure rules iteratively until no changes occur
            while True:
                modified = False
                for rule in instrument.structure_rules:
                    for i, symbol in enumerate(current_string):
                        if symbol == rule["left"][0]:  # Match the left-hand side
                            current_string = current_string[:i] + rule["right"] + current_string[i + 1:]
                            steps.append(f"Applied structure rule: {rule['left']} -> {rule['right']}")
                            modified = True
                            break
                    if modified:
                        break
                if not modified:
                    break  # Exit when no more rules can be applied

            # Apply tone rules based on states
            for state in self.grammar_system.states:
                if instrument_name in state:  # Check if the instrument has a state
                    state_index = state[instrument_name]  # Get the current state index
                    for i, symbol in enumerate(current_string):
                        for rule_index, rule in enumerate(instrument.tone_rules):
                            if rule_index == state_index and symbol == rule["left"][0]:  # Match state and left-hand side
                                tones = [
                                    f"{tone.tone or tone.chord}({tone.length}, {tone.octave}, {tone.dynamics}, {tone.variation})"
                                    for tones_group in rule["right"]
                                    for tone in tones_group
                                ]
                                current_string = current_string[:i] + tones + current_string[i + 1:]
                                steps.append(f"Applied tone rule (state {state_index}): {rule['left']} -> {tones}")
                                break

            # Store the generated string for the instrument
            multi_string[instrument_name] = {
                "final_string": current_string,
                "steps": steps
            }

        return multi_string