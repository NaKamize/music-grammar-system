import unittest
from src.grammar.parser import Parser

class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_grammar_valid(self):
        grammar_example = "S -> A | B\nA -> 'a'\nB -> 'b'"
        result = self.parser.parse_grammar(grammar_example)
        self.assertIsNotNone(result)
        self.assertTrue(result.is_valid)

    def test_parse_grammar_invalid(self):
        grammar_example = "S -> A | B\nA -> 'a'\nB -> 'b' |"
        result = self.parser.parse_grammar(grammar_example)
        self.assertIsNotNone(result)
        self.assertFalse(result.is_valid)

    def test_validate_grammar(self):
        valid_grammar = "S -> A | B\nA -> 'a'\nB -> 'b'"
        invalid_grammar = "S -> A | B\nA -> 'a'\nB -> 'b' |"
        self.assertTrue(self.parser.validate_grammar(valid_grammar))
        self.assertFalse(self.parser.validate_grammar(invalid_grammar))

if __name__ == '__main__':
    unittest.main()