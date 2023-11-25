from sympy import symbols, simplify_logic
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re
import requests
from urllib.parse import quote

class SetSimplifier:
    def __init__(self):
        self.transformations = standard_transformations + (implicit_multiplication_application,)
        self.replacements = {
            '∩': '&',
            '∪': '|',
            '\\': '& ~',
            'not ': '~',
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
        input_expr = input_expr.replace('not(', '~(')
        for old, new in self.replacements.items():
            input_expr = input_expr.replace(old, new)
        return input_expr

    def simplify_expression(self, expr_str):
        expr_str = self.transform(expr_str)

        all_symbols = set(re.findall(r'\b[A-Za-z]+\b', expr_str))
        symbols_dict = {s: symbols(s) for s in all_symbols}
        
        expr = parse_expr(expr_str, local_dict=symbols_dict, transformations=self.transformations)
        simplified_expr = simplify_logic(expr, form='dnf', force=True)

        return self.reverse_transform(simplified_expr)

    def reverse_transform(self, simplified_expr):
        reversed_str = str(simplified_expr)
        for old, new in self.reverse_replacements.items():
            reversed_str = reversed_str.replace(old, new)
        reversed_str = re.sub(r'~\(?([A-Za-z0-9_]+)\)?', r'not(\1)', reversed_str)
        reversed_str = re.sub(r'not\s+(\b[A-Za-z0-9_]+\b)', r'not(\1)', reversed_str)
        return reversed_str

class VennDiagramBuilder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.simplifier = SetSimplifier()

    def build_diagram(self, expression):
        simplified_expr = self.simplifier.simplify_expression(expression)
        transformed_expr = self.simplifier.reverse_transform(simplified_expr)

        venn_query = f"Venn diagram of {transformed_expr}"

        encoded_query = quote(venn_query)

        query = f"http://api.wolframalpha.com/v2/query?input={encoded_query}&format=image&output=JSON&appid={self.api_key}"
        
        response = requests.get(query)
        if response.status_code == 200:
            data = response.json()
            if 'pods' in data['queryresult']:
                for pod in data['queryresult']['pods']:
                    if 'Venn diagram' in pod['title']:
                        return pod['subpods'][0]['img']['src']
                raise ValueError("Error while collecting an image")
            else:
                raise ValueError("Error with data")
        else:
            raise ValueError("Error with request")