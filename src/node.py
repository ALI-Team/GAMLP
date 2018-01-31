class Node:
    """Base class for all nodes. Not meant to be used to be directly used only extended
    """
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

    def __hash__(self):
        raise NotImplementedError

    def __str__(self):
        return self.formatted()

    def __format__(self, format_spec):
        return self.formatted()

    def get_children(self):
        """Returns The children of a node returns node if no children.
        """
        return None
        

    def formatted(self):
        """Return a text representation of the node
        """
        pass

    def __hash__(self):
        return NotImplemented
    
    def eval(self):
        """Calculates the approxemate value of the node.
        """
        raise NotImplementedError

    def simplifyed(self):
        """Return a simplifyed clone of the node.
        """
        raise NotImplementedError

    def simplify(self):
        raise NotImplementedError

    def latex(self):
        """Return latex for the node.
        """
        raise NotImplementedError

    def contains_unknowns(self):
        """Uses the get_children method to recursively check for unknowns. Override on nodes without children.
        """
        children=self.get_children()
        if children == None:
            print("NODE WITHOUT A GET_CHILDEN MUST CONTAIN A contains_unknown")
            raise NotImplementedError
        return True in list(map(lambda x:x.contains_unknown(value),children))

    def contains(self, value):
        """Uses the get_children() method to recursively check for a node. Override on nodes without children.
        """
        children=self.get_children()
        if children == None:
            print("NODE WITHOUT A GET_CHILDEN MUST CONTAIN A contains")
            raise NotImplementedError
        return True in list(map(lambda x:x.contains(value),children))
        


from .operators import *
from .equation import Equation
