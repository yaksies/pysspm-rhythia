"""
Collection of items I created that I thought I might import into the library in case anyone finds them useful
"""
import numpy as np
from collections import defaultdict
import math
from pysspm import SSPMParser

def calcObsiidRating(self: SSPMParser, notes: list = None) -> SSPMParser:
    """
    calculates difficulty by using Obsiids difficulty calculation.
    This method is essentially just the dot product of the notes
    """

    print(self.Notes[1:5])

    if not notes: # if we pass in notes
        pass
    raise NotImplementedError("CalcObsiidRating function is a W.I.P.")

    return self


def calcPPRating(self: SSPMParser) -> float:
    """
    This calculation method is the method used in rhythia-online. | May change in future updates
    """
    return len(self.Notes) / 100 

def calcStarRating(self: SSPMParser) -> float:
    """
    # Pseudo-code outline:

    - get notes [0, 0, 100, 1, 0, 150]
    - apply exponential decay (of some sorts)
    """

class NoteClassifier:
    def __init__(self, notes, time_multiplier=5):
        self.notes = sorted(notes, key=lambda n: n[2])  # Sort by time
        self.time_multiplier = time_multiplier
        self.vectors = self.compute_vectors()
        #print(self.vectors[0:500])

        self.patterns = []
        #self.classified_notes = set()

    def classify_patterns(self):
        self.detect_sequences()
        return self.patterns
        #return dict(self.patterns)

    def compute_vectors(self):
        """Compute the movement vectors between consecutive notes."""
        vectors = []
        for i in range(1, len(self.notes)):
            x1, y1, t1 = self.notes[i-1]
            x2, y2, t2 = self.notes[i]
            vector = (abs(x2 - x1), abs(y2 - y1), abs(t2 - t1), round(math.hypot((x2 - x1), abs(y2 - y1)), 2))# max((x2 - x1), abs(y2 - y1)))#  # |(dx, dy, dt, dxy)| = |(dx, dy, dt, math.sqrt((p*p)+(b*b)))|
            vectors.append(vector) # last one should always go up but if it doesnt then whatever
        return vectors
    
    def detect_sequences(self, maxjumpcount=2, maxspiralcount=3):
        vectors = self.vectors
        notes = self.notes

        jumpcount = 0
        spiralcount = 0
        brokenspiral = bool
        vectorBuffer = []
        detectingJumpstream = None  # Track whether we're detecting jumpstream or spiralstream

        current_pattern_type = None  # Track the current pattern (jumpstream/spiral)
        current_pattern_notes = []  # To store the sequence of notes for the current pattern

        i = 0
        while i < len(vectors):
            dx, dy, dt, dxy = vectors[i]

            if detectingJumpstream is None:
                detectingJumpstream = dxy > 1  # Set initial detection mode based on dxy

            if detectingJumpstream:
                # We're detecting a jumpstream
                if dxy > 1.5:
                    jumpcount += 1
                    spiralcount = 0
                elif dxy < 0.1: # stack notes | W.I.P
                    spiralcount += 1
                    jumpcount = 0
                else:
                    spiralcount += 1
                    jumpcount = 0

                vectorBuffer.append((dx, dy, dt, dxy))
                current_pattern_notes.append(notes[i])

                if spiralcount >= maxspiralcount:
                    # End of a jumpstream and beginning of a spiralstream
                    self.patterns.append(("jumpstream", current_pattern_notes[:-spiralcount]))
                    current_pattern_notes = current_pattern_notes[-spiralcount:]  # Move to spiral
                    vectorBuffer = []
                    detectingJumpstream = False
                    brokenspiral = False
                    jumpcount = 0
                    spiralcount = 0
            else:
                # We're detecting a spiralstream
                if dxy <= 1.5:
                    spiralcount += 1
                    if jumpcount != 0:
                        brokenspiral = True
                    if jumpcount != 0 and len(vectorBuffer) < 5: # max slide Ill allow
                        self.patterns.append(("slide", current_pattern_notes[:-jumpcount]))
                        current_pattern_notes = current_pattern_notes[-jumpcount:]  # Move to jumpstream
                        vectorBuffer = []
                        detectingJumpstream = True
                        brokenspiral = False
                        jumpcount = 0
                        spiralcount = 0
                    print(jumpcount, vectorBuffer)
                    jumpcount = 0
                else:
                    jumpcount += 1
                    spiralcount = 0

                vectorBuffer.append((dx, dy, dt, dxy))
                current_pattern_notes.append(notes[i])

                if jumpcount >= maxjumpcount:
                    # End of a spiralstream and beginning of a jumpstream
                    self.patterns.append(("spiral", current_pattern_notes[:-jumpcount]) if not brokenspiral else ("broken_spiral", current_pattern_notes[:-jumpcount]))
                    current_pattern_notes = current_pattern_notes[-jumpcount:]  # Move to jumpstream
                    vectorBuffer = []
                    detectingJumpstream = True
                    brokenspiral = False
                    jumpcount = 0
                    spiralcount = 0



            i += 1

        # Add the last detected pattern at the end of the loop
        if current_pattern_notes:
            if detectingJumpstream:
                self.patterns.append(("jumpstream", current_pattern_notes))
            else:
                self.patterns.append(("spiral", current_pattern_notes))

        return self.patterns
    
    def detect_off_grid(self): # keeping for reference
        off_grid = [note for note in self.notes if not (isinstance(note[0], int) and isinstance(note[1], int))]
        if off_grid:
            self.patterns['off_grid'] = [off_grid]
            self.classified_notes.update(off_grid)

    """
    def get_pattern_prevalence(self):
        total_notes = sum(len(seq) for seqs in self.patterns.values() for seq in seqs)
        return {pattern: sum(len(seq) for seq in seqs) / total_notes 
                for pattern, seqs in self.patterns.items()}
    """
    
    def get_pattern_prevalence(self):
        total_notes = sum(len(seq) for _, seq in self.patterns)
        pattern_counts = {}
        for pattern, seq in self.patterns:
            if pattern not in pattern_counts:
                pattern_counts[pattern] = 0
            pattern_counts[pattern] += len(seq)
        return {pattern: count / total_notes for pattern, count in pattern_counts.items()}


