import unittest
from io import BytesIO

from src.math_algos.binary_relation.graph_generator import BinaryRelationGraph
from src.math_algos.binary_relation.properties_of_relation import BinaryRelation


class TestBinaryRelationGraph(unittest.TestCase):
    def test_initialization_with_non_empty_set(self):
        elements = {1, 2, 3}
        relation = {(1, 2), (2, 3)}
        graph = BinaryRelationGraph(elements, relation)
        self.assertEqual(graph.set_of_elements, elements)
        self.assertEqual(graph.binary_relation, relation)

    def test_initialization_with_empty_set(self):
        relation = {(1, 2), (2, 3)}
        graph = BinaryRelationGraph(set(), relation)
        self.assertEqual(graph.set_of_elements, {1, 2, 3})
        self.assertEqual(graph.binary_relation, relation)

    def test_graph_nodes_and_edges(self):
        elements = {1, 2, 3}
        relation = {(1, 2), (2, 3)}
        graph = BinaryRelationGraph(elements, relation)
        self.assertEqual(len(graph.graph.nodes), 3)
        self.assertEqual(len(graph.graph.edges), 2)

    def test_image_generation(self):
        graph = BinaryRelationGraph({1, 2}, {(1, 2)})
        img = graph.get_image()
        self.assertIsInstance(img, BytesIO)


class TestBinaryRelationProperties(unittest.TestCase):
    def test_initialization(self):
        relation = "1,2),(2,3"
        binary_relation = BinaryRelation(None, relation)
        self.assertEqual(binary_relation.relation_set, {(1, 2), (2, 3)})

    def test_reflexive_property(self):
        binary_relation = BinaryRelation(None, {(1, 1), (2, 2), (3, 3)})
        self.assertTrue(binary_relation.check_reflexive_property()["Рефлексивно"])

    def test_symmetry_properties(self):
        binary_relation = BinaryRelation(None, {(1, 2), (2, 1)})
        self.assertTrue(binary_relation.check_symmetry_properties()["Симметрично"])

    def test_transitivity_properties(self):
        binary_relation = BinaryRelation(None, {(1, 2), (2, 3), (1, 3)})
        self.assertTrue(binary_relation.check_transitivity_properties()["Транзитивно"])

    def test_properties_as_list(self):
        binary_relation = BinaryRelation(None, "1,2),(2,3),(1,3")
        properties = binary_relation.get_properties_as_list()
        self.assertIn("Транзитивно", properties)

    def test_first_set(self):
        elements = "1,2,3,4,5,6,7,8,9"
        relation = "(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(2,4),(2,6),(2,8),(3,6),(3,9),(4,8)"
        binary_relation = BinaryRelation(elements, relation)

        self.assertTrue(binary_relation.check_reflexive_property()["Рефлексивно"])
        self.assertTrue(binary_relation.check_symmetry_properties()["Антисимметрично"])
        self.assertTrue(binary_relation.check_transitivity_properties()["Транзитивно"])

    def test_second_set(self):
        elements = "1,2,3,4,5,6,7,8,9"
        relation = "(1,7),(7,1),(2,6),(6,2),(3,5),(5,3),(4,4)"
        binary_relation = BinaryRelation(elements, relation)

        self.assertTrue(binary_relation.check_reflexive_property()["Нерефлексивно"])
        self.assertTrue(binary_relation.check_symmetry_properties()["Симметрично"])
        self.assertTrue(
            binary_relation.check_transitivity_properties()["Антитранзитивно"]
        )

    def test_third_set(self):
        elements = "Алекскей,Иван,Петр,Александр,Павел,Андрей"
        relation = "(Алекскей,Алекскей),(Алекскей,Александр),(Алекскей,Андрей),(Александр,Александр),(Александр,Алекскей),(Александр,Андрей),(Андрей,Андрей),(Андрей,Алекскей),(Андрей,Александр),(Петр,Петр),(Петр,Павел),(Павел,Павел),(Павел,Петр),(Иван,Иван)"
        binary_relation = BinaryRelation(elements, relation)

        self.assertTrue(binary_relation.check_reflexive_property()["Рефлексивно"])
        self.assertTrue(binary_relation.check_symmetry_properties()["Симметрично"])
        self.assertTrue(binary_relation.check_transitivity_properties()["Транзитивно"])

    def test_fourth_set(self):
        elements = "1,2,3"
        relation = "(1,1),(2,2),(3,3),(3,2),(1,2),(2,1)"
        binary_relation = BinaryRelation(elements, relation)

        self.assertTrue(binary_relation.check_reflexive_property()["Рефлексивно"])
        self.assertTrue(binary_relation.check_symmetry_properties()["Несимметрично"])
        self.assertTrue(
            binary_relation.check_transitivity_properties()["Нетранзитивно"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
