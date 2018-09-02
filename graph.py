#!/usr/bin/env python
from copy import copy

class lset():
    """A levelized set"""
    def __init__(self):
        self.body = []
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
    def backtrack(self):
        res = frozenset()
        while self.body:
            res = self.body[-1]
            self.body = self.body[0:-1]
            if not self.terminals.isdisjoint(res):
                break
            res = frozenset()
        return res.intersection(self.terminals)
    def pop(self,prev):
        res = frozenset()
        if self.body:
            pred = self.body[-1]
            res |= prev.intersection(pred)
            res |= self.terminals.intersection(pred)
            self.body = self.body[0:-1]
        return res

class igraph(dict):
    def __missing__(self, key):
        return frozenset([])
    def clone(self):
        return copy(self)
    def add(self,a,b):
        self[(- a)] |= frozenset([b])
        self[(- b)] |= frozenset([a])
    def pred(self,a):
        x = self[(- a)]
        return frozenset([(- v) for v in x])
    def ipaths(self,a,n):
        reach = lset()
        next = [a]
        for i in range(0,n):
            step = frozenset([])
            for v in next:
                step |= self[v]
            reach.add(step)
            next = reach.next()
            if not next:
                break
        prev = reach.backtrack()
        paths = prev
        while prev:
            preds = frozenset()
            for v in prev:
                preds |= self.pred(v)
            prev  = reach.pop(preds)
            paths |= prev
        return paths

def main():
    x = igraph()
    x.add(1,2)
    x.add(-2,3)
    x.add(-3,4)
    x.add(-4,1)
    r = x.ipaths(-1,5)
    print r
    x = igraph()
    x.add(1,2)
    x.add(-2,3)
    x.add(-3,1)
    r = x.ipaths(-1,5)
    print r

if __name__ == "__main__":
    main()
