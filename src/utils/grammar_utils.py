import random

def get_tone_nonterminals(g_system, instrument_name):
    tone_nonterminals = set()
    for non_terminal in g_system.instruments[instrument_name].tone_rules:
        left = non_terminal['left']
        print(f"Left side: {left}")
        for item in left:
            tone_nonterminals.add(item)
    return tone_nonterminals

def applicable_rules_count(tone_rules, left):
    left_count = 0
    for rule in tone_rules:
        if left == rule["left"]:
            left_count += 1
    return left_count

def select_random_applicable_rule(tone_rules, left):
    random_rule = random.choice([rule for rule in tone_rules if rule["left"] == left])
    print(f"Random rule: {random_rule}")
    left = random_rule["left"]
    right = random_rule["right"]
    return left, right, random_rule