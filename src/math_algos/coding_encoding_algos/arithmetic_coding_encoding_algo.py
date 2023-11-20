from decimal import Decimal, getcontext

getcontext().prec = 500

class Segment:
    def __init__(self, left, right, character=None):
        self.left = Decimal(left)
        self.right = Decimal(right)
        self.character = character

class ProbabilityCalculating:
    def __init__(self, string):
        self.string = string
        self.letter_counts = {}
        self.total_letters = Decimal(len(string))
        self.calculate_letter_counts()
    
    def calculate_letter_counts(self):
        for letter in self.string:
            if letter in self.letter_counts:
                self.letter_counts[letter] += Decimal(1)
            else:
                self.letter_counts[letter] = Decimal(1)

    def get_probabilities(self):
        sorted_letters_counts = sorted(self.letter_counts.items())
        letters = [letter for letter, _ in sorted_letters_counts]
        probabilities = [Decimal(count) / self.total_letters for _, count in sorted_letters_counts]
        return letters, probabilities

class ArithmeticCoder:
    def __init__(self, letters, probabilities):
        self.segments = self.define_segments(letters, probabilities)

    def define_segments(self, letters, probabilities):
        segment_dict = {}
        left = Decimal(0)
        for letter, prob in zip(letters, probabilities):
            segment_dict[letter] = Segment(left, left + prob, letter)
            left = segment_dict[letter].right
        return segment_dict

    def encode(self, string):
        left, right = Decimal(0), Decimal(1)
        for symb in string:
            segment = self.segments[symb]
            new_right = left + (right - left) * segment.right
            new_left = left + (right - left) * segment.left
            left, right = new_left, new_right
        return (left + right) / 2

    def decode(self, code, length):
        code = Decimal(code)
        result = ""
        for _ in range(length):
            for segment in self.segments.values():
                if segment.left <= code < segment.right:
                    result += segment.character
                    code = (code - segment.left) / (segment.right - segment.left)
                    break
        return result