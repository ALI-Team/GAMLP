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

    def simplifyed(self):
        if True and self.value.contains(self.unit):
            print("err")
            print(self)
            print (copy.deepcopy(self.value)*copy.deepcopy(UnitNode(self.unit, intnode.IntNode(1))))
            return (copy.deepcopy(self.value)*copy.deepcopy(UnitNode(self.unit, intnode.IntNode(1)))).simplifyed()
        else:
            return self
    def formatted(self):
        if isinstance(self.unit, VarNode):
            return "({}){}".format(self.value, self.unit)
        else:
            return "({})({})".format(self.value, self.unit)
            

    def eval(self):
        raise ValueError("Cant eval with variables")
        #return self.value*self.unit

    def contains(self, value):
        return True in [self.unit.contains(value), self.value.contains(value)]

    
        
