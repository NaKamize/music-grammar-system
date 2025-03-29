import unittest
from src.grammar.generator import Generator

class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = Generator()

    def test_generate_music(self):
        # Test the music generation functionality
        grammar_example = "some grammar example"
        midi_data = self.generator.generate_music(grammar_example)
        self.assertIsNotNone(midi_data)
        self.assertIsInstance(midi_data, bytes)  # Assuming MIDI data is returned as bytes

    def test_apply_grammar(self):
        # Test applying grammar to generate music
        grammar = "some grammar"
        result = self.generator.apply_grammar(grammar)
        self.assertTrue(result)  # Assuming apply_grammar returns a boolean indicating success

if __name__ == '__main__':
    unittest.main()