import copy


class Node:
    """Base class for all nodes. Not meant to be used to be directly used only extended
    """
    def __init__(self):
        pass

    def __add__(self, other):
        """Creates a AddNode
        """
        return AddNode(self, other)

    def __sub__(self, other):
        """Creates a SubNode
        """
        return SubNode(self, other)

    def __mul__(self, other):
        """Creates a MulNode
        """
        return MulNode(self, other)

    def __truediv__(self, other):
        """Creates a DivNode
        """
        return DivNode(self, other)
    def __pow__(self, other):
        """Creates a PowNode
        """
        return PowNode(self, other)

    def hash_node(self):
        """Hash the node with children should be the same for equal nodes.
        """
        raise NotImplementedError

    def __str__(self):
        """Calls node.formatted.
        """
        return self.formatted(None)

    def __format__(self, format_spec):
        """Calls node.formatted.
        """
        return self.formatted(None)

    def get_children(self):
        """Returns The children of a node returns node if no children.
        """
        return None
        

    def formatted(self):
        """Return a text representation of the node
        """
        pass

    def eval(self):
        """Calculates the approxemate value of the node.
        """
        raise NotImplementedError

    def label(self):
        raise NotImplementedError

    def child_labels(self, amount=1):
        return None

    def simplifyed(self, target=None, context=None):
        """Return a simplifyed clone of the node.
        """
        raise NotImplementedError

    def clone(self):
        """Return a clone of the node.
        """
        return copy.deepcopy(self)

    def simplify(self):
        raise NotImplementedError

    def latex(self):
        """Return latex for the node.
        """
        raise NotImplementedError

    def eq(self, other):
        """Checks if two nodes are the same (has the same hash).
        """
        return self.hash_node()==other.hash_node()

    def contains_unknowns(self):
        """Uses the get_children method to recursively check for unknowns. Override on nodes without children.
        """
        children=self.get_children()
        if children == None:
            print("NODE WITHOUT A GET_CHILDEN MUST CONTAIN A contains_unknown")
            raise NotImplementedError
        return True in list(map(lambda x:x.contains_unknowns(),children))

    def contains(self, value):
        """Uses the get_children() method to recursively check for a node. Override on nodes without children.
        """
        children=self.get_children()
        if children == None:
            print("NODE WITHOUT A GET_CHILDEN MUST CONTAIN A contains")
            raise NotImplementedError
        return True in list(map(lambda x:x.contains(value),children))

    def get_int_value(self):
        """Try to get a integer value of the node, if node is non integer or contains unknowns returns None.
        """
        if self.contains_unknowns():
            return None

        value=self.eval()
        if isinstance(value, int) or value.is_integer():
            return intnode.IntNode(int(value))
        return None

from .operators import *
from . import intnode
from .equation import Equation
