from .unitnode import UnitNode
from .varnode import VarNode
class VariableSet:
    def __init__(self):
        self.variables={}
    def append(self, node):
        if isinstance(node, UnitNode):
            if node.unit in self.variables:
                self.variables[node.unit]+=node.value
            else:
                self.variables[node.unit]=node.value
        else:
            raise ValueError("Bad node type")

    def nodes(self):
        terms=[]
        for unit in variables:
            terms.append(UnitNode(unit, variables[unit]))
        return terms
            
                
def var(name):
    return UnitNode(VarNode(name), 1)
