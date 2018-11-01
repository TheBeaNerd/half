#!/usr/bin/env python
import argparse
from randomSAT import *
from dimacs import readDIMACS
from graph import igraph
from split import split,random2SAT,sat2SAT
import Bayes
from hist import histogram

def test(filename):
    if not filename:
        filename = "test.dimacs"
        randomSAT(variables=100,clauses=426,ofile=filename)
    (varCount,cnf,slns) = readDIMACS(file=filename)
    vars = range(1,varCount+1)
    pdist = Bayes.init_pdist(vars,cnf)
    ndist = Bayes.update_pdist(cnf,pdist)
    kdist = Bayes.update_pdist(cnf,ndist)
    sln = slns[0]
    hits = 0
    for key in pdist.keys():
        kp = kdist.get(key,0.5)
        acc = ((kp > 0.5) == (key in sln))
        hits += 1 if acc else 0
        print('{:4d} : {:0.2f} : {:0.2f} : {:0.2f} : {}'.format(key,pdist.get(key,0.5),ndist.get(key,0.5),kp,acc))
    print('Accuracy : {:0.2f}'.format((hits*1.0)/len(pdist)))
    for clause in cnf:
        for var in clause:
            sc += '{:4d}'.format(var)
            sc += '{:4d}'.format(Bayes.pget(var,kdist))
    #hist = histogram(varCount,cnf,slns[0])
    #print('Done.')
    # if slns:
    #     cnf2 = sat2SAT(split(cnf3),slns[0])
    # else:
    #     cnf2 = random2SAT(split(cnf3))
    #cnf2 = random2SAT(split(cnf3))
    # cnf2 = sat2SAT(split(cnf3),slns[0])
    # ig = igraph()
    # ig.addCNF(cnf2)
    # for i in range(1,101):
    #     print str(i) + " : " + str(len(ig.ipaths(i,5).keys())) + "," + str(len(ig.ipaths((- i),5).keys()))

def processArgs():
    parser = argparse.ArgumentParser(description="Test Path")
    parser.add_argument('-f', '--file', help="Input Filename")
    parser.set_defaults(file=None)
    args = parser.parse_args()
    test(args.file)

if __name__ == "__main__":
    processArgs()
