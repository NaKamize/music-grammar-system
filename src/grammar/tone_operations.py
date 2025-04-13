import random

class ToneOperator:    
    @staticmethod
    def counterpoint(note):
        # Basic mapping of note names to semitone values in C major
        note_to_semitone = {
            "C": 0, "D": 2, "E": 4, "F": 5,
            "G": 7, "A": 9, "B": 11
        }
        semitone_to_note = {v: k for k, v in note_to_semitone.items()}

        # Allowed consonant intervals (in semitones)
        consonant_intervals = [3, 4, 7, 8, 9, 12]  # m3, M3, P5, m6, M6, P8


        base_semitone = note_to_semitone.get(note.upper())
        if base_semitone is None:
            raise ValueError(f"Unknown note: {note}")

        # Try all consonant intervals above the melody note
        possible_notes = []
        for interval in consonant_intervals:
            cp_semitone = (base_semitone + interval) % 12
            if cp_semitone in semitone_to_note:
                possible_notes.append(semitone_to_note[cp_semitone])

        # Pick one possible counterpoint note at random
        if possible_notes:
            chosen = random.choice(possible_notes)
        else:
            chosen = "?"  # fallback

        return chosen
