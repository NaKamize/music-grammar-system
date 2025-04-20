from music21 import chord, pitch, interval, note

class NeoRiemannian:
    def __init__(self, chord_notes):
        self.ch = chord.Chord(chord_notes)
        self.root = self.ch.root()
        self.quality = self.ch.quality  # 'major' or 'minor'

    def P(self):
        """Parallel: major → minor, minor → major"""
        new_quality = 'minor' if self.quality == 'major' else 'major'
        return self.build_from_root_and_quality(self.root, new_quality)

    def R(self):
        """Relative: major → relative minor, minor → relative major"""
        if self.quality == 'major':
            # relative minor is down a minor third from root
            new_root = self.root.transpose('-m3')
            return self.build_from_root_and_quality(new_root, 'minor')
        else:
            # relative major is up a minor third from root
            new_root = self.root.transpose('m3')
            return self.build_from_root_and_quality(new_root, 'major')

    def L(self):
        """Leading-tone exchange: major → minor with root a major third up, and vice versa"""
        if self.quality == 'major':
            new_root = self.root.transpose('M3')
            return self.build_from_root_and_quality(new_root, 'minor')
        else:
            new_root = self.root.transpose('-M3')
            return self.build_from_root_and_quality(new_root, 'major')

    def build_from_root_and_quality(self, root_note, quality):
        """Construct a chord from root and quality"""
        if quality == 'major':
            third = root_note.transpose('M3')
        else:
            third = root_note.transpose('m3')
        fifth = root_note.transpose('P5')
        return chord.Chord([root_note, third, fifth])
    
    @staticmethod
    def normalize_pitch_name(p):
        """
        Normalize pitch names by converting double flats (--) or double sharps (##)
        to their enharmonic equivalents if possible.
        """
        if '--' in p.name:
            return p.getEnharmonic().name  # Convert double flat to enharmonic equivalent
        elif '##' in p.name:
            return p.getEnharmonic().name  # Convert double sharp to enharmonic equivalent
        return p.name  # Return the original name if no conversion is needed

    @staticmethod
    def chord_id(ch):
        """
        Return a transposition-invariant ID (e.g., pitch class set as tuple),
        with normalization for double flats and double sharps.
        """
        normalized_pitches = [p.pitchClass for p in ch.pitches]
        normalized_names = [NeoRiemannian.normalize_pitch_name(p) for p in ch.pitches]
        print(f"Normalized pitches: {normalized_names}")
        return tuple(sorted(normalized_pitches))

    def print_chord(self, ch, step):
        """
        Prints the chord with normalized pitch names and the step number.
        """
        normalized_names = [self.normalize_pitch_name(p) for p in ch.pitches]
        print(f"{step}. {ch.commonName}: {normalized_names}")