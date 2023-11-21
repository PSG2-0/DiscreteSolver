import requests
from urllib.parse import quote

from ..set_theory.set_simplifier import SetSimplifier

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
                        image_url = pod['subpods'][0]['img']['src']
                        return image_url
                return "Cant build diagram"
            else:
                return "Error with data"
        else:
            return "Error of request"