from itertools import product
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from ..bulean_algebra.bulean_simplifier import LogicSimplifier

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