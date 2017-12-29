from itertools import product
from collections import defaultdict


class GroupPermutations:
    class TypeUnit:
        def __init__(self, ptype):
            self.type = ptype[::]
            self.stack = []
            self.index = 0

        def get_new_key(self, start=-1):
            if start >= 0:
                self.index = start
            while self.index < len(self.type):
                if self.type[self.index] > 0:
                    self.type[self.index] -= 1
                    self.stack.append(self.index)
                    return self.index
                self.index += 1
            self.index = 0
            raise StopIteration()

        def increment(self):
            self.pop_key()
            self.index += 1
            return self.get_new_key()

        def pop_key(self):
            self.index = self.stack.pop()
            self.type[self.index] += 1

    def __init__(self, group_lst, types):
        self.group_lst = sorted(group_lst, key=lambda g: len(g))
        self.solutions = []
        self.validated_solutions = []
        self.group_calculated = defaultdict(lambda: set())
        self.type_units = {t: GroupPermutations.TypeUnit(types[t]) for t in types}
        self.found_all_solutions = False
        self.good_solution = self.group_index = self.group_candidates = self.last_finished_group = None
        self.validated_groups = {}

    def __len__(self):
        return len(self.group_lst)

    @property
    def get_solutions(self):
        return self.solutions

    @property
    def get_validated_solutions(self):
        return self.validated_solutions

    @property
    def get_found_all_solutions(self):
        return self.found_all_solutions

    def set_good_solution(self, group_solution=None):
        # if a new solution came from the validation process => save it
        if group_solution is not None:
            self.validated_groups[self.last_finished_group] = group_solution
        # self.good_solution = False
        self.group_index += 1
        # if we have exceeded the number of the groups => terminate the iteration
        if self.group_index >= len(self.group_lst):
            self.solutions.append([tuple(c) for c in self.group_candidates])
            if self.validated_groups != {}:
                self.validated_solutions.append([self.validated_groups[tuple(c)] for c in self.group_candidates])
            # step back to the penultimate group and reset the last group
            self.group_index -= 1

    def __iter__(self):
        # if we have tried out every possible settings (found every solutions)
        if self.found_all_solutions:
            return iter(self.solutions)
        self.group_index = 0
        self.good_solution = False
        self.group_candidates = [[] for _ in xrange(len(self.group_lst))]
        return self

    def next(self):
        while True:
            # find the next candidate
            while self.group_index >= 0:
                group_candidate = self.group_candidates[self.group_index]
                actgroup = self.group_lst[self.group_index]
                index = len(group_candidate) - 1
                if index >= 0:
                    # try to increment the last built group
                    while index >= 0:
                        try:
                            group_candidate[index] = self.type_units[actgroup[index]].increment()
                            break
                        except StopIteration:
                            group_candidate.pop()
                            index -= 1
                    else:
                        # if we couldn't find another proper match
                        self.group_index -= 1
                        continue

                for i in xrange(index + 1, len(actgroup)):
                    k = actgroup[i]
                    try:
                        group_candidate.append(
                            self.type_units[k].get_new_key(0 if i == 0 or k != actgroup[i - 1] else -1))
                    except StopIteration:
                        break
                else:
                    # otherwise we could place all the key-types
                    # if the current group is the same as the previous and lexicographically less than that =>
                    # this is not a new solution...
                    if self.group_index >= 1 and actgroup == self.group_lst[self.group_index - 1] \
                            and group_candidate < self.group_candidates[self.group_index - 1]:
                        continue
                    # if this is a new group setting
                    self.last_finished_group = tuple(group_candidate)
                    if self.last_finished_group not in self.group_calculated[actgroup]:
                        # save the candidate
                        self.group_calculated[actgroup].add(self.last_finished_group)
                        # return the actual group itself and the new candidate for it
                        return actgroup, self.last_finished_group
                    else:
                        # self.good_solution = True
                        if self.last_finished_group in self.validated_groups:
                            self.set_good_solution()
                        break
            else:
                # there are no more possible solutions...
                self.found_all_solutions = True
                raise StopIteration()


