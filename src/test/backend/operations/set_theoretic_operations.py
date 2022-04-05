import unittest

import portion

from src.main.backend.models.cyclogram import Cyclogram
from src.main.backend.operations.set_theoretic_operations import union, intersection, substraction


class TestSetTheoreticOperations(unittest.TestCase):
    def test_union_with_different_start_and_end_times_should_throws_value_error(self):
        x = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1, [[portion.empty() for _ in range(1)] for _ in range(2)])
        y = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1.1, [[portion.empty() for _ in range(1)] for _ in range(2)])

        self.assertRaises(ValueError, lambda: union(x, y))

    def test_union_with_different_sets_should_throws_value_error(self):
        x = Cyclogram('Name', ['a', 'b'], ['a', 'b'], -10, 1, [[portion.empty() for _ in range(2)] for _ in range(2)])
        y = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1, [[portion.empty() for _ in range(1)] for _ in range(2)])

        self.assertRaises(ValueError, lambda: union(x, y))

    def test_union_with_empty_intervals_should_returns_empty_intervals(self):
        x = Cyclogram('Name', ['A', 'B', 'C', 'D'], ['a', 'b', 'c'], -100.11, 874,
                      [[portion.empty() for _ in range(3)] for _ in range(4)])
        y = Cyclogram('Name', ['A', 'B', 'C', 'D'], ['a', 'b', 'c'], -100.11, 874,
                      [[portion.empty() for _ in range(3)] for _ in range(4)])

        self.assertListEqual([[portion.empty() for _ in range(3)] for _ in range(4)], union(x, y).intervals)

    def test_union_with_full_intervals_should_returns_full_intervals(self):
        x = Cyclogram('Name', ['A', 'B'], ['a', 'b', 'c'], 100.11, 100.12,
                      [[portion.open(10, 400) for _ in range(3)] for _ in range(2)])
        y = Cyclogram('Name', ['A', 'B'], ['a', 'b', 'c'], 100.11, 100.12,
                      [[portion.closedopen(100, 200) for _ in range(3)] for _ in range(2)])

        self.assertListEqual([[portion.closed(100.11, 100.12) for _ in range(3)] for _ in range(2)],
                             union(x, y).intervals)

    def test_union_with_correct_data_should_works_correctly(self):
        x = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                      [[portion.open(1, 5), portion.closedopen(3, 7) | portion.closed(7, 7)],
                       [portion.empty(), portion.closedopen(1, 12)]])
        y = Cyclogram('Name2', ['A', 'B'], ['a', 'b'], 1, 10,
                      [[portion.closed(2, 5), portion.open(1, 2)],
                       [portion.empty(), portion.closed(3, 4) | portion.openclosed(1, 2)]])
        expected = Cyclogram('Name1 | Name2', ['A', 'B'], ['a', 'b'], 1, 10,
                             [[portion.openclosed(1, 5), portion.open(1, 2) | portion.closed(3, 7)],
                              [portion.empty(), portion.closed(1, 10)]])

        self.assertDictEqual(expected.__dict__, union(x, y).__dict__)

    def test_intersection_with_different_start_and_end_times_should_throws_value_error(self):
        x = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1, [[portion.empty() for _ in range(1)] for _ in range(2)])
        y = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1.1, [[portion.empty() for _ in range(1)] for _ in range(2)])

        self.assertRaises(ValueError, lambda: intersection(x, y))

    def test_intersection_with_different_sets_should_throws_value_error(self):
        x = Cyclogram('Name', ['a', 'b'], ['a', 'b'], -10, 1, [[portion.empty() for _ in range(2)] for _ in range(2)])
        y = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1, [[portion.empty() for _ in range(1)] for _ in range(2)])

        self.assertRaises(ValueError, lambda: intersection(x, y))

    def test_intersection_with_empty_intervals_should_returns_empty_intervals(self):
        x = Cyclogram('Name', ['A', 'B', 'C', 'D'], ['a', 'b', 'c'], -100.11, 874,
                      [[portion.empty() for _ in range(3)] for _ in range(4)])
        y = Cyclogram('Name', ['A', 'B', 'C', 'D'], ['a', 'b', 'c'], -100.11, 874,
                      [[portion.empty() for _ in range(3)] for _ in range(4)])

        self.assertListEqual([[portion.empty() for _ in range(3)] for _ in range(4)], intersection(x, y).intervals)

    def test_intersection_with_full_intervals_should_returns_full_intervals(self):
        x = Cyclogram('Name', ['A', 'B'], ['a', 'b', 'c'], 100.11, 100.12,
                      [[portion.open(10, 400) for _ in range(3)] for _ in range(2)])
        y = Cyclogram('Name', ['A', 'B'], ['a', 'b', 'c'], 100.11, 100.12,
                      [[portion.closedopen(100, 200) for _ in range(3)] for _ in range(2)])

        self.assertListEqual([[portion.closed(100.11, 100.12) for _ in range(3)] for _ in range(2)],
                             intersection(x, y).intervals)

    def test_intersection_with_correct_data_should_works_correctly(self):
        x = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                      [[portion.empty(), portion.closedopen(1, 4) | portion.closed(7, 8)],
                       [portion.empty(), portion.closedopen(1, 12)]])
        y = Cyclogram('Name2', ['A', 'B'], ['a', 'b'], 1, 10,
                      [[portion.closed(2, 5), portion.open(5, 6)],
                       [portion.closed(1, 10), portion.closed(3, 4)]])
        expected = Cyclogram('Name1 & Name2', ['A', 'B'], ['a', 'b'], 1, 10,
                             [[portion.empty(), portion.empty()],
                              [portion.empty(), portion.closed(3, 4)]])

        self.assertDictEqual(expected.__dict__, intersection(x, y).__dict__)

    def test_substraction_with_different_start_and_end_times_should_throws_value_error(self):
        x = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1, [[portion.empty() for _ in range(1)] for _ in range(2)])
        y = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1.1, [[portion.empty() for _ in range(1)] for _ in range(2)])

        self.assertRaises(ValueError, lambda: substraction(x, y))

    def test_substraction_with_different_sets_should_throws_value_error(self):
        x = Cyclogram('Name', ['a', 'b'], ['a', 'b'], -10, 1, [[portion.empty() for _ in range(2)] for _ in range(2)])
        y = Cyclogram('Name', ['a', 'b'], ['a'], -10, 1, [[portion.empty() for _ in range(1)] for _ in range(2)])

        self.assertRaises(ValueError, lambda: substraction(x, y))

    def test_substraction_with_empty_intervals_should_returns_empty_intervals(self):
        x = Cyclogram('Name', ['A', 'B', 'C', 'D'], ['a', 'b', 'c'], -100.11, 874,
                      [[portion.empty() for _ in range(3)] for _ in range(4)])
        y = Cyclogram('Name', ['A', 'B', 'C', 'D'], ['a', 'b', 'c'], -100.11, 874,
                      [[portion.empty() for _ in range(3)] for _ in range(4)])

        self.assertListEqual([[portion.empty() for _ in range(3)] for _ in range(4)], substraction(x, y).intervals)

    def test_substraction_with_full_intervals_should_returns_empty_intervals(self):
        x = Cyclogram('Name', ['A', 'B'], ['a', 'b', 'c'], 100.11, 100.12,
                      [[portion.open(10, 400) for _ in range(3)] for _ in range(2)])
        y = Cyclogram('Name', ['A', 'B'], ['a', 'b', 'c'], 100.11, 100.12,
                      [[portion.closedopen(100, 200) for _ in range(3)] for _ in range(2)])

        self.assertListEqual([[portion.empty() for _ in range(3)] for _ in range(2)],
                             substraction(x, y).intervals)

    def test_substraction_with_correct_data_should_works_correctly(self):
        x = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                      [[portion.closed(2, 9), portion.closedopen(3, 7)],
                       [portion.empty(), portion.closedopen(1, 12)]])
        y = Cyclogram('Name2', ['A', 'B'], ['a', 'b'], 1, 10,
                      [[portion.open(2, 9), portion.open(1, 2) | portion.closed(8, 10)],
                       [portion.closed(1, 8), portion.empty()]])
        expected = Cyclogram('Name1 \\ Name2', ['A', 'B'], ['a', 'b'], 1, 10,
                             [[portion.closed(2, 2) | portion.closed(9, 9), portion.closedopen(3, 7)],
                              [portion.empty(), portion.closed(1, 10)]])

        self.assertDictEqual(expected.__dict__, substraction(x, y).__dict__)
