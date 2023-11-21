class ShennonFanoCoding:
    def __init__(self, string):
        self.string = string
        self.alphabet, self.probabilities = self.calculate_probabilities()
        self.sorted_symbols = sorted(zip(self.alphabet, self.probabilities), key=lambda x: x[1], reverse=True)
        self.code_dict = self.create_codes()

    def calculate_probabilities(self):
        letter_counts = {}
        for letter in self.string:
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
        total_letters = len(self.string)
        alphabet = list(letter_counts.keys())
        probabilities = [count / total_letters for count in letter_counts.values()]
        return alphabet, probabilities

    def split_into_parts(self, symbols):
        total = sum(weight for _, weight in symbols)
        running_sum = 0
        for i, (_, weight) in enumerate(symbols):
            running_sum += weight
            if running_sum >= total / 2:
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