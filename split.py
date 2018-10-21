import random
from util import isSAT

def split(cnf):
    res = []
    for clause in cnf:
        clause = list(clause)
        if (len(clause) == 3):
            res += [(clause[0:2],clause[1:3])]
        else:
            res += [(clause,clause)]
    return res

def random2SAT(split):
    return [a if random.randint(0,1) == 0 else b for (a,b) in split ]

def sat2SAT(split,sln):
    res = [a if isSAT(a,sln) else b for (a,b) in split]
    assert(all([isSAT(a,sln) for a in res]))
    return res
