from mido import Message, MidiFile, MidiTrack

class MidiWriter:
    def __init__(self, multi_string):
        self.multi_string = multi_string

    def write_to_midi(self, output_file):
        """
        Writes the multi_string structure to a MIDI file.
        """
        midi_file = MidiFile()
        print(self.multi_string)

        # Define mappings for pitch, length, and dynamics
        pitch_map = {
            'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
            'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
        }
        length_map = {
            'whole': 1920,  # 4 beats
            'half': 960,    # 2 beats
            'quarter': 480, # 1 beat
            'eighth': 240,  # 1/2 beat
            'sixteenth': 120 # 1/4 beat
        }
        dynamics_map = {
            'piano': 40,
            'mezo-forte': 64,
            'forte': 100
        }

        for instrument_index, instrument_tracks in enumerate(self.multi_string['violin']['final_string']):
            track = MidiTrack()
            track_name = f"Instrument {instrument_index + 1}"
            track.append(Message('program_change', program=instrument_index, time=0))
            midi_file.tracks.append(track)
            print("======================")
            print(instrument_tracks)

            for tone_rule_group in instrument_tracks:
                for tone_rule in tone_rule_group:
                    print(tone_rule)
                    if tone_rule.tone is not None:
                        # Convert ToneRule to MIDI note information
                        pitch_name = tone_rule.tone[:-1]  # Extract pitch (e.g., "C" from "C4")
                        octave = int(tone_rule.tone[-1])  # Extract octave (e.g., "4" from "C4")
                        pitch = pitch_map[pitch_name] + (octave + 1) * 12  # Calculate MIDI pitch number

                        length = length_map.get(tone_rule.length, 480)  # Default to quarter note
                        velocity = dynamics_map.get(tone_rule.dynamics, 64)  # Default to mezo-forte

                        # Add note_on and note_off messages
                        track.append(Message('note_on', note=pitch, velocity=velocity, time=0))
                        track.append(Message('note_off', note=pitch, velocity=0, time=length))
                    else:
                        # Handle chord (if needed in the future)
                        pass

        # Save the MIDI file
        midi_file.save(output_file)
        print(f"MIDI file written to {output_file}")