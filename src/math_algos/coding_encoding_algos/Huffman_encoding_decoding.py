import heapq
from decimal import Decimal

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

class HuffmanNode:
    def __init__(self, char=None, freq=None, code=""):
        self.char = char
        self.freq = freq
        self.code = code
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(letters, probabilities):
    heap = [HuffmanNode(char=char, freq=freq) for char, freq in zip(letters, probabilities)]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged_node = HuffmanNode(freq=left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right

        # Сохраняем коды в узлах
        merged_node.left.code = "0"
        merged_node.right.code = "1"

        heapq.heappush(heap, merged_node)

    return heap[0]

def build_huffman_code(node, current_code="", code_dict=None):
    if code_dict is None:
        code_dict = {}

    if node.char is not None:
        code_dict[node.char] = current_code
    if node.left is not None:
        build_huffman_code(node.left, current_code + node.left.code, code_dict)
    if node.right is not None:
        build_huffman_code(node.right, current_code + node.right.code, code_dict)

    return code_dict

class HuffmanCoder:
    def __init__(self, letters, probabilities):
        self.root = build_huffman_tree(letters, probabilities)
        self.code_dict = build_huffman_code(self.root)
        self.letters = letters
        self.initial_length = len(string)

    def encode(self, string):
        encoded_string = ""
        for char in string:
            encoded_string += self.code_dict[char]
        return encoded_string

    def decode(self, encoded_string):
        decoded_string = ""
        current_node = self.root

        for bit in encoded_string:
            if bit == "0":
                current_node = current_node.left
            elif bit == "1":
                current_node = current_node.right

            if current_node.char is not None:
                decoded_string += current_node.char
                current_node = self.root

        return decoded_string

    def print_info(self):
        print("Alphabet:")
        for letter in self.letters:
            print(f"{letter}: {self.code_dict[letter]}")
        print("Initial String Length:", self.initial_length)
