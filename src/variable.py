from .unitnode import UnitNode
from .varnode import VarNode
class VariableSet:
    def __init__(self):
        self.variables={}
    def append(self, node):
        if isinstance(node, UnitNode):
            if node.unit in self.variables:
                self.variables[node.unit]=self.variables[node.unit]+node.value
            else:
                self.variables[node.unit]=node.value
                print("Node value {}".format(node.value))
        else:
            raise ValueError("Bad node type")

    def nodes(self):
        terms=[]
        for unit in self.variables:
            terms.append(UnitNode(unit, self.variables[unit].simplifyed()))
        return terms

    def formatted(self):
        return str(self.variables)
    def __str__(self):
        return self.formatted()
            
                
def var(name):
    return UnitNode(VarNode(name), IntNode(1))

from .intnode import IntNode
