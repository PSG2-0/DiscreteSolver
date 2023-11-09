# calc_elements_of_set.py
from set_simplifier import SetSimplifier
import ast

class SetCalculator:
    def __init__(self):
        self.simplifier = SetSimplifier()
        self.replacements = {
            '∩': '&',
            '∪': '|',
            '\\': '-',
            '∅': 'set()',
            'U': 'set()',
            '∆': '^',
        }
        self.variable_values = {}

    def parse_variable_values(self, variable_values_str):
        pairs = variable_values_str.split(', ')
        for pair in pairs:
            key, value = pair.split('=')
            self.variable_values[key.strip()] = set(ast.literal_eval(value))

    def calculate(self, expr_str):
        simplified_expr = self.simplifier.simplify_expression(expr_str)
        reversed_expr = self.simplifier.reverse_transform(simplified_expr)
        final_set = self.evaluate_set_expression(reversed_expr)

        return '∅' if not final_set else final_set

    def evaluate_set_expression(self, expr_str):
        for var, value in self.variable_values.items():
            expr_str = expr_str.replace(var, f'set({value})')

        for old, new in self.replacements.items():
            expr_str = expr_str.replace(old, new)

        universal_set = self.determine_universal_set()

        expr_str = self.handle_not_operation(expr_str, universal_set)
        
        final_set = eval(expr_str)

        return final_set

    def determine_universal_set(self):
        return set().union(*self.variable_values.values())

    def handle_not_operation(self, expr_str, universal_set):
        while 'not(' in expr_str:
            start_index = expr_str.find('not(')
            end_index = start_index + 4
            nested_level = 1

            for i in range(end_index, len(expr_str)):
                if expr_str[i] == '(':
                    nested_level += 1
                elif expr_str[i] == ')':
                    nested_level -= 1
                if nested_level == 0:
                    end_index = i
                    break

            subset_str = expr_str[start_index + 4:end_index]
            subset = eval(subset_str)
            complement = universal_set - subset
            expr_str = expr_str[:start_index] + f'set({complement})' + expr_str[end_index + 1:]
            
        return expr_str