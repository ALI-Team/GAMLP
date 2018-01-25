class Node:
    def __init__(self):
        pass

    def __add__(self, other):
        return AddNode(self, other)

    def __sub__(self, other):
        return SubNode(self, other)

    def __mul__(self, other):
        return MulNode(self, other)

    def __truediv__(self, other):
        return DivNode(self, other)
    def __pow__(self, other):
        return PowNode(self, other)

    def __eq__(self, other):
        return Equation(self, other)

    def __hash__(self):
        raise NotImplementedError

    def eval(self):
        raise NotImplementedError

    def simplifyed(self):
        raise NotImplementedError

    def simplify(self):
        raise NotImplementedError


from .operators import *
from .equation import Equation
