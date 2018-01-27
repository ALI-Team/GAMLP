from .node import Node
class IntNode(Node):
    def __init__(self,n):
        super().__init__()
        self.n=n

    def eval(self):
        return self.n
    def simplifyed(self):
        return self
        
    def formatted(self):
        return str(self.n)
        
    
