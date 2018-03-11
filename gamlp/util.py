import operator as op
import functools

def ncr(n, r):
    r = min(r, n-r)
    numer = functools.reduce(op.mul, range(n, n-r, -1), 1)
    denom = functools.reduce(op.mul, range(1, r+1), 1)
    return numer//denom

def factorial(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f
