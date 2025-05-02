def get_tone_nonterminals(g_system, instrument_name):
    tone_nonterminals = set()
    for non_terminal in g_system.instruments[instrument_name].tone_rules:
        left = non_terminal['left']
        print(f"Left side: {left}")
        for item in left:
            tone_nonterminals.add(item)
    return tone_nonterminals