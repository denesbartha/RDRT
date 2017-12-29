from collections import defaultdict
from unittest import TestCase
from collection_permutations import GroupPermutations, CollectionPermutations


class TestPartitions(TestCase):
    @staticmethod
    def tryGroupPermutations(group_list, types, expected=-1):
        g = GroupPermutations(group_list, types)
        # all the possibilities are wrong
        for _ in g:
            pass
        # => there shouldn't be any solutions at all...
        assert 0 == sum(1 for _ in g)

        g = GroupPermutations(group_list, types)
        # assume that all the possibilities are good
        for c in g:
            g.set_good_solution(c)
        if expected != -1:
            assert expected == sum(1 for _ in g)
            # for the second, third, etc. time it should just iterate through the solutions (not create them again)
            assert expected == sum(1 for _ in g)
            assert expected == sum(1 for _ in g)

    def testGroupPermutations(self):
        TestPartitions.tryGroupPermutations([(1,)], {1: [1]}, 1)
        TestPartitions.tryGroupPermutations([(1,), (1, 2)], {1: [1, 1], 2: [1]}, 2)
        TestPartitions.tryGroupPermutations([(1,), (2,), (1, 2)], {1: [1, 1], 2: [1, 1]}, 4)
        TestPartitions.tryGroupPermutations([(1,), (1,), (1,), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1)],
                                            {-1: [1, 2], 0: [1, 1, 1], 1: [2, 4, 1], 2: [1]})

    def tryTypeUnit(self, atype):
        g = GroupPermutations.TypeUnit(atype)
        lst = []
        type_copy = atype[::]
        plst = [i for i in xrange(len(atype)) for _ in xrange(atype[i])]
        n = sum(atype)
        for i in xrange(n):
            lst.append(g.get_new_key())
        assert lst == plst

        with self.assertRaises(IndexError):
            for i in xrange(n + 1):
                g.pop_key()
        assert atype == type_copy

        lst = []
        for i in xrange(n):
            lst.append(g.get_new_key())
        assert lst == plst

        with self.assertRaises(IndexError):
            for i in xrange(n + 1):
                g.pop_key()
        assert atype == type_copy

    def testTypeUnit(self):
        self.tryTypeUnit([1])
        self.tryTypeUnit([10])
        self.tryTypeUnit([2, 2, 2])
        self.tryTypeUnit([1, 2, 3, 4])
        self.tryTypeUnit([5, 4, 3, 2, 1])

    class MultiSet:
        def __init__(self, lst):
            self.d = defaultdict(lambda: 0)
            for e in lst:
                self.d[e] += 1

        def __eq__(self, other):
            return self.d == other.d

    @staticmethod
    def proper_grouping(group_lst, types, groupcnt):
        collection = CollectionPermutations(group_lst, types).get_collections
        assert len(collection) == groupcnt
        assert TestPartitions.MultiSet([item for subset in collection for item in subset]) == TestPartitions.MultiSet(
            group_lst)

    def try_all_possible_permutations(self, group_lst, types, groupcnt, solution_cnt=-1, good_groups=None):
        self.proper_grouping(group_lst, types, groupcnt)
        collection = CollectionPermutations(group_lst, types)
        for c in collection:
            if good_groups is None or c in good_groups:
                collection.set_good_solution(c)

        if solution_cnt != -1:
            assert solution_cnt == sum(1 for _ in collection.get_validated_solutions)
        # if all of them are different => OK
        sols = [s for s in collection.get_validated_solutions]
        for i in xrange(len(sols)):
            for j in xrange(i + 1, len(sols)):
                assert sols[i] != sols[j]

    def testCollectionPermutations(self):
        self.try_all_possible_permutations([(1,)], {1: [1]}, 1, 1)
        self.try_all_possible_permutations([(1,), (1, 2)], {1: [1, 1], 2: [1]}, 1, 2)
        self.try_all_possible_permutations([(1,), (2,), (1, 2)], {1: [1, 1], 2: [1, 1]}, 1, 4)
        self.try_all_possible_permutations([(1,), (2,), (3,), (1, 2)], {1: [1, 1], 2: [1, 1], 3: [1]}, 2, 4)
        self.try_all_possible_permutations([(1,), (2,), (3,), (3, 4), (1, 2)],
                                           {1: [1, 1], 2: [1, 1], 3: [2], 4: [1]},
                                           2, 4)
        self.try_all_possible_permutations([(1,), (2,), (3,), (3, 4), (1, 2)],
                                           {1: [1, 1], 2: [1, 1], 3: [1, 1], 4: [1]},
                                           2, 8)
        self.try_all_possible_permutations([(1,), (2,), (3,), (3, 4), (1, 2, 3)],
                                           {1: [1, 1], 2: [1, 1], 3: [2, 1], 4: [1]},
                                           1, 12)
        self.try_all_possible_permutations([(1,), (2,), (3,), (7,), (3, 4), (5, 6), (5, 6), (7, 8), (7, 9), (1, 2, 3)],
                                           {1: [1, 1], 2: [1, 1], 3: [2, 1], 4: [1], 5: [1, 1], 6: [1, 1], 7: [1, 2],
                                            8: [1], 9: [1]},
                                           3, 72)
        self.try_all_possible_permutations([(1,), (2,), (3,), (7,), (3, 4), (5, 6), (5, 6), (7, 8), (7, 9), (1, 2, 3)],
                                           {1: [1, 1], 2: [1, 1], 3: [2, 1], 4: [1], 5: [1, 1], 6: [1, 1], 7: [1, 2],
                                            8: [1], 9: [1]},
                                           3, 72)
        self.try_all_possible_permutations([(1,), (2,), (3,), (7,), (3, 4), (5, 6), (5, 6), (7, 8), (7, 9), (1, 2, 3)],
                                           {1: [1, 1], 2: [1, 1], 3: [2, 1], 4: [1], 5: [1, 1], 6: [1, 1], 7: [1, 2],
                                            8: [1], 9: [1]},
                                           3, 0,
                                           [((1,), (0,)), ((2,), (1,)), ((3,), (1,)), ((7,), (1,)),
                                            ((3, 4), (0, 0)), ((5, 6), (0, 0)), ((5, 6), (1, 1)),
                                            ((7, 8), (1, 0)), ((7, 9), (1, 0)), ((1, 2, 3), (1, 0, 0))])
        self.try_all_possible_permutations([(1,), (2,), (3,), (7,), (3, 4), (5, 6), (5, 6), (7, 8), (7, 9), (1, 2, 3)],
                                           {1: [1, 1], 2: [1, 1], 3: [2, 1], 4: [1], 5: [1, 1], 6: [1, 1], 7: [1, 2],
                                            8: [1], 9: [1]},
                                           3, 1,
                                           [((1,), (0,)), ((2,), (1,)), ((3,), (1,)), ((7,), (1,)),
                                            ((3, 4), (0, 0)), ((5, 6), (0, 0)), ((5, 6), (1, 1)),
                                            ((7, 8), (1, 0)), ((7, 9), (0, 0)), ((1, 2, 3), (1, 0, 0))])
        self.try_all_possible_permutations(
            [(1,), (1,), (1, 2), (3, 4, 5), (19, 6), (6, 7, 8), (9, 10, 11, 12), (2, 5, 7, 11), (5,),
             (19, 20)],
            {1: [3], 2: [2], 3: [1], 4: [1], 5: [1, 1, 1], 6: [1, 1], 7: [2], 8: [1],
             9: [1], 10: [1], 11: [2], 12: [1], 19: [1, 1], 20: [1]}, 1)

        self.try_all_possible_permutations([(1,), (1,), (1,), (1,), (1,), (1,), (1,), (1,), (1,), (0, 1)],
                                           {0: [1], 1: [1, 5, 1, 2, 1]}, groupcnt=1, solution_cnt=5)

        self.try_all_possible_permutations(((1,), (1,), (1,), (1,), (1,), (1,), (0, 1)), {0: [1], 1: [1, 1, 5]}, 1,
                                           solution_cnt=3)
        self.try_all_possible_permutations(((1,), (1,), (1,), (1,), (1,), (1,), (0, 1)), {0: [1], 1: [1, 5, 1]}, 1,
                                           solution_cnt=3)

    def testCollectionPermutationsInit(self):
        self.proper_grouping([(1,)], {1: [1]}, 1)
        # (1,), (1,), (1,), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1)
        self.proper_grouping([(1,), (1,), (1,), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1)],
                             {-1: [1, 2], 0: [1, 1, 1], 1: [2, 4, 1], 2: [1]}, 1)
        self.proper_grouping([(1,), (1,), (1,), (-2, 3), (-2, 3), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1)],
                             {-2: [1, 1], -1: [1, 2], 0: [1, 1, 1], 1: [2, 4, 1], 2: [1], 3: [2]}, 2)
        self.proper_grouping([(1,), (1,), (1,), (-2, 3), (-2, 3), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1),
                              (-3, 4), (1, 3, -2, 4)],
                             {-3: [1], -2: [1, 2], -1: [1, 2], 0: [1, 1, 1], 1: [2, 4, 2], 2: [1], 3: [3], 4: [2]}, 1)

        self.proper_grouping([(1,), (1,)], {1: [2]}, 1)
        self.proper_grouping([(1,), (1,), (1, 2)], {1: [3], 2: [1]}, 1)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5)], {1: [3], 2: [1], 3: [1], 4: [1], 5: [1]}, 2)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5), (6, 7, 8)],
                             {1: [3], 2: [1], 3: [1], 4: [1], 5: [1], 6: [1], 7: [1], 8: [1]}, 3)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11, 12)],
                             {1: [3], 2: [1], 3: [1], 4: [1], 5: [1], 6: [1], 7: [1], 8: [1],
                              9: [1], 10: [1], 11: [1], 12: [1]}, 4)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11, 12), (2, 5, 7, 11)],
                             {1: [3], 2: [2], 3: [1], 4: [1], 5: [2], 6: [1], 7: [2], 8: [1],
                              9: [1], 10: [1], 11: [2], 12: [1]}, 1)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11, 12), (2, 5, 7, 11), (5,)],
                             {1: [3], 2: [2], 3: [1], 4: [1], 5: [3], 6: [1], 7: [2], 8: [1],
                              9: [1], 10: [1], 11: [2], 12: [1]}, 1)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11, 12), (2, 5, 7, 11), (5,), (19, 20)],
                             {1: [3], 2: [2], 3: [1], 4: [1], 5: [3], 6: [1], 7: [2], 8: [1],
                              9: [1], 10: [1], 11: [2], 12: [1], 19: [1], 20: [1]}, 2)
        self.proper_grouping([(1,), (1,), (1, 2), (3, 4, 5), (19, 6), (6, 7, 8), (9, 10, 11, 12), (2, 5, 7, 11), (5,),
                              (19, 20)],
                             {1: [3], 2: [2], 3: [1], 4: [1], 5: [1, 1, 1], 6: [1, 1], 7: [2], 8: [1],
                              9: [1], 10: [1], 11: [2], 12: [1], 19: [1, 1], 20: [1]}, 1)
        self.proper_grouping(
            [(1,), (1,), (1,), (1,), (1, 2), (3, 4, 5), (19, 6), (6, 7, 8), (9, 10, 11, 12), (2, 5, 7, 11), (5,),
             (19, 20)],
            {1: [1, 1, 1, 1, 1], 2: [2], 3: [1], 4: [1], 5: [1, 1, 1], 6: [1, 1], 7: [1, 1], 8: [1],
             9: [1], 10: [1], 11: [1, 1], 12: [1], 19: [1, 1], 20: [1]}, 1)

        # check invalid inputs
        with self.assertRaises(ValueError):
            CollectionPermutations([], {})
        with self.assertRaises(AssertionError):
            CollectionPermutations([(1,), (1,), (1,), (-2, 3), (-2, 3), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1)],
                                   {-2: [1, 1], -1: [1, 2], 0: [1, 1, 1], 1: [2, 4, 1], 2: [1], 3: [3]})
        with self.assertRaises(AssertionError):
            CollectionPermutations([(1,)], {1: [2]})
        with self.assertRaises(AssertionError):
            CollectionPermutations([(1,), (1,), (1,), (-1, 0, 2), (-1, 0, 1, 1), (-1, 0, 1, 1)],
                                   {-2: [1, 1], -1: [1, 2], 0: [1, 1, 1], 1: [2, 4, 1], 2: [1], 3: [2]})
