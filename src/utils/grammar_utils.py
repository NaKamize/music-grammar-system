from __future__ import annotations
import random
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from grammar.parser import GrammarSystem

def get_tone_nonterminals(g_system: GrammarSystem, instrument_name: str) -> set[str]:
    tone_nonterminals: set[str] = set()
    for non_terminal in g_system.instruments[instrument_name].tone_rules:
        left = non_terminal['left']
        for item in left:
            tone_nonterminals.add(item)
    return tone_nonterminals

def applicable_rules_count(tone_rules: list[dict[str, Any]], left: list[str]) -> int:
    left_count = 0
    for rule in tone_rules:
        if left == rule["left"]:
            left_count += 1
    return left_count

def select_random_applicable_rule(tone_rules: list[dict[str, Any]], left: list[str]) -> tuple[list[str], list[list[Any]], dict[str, Any]]:
    random_rule = random.choice([rule for rule in tone_rules if rule["left"] == left])
    left = random_rule["left"]
    right = random_rule["right"]
    return left, right, random_rule