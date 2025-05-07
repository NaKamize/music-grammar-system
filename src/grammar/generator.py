from .tone_operations import ToneOperator 
from utils.grammar_utils import get_tone_nonterminals, applicable_rules_count, select_random_applicable_rule

class Generator:
    def __init__(self, grammar_system, repetitions):
        self.grammar_system = grammar_system
        self.repetitions = repetitions
        
        # Initialize a dictionary to keep count of structure rules for each instrument
        self.structure_rule_counts = {
            instrument_name: len(instrument.structure_rules)
            for instrument_name, instrument in grammar_system.instruments.items()
        }
        
        self.finished = False
        self.first_instrument = list(self.grammar_system.instruments.keys())[0]
        self.current_state = None
        self.prev_structure_rule = None
        self.rep_count = 0
        
    def terminal_nonterminal_check(self, left = None, right = None, instrument_name = None):
        """
        Checks if the left side of the rule contains any nonterminals that are also present in the right side.
        Raises a ValueError if such a case is found.
        """
        
        if left is not None and left not in self.grammar_system.instruments[instrument_name].nonterminals:
            raise ValueError(f"Left side {left} not found in nonterminals")
        
        if right is not None:
            for r in right:
                if isinstance(r, str):
                    continue  # Skip strings (nonterminals)
        
                if r.tone is not None and r.tone not in self.grammar_system.instruments[instrument_name].terminals:
                    raise ValueError(f"Right side tone {r.tone} not found in terminals")
                
                if r.chord is not None and r.chord not in self.grammar_system.instruments[instrument_name].terminals:
                    raise ValueError(f"Right side chord {r.chord} not found in terminals")
        
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
    
    def is_scattered_match_list(self, current_string, left, instrument_name):
        """
        Checks if the characters in 'left' appear in 'current_string' in the correct order,
        but not necessarily consecutively. Handles multi-character non-terminals.
        """
        left_index = 0
        i = 0
        while i < len(current_string):
            # Check if the substring matches the current left non-terminal
            substring = ''.join(str(x) for x in current_string[i:i + len(left[left_index]) + 1])
            is_last_char = i == len(current_string) - 1 and list(current_string[i:i + len(left[left_index])]) == list(left[left_index])
            is_second_last_char = i == len(current_string) - 2 and list(current_string[i:i + len(left[left_index])]) == list(left[left_index])
            is_not_nonterminal = list(current_string[i:i + len(left[left_index])]) == list(left[left_index]) and substring not in self.grammar_system.instruments[instrument_name].nonterminals
            if is_last_char or is_second_last_char or is_not_nonterminal:
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
            if haystack[i:i + len(needle)] == needle and len(needle) == 1:
                return i
        return -1
    
    def replace_scattered_tone_rule(self, current_string, left, right, instrument_name):
        """
        Applies the scattered tone rule by replacing the left side with the right side in the current string.
        """
        
        def apply_counterpoint_if_needed(rule):
            """
            Applies the counterpoint operation to a rule if the conditions are met.
            """
            if not isinstance(rule, str) and isinstance(rule.operations, dict) and rule.operations.get('counterpoint', False) and rule.tone:
                operator = ToneOperator()
                counter_point = operator.counterpoint(rule.tone)
                rule.set_tone_name(counter_point)
        
        # Replace only the symbols in 'left' with the corresponding symbols in 'right'
        new_string = list(current_string)  # Convert to list for mutable operations
        left_index = 0
        i = 0
        j = 0
        while i < len(current_string):
            substring = ''.join(str(x) for x in current_string[i:i + len(left[left_index]) + 1])
            is_last_char = i == len(current_string) - 1 and list(current_string[i:i + len(left[left_index])]) == list(left[left_index])
            is_second_last_char = i == len(current_string) - 2 and list(current_string[i:i + len(left[left_index])]) == list(left[left_index])
            is_not_nonterminal = list(current_string[i:i + len(left[left_index])]) == list(left[left_index]) and substring not in self.grammar_system.instruments[instrument_name].nonterminals
            
            if (is_last_char or is_second_last_char or is_not_nonterminal):
                if len(left[left_index]) > 1:
                    # Remove following characters
                    new_string[j:j + len(left[left_index])] = [' '] * (len(left[left_index]) - 1)
                    # Apply the right side
                    for rule in right[left_index]:
                        apply_counterpoint_if_needed(rule)
                    new_string[j] = right[left_index]
                else:
                    # Replace the matched substring with the corresponding symbol from 'right'
                    # Replacing {new_string[j]} with {right[left_index]}
                    for rule in right[left_index]:
                        apply_counterpoint_if_needed(rule)
                    # Check if the left side is in the nonterminals; if not, throw an error
                    self.terminal_nonterminal_check(left[left_index], right[left_index], instrument_name)
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
                
                # Replace the matched substring with the corresponding symbol from 'right'
                new_string[j:j + len(left[left_index])] = list(str(right[left_index]))
                
                # Adjust the indices based on the length difference
                i += len(left[left_index])  # Move `i` forward by the length of the matched substring
                j += len(right[left_index])  # Move `j` forward by the length of the replacement
                
                left_index += 1  # Move to the next symbol in the `left` list
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
    
    
    def handle_structure_rule_application(self, rule, steps, current_string, tone_rules, sync):
        left = rule["left"]
        right = rule["right"]
        rule_applied = False
        print(f"Current string: {current_string}")
        print(f"Trying to apply transform rule: {left} -> {right}")
        # Check if the left side of the rule matches the current string
        match_index = current_string.find(''.join(left))            
        if match_index != -1:
            applicable_count = applicable_rules_count(tone_rules, left)
            if applicable_count > 1 and not sync:
                left, right, rule = select_random_applicable_rule(tone_rules, left)
            # Replace the left side with the right side at the specific position
            new_string = (
                current_string[:match_index] +
                ''.join([str(note) for note in right]) +
                current_string[match_index + len(''.join(left)):]
            )
            steps.append(f"Applied structure rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
            current_string = new_string
            rule_applied = True
        else:
            # Check if the left side matches in a scattered manner
            if self.is_scattered_match(current_string, left):
                applicable_count = applicable_rules_count(tone_rules, left)
                if applicable_count > 1 and not sync:
                    left, right, rule = select_random_applicable_rule(tone_rules, left)
                new_string = self.replace_scattered_strucutre_symbols(current_string, left, right)
                steps.append(f"Applied structure rule: {''.join(left)} -> {''.join([str(note) for note in right])}")
                current_string = new_string
                rule_applied = True
            else:
                print("No match found for scattered structure rule")
        return steps, current_string, rule_applied, rule
        
    
    def apply_structure_transformation_rules(self, current_string, structure_rules, instrument_name, steps, multi_string):
        # Apply structure rules iteratively
        while True:
            rule_applied = False
            is_sync = False

            # Determine if synchronization is required
            if instrument_name != self.first_instrument:
                rule_index = self.current_state[0][instrument_name]
                is_sync = True

            if is_sync:
                # Apply the synchronization rule directly
                print(f"Applying sync rule for {instrument_name}")
                rule = structure_rules[rule_index]
                steps, current_string, rule_applied, rule = self.handle_structure_rule_application(rule, steps, current_string, structure_rules, is_sync)
            else:
                for rule in structure_rules:
                    left = rule["left"]
                    right = rule["right"]
                    print(f"Current string: {current_string}")
                    print(f"Trying to apply transform rule: {left} -> {right}")
                    # Check here if the last rule is equal to this one then skip it
                    if self.prev_structure_rule == rule:
                        # Check if the rule is repeated
                        self.rep_count += 1
                        print(f"Repeated count: {self.rep_count}")
                        if self.rep_count > self.repetitions and rule != structure_rules[-1]:
                            # Rule is being skipped
                            self.rep_count = 0
                            continue

                    steps, current_string, rule_applied, rule = self.handle_structure_rule_application(rule, steps, current_string, structure_rules, is_sync)
                    if rule_applied:
                        self.prev_structure_rule = rule
                        break
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
            sync_state = [item for item in states if item.get(list(self.grammar_system.instruments.keys())[0]) == rule_index]
            print(f"Next sync state: {sync_state}")
            break

        return multi_string, sync_state
    
    def get_next_sync_state(self, states, instrument_name, rule_index):
        # Find the next sync state where the rule index matches
        next_state = next(
            (state for state in states if state.get(instrument_name) == rule_index),
            None
        )
        return next_state
    
    def sync_with_terminal_only_rules(self, instrument_name, rule_index):
        return self.grammar_system.instruments[instrument_name].tone_rules[rule_index]
    
    def convert_to_dict(self, obj):
        if isinstance(obj, list):
            # Recursively convert each item in the list
            return [self.convert_to_dict(item) for item in obj]
        elif hasattr(obj, 'to_dict'):
            # Convert the object to a dictionary if it has a `to_dict` method
            return obj.to_dict()
        else:
            # Fallback to string representation for other types
            return str(obj)
    
    def handle_tone_rule_application(self, rule, steps, current_string, instrument_name, sync, tone_rules):
        left = rule["left"]
        right = rule["right"]
        print(f"Current string: {current_string}")
        print(f"Trying to apply transform rule: {left} -> {right}")
        rule_applied = False
        # Check if the left side of the rule matches the current string
        match_index = self.find_sublist(current_string, left)
        if match_index != -1:
            applicable_count = applicable_rules_count(tone_rules, left)
            if applicable_count > 1 and not sync:
                left, right, rule = select_random_applicable_rule(tone_rules, left)
            # Replace the left side with the right side at the specific position
            steps.append({"left": ''.join(left), "right": self.convert_to_dict(right)})
            current_string[match_index] = right[0]
            rule_applied = True
        else:
            # Check if the left side matches in a scattered manner
            if self.is_scattered_match_list(current_string, left, instrument_name):
                applicable_count = applicable_rules_count(tone_rules, left)
                if applicable_count > 1 and not sync:
                    left, right, rule = select_random_applicable_rule(tone_rules, left)
                # Convert back to string
                steps.append({"left": ''.join(left), "right": self.convert_to_dict(right)})
                current_string = self.replace_scattered_tone_rule(current_string, left, right, instrument_name)
                rule_applied = True
            else:
                print("No match found for scattered tone rule")
        return steps, current_string, rule_applied, rule
    
    
    def apply_tone_transformation_rules(self, current_string, tone_rules, instrument_name, steps, multi_string, is_last):
        while True:
            rule_applied = False
            is_sync = False

            # Determine if synchronization is required
            if instrument_name != self.first_instrument:
                rule_index = self.current_state[0][instrument_name] - len(self.grammar_system.instruments[instrument_name].structure_rules)
                is_sync = True

            if is_sync:
                # Apply the synchronization rule directly
                print(f"Applying sync rule for {instrument_name}")
                print(is_last)
                rule = tone_rules[rule_index] if not is_last else self.sync_with_terminal_only_rules(instrument_name, rule_index)
                print(rule)
                steps, current_string, rule_applied, _ = self.handle_tone_rule_application(rule, steps, current_string, instrument_name, is_sync, tone_rules)
            else:
                # Apply tone rules iteratively
                for rule in tone_rules:
                    steps, current_string, rule_applied, rule = self.handle_tone_rule_application(rule, steps, current_string, instrument_name, is_sync, tone_rules)
                    if rule_applied:
                        break

            # Update the final string in multi_string
            multi_string[instrument_name]["final_string"][0] = current_string
            # Break the loop if no rule was applied
            sync_state = [self.grammar_system.states[0]]
            if not rule_applied:
                self.finished = True
                break
            # Get the index of the applied rule in the instrument.structure_rules
            states = self.grammar_system.states
            rule_index = next(
                    (i for i, f_rule in enumerate(self.grammar_system.instruments[instrument_name].tone_rules) if rule == f_rule),
                    -1
                )

            sync_state = [item for item in states if item.get(list(self.grammar_system.instruments.keys())[0]) == (rule_index + self.structure_rule_counts[instrument_name])]
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
    
    def check_for_remaining_nonterminals(self, multi_string):
        """
        Checks if there are any nonterminals left in the multi_string that need to be rewritten.

        Args:
            multi_string (dict): The multi-string representation of the grammar system.

        Returns:
            bool: True if there are nonterminals left, False otherwise.
        """
        for instrument_name, instrument_data in multi_string.items():
            # Get the nonterminals for the current instrument
            nonterminals = set(
                tuple(nt) if isinstance(nt, list) else nt
                for nt in self.grammar_system.instruments[instrument_name].nonterminals
            )
            
            # Get the final string for the current instrument
            final_string = instrument_data["final_string"][0]
            
            # Check if any symbol in the final string is a nonterminal
            for symbol in final_string:
                # Convert symbol to a tuple if it's a list
                symbol_to_check = tuple(symbol) if isinstance(symbol, list) else symbol
                for sym in symbol_to_check:
                    if isinstance(sym, str) and sym in nonterminals:
                        # Nonterminal sym was found in instrument 
                        return True
            
        return False
    
    
    def expand_nonterminals_in_rules(self, multi_string):
        skip_next = False
        for instrument_name, _ in self.grammar_system.instruments.items():
            for note_index, note in enumerate(multi_string[instrument_name]["final_string"][0]):
                if skip_next:
                    skip_next = False
                    continue

                for item in note:
                    if isinstance(item, str):
                        # Find the index of the string item
                        index = note.index(item)
                        # Split the note list into two parts
                        before_split = note[:index]
                        after_split = note[index + 1:]
                        
                        # Replace the original note in the multi_string with the split parts
                        final_string = multi_string[instrument_name]["final_string"][0]
                        note_index = final_string.index(note)  # Find the index of the original note in the final string
                        
                        # Build the new list to replace the original note
                        new_parts = []
                        if before_split:  # Only add if before_split is not empty
                            new_parts.append(before_split)
                        new_parts.append(item)  # Add the string item as is
                        if after_split:  # Only add if after_split is not empty
                            new_parts.append(after_split)
                        # Replace the original note with the flattened parts
                        final_string[note_index:note_index + 1] = new_parts
                        
                        # Skip the newly created objects in the next iteration
                        skip_next = True
                        break
        return multi_string
    
    def check_rewritable_nonterminals(self, multi_string):
        final_structure = 0
        for instrument_name, instrument_data in multi_string.items():
            # get the left side nonterminals from tone rules
            tone_nonterminals = get_tone_nonterminals(self.grammar_system, instrument_name)
            
            # Get the final string for the current instrument
            final_string = instrument_data["final_string"][0]

            skip_next = False  # Flag to skip the next symbol
            for index, symbol in enumerate(final_string):
                if skip_next:
                    skip_next = False  # Reset the flag and skip this iteration
                    continue

                # Ensure there is a next symbol to form a pair
                if index < len(final_string) - 1:
                    next_symbol = final_string[index + 1]
                    # Concatenate symbol and next_symbol and check if it's in tone_nonterminals
                    combined_symbol = symbol + next_symbol
                    if combined_symbol in tone_nonterminals:
                        skip_next = True  # Set the flag to skip the next symbol
                        continue  # Skip further checks for this pair

                if symbol not in tone_nonterminals:
                    final_strucutre += 1
                    break
                
        return final_structure

    def generate_music(self):
        """
        Generates multi-string music representation based on the grammar system.
        """
        multi_string = self.initialize_multi_string()
       
        # Get the first instrument name and instrument by itself
        instrument_name = list(self.grammar_system.instruments.keys())[0]
        instrument = self.grammar_system.instruments[instrument_name]
        self.current_instrument = instrument_name
        i = 0

        while i < self.repetitions:
            instrument_name = self.first_instrument
            instrument = self.grammar_system.instruments[instrument_name]
            
            # Loop rules and find rule for current nonterminal
            while self.finished is False:
                current_string = multi_string[instrument_name]["final_string"][0]
                steps = multi_string[instrument_name]["steps"]

                sorted_structure_rules = instrument.structure_rules
                
                multi_string, sync_state = self.apply_structure_transformation_rules(
                    current_string,
                    sorted_structure_rules,
                    instrument_name,
                    steps,
                    multi_string
                )
                
                if instrument_name == self.first_instrument:
                    self.current_state = sync_state
                instrument_name = self.get_next_instrument(instrument_name, self.current_state)
                instrument = self.grammar_system.instruments[instrument_name]
                
            print(f"Multi-string after structure rules: {multi_string}")
            final_strucutre = self.check_rewritable_nonterminals(multi_string)
                    
            if final_strucutre == 1:
                raise ValueError("Wrong rule design, it is not being synchronized.")
            elif final_strucutre == 0:
                print("All nonterminals have been rewritten.")
                break
            else: 
                i += 1
                
        
        self.finished = False
        is_last = False
        i = 0

        while i < self.repetitions:
            instrument_name = self.first_instrument
            instrument = self.grammar_system.instruments[instrument_name]
            
            # Apply tone rules to generate tones
            while self.finished is False:
                current_string = multi_string[instrument_name]["final_string"][0]
                steps = multi_string[instrument_name]["steps"]

                sorted_tone_rules = instrument.tone_rules
                # If it's the last cycle, filter out rules with non-terminals on the right-hand side
                if i == self.repetitions - 1:
                    sorted_tone_rules = [rule for rule in sorted_tone_rules if all(
                        not isinstance(symbol, str)
                        for symbol in rule["right"][0]
                    )]
                    is_last = True
                    print(f"Filtered rules for the last cycle (only terminals on the right): {sorted_tone_rules}")

                # For other instruments, proceed with the normal sorted tone rules
                multi_string, sync_state = self.apply_tone_transformation_rules(
                    current_string,
                    sorted_tone_rules,
                    instrument_name,
                    steps,
                    multi_string,
                    is_last
                )
                if instrument_name == self.first_instrument:
                    self.current_state = sync_state
                instrument_name = self.get_next_instrument(instrument_name, self.current_state)
                instrument = self.grammar_system.instruments[instrument_name]

            # Check the final strings if there are non-terminal left
            if self.check_for_remaining_nonterminals(multi_string):
                i += 1
                self.finished = False
                multi_string = self.expand_nonterminals_in_rules(multi_string)
            else:
                print("All nonterminals have been rewritten.")
                break
        
        return multi_string