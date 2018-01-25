from .operators import MulNode
class UnitNode(MulNode):
    def __init__(self, unit, value):
        self.value=value
        self.unit=unit
        super().__init__(unit,value)

    def simplifyed(self):
        return self

    
        
