from sets import Set
import sys
import contextlib

def stringToClause(ln):
    return Set([int(word) for word in ln.split() if int(word) != 0])

def readCNF(file):
    with open(file) as f:
        cnf = [stringToClause(line) for line in f if (line[0] != "%" and line[0] != "c" and line[0] != "p")]
    sln = []
    with open(file) as f:
        for line in f:
            if line[0:5] == "c SAT":
                sln += [stringToClause(line[5:])]
            if (line[0] != "%" and line[0] != "c" and line[0] != "p"):
                break
    return (cnf,sln)

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def printDIMACS(k,n,cnf,sln=[],filename=None):
    with smart_open(filename) as fh:
        if sln:
            print >>fh, "c SAT " + " ".join('{0}'.format(n) for n in sln)
        print >>fh, 'p cnf {k} {n}'.format(k=k,n=n)
        for clause in cnf:
            print >>fh, " ".join('{0}'.format(n) for n in clause) + " 0"
