#!/usr/bin/env python
import copy

class rewriteArray(dict):
    def __missing__(self, key):
        return key

## We want the graph data structure to preserve a fixpoint on update:
##
## Things that y could reach are now reachable by !x and !A, its predecessors
## Things that x could reach are now reachable by !y and !B, its predecessors
##
## Predecessors of y now includes !A + !x
## Predecessors of x now includes !B + !y
##
## a in A: g[ a] = g[ a] +  y + g[ y]
## b in B: g[!b] = g[!b] + !x + g[!x]

## -4 -> 3 | 3 -> -4
## -3 -> 4 | 4 -> -3

def printGraph(graph):
    for (key,val) in graph.items():
        print key,"->",list(val)

class unitMap(dict):
    def __missing__(self,key):
        return 0
    def copy(self):
        return copy.copy(self)
    def trueVar(self,var):
        self[var] =  1
        self[var] = -1
        return self
    def falseVar(self,var):
        self.trueVar((- var))
        return self

class rewriteMap(dict):
    def __missing__(self,key):
        return key
    def copy(self):
        return copy.copy(self)

class eqMap(dict):
    def __missing__(self,key):
        return frozenset([key])
    def copy(self):
        return copy.copy(self)

class IMPACT():
    ## 6 : UNSAT
    UNSAT = 6
    ## 5 : forces unit
    UNIT  = 5
    ## 4 : forces equivalence
    EQUIV = 4
    ## 3 : no deductions
    NOIMP = 3
    ## 2 : new, one
    NEW_1 = 2
    ## 1 : new, both
    NEW_2 = 1
    ## 0 : SAT (redundant)
    SAT   = 0

class fixpointGraph(dict):
    def __init__(self):
        ## Maps an external variable to an internal node
        self.rw    = rewriteMap()
        ## Maps nodes in graph to -1,0,1 (0 : unbound)
        self.units = unitMap()
        ## Maps an internal node to a set of external variables
        self.eclass = eqMap()
    def __missing__(self, key):
        return frozenset([])
    def copy(self):
        return copy.copy(self)
    def impact(self,x,y):
        x = self.rw[x]
        y = self.rw[y]
        xv = self.units[x]
        if xv > 0:
            return IMPACT.SAT
        yv = self.units[y]
        if yv > 0:
            return IMPACT.SAT
        if xv < 0:
            if yv < 0:
                return IMPACT.UNSAT
            return IMPACT.UNIT
        if yv < 0:
            return IMPACT.UNIT
        if (x == y):
            return IMPACT.UNIT
        if (x == (- y)):
            return IMPACT.SAT
        nxset = self[(- x)]
        if y in nxset:
            return IMPACT.SAT
        nyset = self[(- y)]
        assert(not x in nyset);
        if (- y) in self[x]:
            return IMPACT.EQUIV
        assert(not (- x) in self[y])
        if not nxset:
            if not nyset:
                return IMPACT.NEW_1
            return IMPACT.NEW_2
        if not nyset:
            return IMPACT.NEW_1
        if (- y) in nxset:
            return IMPACT.UNIT
        if (- x) in nyset:
            return IMPACT.UNIT
        return IMPACT.NOIMP
    ##
    ##  !A -> !x ->  x -> A
    ##
    def addUnit(self,x):
        ## print "Add Unit",x
        g = self
        A = g[x]
        Ax = A | {x}
        for a in A:
            g[(- a)] |= Ax
        g[(- x)] |= Ax
    ##
    ##  !A -> !x ->  y -> B
    ##  !B -> !y ->  x -> A
    ##
    def addClause(self,x,y):
        ## print "Add Clause",x,y
        g = self
        A = g[x]
        B = g[y]
        By = B | {y}
        Ax = A | {x}
        if (- y) in B:
            B |= Ax
        if (- x) in B:
            B |= {y}
        g[y] = B
        if (- x) in A:
            A |= By
        if (- y) in A:
            A |= {x}
        g[x] = A
        By = B | {y}
        Ax = A | {x}
        for a in A:
            g[(- a)] |= By
        for b in B:
            g[(- b)] |= Ax
        g[(- x)] |= By
        g[(- y)] |= Ax
    
    def graphDeductions(self):
        g = self
        nloops = set()
        ## The set of all equivalence class members
        alleq = set()
        ## A list of (one polarity of all) equivalence classes
        eclasses = []
        units  = []
        for (key,val) in g.items():
            if (- key) in val:
                if key in g[(- key)]:
                    nloops.add(abs(key))
                else:
                    units += [(- key)]
            elif ((key in val) and (key not in alleq)):
                ##
                ## So, to be in key's equiv class it needs
                ## to reach both itself and key.
                ##
                eclass = set([key])
                alleq.add(key)
                alleq.add((- key))
                for dkey in val:
                    dval = g[dkey]
                    if ((dkey in dval) and (key in dval)):
                        eclass.add(dkey)
                        alleq.add(dkey)
                        alleq.add((- dkey))
                eclasses += [eclass]
        return (nloops,eclasses,units)
    ## !A ->  x -> B
    ## !B -> !x -> A
    def performAbstraction(self,x,xclass):
        ## print "Abstracting",x,xclass
        g = self
        nxclass = set([ (- e) for e in xclass ])
        A = g[(- x)]
        B = g[x]
        for a in A:
            g[(- a)] -= xclass
        for b in B:
            g[(- b)] -= nxclass
        g[x] -= {x}
        g[(- x)] -= {(- x)}
        for x  in xclass: g.pop(x,0)
        for nx in nxclass: g.pop(nx,0)
    ## !A ->  x -> B
    ## !B -> !x -> A
    def dropUnits(self,units):
        g = self
        for x in units:
            A = g[(- x)]
            B = g[x]
            for a in A:
                g[(- a)] -= {x}
            for b in B:
                g[(- b)] -= {(- x)}
        for x in units:
            g.pop(x,0)
            g.pop((- x),0)
    def updateGraph(self,units,sat2,rw):
        g = self
        for unit in units:
            g.addUnit(unit)
        for (x,y) in sat2:
            g.addClause(x,y)
        (nloops,eclasses,units) = g.graphDeductions()
        ## print "(Pre) Graph Units",units
        if nloops:
            return (nloops,units,rw,eclasses)
        for eclass in eclasses:
            ## print "Graph EClass",eclass
            rep = next(iter(eclass))
            xclass = set(eclass)
            xclass.remove(rep)
            g.performAbstraction(rep,xclass)
            for e in xclass:
                rw[e] = rep
                rw[(- e)] = (- rep)
        units = set([ rw[unit] for unit in units ])
        ## print "(Post) Graph Units",units
        g.dropUnits(units)
        return (nloops,units,rw,eclasses)
        
