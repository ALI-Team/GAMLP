from .operatornode import OperatorNode
import functools
class AddNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=terms

    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval()))


class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()-self.right.eval()


class MulNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=terms

    def eval(self):
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval()))


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

