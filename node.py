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

    def eval(self):
        return NotImplemented

from operators import *