def unitTestUpdate():
    z = fixpointGraph()
    ## Add an equivalence class
    z.addClause( 1,-2)
    z.addClause(-1, 2)
    ## Add an equivalence class
    z.addClause( 3, 4)
    z.addClause(-4,-3)
    ## Add a unit
    z.addClause( 5, 6)
    z.addClause( 5,-6)
    ## Add a unit
    z.addClause(-7, 8)
    z.addClause(-7,-8)
    ## Add a unit
    z.addUnit(9)
    rw = rewriteArray()
    (nloops,units,rw,eqs) = z.updateGraph([],[],rw)
    assert(nloops == set())
    assert(set(units) == set([9,-7,5]))
    for x in [1,2]:
        assert(rw[x] == rw[1])
        assert(rw[(- x)] == rw[-1])
    for x in [3,-4]:
        assert(rw[x] == rw[3])
        assert(rw[(- x)] == rw[-3])

def unitTestUnitEquiv1():
    z = fixpointGraph()
    ## Add an equivalence class
    z.addClause(-1, 2)
    z.addClause(-2, 3)
    z.addClause(-3, 4)
    z.addClause(-4, 1)
    ## Make 1 unit .. we have a unit equivalence class.
    z.addUnit(1)
    rw = rewriteArray()
    (nloops,units,rw,eqs) = z.updateGraph([],[],rw)
    assert(nloops == set())
    assert(units == set([1]))
    for x in [1,2,3,4]:
        assert(rw[x] == 1)
        assert(rw[(- x)] == -1)

def unitTestUnitEquiv2():
    z = fixpointGraph()
    ## Add an equivalence class
    z.addClause(-1, 2)
    z.addClause(-2, 3)
    z.addClause(-3, 4)
    z.addClause(-4, 1)
    ## Make 1 and 3 unit .. we have a unit equivalence class.
    z.addUnit(1)
    z.addUnit(3)
    rw = rewriteArray()
    (nloops,units,rw,eqs) = z.updateGraph([],[],rw)
    assert(nloops == set())
    for x in [1,2,3,4]:
        assert(rw[x] == rw[1])
        assert(rw[(- x)] == rw[-1])

def unitTestNLoop():
    z = fixpointGraph()
    ## Add a negated loop
    z.addClause( 1, 2)
    z.addClause( 1,-2)
    z.addClause(-1, 2)
    z.addClause(-1,-2)
    rw = rewriteArray()
    (nloops,x,y,eqs) = z.updateGraph([],[],rw)
    assert(nloops == set([1,2]))

def main():
    unitTestUpdate()
    unitTestNLoop()
    unitTestUnitEquiv1()
    unitTestUnitEquiv2()

if __name__ == "__main__":
    main()
