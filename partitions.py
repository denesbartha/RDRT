class Partitions:
    class Units:
        def __init__(self, lst):
            self.keymin, self.keymax = min(lst), max(lst)
            self.keys = range(self.keymin, self.keymax + 1)
            self.keys_len = self.keymax - self.keymin + 1
            self.multiplicities = self.keys_len * [0]
            self.size = len(lst)
            self.sum = 0
            self.keyindex = None

            for e in lst:
                self.multiplicities[e - self.keymin] += 1
                self.sum += e

        def decrement(self, key):
            self.sum -= key
            key -= self.keymin
            u = self.multiplicities[key]
            self.size -= 1

            if u >= 1:
                self.multiplicities[key] -= 1
            else:
                raise KeyError
            return

        def increment(self, key):
            self.sum += key
            key -= self.keymin
            self.multiplicities[key] += 1
            self.size += 1

        def get_proper_keys(self, minkey=None):
            for i in xrange(0 if minkey is None else minkey - self.keymin, self.keys_len):
                if self.multiplicities[i] > 0:
                    yield self.keys[i]

        def __len__(self):
            return self.size

        def get_sum(self):
            return self.sum

        def get_min_key(self):
            return self.keymin

    class Solutions:
        def __init__(self):
            self.solutions = []

        @staticmethod
        def create_groups(lst):
            asum = 0
            t = []
            solution = []
            for e in lst:
                asum += e
                t.append(e)
                if asum == 1:
                    solution.append(tuple(t))
                    asum = 0
                    t = []
            return tuple(solution)

        def add(self, lst):
            g = self.create_groups(lst)
            self.solutions.append(g)

        def __iter__(self):
            return iter(self.solutions)

    # a static dictionary for storing the solutions
    solution_dict = {}

    def __init__(self, lst, max_one_cnt=-1):
        if len(lst) == 0:
            raise ValueError("An empty list was given, please specify a non-empty list...")
        self.lst = lst if isinstance(lst, tuple) else tuple(lst)
        self.units = Partitions.Units(lst)
        # if the user has specified a maximum limit for the number of (1) groups, then take the minimal value among
        # the given number and the number of 1s appearing in the list
        self.max_one_cnt = min(max_one_cnt, lst.count(1)) if max_one_cnt != -1 else max_one_cnt
        if self.units.get_sum() <= 0:
            # raise ValueError("Bad list was given: the sum of the elements should be positive... The current sum is:"
            #                  " %d" % (self.units.get_sum()))
            # if the sum of the group is less than 1 => there is no solution
            Partitions.solution_dict[(tuple(self.lst), self.max_one_cnt)] = []
            return
        self.solutions = Partitions.Solutions()
        # for debugging / time measurement purposes
        self.extension_cnt = 0

    def find_groups(self, units, path, prevgroup, actgroup, asum, onecnt=0):
        """finds all the groups from the specified number and remaining units"""
        self.extension_cnt += 1
        parent, length = actgroup[-1], len(actgroup)
        # the sum of the actual group must not exceed 1
        if asum > 1:
            return
        # either continue from the parent key or if the group's sum is 1 => start from the lowest available key
        minkey = parent
        if asum == 1:
            # if a limit was specified on the number of (1) group solutions
            if self.max_one_cnt >= 0 and len(actgroup) == 1:
                onecnt += 1
                if onecnt > self.max_one_cnt:
                    return

            # if the sizes are monotonically increase or lexicographically follow each other => it is a good solution
            # otherwise backtrack
            if length < len(prevgroup) or length == len(prevgroup) and actgroup < prevgroup:
                return
            # if we are at a leaf node and the sum is 1 => we have found a good solution
            elif len(units) - 1 == 0:
                self.solutions.add(path)
                return
            # otherwise start a new group (the actual sum will be 0, start the iteration from the lowest key)
            asum = 0
            minkey = units.get_min_key()
            prevgroup, actgroup = actgroup, []

        # if the remaining sum of the numbers are less than 1 => there is no solution...
        if units.get_sum() - parent < 1:
            return

        units.decrement(parent)
        for u in units.get_proper_keys(minkey):
            actgroup.append(u)
            path.append(u)
            self.find_groups(units=units, path=path, prevgroup=prevgroup, actgroup=actgroup, asum=asum + u,
                             onecnt=onecnt)
            path.pop()
            actgroup.pop()
        units.increment(parent)

    def __iter__(self):
        # if the list was already processed before => just look it up in the solutions_dict
        t = (self.lst, self.max_one_cnt)
        if t in Partitions.solution_dict:
            self.solutions = Partitions.solution_dict[t]
        else:
            for u in self.units.get_proper_keys():
                if u > 1:
                    break
                self.find_groups(units=self.units, path=[u], prevgroup=[], actgroup=[u], asum=u)
            # save the solutions for the list to the dictionary
            Partitions.solution_dict[t] = self.solutions

        self.solutions_iter = iter(self.solutions)
        return self

    def next(self):
        return next(self.solutions_iter)

    def get_extension_cnt(self):
        return self.extension_cnt

