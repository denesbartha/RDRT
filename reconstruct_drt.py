from itertools import product
from collections import defaultdict
from functools import reduce
import operator
import partitions
import collection_permutations
from itertools import combinations_with_replacement

from sage.all import *

# turn off the warnings (because of sage)...
warnings.filterwarnings('ignore')

# introduce a new symbolic variable
x = sage.all.SR.var('x')


class ReconstructDirectedRootedTree:
    class TypeSet:
        def __init__(self):
            self.pl = defaultdict(lambda: [])
            self.ml = defaultdict(lambda: [])

        def add(self, k, v, cnt=1):
            self.pl[k].append(v)
            self.ml[k].append(cnt)

        def get_type_dict(self):
            return {k: self.ml[k] for k in self.ml}

        def get_key_by_index(self, k, v):
            return self.pl[k][v]

    leaf_pol = x + 1
    finished = {leaf_pol: [leaf_pol]}

    def __init__(self, p, reset_finished=True):
        self.polynomial = p
        if reset_finished:
            ReconstructDirectedRootedTree.finished = {self.leaf_pol: [self.leaf_pol]}
        if p.degree(x) > len(ReconstructDirectedRootedTree.terms):
            ReconstructDirectedRootedTree.terms = [x**k for k in xrange(1, p.degree(x) + 1)]

    @staticmethod
    def pretty_print(p):
        return "+".join(
            map(str, sorted([f for f in p.operands()], key=lambda expression: expression.degree(x)))).replace("*", "")
        # return latex(p)

    terms = []

    @staticmethod
    def pol_to_list(p):
        try:
            return p.list()
        except TypeError:
            return [p(0)] + [p.coefficient(ReconstructDirectedRootedTree.terms[k]) for k in xrange(p.degree(x))]

    @staticmethod
    def proper_coefficient_list(pl):
        length = len(pl)
        index = 1
        if pl[0] != 1 or pl[-1] != 1:
            return False
        while index < length and pl[index - 1] <= pl[index]:
            index += 1
        if index <= 1:
            return False
        while index < length and pl[index - 1] >= pl[index]:
            index += 1
        return index >= length

    class SolutionWrapper:
        def __init__(self, solutions):
            self.solutions = solutions

        @property
        def get_solutions(self):
            return self.solutions

    @staticmethod
    def reconstruct(p):
        # if p == 1 or p == 1 + x:
        #     return [p]
        p_degree = p.degree(x)
        if p_degree == 0:
            if p == 1:
                return [p]
            else:
                return []
        elif p_degree == 1:
            if p == ReconstructDirectedRootedTree.leaf_pol:
                return [p]
            else:
                return []
        # elif p.coefficient(x) <= 0:
        #     return []
        elif p(0) != 1:
            return []
        elif p in ReconstructDirectedRootedTree.finished:
            return ReconstructDirectedRootedTree.finished[p]

        # pol_list = ReconstructDirectedRootedTree.pol_to_list(p)
        pol_listn = p.coefficient(ReconstructDirectedRootedTree.terms[p.degree(x) - 1])
        # if not ReconstructDirectedRootedTree.proper_coefficient_list(pol_list):
        if pol_listn != 1:
            ReconstructDirectedRootedTree.finished[p] = []
            return []

        pol_list1 = p.coefficient(x)
        if pol_list1 == 1:
            # try out if (p - 1) / x works...
            rdt_solution_lst = [1 + x * rp for rp in ReconstructDirectedRootedTree.reconstruct(((p - 1) / x).expand())]
            # if not was_solution:
            ReconstructDirectedRootedTree.finished[p] = rdt_solution_lst
            return rdt_solution_lst

        # if there was no solution => factorize p
        # print "factorize..."
        fl = p.factor_list()
        # print "end of factorize..."
        # print "$$", [ReconstructDirectedRootedTree.pretty_print(ff) for ff in fl], "$$"
        good_pols = defaultdict(lambda: [])
        badcnt = 0
        pold = ReconstructDirectedRootedTree.TypeSet()
        pol_type_occurrences = []
        # print "iter through factors..."
        for prime_pol in fl:
            # prl = ReconstructDirectedRootedTree.pol_to_list(prime_pol[0])
            # coefficients = prime_pol[0].coefficients()
            if prime_pol[0].degree(x) == 1:
                if prime_pol[0] == ReconstructDirectedRootedTree.leaf_pol:
                    good_pols[prime_pol[0]] = [(prime_pol[0], prime_pol[1])]
                    prl1 = 1
                else:
                    prl1 = prime_pol[0].coefficient(x)
                    badcnt += prime_pol[1]
            else:
                prl0 = prime_pol[0](0)
                prl1 = prime_pol[0].coefficient(x)
                prl_n = prime_pol[0].coefficient(ReconstructDirectedRootedTree.terms[prime_pol[0].degree(x) - 1])

                # if there is a prime among the factors whose constant value or the largest power's coefficient is not 1
                # => no solution and if there is negative value
                if prl0 != 1 or prl_n != 1:  # or prl[1] > 1 next((True for e in prl if e < 0), False)
                    ReconstructDirectedRootedTree.finished[p] = []
                    return []

                was_solution = False
                # if the x term's coefficient is 1 => check it, otherwise this is a bad polynomial
                if prl1 == 1:
                    for rp in ReconstructDirectedRootedTree.reconstruct(((prime_pol[0] - 1) / x).expand()):
                        was_solution = True
                        good_pols[prime_pol[0]].append((1 + x * rp, prime_pol[1]))
                if not was_solution:
                    badcnt += prime_pol[1]

            pol_type_occurrences += prime_pol[1] * [prl1]
            pold.add(prl1, prime_pol[0], prime_pol[1])
        # print "end of iter through factors..."

        # if each polynomial was good => return the product
        if badcnt == 0:
            rdt_solution_lst = []
            for rp in product(*good_pols.values()):
                prod_pol = reduce(operator.mul, (ap[0] ** ap[1] for ap in rp), 1)
                rdt_solution_lst.append(prod_pol)
            ReconstructDirectedRootedTree.finished[p] = rdt_solution_lst
            return rdt_solution_lst

        rdt_solution_lst = []
        type_dict = pold.get_type_dict()
        # print "calculate ", pol_type_occurrences
        for groups in partitions.Partitions(pol_type_occurrences):
            # print groups, fl, [ReconstructDirectedRootedTree.pretty_print(f[0]) for f in fl]
            # print "f", p
            # print groups, type_dict
            cp = collection_permutations.CollectionPermutations(groups, type_dict)
            for agroup in cp:
                # if the checked group is a prime polynomial
                if len(agroup[0]) == 1:
                    # if it is a good polynomial => inform the cp object about it
                    type_1_prime_pol = pold.get_key_by_index(agroup[0][0], agroup[1][0])
                    if type_1_prime_pol in good_pols:
                        cp.set_good_solution(
                            ReconstructDirectedRootedTree.SolutionWrapper([g[0] for g in good_pols[type_1_prime_pol]]))
                # otherwise create the product of the given group and verify it
                else:
                    # have the product of the actual group
                    prod_pol = reduce(operator.mul,
                                      (pold.get_key_by_index(agroup[0][j], agroup[1][j]) for j in
                                       xrange(len(agroup[0]))), 1)
                    # check if it represents a valid directed rooted tree
                    # if len(ReconstructDirectedRootedTree.reconstruct(((prod_pol - 1) / x).expand())) > 0:
                    act_group_solution =\
                        [1 + x * rp for rp in ReconstructDirectedRootedTree.reconstruct(((prod_pol - 1) / x).expand())]
                    if len(act_group_solution) > 0:
                        cp.set_good_solution(ReconstructDirectedRootedTree.SolutionWrapper(act_group_solution))

            # print "generating solutions..."
            for solution in cp.get_validated_solutions:
                gpl = defaultdict(lambda: 0)
                for solution_groups in solution:
                    for group in solution_groups:
                        gpl[group] += 1

                for rp in product(*[combinations_with_replacement(g[0].get_solutions, g[1]) for g in gpl.items()]):
                    prod_pol = reduce(operator.mul, (reduce(operator.mul, ct, 1) for ct in rp), 1)
                    rdt_solution_lst.append(prod_pol)
            # print "end of generating solutions..."

        # print "end of calculation..."
        ReconstructDirectedRootedTree.finished[p] = rdt_solution_lst
        return rdt_solution_lst

    def __iter__(self):
        # self.tree_iter = iter(ReconstructDirectedRootedTree.reconstruct(self.polynomial))
        # %lprun -f ReconstructDirectedRootedTree.reconstruct
        return iter(ReconstructDirectedRootedTree.reconstruct(self.polynomial))
