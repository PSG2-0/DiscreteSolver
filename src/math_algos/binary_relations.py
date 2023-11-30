from abc import ABC
from io import BytesIO
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx


class BinaryRelation(ABC):
    set_of_elements: set[str | int]
    binary_relation = set[tuple[str | int, str | int]]

    def __init__(
        self,
        set_of_elements: Optional[set[str | int]],
        binary_relation: set[tuple[str | int, str | int]],
    ):
        if not set_of_elements:
            self.set_of_elements = set(
                element for pair in binary_relation for element in pair
            )
        else:
            self.set_of_elements = set_of_elements
        self.binary_relation = binary_relation


class BinaryRelationProperties(BinaryRelation):
    def check_reflexive_property(self):
        is_reflexive = all((e, e) in self.binary_relation for e in self.set_of_elements)
        is_antireflexive = all(
            (e, e) not in self.binary_relation for e in self.set_of_elements
        )
        is_nonreflexive = not is_reflexive and not is_antireflexive

        return {
            "Рефлексивно": is_reflexive,
            "Антирефлексивно": is_antireflexive,
            "Нерефлексивно": is_nonreflexive,
        }

    def check_symmetry_properties(self):
        is_symmetric = all(
            (b, a) in self.binary_relation for a, b in self.binary_relation
        )
        is_asymmetric = all(
            (b, a) not in self.binary_relation for a, b in self.binary_relation
        )
        is_antisymmetric = all(
            (b, a) not in self.binary_relation or a == b
            for a, b in self.binary_relation
        )
        is_nonsymmetric = not is_symmetric and not is_antisymmetric

        return {
            "Симметрично": is_symmetric,
            "Асимметрично": is_asymmetric,
            "Антисимметрично": is_antisymmetric,
            "Несимметрично": is_nonsymmetric,
        }

    def check_transitivity_properties(self):
        is_transitive = True
        for a, b in self.binary_relation:
            for c, d in self.binary_relation:
                if b == c and (a, d) not in self.binary_relation:
                    is_transitive = False
                    break

        is_antitransitive = all(
            (a, d) not in self.binary_relation
            for a, b in self.binary_relation
            for c, d in self.binary_relation
            if b == c and a != d
        )

        is_nontransitive = not is_transitive and not is_antitransitive

        return {
            "Транзитивно": is_transitive,
            "Антитранзитивно": is_antitransitive,
            "Нетранзитивно": is_nontransitive,
        }

    def get_properties_as_list(self) -> list[str]:
        properties_list = []
        reflexive_properties = self.check_reflexive_property()
        symmetry_properties = self.check_symmetry_properties()
        transitive_properties = self.check_transitivity_properties()

        for property_name, is_true in reflexive_properties.items():
            if is_true:
                properties_list.append(property_name)

        for property_name, is_true in symmetry_properties.items():
            if is_true:
                properties_list.append(property_name)

        for property_name, is_true in transitive_properties.items():
            if is_true:
                properties_list.append(property_name)

        return properties_list


class BinaryRelationGraph(BinaryRelation):
    def __init__(
        self,
        set_of_elements: Optional[set[str | int]],
        binary_relation: set[tuple[str | int, str | int]],
    ):
        super().__init__(set_of_elements, binary_relation)
        self.graph = nx.DiGraph()
        self._create_graph()

    def _create_graph(self):
        for element in self.set_of_elements:
            self.graph.add_node(element)

        self.graph.add_edges_from(self.binary_relation)
        self.position = nx.spring_layout(self.graph, k=0.3, iterations=10)

    def get_image(self, node_color="skyblue", font_size=20):
        nx.draw(
            self.graph,
            self.position,
            with_labels=True,
            node_size=500,
            node_color=node_color,
            font_size=font_size,
            font_weight="bold",
            arrowsize=15,
        )
        img = BytesIO()
        plt.savefig(img, format="png")
        plt.clf()
        img.seek(0)
        return img
