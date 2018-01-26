from .node import Node
class VarNode(Node):
    def __init__(self, name):
        self.name=name
    def simplifyed(self):
        return self
    def __hash__(self):
        return hash(self.name)

    def formatted(self):
        return self.name
