import math

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