from .node import Node
from . import constants
class VarNode(Node):
    def __init__(self, name):
        self.priority=5
        self.name=name
        if constants.get(self.name) != None:
            self.is_constant=True
            #print(constants.get(self.name)
            self.constant=constants.get(self.name)
        else:
            self.is_constant=False
            self.constant=None
        super().__init__()

    def eval(self):
        if self.is_constant:
            return self.constant.value
        print("varnode is not a constant")
        raise ValueError
    def hash_node(self):
        return hash(self.name)
    #def __eq__(self, other):
        #if isinstance(other, VarNode):
        #    return self.name==other.name
    def simplifyed(self, target=None, context=None):
        return self

    def formatted(self, parent):
        return self.name

    def contains(self, value):
        if isinstance(value, VarNode):
            if value.name == self.name:
                return True
        return False
    def contains_unknowns(self):
        return not self.is_constant

    def latex(self, parent):
        return self.name

    def unknowns(self):
        return set([self.name])

    def label(self, debug=False):

        if self.is_constant and not debug:
            return self.constant.symbol
            
        return self.name
    def compact_format(self):
        return "{name}}}".format(name=self.name)
