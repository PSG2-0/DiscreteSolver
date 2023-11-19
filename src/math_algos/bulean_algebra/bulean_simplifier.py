from sympy import symbols, simplify_logic, Or, And, Not, Nand, Nor
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

class LogicSimplifier:
    def __init__(self):
        self.transformations = standard_transformations + (implicit_multiplication_application,)

    def extract_variables(self, expr_str):
        return set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expr_str))

    def simplify_expression(self, expr_str):
        variables = self.extract_variables(expr_str)
        sympy_symbols = {var: symbols(var) for var in variables}
        local_dict = sympy_symbols.copy()

        expr_str = expr_str.replace('∧', '&').replace('∨', '|')
        expr_str = expr_str.replace('⊕', '^').replace('=', '==').replace('¬', '~')
        expr_str = expr_str.replace('←', '<<').replace('→', '>>').replace('↑', 'Nand')

        expr_str = re.sub(r'(\b\w+)\s*↓\s*(\b\w+)', r'Nor(\1, \2)', expr_str)

        expr = parse_expr(expr_str, transformations=self.transformations, local_dict=local_dict)
        simplified_expr = simplify_logic(expr, form='dnf', force=True)
        return simplified_expr

    def reverse_transform(self, simplified_expr):
        expr_str = str(simplified_expr)
        expr_str = expr_str.replace('&', '∧').replace('|', '∨')
        expr_str = expr_str.replace('^', '⊕').replace('Nor', '↓')
        expr_str = expr_str.replace('==', '=').replace('~', '¬')
        expr_str = expr_str.replace('<<', '←').replace('>>', '→')
        expr_str = expr_str.replace('Nand', '↑')

        return expr_str
