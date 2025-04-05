import random


class Generator:
    def __init__(self, grammar_system, iterations=10):
        self.grammar_system = grammar_system
        self.iterations = iterations
        
        # Initialize a dictionary to keep count of structure rules for each instrument
        self.structure_rule_counts = {
            instrument_name: len(instrument.structure_rules)
            for instrument_name, instrument in grammar_system.instruments.items()
        }
        print(f"Structure rule counts: {self.structure_rule_counts}")
        self.finished = False
        self.first_instrument = list(self.grammar_system.instruments.keys())[0]
        
    def get_nonterminals_from_string(self, instrument_name, multi_string):
        """
        Retrieves nonterminals from the instrument's final string, matching multi-symbol nonterminals.
        Multi-character nonterminals (e.g., S1) have higher priority over single-character ones (e.g., S).
        """
        instrument = self.grammar_system.instruments.get(instrument_name)
        nonterminals = []

        # Get the string from multi_string
        notes = multi_string[instrument_name]["final_string"][0]  # Assuming final_string is a single string like "AABAS1"

        # Sort nonterminals by length in descending order to prioritize multi-character nonterminals
        sorted_nonterminals = sorted(instrument.nonterminals, key=len, reverse=True)

        # Iterate over the string to find matches for nonterminals
        i = 0
        while i < len(notes):
            matched = False
            # Check each nonterminal in the sorted list
            for nonterminal in sorted_nonterminals:
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
    
    def is_scattered_match_list(self, current_string, left):
        """
        Checks if the characters in 'left' appear in 'current_string' in the correct order,
        but not necessarily consecutively. Handles multi-character non-terminals.
        """
        left_index = 0
        i = 0
        while i < len(current_string):
            # Check if the substring matches the current left non-terminal
            if list(current_string[i:i + len(left[left_index])]) == list(left[left_index]):
                left_index += 1
                i += len(left[left_index - 1])  # Skip the length of the matched non-terminal
                print(f"Matched {left[left_index - 1]} at position {i}")
                if left_index == len(left):
                    return True
            else:
                i += 1
        return False
        
    # Check if the left side of the rule matches the current string in a scattered manner
    def is_scattered_match(self, current_string, left):
        """
        Checks if the characters in 'left' appear in 'current_string' in the correct order,
        but not necessarily consecutively. Handles multi-character non-terminals.
        """
        left_index = 0
        i = 0
        while i < len(current_string):
            # Check if the substring matches the current left non-terminal
            if current_string[i:i + len(left[left_index])] == left[left_index]:
                left_index += 1
                i += len(left[left_index - 1])  # Skip the length of the matched non-terminal
                if left_index == len(left):
                    return True
            else:
                i += 1
        return False

    # Check if the left side of the rule matches the current string as a list
    def find_sublist(self, haystack, needle):
        """
        Finds the starting index of the first occurrence of the sublist `needle` in the list `haystack`.
        Returns -1 if `needle` is not found.
        """
        
        for i in range(len(haystack) - len(needle) + 1):
            if haystack[i:i + len(needle)] == needle:
                return i
        return -1
    
    def replace_scattered_tone_rule(self, current_string, left, right):
        """
        Applies the scattered tone rule by replacing the left side with the right side in the current string.
        """
        # Replace only the symbols in 'left' with the corresponding symbols in 'right'
        new_string = list(current_string)  # Convert to list for mutable operations
        left_index = 0
        i = 0
        j = 0
        while i < len(current_string):
            if list(current_string[i:i + len(left[left_index])]) == list(left[left_index]):
                if len(left[left_index]) > 1:
                    # remove following characters
                    new_string[j:j + len(left[left_index])] = [' '] * (len(left[left_index]) - 1)
                    # apply the right side
                    new_string[j] = right[left_index]
                    j += 0
                else:
                    # replace the matched substring with the corresponding symbol from 'right'
                    print(f"Replacing {new_string[j]} with {right[left_index]}")
                    new_string[j] = right[left_index]
                    j += 1
                left_index += 1
                i += 1
                if left_index == len(left):
                    break
            else:
                i += 1
                j += 1
        return new_string
    
    def replace_scattered_strucutre_symbols(self, current_string, left, right):
        """
        Applies the scattered structure rule by replacing the left side with the right side in the current string.
        """
        # Replace only the symbols in 'left' with the corresponding symbols in 'right'
        new_string = list(current_string)  # Convert to list for mutable operations
        left_index = 0
        i = 0
        j = 0
        while i < len(current_string):
            if current_string[i:i + len(left[left_index])] == left[left_index]:
                print(f"Matched {left[left_index]} at position {i}")
                # Insert extra white space after the matched substring
                new_string[j + len(left[left_index]):j + len(left[left_index])] = [' '] * len(left[left_index])
                # Replace the matched substring with the corresponding symbol from 'right'
                new_string[j:j + len(right[left_index])] = list(str(right[left_index]))
                i += len(left[left_index])
                j += len(right[left_index])
                left_index += 1
                if left_index == len(left):
                    break
            else:
                i += 1
                j += 1
        return ''.join(new_string)  # Convert back to string
    
    def initialize_multi_string(self):
        """
        Initializes the generator with the grammar system.
        """
        multi_string = {}
        # Initialize multi-string for all instruments
        for instrument_name, instrument in self.grammar_system.instruments.items():
            multi_string[instrument_name] = {
                "final_string": [instrument.start],  # Start with the start symbol
                "steps": []
        }
        
        return multi_string
    
    def apply_structure_transformation_rules(self, current_string, sorted_structure_rules, instrument_name, steps, multi_string):
        """
        Applies structure transformation rules to the current string iteratively.

        This method processes a list of structure rules, replacing the left-hand side of each rule
        with its corresponding right-hand side in the current string. It supports both direct
        and scattered matches.

        Args:
            current_string (list): The current string representation of structures.
            sorted_structure_rules (list): A list of structure rules sorted by the length of their left-hand side.
            instrument_name (str): The name of the instrument being processed.
            steps (list): A list to record the steps of rule application.
            multi_string (dict): A dictionary containing the multi-string representation for all instruments.

        Returns:
            dict: The updated multi_string with the transformed structures.
        """
        # Apply structure rules iteratively
        while True:
            rule_applied = False
            for rule in sorted_structure_rules:
                left = rule["left"]
                right = rule["right"]
                print(f"Current string: {current_string}")
                print(f"Trying to apply structure rule: {left} -> {right}")

                # Check if the left side of the rule matches the current string
                match_index = current_string.find(''.join(left))                    
                if match_index != -1:
                    # Replace the left side with the right side at the specific position
                    new_string = (
                        current_string[:match_index] +
                        ''.join([str(note) for note in right]) +
                        current_string[match_index + len(''.join(left)):]
                    )
                    steps.append(f"Applied structure rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                    current_string = new_string
                    rule_applied = True
                    break
                else:
                    # Check if the left side matches in a scattered manner
                    if self.is_scattered_match(current_string, left):
                        new_string = self.replace_scattered_strucutre_symbols(current_string, left, right)
                        steps.append(f"Applied scattered structure rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                        current_string = new_string
                        rule_applied = True
                        break
                    else:
                        print("No match found for scattered structure rule")
            # Update the final string in multi_string
            multi_string[instrument_name]["final_string"][0] = current_string
            # Break the loop if no rule was applied
            sync_state = [self.grammar_system.states[0]]
            if not rule_applied:
                self.finished = True
                break
            # Get the index of the applied rule in the instrument.structure_rules
            rule_index = next(
                (i for i, f_rule in enumerate(self.grammar_system.instruments[instrument_name].structure_rules) if rule == f_rule),
                -1
            )
            
            states = self.grammar_system.states
            sync_state = [item for item in states if item.get('piano_bass') == rule_index]
            break
        
        return multi_string, current_string, steps, sync_state
    
    def apply_tone_transformation_rules(self, current_string, sorted_tone_rules, instrument_name, steps, multi_string):
        """
        Applies tone transformation rules to the current string iteratively.

        This method processes a list of tone rules, replacing the left-hand side of each rule
        with its corresponding right-hand side in the current string. It supports both direct
        and scattered matches.

        Args:
            current_string (list): The current string representation of tones.
            sorted_tone_rules (list): A list of tone rules sorted by the length of their left-hand side.
            instrument_name (str): The name of the instrument being processed.
            steps (list): A list to record the steps of rule application.
            multi_string (dict): A dictionary containing the multi-string representation for all instruments.

        Returns:
            dict: The updated multi_string with the transformed tones.
        """
        while True:
            rule_applied = False
            # Apply tone rules iteratively
            for rule in sorted_tone_rules:
                left = rule["left"]
                right = rule["right"]
                print(f"Current string: {current_string}")
                print(f"Trying to apply structure rule: {left} -> {right}")
                
                # Check if the left side of the rule matches the current string
                match_index = self.find_sublist(current_string, left)
                if match_index != -1:
                    # Replace the left side with the right side at the specific position
                    steps.append(f"Applied tone rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                    current_string[match_index] = right[0]
                    rule_applied = True
                    break
                else:
                    # Check if the left side matches in a scattered manner
                    if self.is_scattered_match_list(current_string, left):
                        # Convert back to string
                        steps.append(f"Applied scattered tone rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                        current_string = self.replace_scattered_tone_rule(current_string, left, right)
                        rule_applied = True
                        break
                    else:
                        print("No match found for scattered tone rule")
            
            # Update the final string in multi_string
            multi_string[instrument_name]["final_string"][0] = current_string
            # Break the loop if no rule was applied
            sync_state = [self.grammar_system.states[0]]
            if not rule_applied:
                self.finished = True
                break
            # Get the index of the applied rule in the instrument.structure_rules
            rule_index = next(
                (i for i, f_rule in enumerate(self.grammar_system.instruments[instrument_name].tone_rules) if rule == f_rule),
                -1
            )
            
            states = self.grammar_system.states
            sync_state = [item for item in states if item.get('piano_bass') == (rule_index + self.structure_rule_counts[instrument_name])]
            break
                
        return multi_string, sync_state
    
    def get_next_instrument(self, current_instrument_name, states):
        """
        Returns the next instrument name in the sequence.
        If the current instrument is the last one, it loops back to the first.
        """
        instrument_names = list(states[0].keys())
        current_index = instrument_names.index(current_instrument_name)
        next_index = (current_index + 1) % len(instrument_names)  # Loop back to the first instrument
        return instrument_names[next_index]

    def generate_music(self):
        """
        Generates multi-string music representation based on the grammar system.
        """
        multi_string = self.initialize_multi_string()

        states = self.grammar_system.states
        print(f"States: {states}")
        
        # Get the first instrument name and instrument by itself
        instrument_name = list(self.grammar_system.instruments.keys())[0]
        instrument = self.grammar_system.instruments[instrument_name]
        
        # Loop rules and find rule for current nonterminal
        while self.finished is False:
            current_string = multi_string[instrument_name]["final_string"][0]
            steps = multi_string[instrument_name]["steps"]

            # Sort structure rules by the length of their left side in descending order
            sorted_structure_rules = sorted(
                instrument.structure_rules,
                key=lambda rule: sum(len(nt) for nt in rule["left"]),
                reverse=True
            )

            multi_string, current_string, steps, sync_state = self.apply_structure_transformation_rules(
                current_string,
                sorted_structure_rules if self.first_instrument == instrument_name else sorted_structure_rules,
                instrument_name,
                steps,
                multi_string
            )
            
            instrument_name = self.get_next_instrument(instrument_name, sync_state)
            instrument = self.grammar_system.instruments[instrument_name]
        
        self.finished = False
        # Apply tone rules to generate tones
        while self.finished is False:
            current_string = multi_string[instrument_name]["final_string"][0]
            steps = multi_string[instrument_name]["steps"]

            # Sort tone rules by the length of their left side in descending order
            sorted_tone_rules = sorted(
                instrument.tone_rules,
                key=lambda rule: sum(len(nt) for nt in rule["left"]),
                reverse=True
            )
            
            multi_string, sync_state = self.apply_tone_transformation_rules(
                current_string,
                sorted_tone_rules,
                instrument_name,
                steps,
                multi_string
            )
            
            instrument_name = self.get_next_instrument(instrument_name, sync_state)
            instrument = self.grammar_system.instruments[instrument_name]

        return multi_string