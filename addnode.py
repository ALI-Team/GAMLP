from operatornode import OperatorNode
class AddNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()+self.right.eval()
        
