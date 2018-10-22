#!/usr/bin/env python
from copy import copy

class lset():
    """A levelized set"""
    def __init__(self,start):
        self.body = [frozenset([start])]
        self.terminals = frozenset()
        self.flat  = frozenset()
    def __str__(self):
        res  = str(self.flat) + "\n"
        res += str(self.terminals) + "\n"
        res += "[\n"
        for vset in self.body:
            res += str(vset) + "\n"
        res += "]"
        return res
    def looper(self):
        for a in self.flat:
            if (- a) in self.flat:
                return True
        return False
    def add(self,sset):
        sset = frozenset(sset)
        sset -= self.flat        
        self.body += [sset]
        m = len(self.body)
        self.flat  |= sset
        for s in sset:
            n = 0
            for xset in self.body:
                n += 1
                if (- s) in xset:
                    self.terminals |= frozenset([s,(- s)])
    def next(self):
        return self.body[-1] - self.terminals
    def backtrack(self,preds=frozenset()):
        preds |= self.terminals
        res = frozenset()
        while self.body:
            res = self.body[-1]
            self.body = self.body[0:-1]
            if not preds.isdisjoint(res):
                break
            res = frozenset()
        return res.intersection(preds)
    def pop(self,preds):
        ##self.body = self.body[0:-1]
        return self.backtrack(preds=preds)
    def filter(self,prev):
        res = frozenset()
        if self.body:
            pred = self.body[-1]
            res |= prev.intersection(pred)
        return res

class igraph(dict):
    def __missing__(self, key):
        return frozenset([])
    def clone(self):
        return copy(self)
    def merge(self,x):
        res = self.clone()
        for z in x.keys():
            res[z] = res[z].union(x[z])
        return res
    def addCNF(self,cnf2):
        print cnf2
        for [a,b] in cnf2:
            self.add(a,b)
    def add(self,a,b):
        #print "Adding arcs from " + str((- a)) + " to " + str(b)
        #print "Adding arcs from " + str((- b)) + " to " + str(a)
        self[(- a)] |= frozenset([b])
        self[(- b)] |= frozenset([a])
    def predecessors(self,a):
        x = self[(- a)]
        return frozenset([(- v) for v in x])
    def addAll(self,alist,b):
        for a in alist:
            self.add((- a),b)
    def ipaths(self,a,n):
        #print "Find all paths no longer than " + str(2*n) +" from " + str(a) + " to " + str((- a))
        reach = lset(a)
        next = [a]
        depth = 0
        for i in range(0,n):
            step = frozenset([])
            for v in next:
                step |= self[v]
            reach.add(step)
            if reach.looper():
                depth = i+1
            next = reach.next()
            if not next:
                break
        #print "Running backwards from :\n" + str(reach)
        prev = reach.backtrack()
        #print "Backtracked to :\n" + str(reach)
        #print "Starting from " + str(prev)
        paths = igraph()
        while prev:
            preds = frozenset()
            for v in prev:
                pv = self.predecessors(v)
                #print "Predecessors of " + str(v) + " are " + str(pv)
                pv = reach.filter(pv)
                # if reach.body:
                #     print "Filtering by " + str(reach.body[-1]) + " results in " + str(pv)
                # else:
                #     print "Oops .. all done"
                preds |= pv
                paths.addAll(pv,v)
            xtra = reach.pop(preds)
            #print "Popped back to :\n" + str(reach)
            #print "Adding terminal nodes " + str(xtra)
            preds |= xtra
            prev = preds
            #print "Iterating on " + str(prev)
        return (depth,paths)
    def iloop(self,var,n):
        (n1,p1) = self.ipaths(var,n)
        #print('{} - {} -> {}'.format(var,(- var),n1))
        (n2,p2) = self.ipaths((- var),n)
        #print('{} - {} -> {}'.format((- var),var,n2))
        if (p1 and p2):
            #print('{} |- {} -> {}'.format(var,n1+n2,(- var)))
            return (0,n1+n2,p1.merge(p2))
        if p1:
            return((- var),0,igraph())
        return(var,0,igraph())
        
def main():
    x = igraph()
    x.add(1,2)
    x.add(-2,3)
    x.add(-3,4)
    x.add(-4,1)
    x.add(1,5)
    x.add(-2,6)
    x.add(-3,7)
    x.add(-4,8)
    r = x.ipaths(-1,2)
    print "Product: " + str(r.keys())
    x = igraph()
    x.add(1,2)
    x.add(-2,3)
    x.add(-3,1)
    x.add(1,5)
    x.add(-2,6)
    x.add(-3,7)
    r = x.ipaths(-1,2)
    print "Product: " + str(r.keys())
    x = igraph()
    x.add(1,2)
    x.add(-2,3)
    x.add(-3,4)
    x.add(-4,5)
    x.add(-5,1)
    x.add(1,6)
    x.add(-2,7)
    x.add(-3,8)
    x.add(-4,9)
    x.add(-5,9)
    r = x.ipaths(-1,2)
    print "Product: " + str(r.keys())
    r = x.ipaths(-1,3)
    print "Product: " + str(r.keys())

if __name__ == "__main__":
    main()
