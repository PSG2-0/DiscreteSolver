import unittest

from src.math_algos.set_theory.set_simplifier import SetSimplifier


class TestSetSimplifier(unittest.TestCase):
    def setUp(self):
        self.simplifier = SetSimplifier()

    def test_transform(self):
        self.assertEqual(self.simplifier.transform("A \\ B"), "A & ~ B")
        self.assertEqual(self.simplifier.transform("not(not(A))"), "~(~(A))")

    def test_simplify_expression(self):
        self.assertEqual(str(self.simplifier.simplify_expression("A \\ B")), "A & ~B")
        self.assertEqual(str(self.simplifier.simplify_expression("not(not(A))")), "A")
        self.assertEqual(
            str(
                self.simplifier.simplify_expression(
                    "(A ∪ not(B)) ∩ (A ∪ not(B) ∪ C) ∩ (A ∪ not(B) ∪ D)"
                )
            ),
            "A | ~B",
        )
        self.assertEqual(
            str(
                self.simplifier.simplify_expression(
                    "not(A) ∩ not(B) ∪ A ∩ B ∪ not(A) ∩ B"
                )
            ),
            "B | ~A",
        )

    def test_reverse_transform(self):
        self.assertEqual(self.simplifier.reverse_transform("A & ~B"), "A ∩ not(B)")
        self.assertEqual(self.simplifier.reverse_transform("~A"), "not(A)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
