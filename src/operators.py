from .operatornode import OperatorNode
import functools
from . import intnode
from . import simplifyer
class AddNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=list(terms)
        
    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval(), self.terms))

    def simplifyed(self):
        term=simplifyer.simplify_homogen(self)
        print("return")
        print(term)
        return term

                

class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()-self.right.eval()


class MulNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=list(terms)

    def eval(self):
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval(), self.terms))

    def simplifyed(self):
        term=simplifyer.simplify_homogen(self)
        print("return")
        print(term)
        return term


class DivNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()/self.right.eval()


class PowNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()**self.right.eval()