class CollectionPermutations:
    def __init__(self, group_lst, types):
        self.group_lst = group_lst
        if len(self.group_lst) == 0:
            raise ValueError("An empty list was given, please specify a non-empty list...")
        # for each type the sum of the different subtypes must be the same as the number of the actual type appearing
        # in the given group_list
        typesums = defaultdict(lambda: 0)
        for e in (e for g in group_lst for e in g):
            typesums[e] += 1
        for t in types:
            assert sum(types[t]) == typesums[t]
        # find the independent regions...
        self.collections = self.find_groups(self.group_lst)
        # create a list of group permutation object that will generate the actual permutations for the groups
        self.groupings = [GroupPermutations(c, types) for c in self.collections]
        self.group_index = self.good_solution = self.find_one_solution = None
        # self.solutions = []
        self.validated_solutions = []

    @staticmethod
    def find_groups(group_lst):
        """Finds the connected groups (the common intersection is not empty)."""
        collections = {}
        type_indexes = {}
        collection_index = 0
        s = {}
        for g in group_lst:
            act_collections, new_keys = set(), set()
            for key in g:
                if key in s:
                    act_collections.add(s[key])
                else:
                    new_keys.add(key)
            # if we haven't found an existing grouping that is
            if len(act_collections) == 0:
                collection_index += 1
                collections[collection_index] = [g]
                type_indexes[collection_index] = set(g)
                for key in g:
                    s[key] = collection_index
            # otherwise we have to merge the currently found groupings
            else:
                # take the first collection's index
                ci = next(iter(act_collections))
                for i in act_collections:
                    if i != ci:
                        for key in type_indexes[i]:
                            s[key] = ci
                        collections[ci] += collections[i]
                        type_indexes[ci].update(type_indexes[i])
                        del collections[i]
                        del type_indexes[i]
                for key in new_keys:
                    s[key] = ci
                collections[ci].append(g)
        # sort by the size of the lists
        return sorted(collections.values(), key=lambda c: len(c))

    @property
    def get_collections(self):
        return self.collections

    def __iter__(self):
        self.iterlst = [iter(g) for g in self.groupings]
        self.group_index = 0
        self.good_solution = False
        # the first task is to find at least one good solution for the whole collection - including each group
        self.find_one_solution = True
        self.group_solutions = []
        self.candidate = None
        return self

    # @property
    # def get_solutions(self):
    #     return self.solutions

    @property
    def get_validated_solutions(self):
        return self.validated_solutions

    def check_current_group_solutions(self):
        if len(self.groupings[self.group_index].get_validated_solutions) > 0:
            # self.group_solutions.append(tuple(self.groupings[self.group_index].get_solutions))
            self.group_index += 1
            # if we have reached the last
            if self.group_index >= len(self.groupings):
                self.find_one_solution = False
                self.group_index = 0
            return True
        return False

    def set_good_solution(self, group_solution):
        self.groupings[self.group_index].set_good_solution(group_solution)
        if self.find_one_solution:
            # if there is a solution for the actual group
            self.check_current_group_solutions()

    def next(self):
        while True:
            # if we just want to find a good solution for the whole collection
            if self.find_one_solution:
                try:
                    # send the next candidate for validation
                    return next(self.iterlst[self.group_index])
                except StopIteration:
                    # check whether there was any solutions for the current group
                    if self.check_current_group_solutions():
                        continue
                    # there was no solution for one of the collections => stop...
                    raise StopIteration()

            else:
                # find all the current group's solutions
                while self.group_index < len(self.groupings):
                    try:
                        # if there is another possibility => send it to validation
                        return next(self.iterlst[self.group_index])
                    except StopIteration:
                        # reset the iterator of the current group
                        self.iterlst[self.group_index] = iter(self.groupings[self.group_index])
                        self.group_index += 1
                else:
                    # self.solutions = product(*(iter(g.get_solutions) for g in self.groupings))
                    self.validated_solutions = product(*(iter(g.get_validated_solutions) for g in self.groupings))
                    raise StopIteration()
