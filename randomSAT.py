#!/usr/bin/env python
import argparse
import random
from dimacs import writeDIMACS
from util import countSAT

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

def randomSAT(k,n,ofile=None):
    assert(k < n)
    sln = [i if (random.randrange(0,2) == 1) else (- i) for i in range(1,k+1)]
    p1 = range(1,k+1)
    p2 = [(- i) for i in p1]
    population = p1 + p2
    sat3 = n // 7
    sat2 = (3 * n) // 7
    sat1 = n - sat3 - sat2
    if (sat1 < k):
        sat1 = k
        sat3 = (n - k) // 4
        sat2 = n - sat1 - sat3
    #print "c 3:" + str(sat3) + " 2:" + str(sat2) + " 1:" + str(sat1)
    cnf = minSAT(sln)
    sat1 -= k
    cnf = addClauses(population,sln,sat1,1,cnf)
    cnf = addClauses(population,sln,sat2,2,cnf)
    cnf = addClauses(population,sln,sat3,3,cnf)
    writeDIMACS(k,n,cnf,sln,filename=ofile)

def main():
    parser = argparse.ArgumentParser(description="Random satisfiable 3-SAT")
    parser.add_argument('-k', '--clauses', help="Number of clauses [426]")
    parser.add_argument('-n', '--variables', help="Number of variables [100]")
    parser.add_argument('-o', '--output', help="Output filename [stdout]")
    parser.set_defaults(clauses='426')
    parser.set_defaults(variables='100')
    parser.set_defaults(output=None)
    args = parser.parse_args()
    randomSAT(k=int(args.variables),n=int(args.clauses),ofile=args.output)

if __name__ == "__main__":
    main()
