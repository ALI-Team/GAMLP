import copy

from .varnode import VarNode
from . import node
from . import intnode
from . import operators
from . import latex

class UnitNode(node.Node):
    def __init__(self, unit, value):
        self.value=value
        self.unit=unit
        super().__init__()
        self.priority=2

    def hash_node(self):
        return hash(str(self.unit.hash_node())+str(self.value.hash_node())+"u")
        
    def simplifyed(self, target=None, context=None):
        value_int_val=self.value.get_int_value()
        if value_int_val != None and value_int_val.eq(intnode.IntNode(0)):
            return intnode.IntNode(0)
        if self.value.eq(self.unit):
            return UnitNode(operators.PowNode(self.unit.simplifyed(),2), intnode.IntNode(1))
        return UnitNode(self.unit.simplifyed(), self.value.simplifyed())
    def formatted(self, parent):
        int_value=self.value.get_int_value()
        if int_value != None and int_value.eq(intnode.IntNode(1)):
            return self.unit.formatted(self)
        if int_value != None and int_value.eq(intnode.IntNode(-1)):
            return "-"+self.unit.formatted(self)

        return "{}{}".format(self.value.formatted(self), self.unit.formatted(self))
            

    def eval(self):
        #raise ValueError("Cant eval with variables")
        return self.value.eval()*self.unit.eval()

    #def contains(self, value):
        #return True in [self.unit.contains(value), self.value.contains(value)]
    def get_children(self):
        return [self.unit, self.value]

    def latex(self, parent):
        #return "{}{}".format(self.value.latex(self), latex.parentheses(self, parent, self.unit.latex(self)))
        int_value=self.value.get_int_value()
        if int_value != None and int_value.eq(intnode.IntNode(1)):
            return latex.parentheses(self.unit,parent,self.unit.latex(parent))
        if int_value != None and int_value.eq(intnode.IntNode(-1)):
            return "-"+latex.parentheses(self.unit,parent,self.unit.formatted(self))
            #return "-"+self.unit.formatted(self)

        return latex.parentheses(self,parent,"{}{}".format(self.value.latex(self), self.unit.latex(self)))

    def label(self, debug=False):
        if debug:
            return "Unit"
        return "×"
    def child_labels(self, amount=1):
        if amount > 1:
            return ["Unit","Value"]
        else:
            return None

    def flattend(self):
        return UnitNode(self.unit.flattend(), self.value.flattend())

    def compact_format(self):
        if self.value.eq(intnode.IntNode(1)):
            return "@{unit}}}".format(unit=self.unit.compact_format())
        return "@{unit}{value}}}".format(unit=self.unit.compact_format(), value=self.value.compact_format())
