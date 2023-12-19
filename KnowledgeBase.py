import copy
from pysat.solvers import Glucose3

class KnowledgeBase:
    def __init__(self):
        self.KB = []

    def standardize_clause(self,clause):
        return sorted(list(set(clause)))


    def add_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause not in self.KB:
            self.KB.append(clause)


    def del_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)


    def Resolution_Algorithm(self, negative_alpha):
        g = Glucose3()
        clause_list = copy.deepcopy(self.KB)
        for it in clause_list:
            g.add_clause(it)
        for it in negative_alpha:
            g.add_clause(it)
        sol = g.solve()
        if sol:
            return False
        return True
    def representation(self):
        for i in self.KB:
            print(i)