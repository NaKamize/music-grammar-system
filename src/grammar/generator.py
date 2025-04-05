import random


class Generator:
    def __init__(self, grammar_system, iterations=10):
        self.grammar_system = grammar_system
        self.iterations = iterations
        
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

            # Sort structure rules by the length of their left side in descending order
            sorted_structure_rules = sorted(
                instrument.structure_rules,
                key=lambda rule: sum(len(nt) for nt in rule["left"]),
                reverse=True
            )

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
                            # Convert back to string
                            new_string = ''.join(new_string)
                            steps.append(f"Applied scattered structure rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                            current_string = new_string
                            rule_applied = True
                        else:
                            print("No match found for scattered structure rule")

                # Update the final string in multi_string
                multi_string[instrument_name]["final_string"][0] = current_string

                # Break the loop if no rule was applied
                if not rule_applied:
                    break
        
        # Apply tone rules to generate tones
        for instrument_name, instrument in self.grammar_system.instruments.items():
            current_string = multi_string[instrument_name]["final_string"][0]
            steps = multi_string[instrument_name]["steps"]

            # Sort tone rules by the length of their left side in descending order
            sorted_tone_rules = sorted(
                instrument.tone_rules,
                key=lambda rule: sum(len(nt) for nt in rule["left"]),
                reverse=True
            )
            print(f"Sorted tone rules: {sorted_tone_rules}")
            
            while True:
                #print(f"Sorted tone rules: {sorted_tone_rules}")
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
                        print(f"SINGLE Matched {left} at position {match_index}")
                        rule_applied = True
                        break
                    else:
                        # Check if the left side matches in a scattered manner
                        if self.is_scattered_match_list(current_string, left):
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
                                        print(new_string)
                                        # apply the right side
                                        new_string[j] = right[left_index]
                                        print(new_string)
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
                            # Convert back to string
                            steps.append(f"Applied tone rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                            current_string = new_string
                            rule_applied = True
                        else:
                            print("No match found for scattered tone rule")
                            

                # Update the final string in multi_string
                multi_string[instrument_name]["final_string"][0] = current_string
                # Break the loop if no rule was applied
                if not rule_applied:
                    break


        return multi_string