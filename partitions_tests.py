import partitions
from unittest import TestCase


class TestPartitions(TestCase):
    @staticmethod
    def get_solutions(lst, ones_restriction=-1):
        return [solution for solution in partitions.Partitions(lst, ones_restriction)]

    def test_basic_lists(self):
        # valid lists
        self.assertEqual([((1,),)], TestPartitions.get_solutions([1]))
        self.assertEqual([((1,),)], TestPartitions.get_solutions([1]))
        self.assertEqual([((1,), (1,))], TestPartitions.get_solutions([1, 1]))
        self.assertEqual([((0, 1,),)], TestPartitions.get_solutions([0, 1]))
        self.assertEqual([((0, 1),)], TestPartitions.get_solutions([1, 0]))
        self.assertEqual([((0, 1),(0,1)), ((1,), (0, 0, 1))], TestPartitions.get_solutions([1, 0, 0, 1]))
        self.assertEqual([((-2, 0, 1, 1, 1),)], TestPartitions.get_solutions([1, 0, -2, 1, 1]))
        self.assertEqual([((-1, 2), (0, 1)), ((1,), (-1, 0, 2))], TestPartitions.get_solutions([-1, 1, 0, 2]))
        self.assertEqual([((-1, 2), (0, 1))], TestPartitions.get_solutions([-1, 1, 0, 2], 0))
        self.assertEqual([((-1, 2), (0, 1))], TestPartitions.get_solutions([-1, 1, 0, 2], 0))
        self.assertEqual([((1,), (1,), (1,), (1,), (0, 1))], TestPartitions.get_solutions([1, 1, 1, 1, 1, 0]))
        self.assertEqual([((1,), (1,), (1,), (1,), (0, 1))], TestPartitions.get_solutions([1, 1, 1, 1, 1, 0], 4))
        self.assertEqual([], TestPartitions.get_solutions([1, 1, 1, 1, 1, 0], 3))
        self.assertEqual([], TestPartitions.get_solutions([1, 1, 1, 1, 1, 0], 3))
        self.assertEqual([((0, 1), (-1, 1, 1)), ((1,), (-1, 0, 1, 1))], TestPartitions.get_solutions([-1, 0, 1, 1, 1]))
        self.assertEqual([((0, 1), (0, 1)), ((1,), (0, 0, 1))], TestPartitions.get_solutions([0, 0, 1, 1]))

        # invalid lists
        self.assertEqual([], TestPartitions.get_solutions([1, 3]))
        self.assertEqual([], TestPartitions.get_solutions([2]))
        with self.assertRaises(ValueError):
            self.assertEqual([], TestPartitions.get_solutions([]))

        self.assertEqual([], [solution for solution in TestPartitions.get_solutions([-1, -1, 0, 1])])

    def test_complex_lists(self):
        self.assertEqual(4, len(TestPartitions.get_solutions([-1, -1, -1, 1, 1, 1, 1, 2])))
        self.assertEqual(107, len(TestPartitions.get_solutions([-3, -2, -2 - 1, -1, -1, 1, 1, 1, 1, 1, 2, 2, 3, 3])))
        self.assertEqual(382,
                         len(TestPartitions.get_solutions([-1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])))
        self.assertEqual(139, len(TestPartitions.get_solutions(
            [-2, -2, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, -2])))
        self.assertEqual([((1,), (1,), (1,), (1,), (1,), (1,), (1,), (-1, 2), (-2, -2, -1, -1, 7))],
                         TestPartitions.get_solutions([-2, -2, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 2, 7]))
