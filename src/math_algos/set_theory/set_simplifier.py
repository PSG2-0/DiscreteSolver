from sympy import symbols, simplify_logic
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

class SetSimplifier:
    def __init__(self):
        self.transformations = standard_transformations + (implicit_multiplication_application,)
        self.replacements = {
            '∩': '&',
            '∪': '|',
            '\\': '& ~',
            'not(': '~(',
            '∅': 'False',
            'U': 'True',
            '∆': '^'
        }
        self.reverse_replacements = {
            '&': '∩',
            '|': '∪',
            '& ~': '\\',
            '~': 'not ',
            'False': '∅',
            'True': 'U',
            '^': '∆'
        }

    def transform(self, input_expr):
        for old, new in self.replacements.items():
            input_expr = input_expr.replace(old, new)
        return input_expr

    def simplify_expression(self, expr_str):
        expr_str = self.transform(expr_str)
        expr = parse_expr(expr_str, transformations=self.transformations)
        simplified_expr = simplify_logic(expr, form='dnf', force=True)
        return simplified_expr

    def reverse_transform(self, simplified_expr):
        reversed_str = str(simplified_expr)
        for old, new in self.reverse_replacements.items():
            reversed_str = reversed_str.replace(old, new)
        reversed_str = re.sub(r'~\(?([A-Za-z0-9_]+)\)?', r'not(\1)', reversed_str)
        reversed_str = re.sub(r'not ([A-Za-z0-9_]+)', r'not(\1)', reversed_str)
        return reversed_str