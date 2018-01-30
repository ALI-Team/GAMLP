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

    #def __eq__(self, other):
    #    return Equation(self, other)

    def __hash__(self):
        raise NotImplementedError

    def __str__(self):
        return self.formatted()

    def __format__(self, format_spec):
        return self.formatted()

    def get_children(self):
        return None
        

    def formatted(self):
        pass

    def __hash__(self):
        return NotImplemented
    
    def eval(self):
        raise NotImplementedError

    def simplifyed(self):
        raise NotImplementedError

    def simplify(self):
        raise NotImplementedError

    def latex(self):
        raise NotImplementedError

    def contains_unknowns(self):
        children=self.get_children()
        if children == None:
            print("NODE WITHOUT A GET_CHILDEN MUST CONTAIN A contains_unknown")
            raise NotImplementedError
        return True in list(map(lambda x:x.contains_unknown(value),children))

    def contains(self, value):
        children=self.get_children()
        if children == None:
            print("NODE WITHOUT A GET_CHILDEN MUST CONTAIN A contains")
            raise NotImplementedError
        return True in list(map(lambda x:x.contains(value),children))
        


from .operators import *
from .equation import Equation
