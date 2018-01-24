
from node import Node
class IntNode(Node):
    def __init__(self,n):
        super().__init__()
        self.n=n

    def eval(self):
        return self.n
        
        
    
