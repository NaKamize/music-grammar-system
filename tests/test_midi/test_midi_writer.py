import unittest
from src.midi.midi_writer import MidiWriter

class TestMidiWriter(unittest.TestCase):

    def setUp(self):
        self.midi_writer = MidiWriter()

    def test_write_midi(self):
        # Test writing a simple MIDI file
        music_data = [
            (60, 100, 480),  # Note on, pitch 60, velocity 100, duration 480 ticks
            (62, 100, 480),  # Note on, pitch 62, velocity 100, duration 480 ticks
            (64, 100, 480),  # Note on, pitch 64, velocity 100, duration 480 ticks
        ]
        file_path = 'test_output.mid'
        self.midi_writer.write_midi(music_data, file_path)
        # Verify that the file was created
        self.assertTrue(os.path.exists(file_path))

    def test_configure_midi(self):
        # Test configuring MIDI settings
        self.midi_writer.configure_midi(tempo=120, time_signature=(4, 4))
        self.assertEqual(self.midi_writer.tempo, 120)
        self.assertEqual(self.midi_writer.time_signature, (4, 4))

if __name__ == '__main__':
    unittest.main()