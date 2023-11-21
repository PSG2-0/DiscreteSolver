import matplotlib.pyplot as plt
import networkx as nx

from io import BytesIO

class BinaryRelationGraph:
    def __init__(self, set_of_elements, binary_relation):
        if not set_of_elements:
            self.set_of_elements = {element for pair in binary_relation for element in pair}
        else:
            self.set_of_elements = set_of_elements
        self.binary_relation = binary_relation
        self.graph = nx.DiGraph()
        self._create_graph()

    def _create_set_of_elements(self, binary_relation):
        elements_set = {self._convert_to_number(element) 
                        for pair in binary_relation 
                        for element in pair}
        return elements_set


    def _convert_to_number(self, element):
        try:
            return int(element)
        except ValueError:
            return element

    def _create_relation_set(self, binary_relation):
        if isinstance(binary_relation, str):
            binary_relation = binary_relation.replace(" ", "")
            binary_relation = binary_relation.strip('()')
            binary_relation_list = binary_relation.split("),(")
            relation_set = set()
            for pair in binary_relation_list:
                elements = pair.split(',')
                try:
                    el1, el2 = int(elements[0]), int(elements[1])
                except ValueError:
                    el1, el2 = elements[0], elements[1]
                relation_set.add((el1, el2))
            return relation_set
        elif binary_relation:
            return set(binary_relation)
        else:
            return set()

    def _create_graph(self):
        for element in self.set_of_elements:
            self.graph.add_node(element)
            
        self.graph.add_edges_from(self.binary_relation)
        self.position = nx.spring_layout(self.graph, k=0.3, iterations=10)

    def get_image(self, node_color='skyblue', font_size=20):
        nx.draw(self.graph, self.position, with_labels=True, node_size=500, 
                node_color=node_color, font_size=font_size, font_weight='bold', arrowsize=15)
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)
        return img