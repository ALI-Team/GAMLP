from .operatornode import OperatorNode
import functools
from . import intnode
class AddNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=list(terms)

    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval(), self.terms))

    def simplifyed(self):
        term=simplifyer.simplify_homogen(self)
        return term

    def formatted(self):
        return "("+"+".join(map(lambda x:x.formatted(), self.terms))+")"

                

class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()-self.right.eval()

    def formatted(self):
        return "({}-{})".format(self.left, self.right)


class MulNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=list(terms)

    def eval(self):
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval(), self.terms))

    def simplifyed(self):
        term=simplifyer.simplify_homogen(self)
        return term

    def formatted(self):
        return "("+"*".join(map(lambda x:x.formatted(), self.terms))+")"


class DivNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()/self.right.eval()

    def formatted(self):
        return "({}/{})".format(self.left, self.right)


class PowNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()**self.right.eval()

    def formatted(self):
        return "({}^{})".format(self.left, self.right)



from . import simplifyer
