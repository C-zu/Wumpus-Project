import copy


def is_complentary_literals(literal_1, literal_2):
    return (literal_1 + literal_2 == 0)

def is_valid_clause(clause):
    for i in range(len(clause) - 1):
        if is_complentary_literals(clause[i], clause[i + 1]):
            return True
    return False

def standard_clause(clause):
    return sorted(list(set(copy.deepcopy(clause))))

def generate_combinations_recursively(set_list, combination_list, combination, depth):
    if depth == len(set_list):
        combination_list.append(copy.deepcopy(combination))
        return

    for element in set_list[depth]:
        combination.append(copy.deepcopy(element))
        generate_combinations_recursively(set_list, combination_list, combination, depth + 1)
        combination.pop()

def generate_combinations(set_list):
    combination_list, combination, depth = [], [], 0
    generate_combinations_recursively(set_list, combination_list, combination, 0)
    return combination_list

# Resolve 2 clauses then return a list of resolvents (list of clauses).
def resolve(clause_1, clause_2):
    resolvents = []
    for i in range(len(clause_1)):
        for j in range(len(clause_2)):
            if is_complentary_literals(clause_1[i], clause_2[j]):
                resolvent = clause_1[:i] + clause_1[i + 1:] + clause_2[:j] + clause_2[j + 1:]
                resolvents.append(standard_clause(resolvent))
    return resolvents


# PL Resolution algorithm.
def pl_resolution(KB,neg_alpha):
    cnf_clause_list = copy.deepcopy(KB)
#     neg_alpha = standard_cnf_sentence(negation_of_cnf_sentence(alpha))
    for clause in neg_alpha:
        if clause not in cnf_clause_list:
            cnf_clause_list.append(clause)
    new_clauses_list = []
    solution = False
    while True:
        new_clauses_list.append([])

        for i in range(len(cnf_clause_list)):
            for j in range(i + 1, len(cnf_clause_list)):
                resolvents = resolve(cnf_clause_list[i], cnf_clause_list[j])
                if [] in resolvents:
                    solution = True
                    new_clauses_list[-1].append([])
                    return solution

                for resolvent in resolvents:
                    if is_valid_clause(resolvent):
                        break
                    if resolvent not in cnf_clause_list and resolvent not in new_clauses_list[-1]:
                        new_clauses_list[-1].append(resolvent)

        if len(new_clauses_list[-1]) == 0:
            solution = False
            return solution
        cnf_clause_list += new_clauses_list[-1]

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

    def representation(self):
        for i in self.KB:
            print(i)

    def Resolution(self, neg_alpha):
        clause_list = copy.deepcopy(self.KB)
        state = pl_resolution(clause_list,neg_alpha)
        return state
    # def Resolution_Algorithm(self, negative_alpha):
    #     g = Glucose3()
    #     clause_list = copy.deepcopy(self.KB)
    #     for it in clause_list:
    #         g.add_clause(it)
    #     for it in negative_alpha:
    #         g.add_clause(it)
    #     sol = g.solve()
    #     if sol:
    #         return False
    #     return True