from .operatornode import OperatorNode
import functools
class AddNode(OperatorNode):
    def __init__(self, *terms):
        self.terms=terms

    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval(), self.terms))

    def simplifyed(self):
        terms=[]
        for term in self.terms:
            simplifyed=term.simplify()
            if isinstance(simplifted, AddNode):
                terms.extend(simplifyed.terms)
            else:
                terms.append(simplifyed)

                

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
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval(), self.terms))


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

