import random


class Generator:
    def __init__(self, grammar_system, iterations=10):
        self.grammar_system = grammar_system
        self.iterations = iterations
        
    def get_nonterminals_from_string(self, instrument_name, multi_string):
        """
        Retrieves nonterminals from the instrument's final string, matching multi-symbol nonterminals.
        """
        instrument = self.grammar_system.instruments.get(instrument_name)
        nonterminals = []
        
        # Get the string from multi_string
        notes = multi_string[instrument_name]["final_string"][0]  # Assuming final_string is a single string like "AABAS1"
        
        # Iterate over the string to find matches for nonterminals
        i = 0
        while i < len(notes):
            matched = False
            # Check each nonterminal in the list
            for nonterminal in instrument.nonterminals:
                # Check if the substring matches the nonterminal
                if notes[i:i + len(nonterminal)] == nonterminal:
                    nonterminals.append(nonterminal)
                    print(f"Matched nonterminal: {nonterminal} at position {i}")
                    i += len(nonterminal)  # Move the index forward by the length of the matched nonterminal
                    matched = True
                    break
            if not matched:
                # If no match, move to the next character
                i += 1
        
        return nonterminals
    
    # Check if the left side of the rule matches the current string in a scattered manner
    def is_scattered_match(self, current_string, left):
        """
        Checks if the characters in 'left' appear in 'current_string' in the correct order,
        but not necessarily consecutively.
        """
        left_index = 0
        for char in current_string:
            if char == left[left_index]:
                left_index += 1
            if left_index == len(left):
                return True
        return False
        

    def generate_music(self):
        """
        Generates multi-string music representation based on the grammar system.
        """
        multi_string = {}

        # Initialize multi-string for all instruments
        for instrument_name, instrument in self.grammar_system.instruments.items():
            multi_string[instrument_name] = {
                "final_string": [instrument.start],  # Start with the start symbol
                "steps": []
            }
        
        # Get the first instrument name
        first_instrument_name = next(iter(self.grammar_system.instruments))
        
        # Pass the first instrument name to the function
        nonterminals = self.get_nonterminals_from_string(first_instrument_name, multi_string)
        print(f"Nonterminals for {first_instrument_name}: {nonterminals}")
        
        # Loop rules and find rule for current nonterminal
        for instrument_name, instrument in self.grammar_system.instruments.items():
            current_string = multi_string[instrument_name]["final_string"][0]
            steps = multi_string[instrument_name]["steps"]
            
            # Apply rules iteratively
            while True:
                rule_applied = False
                for rule in instrument.structure_rules:
                    left = rule["left"]
                    right = rule["right"]
                    print(current_string)
                    print(f"Trying to apply rule: {left} -> {right}")
                    if len(left) == 1:
                        # Check if the left side of the rule matches the current string
                        match_index = current_string.find(''.join(left))
                        if match_index != -1:
                            # Replace the left side with the right side at the specific position
                            new_string = (
                                current_string[:match_index] +
                                ''.join([str(note) for note in right]) +
                                current_string[match_index + len(''.join(left)):]
                            )
                            steps.append(f"Applied rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                            current_string = new_string
                            rule_applied = True
                            break
                    else:
                        # Check if the left side matches in a scattered manner
                        if self.is_scattered_match(current_string, left):
                            # Replace only the symbols in 'left' with the corresponding symbols in 'right'
                            new_string = list(current_string)  # Convert to list for mutable operations
                            left_index = 0
                            for i, char in enumerate(current_string):
                                if char == left[left_index]:
                                    # Replace the matched character with the corresponding symbol from 'right'
                                    new_string[i] = str(right[left_index])
                                    left_index += 1
                                if left_index == len(left):
                                    break
                            # Convert back to string
                            new_string = ''.join(new_string)
                            steps.append(f"Applied scattered rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                            current_string = new_string
                            rule_applied = True
                        
                        
                
                # Update the final string in multi_string
                multi_string[instrument_name]["final_string"][0] = current_string
                
                # Break the loop if no rule was applied
                if not rule_applied:
                    break
        nonterminals = self.get_nonterminals_from_string(first_instrument_name, multi_string)
        print(f"Nonterminals for {first_instrument_name}: {nonterminals}")
        # Pass the first instrument name to the function

        return multi_string