from decimal import Decimal, getcontext
from collections import defaultdict
import math
import heapq

getcontext().prec = 100

class Segment:
    def __init__(self, left, right, character=None):
        self.left = Decimal(left)
        self.right = Decimal(right)
        self.character = character

class ProbabilityCalculating:
    def __init__(self, string):
        self.string = string
        self.letter_counts = self.calculate_letter_counts(string)
        self.total_letters = Decimal(len(string))

    @staticmethod
    def calculate_letter_counts(string):
        counts = defaultdict(Decimal)
        for letter in string:
            counts[letter] += Decimal(1)
        return counts

    def get_probabilities(self):
        return {letter: count / self.total_letters for letter, count in sorted(self.letter_counts.items())}

class ArithmeticCoder:
    def __init__(self, probability_calculator):
        self.segments = self.define_segments(probability_calculator.get_probabilities())

    def define_segments(self, probabilities_dict):
        sorted_probabilities = sorted(probabilities_dict.items(), key=lambda x: (Decimal(x[1]), x[0]))
        segment_dict = {}
        left = Decimal(0)
        for letter, prob in sorted_probabilities:
            prob = Decimal(prob)
            segment_dict[letter] = Segment(left, left + prob, letter)
            left += prob
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

class FixedLengthCoding:
    def __init__(self, string):
        self.alphabet = sorted(list(set(string)))
        self.char_to_code = {}
        self.code_to_char = {}
        self.code_length = math.ceil(math.log2(len(self.alphabet)))
        self.generate_codes()

    def generate_codes(self):
        for i, char in enumerate(self.alphabet):
            binary_code = bin(i)[2:].zfill(self.code_length)
            self.char_to_code[char] = binary_code
            self.code_to_char[binary_code] = char

    def encode(self, string):
        return ''.join(self.char_to_code.get(char, '') for char in string)

    def decode(self, encoded_string):
        return ''.join(self.code_to_char[encoded_string[i:i + self.code_length]]
                       for i in range(0, len(encoded_string), self.code_length))

    def get_alphabet_list(self):
        return list(self.char_to_code.items())    
    
class ShennonFanoCoding:
    def __init__(self, probability_calculator):
        self.probability_calculator = probability_calculator
        self.sorted_symbols = sorted(zip(*probability_calculator.get_probabilities()), key=lambda x: (-x[1], -ord(x[0])))
        self.code_dict = self.create_codes()

    def split_into_parts(self, symbols):
        total = sum(weight for _, weight in symbols)
        running_sum = 0
        for i, (_, weight) in enumerate(symbols):
            running_sum += weight
            if running_sum * 2 >= total:
                return symbols[:i + 1], symbols[i + 1:]
        return symbols, []

    def create_code_tree(self, symbols, prefix=''):
        if not symbols:
            return {}

        if len(symbols) == 1:
            letter = symbols[0][0]
            return {letter: prefix}
        
        left, right = self.split_into_parts(symbols)
        code_dict = {}
        code_dict.update(self.create_code_tree(left, prefix + '0'))
        code_dict.update(self.create_code_tree(right, prefix + '1'))
        return code_dict

    def encode(self, string):
        return ''.join(self.code_dict[char] for char in string)

    @classmethod
    def recreate_from_codes(cls, codes):
        instance = cls(ProbabilityCalculating(''))
        instance.code_dict = codes
        return instance

    def decode(self, encoded_string):
        reverse_code_dict = {v: k for k, v in self.code_dict.items()}
        decoded_string = ''
        code = ''
        for bit in encoded_string:
            code += bit
            if code in reverse_code_dict:
                decoded_string += reverse_code_dict[code]
                code = ''
        return decoded_string

    def create_codes(self):
        return self.create_code_tree(self.sorted_symbols)

class HuffmanCoding:
    def __init__(self, probability_calculator):
        self.probability_calculator = probability_calculator
        self.letters, self.probabilities = probability_calculator.get_probabilities()
        self.root = self.build_huffman_tree()
        self.code_dict = self.build_huffman_code()

    @classmethod
    def recreate_from_codes(cls, codes):
        instance = cls(ProbabilityCalculating(''))
        instance.code_dict = codes
        return instance

    def calculate_letter_counts(self):
        self.letter_counts = {}
        for letter in self.string:
            if letter in self.letter_counts:
                self.letter_counts[letter] += Decimal(1)
            else:
                self.letter_counts[letter] = Decimal(1)

    class HuffmanNode:
        def __init__(self, char=None, freq=None, code=""):
            self.char = char
            self.freq = freq
            self.code = code
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def build_huffman_tree(self):
        heap = [self.HuffmanNode(char=char, freq=freq) for char, freq in zip(self.letters, self.probabilities)]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged_node = self.HuffmanNode(freq=left.freq + right.freq)
            merged_node.left = left
            merged_node.right = right
            merged_node.left.code = "0"
            merged_node.right.code = "1"

            heapq.heappush(heap, merged_node)

        return heap[0]

    def build_huffman_code(self, node=None, current_code="", code_dict=None):
        if node is None:
            node = self.root
        if code_dict is None:
            code_dict = {}

        if node.char is not None:
            code_dict[node.char] = current_code
        if node.left is not None:
            self.build_huffman_code(node.left, current_code + node.left.code, code_dict)
        if node.right is not None:
            self.build_huffman_code(node.right, current_code + node.right.code, code_dict)

        return code_dict

    def encode(self, string):
        encoded_string = ""
        for char in string:
            encoded_string += self.code_dict[char]
        return encoded_string

    def decode(self, encoded_string, codes):
        decoded_string = ""
        current_code = ""

        for bit in encoded_string:
            current_code += bit
            for char, code in codes.items():
                if current_code == code:
                    decoded_string += char
                    current_code = ""
                    break

        return decoded_string