from mido import Message, MidiFile, MidiTrack
import re

class MidiWriter:
    def __init__(self, multi_string):
        self.multi_string = multi_string
        self.instrument_map = {
            "Violin": 40,
            "Cello": 42,
            "Flute": 73,
            "Piano": 0,
    }
        
    def normalize_instrument_name(self, name):
        match = re.match(r"([A-Za-z]+)", name)  # Extracts the base name (letters only)
        return match.group(1) if match else name  # Return the base name or the original name

    def get_program_number(self, instrument_name):
        normalized_name = self.normalize_instrument_name(instrument_name)
        return self.instrument_map.get(normalized_name, 0)
    
    def get_corrected_pitch(self, pitch, transpose):
        """Apply transposition to the pitch."""
        return pitch + transpose           

    def write_to_midi(self, output_file):
        """
        Writes the multi_string structure to a MIDI file.
        """
        midi_file = MidiFile()

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
            'pp': 35,
            'p': 45,
            'mp': 60,
            'mf': 75,
            'f': 90,
            'ff': 110,
            'fff': 125,
        }
        

        for instrument_index, (instrument_name, tracks) in enumerate(self.multi_string.items()):
            track = MidiTrack()
            midi_file.tracks.append(track)
            # Get the program number for the instrument
            program = self.get_program_number(instrument_name)
            
            # Add a program_change message
            track.append(Message('program_change', program=program, channel=instrument_index, time=0))
            print(f"Writing track for instrument: {instrument_name} (program {program})")
            
            octave_shift = 2 if "Piano_bass" == instrument_name else 4
            
            #self.write_notes_to_track(track, tracks, instrument_index)
            string_to_interpret = tracks['final_string'][0]
            for tone_rule in string_to_interpret:
                for tone in tone_rule:
                    if tone.tone is not None:                                
                        # Extract pitch, length, and dynamics
                        transpose = tone.operations.get('transpose', 1) if tone.operations != "none" else 0
                        pitch = self.get_corrected_pitch(pitch_map.get(tone.tone, 0), transpose) + (tone.octave + octave_shift) * 12 
                        length = length_map.get(tone.length, 480)
                        dynamics = dynamics_map.get(tone.dynamics, 64)
                        # Note on
                        track.append(Message('note_on', note=pitch, velocity=dynamics, channel=instrument_index, time=0))
                        # Note off after delay
                        track.append(Message('note_off', note=pitch, velocity=0, channel=instrument_index, time=length))
                    else:
                        # Handle chords
                        if tone.chord is not None:  # Ensure tone.chord is not None
                            for chord_tone in tone.chord:
                                # Extract pitch, length, and dynamics for each note in the chord
                                transpose = tone.operations.get('transpose', 1) if tone.operations != "none" else 0
                                pitch = self.get_corrected_pitch(pitch_map.get(chord_tone, 0), transpose) + (1 + octave_shift) * 12
                                length = length_map.get(tone.length, 480)
                                dynamics = dynamics_map.get(tone.dynamics, 64)

                                # Add note_on and note_off messages for each note in the chord
                                # Set time=0 for all note_on messages in the chord to play them simultaneously
                                track.append(Message('note_on', note=pitch, velocity=dynamics, channel=instrument_index, time=0))
                            
                            # Add note_off messages for all notes in the chord after the specified duration
                            for i, chord_tone in enumerate(tone.chord):
                                pitch = pitch_map.get(chord_tone, 0) + (1 + octave_shift) * 12
                                track.append(Message('note_off', note=pitch, velocity=64, channel=instrument_index, time=length if i == 0 else 0))

            

        # Save the MIDI file
        midi_file.save(output_file)
        print(f"MIDI file written to {output_file}")