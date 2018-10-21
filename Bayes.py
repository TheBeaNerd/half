#!/usr/bin/env python
from util import isSAT

def p2(x,y):
    return x/(x + y*(1- x))

def p3(x,y,z):
    ## x + y + z
    return x/(x + (1 - (1 - y)*(1 - z))*(1- x))

def pn(p,n):
    return p/(1.0 - (1.0 - p)**(n + 1))

def rn(p,n):
    return 1.0 - ((1.0 - p)/(1.0 - (p**(n + 1))))

def pClause(p0,clause,pmap):
    pclause = 1.0
    acc = dict()
    for v in clause:
        acc[v] = pmap[v]
        pclause *= pmap[(- v)]
    res = 1.0 - p0*pclause
    #print acc
    #print 'Weight : {p:01.4f}'.format(p=p0)
    print str(clause) + " = " + '{p:01.4f}'.format(p=res) + '[{p:01.4f}]'.format(p=p0)
    return res

def pE(alpha,cnf,pmap,pref):
    pcnf = 1.0
    for clause in cnf:
        p0 = 1.0 - alpha*pClause(1.0,clause,pref)
        pcnf *= pClause(p0,clause,pmap)
    return pcnf

class PMap(dict):
    def __missing__(self,key):
        return 0.5

def pEH(alpha,n,cnf,pmap,rmap):
    cnf = [ clause for clause in cnf if ((n in clause) or ((- n) in clause))]
    #print "Variable {} is governed by :".format(n)
    #print cnf
    P_H1 = pmap[n]
    P_H2 = pmap[(- n)]
    print "P(H1) = {v:01.4f}".format(v=P_H1)
    print "P(H2) = {v:01.4f}".format(v=P_H2)
    hmap = PMap(pmap)
    hmap[n] = 1.0
    hmap[(- n)] = 0.0
    P_E_H1 = pE(alpha,cnf,hmap,pmap)
    print "P(E|H1) = {v:01.4f}".format(v=P_E_H1)
    hmap = PMap(pmap)
    hmap[n] = 0.0
    hmap[(- n)] = 1.0
    P_E_H2 = pE(alpha,cnf,hmap,pmap)
    print "P(E|H2) = {v:01.4f}".format(v=P_E_H2)
    P_H1_E = (P_E_H1*P_H1)/((P_E_H1*P_H1) + (P_E_H2*P_H2))
    P_H2_E = (P_E_H2*P_H2)/((P_E_H2*P_H2) + (P_E_H1*P_H1))
    print "P(H1|E) = {v:01.4f}".format(v=P_H1_E)
    print "P(H2|E) = {v:01.4f}".format(v=P_H2_E)
    print
    rmap[n]     = P_H1_E
    rmap[(- n)] = P_H2_E
    return rmap

def bitp(n,mask):
    return (((mask >> n) & 1) == 1)

def bit(n,mask):
    return ((mask >> n) & 1)

def cneg(polarity,var):
    return var if polarity else (- var)

def printClauseP(clause,pmap,sln):
    plist = [pmap[v] for v in clause]
    drop = plist.index(min(plist))
    sat2 = list(clause)
    del sat2[drop]
    ok = isSAT(sat2,sln)
    bits = len(clause)
    line = '+-'
    for n in range(0,bits):
        line += '-----'
    line += '+--------+'
    line += '' if ok else ' #'
    print line
    for mask in range(0,2**bits):
        pmin = 1.0
        allin = True
        hot = 0
        for n in range(0,bits):
            hot += bit(n,mask)
            allin &= (cneg(bitp(n,mask),clause[n]) in sln)
            pmin *= pmap[cneg(bitp(n,mask),clause[n])]
        line = '|'
        for n in range(0,bits):
            line += ' {var:4d}'.format(var=cneg(bitp(n,mask),clause[n]))
        line += ' {hot} {pmin:01.4f} |'.format(hot=hot,pmin=pmin)
        line += ' *' if allin else ''
        print line
    line = '+-'
    for n in range(0,bits):
        line += '-----'
    line += '+--------+'
    print line
    line = '|'
    for n in range(0,bits):
        line += ' {p:01.2f}'.format(p=pmap[clause[n]])
    line += ' |        |'
    print line
    line = '+-'
    for n in range(0,bits):
        line += '-----'
    line += '+--------+'
    print line
    return 0 if ok else 1

def postP(vars,cnf,sln):
    rmap = PMap()
    pmap = PMap(rmap)
    qlist = []
    for i in range(0,8):
        for var in vars:
            rmap = pEH(0.0,var,cnf,pmap,rmap)
        pmap = PMap(rmap)
        qlist += [pmap]
    rlist = []
    for i in range(0,8):
        for var in vars:
            rmap = pEH(1.0,var,cnf,pmap,rmap)
        pmap = PMap(rmap)
        rlist += [pmap]
    hits = 0
    miss = 0
    for var in sln:
        line = '{:4d}'.format(var)
        for xmap in rlist:
            hits  += 1 if (xmap[var] >= xmap[(- var)]) else 0
            miss  += 1 if (xmap[var] <  xmap[(- var)]) else 0
            mark = ' ' if (xmap[var] > xmap[(- var)]) else '*'
            line += ' | {mark} {pt:01.4f} {pf:01.4f}'.format(mark=mark,pt=xmap[var],pf=xmap[(- var)])
        print line
    print "Pwin = " + str((1.0*hits)/(hits + miss))
    res = rlist[-1]
    misses = 0
    for clause in cnf:
        misses += printClauseP(clause,res,sln)
    print "Misses : " + str(misses)
    return res

def main():
    x = 0.1
    y = 0.2
    print x
    print y
    xx = p2(x,y)
    yy = p2(y,x)
    print xx
    print yy
    xxx = p2(xx,yy)
    yyy = p2(yy,xx)
    print xxx
    print yyy
    print p3(0.01,0.02,0.03)
    print p3(0.02,0.01,0.03)
    print p3(0.03,0.02,0.01)
    print "P = 0.10"
    for n in range(0,9):
        print("k = " + str(n) + "  Pk=" + '{:01.5f}'.format(pn(0.1,n)) + "  Rk=" + '{:01.5f}'.format(rn(0.1,n)))
    print "P = 0.25"
    for n in range(0,9):
        print("k = " + str(n) + "  Pk=" + '{:01.5f}'.format(pn(0.25,n)) + "  Rk=" + '{:01.5f}'.format(rn(0.25,n)))
    print "P = 0.75"
    for n in range(0,9):
        print("k = " + str(n) + "  Pk=" + '{:01.5f}'.format(pn(0.75,n)) + "  Rk=" + '{:01.5f}'.format(rn(0.75,n)))
    print "P = 0.90"
    for n in range(0,9):
        print("k = " + str(n) + "  Pk=" + '{:01.5f}'.format(pn(0.9,n)) + "  Rk=" + '{:01.5f}'.format(rn(0.9,n)))



if __name__ == "__main__":
    factorExample()
