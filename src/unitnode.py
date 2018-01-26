from .operators import MulNode
from .varnode import VarNode
class UnitNode(MulNode):
    def __init__(self, unit, value):
        self.value=value
        self.unit=unit
        super().__init__(unit,value)

    def simplifyed(self):
        return self
    def formatted(self):
        if isinstance(self.unit, VarNode):
            return "${}({})$".format(self.value, self.unit)


    
        
