#from .operators import MulNode
from .varnode import VarNode
from . import node
from . import intnode
from . import operators
import copy
class UnitNode(node.Node):
    def __init__(self, unit, value):
        self.value=value
        self.unit=unit
        super().__init__()
        self.priority=2

    def hash_node(self):
        return hash(str(self.unit.hash_node())+str(self.value.hash_node())+"u")
        
    def simplifyed(self):
        #if not self.unit.contains_unknowns():
            #return operators.MulNode(self.unit,self.value).simplifyed()
        value_int_val=self.value.get_int_value()
        if value_int_val != None and value_int_val.eq(intnode.IntNode(0)):
            return intnode.IntNode(0)
        #if self.value.contains(self.unit):
        #    return (copy.deepcopy(self.value)*copy.deepcopy(UnitNode(self.unit, intnode.IntNode(1)))).simplifyed()
        if self.value.eq(self.unit):
            return UnitNode(operators.PowNode(self.unit.simplifyed(),2), intnode.IntNode(1))
        return UnitNode(self.unit.simplifyed(), self.value.simplifyed())
    def formatted(self, parent):
        if self.value.get_int_value().eq(intnode.IntNode(1)):
            return self.unit.formatted(self)
        if self.value.get_int_value().eq(intnode.IntNode(-1)):
            return "-"+self.unit.formatted(self)

        #if isinstance(self.unit, VarNode):
        return "{}{}".format(self.value.formatted(self), self.unit.formatted(self))
        #else:
            #return "({})({})".format(self.value.formatted(self), self.unit.formatted(self))
            

    def eval(self):
        #raise ValueError("Cant eval with variables")
        return self.value.eval()*self.unit.eval()

    #def contains(self, value):
        #return True in [self.unit.contains(value), self.value.contains(value)]
    def get_children(self):
        return [self.unit, self.value]

    def latex(self):
        return "{}{}".format(self.value.latex(), self.unit.latex())

    def label(self, debug=False):
        if debug:
            return "Unit"
        return "×"
    def child_labels(self, amount=1):
        if amount > 1:
            return ["Unit","Value"]
        else:
            return None
