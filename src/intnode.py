from .node import Node
class IntNode(Node):
    def __init__(self,n):
        super().__init__()
        self.n=n

    def __hash__(self):
        return hash(str(self.n))
    
    def eval(self):
        return self.n
    def simplifyed(self):
        return self
        
    def formatted(self):
        return str(self.n)

    def contains(self, value):
        if isinstance(value, IntNode):
            if value.n==self.n:
                return True
        return False
    def get_children(self):
        return None
        
    def contains_unknowns(self):
        return False
    
    def latex(self):
        return str(self.n)

    def label(self):
        return str(self.n)
