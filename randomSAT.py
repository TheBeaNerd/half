#!/usr/bin/env python
import argparse
import random
from dimacs import writeDIMACS
from util import countSAT,isSAT

def addClauses(population,sln,number,satCount,cnf):
    for i in range(0,number):
        count = 0
        while (count != satCount):
            clause = random.sample(population,3)
            count = countSAT(clause,sln)
        cnf += [clause]
    return cnf

def minSAT(sln):
    nsln = [(- c) for c in sln]
    cnf = []
    for c in sln:
        clause = [c] + random.sample(nsln,2)
        cnf += [clause]
    return cnf

def randomSAT(variables,clauses,ofile=None):
    assert(variables < clauses)
    sln = [i if (random.randrange(0,2) == 1) else (- i) for i in range(1,variables+1)]
    p1 = range(1,variables+1)
    p2 = [(- i) for i in p1]
    population = p1 + p2
    sat3 = clauses // 7
    sat2 = (3 * clauses) // 7
    sat1 = clauses - sat3 - sat2
    if (sat1 < variables):
        sat1 = variables
        sat3 = (clauses - variables) // 4
        sat2 = clauses - sat1 - sat3
    #print "c 3:" + str(sat3) + " 2:" + str(sat2) + " 1:" + str(sat1)
    cnf = minSAT(sln)
    sat1 -= variables
    cnf = addClauses(population,sln,sat1,1,cnf)
    cnf = addClauses(population,sln,sat2,2,cnf)
    cnf = addClauses(population,sln,sat3,3,cnf)
    for clause in cnf:
        assert(isSAT(clause,sln))
    writeDIMACS(variables,clauses,cnf,sln,filename=ofile)

def main():
    parser = argparse.ArgumentParser(description="Random satisfiable 3-SAT")
    parser.add_argument('-k', '--clauses', help="Number of clauses [426]")
    parser.add_argument('-n', '--variables', help="Number of variables [100]")
    parser.add_argument('-o', '--output', help="Output filename [stdout]")
    parser.set_defaults(clauses='426')
    parser.set_defaults(variables='100')
    parser.set_defaults(output=None)
    args = parser.parse_args()
    randomSAT(variables=int(args.variables),clauses=int(args.clauses),ofile=args.output)

if __name__ == "__main__":
    main()
