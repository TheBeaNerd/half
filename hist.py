import random
import graph

def splitCLAUSE(clause):
    res = []
    for i in range(len(clause) // 2):
        res += [tuple(clause[i:i+2])]
    res += [tuple(clause[-2:])] if len(clause) % 2 else []
    return res

def splitCNF(cnf):
    return [splitCLAUSE(clause) for clause in cnf]

def random2CLAUSE(split):
    return random.choice(split)

def SATto2SAT(cnf):
    return [random2CLAUSE(split) for split in cnf]

def histogram(varCount,cnf,sln):
    snf = splitCNF(cnf)
    hist = {}
    icnt = 0
    hcnt = 0
    for i in range(200):
        print('Graph {}'.format(i+1))
        g = graph.igraph()
        cnf2 = SATto2SAT(snf)
        for (a,b) in cnf2:
            g.add(a,b)
        for i in range(varCount):
            var = i+1
            (index,paths) = g.iloop(var,varCount)
            if index:
                icnt += 1
                hcnt += 1 if index in sln else 0
            else:
                for key in paths.keys():
                    next = paths[key]
                    key = (- key)
                    for v in next:
                        pair = (min(key,v),max(key,v))
                        hist[pair] = hist.get(pair,0) + 1
    tcnt = 0
    fcnt = 0
    for (a,b) in hist.keys():
        if ((a in sln) and (b in sln)):
            tcnt += hist[(a,b)]
        else:
            fcnt += hist[(a,b)]
    print('tcnt  : {}'.format(tcnt))
    print('fcnt  : {}'.format(fcnt))
    print('Power : {}'.format((hcnt*1.0)/icnt))
    return hist