if __name__ == "__main__":
    from pysspm_rhythia import SSPMParser

    parser = SSPMParser()
    parser.ReadSSPM(r"C:/Users/david/AppData/Roaming/SoundSpacePlus/maps/Rhythia-Gen_DigitalDemon_AITEST_-_DAI_V3.sspm")

    classifier = NoteClassifier(parser.Notes, time_multiplier=1)
    patterns = classifier.classify_patterns()
    print(patterns)

    print("Detected Patterns with Notes:")
    with open("./tests/classificationtest.txt", "w") as f:
        for pattern_type, sequence in patterns:
            f.write(f"{pattern_type}:\n")
            for note in sequence:
                f.write(f"  {note}\n")
            f.write(f"Sequence length: {len(sequence)}\n")
        f.write(f"Total patterns detected: {len(patterns)}\n")

        prevalence = classifier.get_pattern_prevalence()
        f.write(f"-----------------\n Prevalence: {prevalence}\n")
        f.write(f"Length of Notes: {len(parser.Notes)}\n")
        f.write("Length of pattern notes: " + ", ".join([f"{pattern}: {len(set(seq))}" for pattern, seq in patterns]) + "\n")
        #f.write(f"Total unique classified notes: {len(classifier.classified_notes)}\n\n")

        f.write("Note classifications:\n")
        for note in parser.Notes:
            classifications = [pattern for pattern, seq in patterns if note in seq]
            f.write(f"  {note}: {', '.join(classifications)}\n")

    print("Prevalence:", prevalence)
    #print(f"Total notes: {len(parser.Notes)}, Unique classified notes: {len(classifier.classified_notes)}")


    #assert 1==1

    COLORS = {
        "vibro": "#FF0000", 
        "off_grid": "#FF00FF", 
        "star": "#E300E3", 
        "jumpstream": "#FFFFFF", 
        "slide": "#FFFF00", 
        "broken_spiral": "#00FF00", 
        "spiral": "#00FFFF",
        "complex": "#00FF00"
    }

    with open(r"C:\Users\david\AppData\Roaming\SoundSpacePlus\colorsets\whatwedidinthedessertvisiontest.txt", "w") as f:
        f.write(COLORS.get(patterns[0][0], '#000000'))
        for pattern_type, note_sequence in patterns:
            # Get the color based on the current pattern type
            color = COLORS.get(pattern_type, '#000000')
            
            # Cycle through the notes in this pattern
            for note in note_sequence:
                f.write(f"\n{color}")
