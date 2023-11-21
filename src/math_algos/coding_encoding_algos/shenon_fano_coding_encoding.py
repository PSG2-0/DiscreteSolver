class ShennonFanoCoding:
    def __init__(self, string):
        self.string = string
        self.alphabet, self.frequencies = self.calculate_frequencies()
        self.sorted_symbols = sorted(zip(self.alphabet, self.frequencies), key=lambda x: (-x[1], -ord(x[0])))
        self.code_dict = self.create_codes()

    def calculate_frequencies(self):
        freq = {}
        for symbol in self.string:
            freq[symbol] = freq.get(symbol, 0) + 1
        total_chars = len(self.string)
        alphabet = list(freq.keys())
        frequencies = [freq[symbol] for symbol in alphabet]
        return alphabet, frequencies

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

    def encode(self):
        return ''.join(self.code_dict[char] for char in self.string)

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