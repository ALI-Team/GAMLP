#from .operators import MulNode
from .varnode import VarNode
from . import node
class UnitNode(node.Node):
    def __init__(self, unit, value):
        self.value=value
        self.unit=unit
        super().__init__()

    def simplifyed(self):
        return self
    def formatted(self):
        if isinstance(self.unit, VarNode):
            return "{}({})".format(self.value, self.unit)

    def eval(self):
        raise ValueError("Cant eval with variables")
        #return self.value*self.unit

    
        
