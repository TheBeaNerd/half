#!/usr/bin/env python

def p2(x,y):
    return x/(x + y*(1- x))

def p3(x,y,z):
    ## x + y + z
    return x/(x + (1 - (1 - y)*(1 - z))*(1- x))

def pn(p,n):
    return p/(1.0 - (1.0 - p)**(n + 1))

def rn(p,n):
    return 1.0 - ((1.0 - p)/(1.0 - (p**(n + 1))))

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
    main()
