from sympy import symbols, simplify_logic
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

class LogicSimplifier:
    def __init__(self):
        self.transformations = standard_transformations + (implicit_multiplication_application,)

    def extract_variables(self, expr_str):
        return set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expr_str))

    def simplify_expression(self, expr_str):
        variables = self.extract_variables(expr_str)
        sympy_symbols = {var: symbols(var) for var in variables}
        local_dict = sympy_symbols.copy()

        expr_str = expr_str.replace('∧', '&').replace('∨', '|').replace('⊕', '^').replace('¬', '~')
        expr_str = expr_str.replace('←', '<<').replace('→', '>>')
        expr_str = expr_str.replace('≡', '==')

        expr_str = re.sub(r'(\b\w+)\s*==\s*(\b\w+)', r'Equivalent(\1, \2)', expr_str)
        expr_str = re.sub(r'(\b\w+)\s*↓\s*(\b\w+)', r'Not(Or(\1, \2))', expr_str)
        expr_str = re.sub(r'(\b\w+)\s*↑\s*(\b\w+)', r'Not(And(\1, \2))', expr_str)

        try:
            expr = parse_expr(expr_str, transformations=self.transformations, local_dict=local_dict)
            simplified_expr = simplify_logic(expr, form='dnf', force=True)
            return simplified_expr
        except Exception as e:
            print(f"Error parsing expression: {expr_str}")
            raise e

    def reverse_transform(self, simplified_expr):
        expr_str = str(simplified_expr)
        expr_str = expr_str.replace('&', '∧').replace('|', '∨')
        expr_str = expr_str.replace('^', '⊕').replace('Nor', '↓')
        expr_str = expr_str.replace('==', '≡').replace('~', '¬')
        expr_str = expr_str.replace('<<', '←').replace('>>', '→')
        expr_str = expr_str.replace('Nand', '↑')

        return expr_str

class TruthTableGenerator:
    def __init__(self, expression):
        self.expression = expression
        self.simplifier = LogicSimplifier()

    def generate_truth_table(self):
        simplified_expr = self.simplifier.simplify_expression(self.expression)
        variables = sorted(self.simplifier.extract_variables(self.expression))
        rows = list(product([False, True], repeat=len(variables)))
        results = []

        for row in rows:
            local_dict = dict(zip(variables, row))
            result = simplified_expr.subs(local_dict)
            results.append(result)

        return variables, rows, results

    @staticmethod
    def boolean_to_int(value):
        return 1 if value else 0

    def create_truth_table_image(self):
        variables, rows, results = self.generate_truth_table()
        data = []

        for row in rows:
            data.append([self.boolean_to_int(val) for val in row] + [self.boolean_to_int(results[len(data)])])

        fig, ax = plt.subplots()
        data = np.array(data)
        ax.axis('tight')
        ax.axis('off')

        table = ax.table(cellText=data, colLabels=variables + [self.expression], cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.05)
        plt.close(fig)
        buffer.seek(0)

        return buffer