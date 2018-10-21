#!/usr/bin/env python
import argparse
from randomSAT import *
from dimacs import readDIMACS
from graph import igraph
from split import split,random2SAT,sat2SAT
from Bayes import postP
from hist import histogram

def test(filename):
    if not filename:
        filename = "test.dimacs"
        randomSAT(variables=100,clauses=426,ofile=filename)
    (varCount,cnf,slns) = readDIMACS(file=filename)
    hist = histogram(varCount,cnf,slns[0])
    print('Done.')
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
