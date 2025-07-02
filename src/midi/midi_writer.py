from mido import Message, MidiFile, MidiTrack, MetaMessage
from utils.neo_riemann import NeoRiemannian

import re

class MidiWriter:
    def __init__(self, multi_string):
        self.multi_string = multi_string
        self.instrument_map = {
            "Violin": 40,
            "Cello": 42,
            "Flute": 73,
            "Piano": 0,
            "Guitar": 24,
            "Trumpet": 56,
            "Saxophone": 65,
            "Clarinet": 71,
            "Trombone": 57,
            "Accordion": 21,
            "Bass": 32
        }
        
        self.key_signature = "C"  
        
    def normalize_instrument_name(self, name):
        match = re.match(r"([A-Za-z]+)", name)
        return match.group(1) if match else name

    def get_program_number(self, instrument_name):
        normalized_name = self.normalize_instrument_name(instrument_name)
        return self.instrument_map.get(normalized_name, 0)
    
    def get_corrected_pitch(self, pitch, transpose):
        """Apply transposition to the pitch."""
        return pitch + transpose        
    
    def handle_chord_with_transformations(self, tone, current_transformed_chord, transformation_sequence, transformation_index):
        if tone.operations != "none":
            op = tone.operations.get('neorieman', None)

            if op in ["P", "L", "R"]:
                # If there is a current transformed chord, apply the operation to it
                if current_transformed_chord is None:
                    # Skip applying the transformation on the first chord
                    current_transformed_chord = tone.chord  # Start with the original chord
                else:
                    # Create a NeoRiemannian object with the current transformed chord
                    transformer = NeoRiemannian(current_transformed_chord)

                    # Dynamically call the method based on the current transformation in the sequence
                    transformation_function = getattr(transformer, op, None)
                    if transformation_function:
                        transformed_chord = transformation_function()  # Call the method
                        # Update the current transformed chord and normalize the pitch names
                        current_transformed_chord = [NeoRiemannian.normalize_pitch_name(p) for p in transformed_chord.pitches]

                        # Move to the next transformation in the sequence
                        transformation_index = (transformation_index + 1) % len(transformation_sequence)
                    else:
                        raise ValueError(f"Invalid Neo-Riemannian operation: {op}")
            else:
                # Reset the transformed chord and transformation sequence if the operation is not Neo-Riemannian
                current_transformed_chord = None
                transformation_index = 0

        return current_transformed_chord, transformation_index   

    def write_to_midi(self, output_file):
        """
        Writes the multi_string structure to a MIDI file.
        """
        midi_file = MidiFile()

        pitch_map = {
            'C': 0, 'C#': 1, 'D-': 1, 'D': 2, 'D#': 3, 'E-': 3, 'E': 4, 'F': 5,
            'F#': 6, 'G-': 6, 'G': 7, 'G#': 8, 'A-': 8, 'A': 9, 'A#': 10, 'B-': 10, 'B': 11
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
            key_signature = MetaMessage('key_signature', key=self.key_signature)
            track = MidiTrack()
            track.append(key_signature)
            midi_file.tracks.append(track)
            # Get the program number for the instrument
            program = self.get_program_number(instrument_name)
            
            # Add a program_change message
            track.append(Message('program_change', program=program, channel=instrument_index, time=0))
            
            # Initialize variables to track the current transformed chord and transformation sequence
            current_transformed_chord = None
            transformation_sequence = ["P", "L", "R"]  # Define the rotation sequence
            transformation_index = 0  # Start with the first transformation in the sequence
            
            string_to_interpret = tracks['final_string'][0]
            for tone_rule in string_to_interpret:
                for tone in tone_rule:
                    if tone.tone is not None:                                
                        # Extract pitch, length, and dynamics
                        transpose = tone.operations.get('transpose', 0) if tone.operations != "none" else 0
                        pitch = self.get_corrected_pitch(pitch_map.get(tone.tone, 0), transpose) + (tone.octave + 1) * 12
                        length = length_map.get(tone.length, 480)
                        dynamics = dynamics_map.get(tone.dynamics, 64)
                        # Note on
                        track.append(Message('note_on', note=pitch, velocity=dynamics, channel=instrument_index, time=0))
                        # Note off after delay
                        track.append(Message('note_off', note=pitch, velocity=0, channel=instrument_index, time=length))
                    else:
                        # Handle chords
                        if tone.chord is not None:
                            current_transformed_chord, transformation_index = self.handle_chord_with_transformations(
                                tone, current_transformed_chord, transformation_sequence, transformation_index
                            )
                                
                            chord_to_write = current_transformed_chord if current_transformed_chord else tone.chord
                            for chord_tone in chord_to_write:
                                # Extract pitch, length, and dynamics for each note in the chord
                                transpose = tone.operations.get('transpose', 0) if tone.operations != "none" else 0
                                pitch = self.get_corrected_pitch(pitch_map.get(chord_tone, 0), transpose) + (tone.octave + 1) * 12
                                length = length_map.get(tone.length, 480)
                                dynamics = dynamics_map.get(tone.dynamics, 64)

                                # Add note_on and note_off messages for each note in the chord
                                # Set time=0 for all note_on messages in the chord to play them simultaneously
                                track.append(Message('note_on', note=pitch, velocity=dynamics, channel=instrument_index, time=0))
                            
                            # Add note_off messages for all notes in the chord after the specified duration
                            for i, chord_tone in enumerate(chord_to_write):
                                pitch = pitch_map.get(chord_tone, 0) + (tone.octave + 1) * 12
                                track.append(Message('note_off', note=pitch, velocity=64, channel=instrument_index, time=length if i == 0 else 0))

            

        # Save the MIDI file
        midi_file.save(output_file)
        print(f"MIDI file written to {output_file}")