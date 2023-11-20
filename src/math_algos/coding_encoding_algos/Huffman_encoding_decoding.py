import heapq
from decimal import Decimal
from collections import OrderedDict

class HuffmanCoding:
    def __init__(self, string=None, alphabet=None, probabilities=None):
        if string is not None:
            self.string = string
            self.total_letters = Decimal(len(string))
            self.calculate_letter_counts()
            self.letters, self.probabilities = self.get_probabilities()
            self.initial_length = len(string)
        elif alphabet is not None and probabilities is not None:
            self.string = None
            self.letters = alphabet
            self.probabilities = [Decimal(prob) for prob in probabilities]
            self.total_letters = sum(self.probabilities)
            self.initial_length = None

        self.root = self.build_huffman_tree()
        self.code_dict = self.build_huffman_code()

    @classmethod
    def recreate_from_alphabet_and_probabilities(cls, alphabet, probabilities):
        return cls(alphabet=alphabet, probabilities=probabilities)

    def calculate_letter_counts(self):
        self.letter_counts = {}
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