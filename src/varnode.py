from .node import Node
class VarNode(Node):
    def __init__(self, name):
        self.name=name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if isinstance(other, VarNode):
            return self.name==other.name
    def simplifyed(self):
        return self

    def formatted(self):
        return self.name

    def contains(self, value):
        if isinstance(value, VarNode):
            if value.name == self.name:
                return True
        return False
