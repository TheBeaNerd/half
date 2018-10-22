import random
import graph

def splitCLAUSE(clause):
    res = []
    for i in range(len(clause) // 2):
        res += [tuple(clause[i:i+2])]
    res += [tuple(clause[-2:])] if len(clause) % 2 else []
    res = [(min(a,b),max(a,b)) for (a,b) in res]
    return res

def splitCNF(cnf):
    return [splitCLAUSE(clause) for clause in cnf]

def random2CLAUSE(split,hist):
    hlist = [hist.get(pair,0) for pair in split]
    minv  = min(hlist)
    mindex = [i for (i,v) in enumerate(hlist) if (v == minv)]
    split = [split[i] for i in mindex]
    return random.choice(split)

def SATto2SAT(cnf,hist):
    return [random2CLAUSE(split,hist) for split in cnf]

## We need to track probabilities at the variable level.
##
## It is unfortunate that we will have to do the updates sequentially.
## Perhaps we should give this more thought .. there may be a way to
## combine the graphs.
##
## Actually, the fact that you are factoring the loops relative to
## specific variables may ease this process ..
##
## Note that, even with this small example, we already see
## paths of 20 steps (unique variables) and more.

def histogram(varCount,cnf,sln):
    snf = splitCNF(cnf)
    hist = {}
    ag = {}
    for i in range(100):
        print('Graph {}'.format(i+1))
        g = graph.igraph()
        gh = {}
        cnf2 = SATto2SAT(snf,hist)
        for (a,b) in cnf2:
            g.add(a,b)
        for i in range(varCount):
            var = i+1
            (index,length,paths) = g.iloop(var,varCount)
            if length:
                loopedges = frozenset([(min((- key),z),max((- key),z)) for key in paths.keys() for z in paths[key]])
                for edge in loopedges:
                    gh[edge] = gh.get(edge,0) + 2**(- length)
        loophist = {}
        for edge in gh.keys():
            hcount = gh[edge]
            loophist[hcount] = loophist.get(hcount,frozenset()).union(frozenset([edge]))
        counts = list(reversed(sorted(loophist.keys())))
        fcount = 0.0
        xcount = 0.0
        for i in range(len(counts)//10):
            print(counts[i])
            for edge in loophist[counts[i]]:
                (a,b) = edge
                truth = ((a in sln) and (b in sln))
                xcount += 1.0
                if not truth:
                    fcount += 1.0
                hist[edge] = hist.get(edge,0) + 1
        print('Accuracy : {:.2f}'.format(fcount/xcount))
    for split in snf:
        res = ''
        for (a,b) in split:
            res += '{}:{} '.format(((a in sln) or (b in sln)),hist.get((min(a,b),max(a,b)),0))
        print res
    return hist

