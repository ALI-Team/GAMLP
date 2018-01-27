from .operatornode import OperatorNode
import functools
from . import intnode
# issubclass

class HomogenOperator(OperatorNode):
    def __init__(self, symbol, *terms):
        self.terms=list(terms)
        self.symbol=symbol

    def simplifyed(self):
        term=simplifyer.simplify_homogen(self)
        return term

    def formatted(self):
        return "("+self.symbol.join(map(lambda x:x.formatted(), self.terms))+")"

    def merge_in(self, *nodes):
        for node in nodes:
            merged=False
            for term in self.terms:
                merged_term=self.merge_two(term, node)
                if None != merged_term:
                    self.terms.remove(term)
                    self.terms.append(merged_term)
                    merged=True
                    break
            if not merged:
                self.terms.append(node)
            

    def merge_two(self, term, node):
        print("WARNING MERGE_TWO NOT IMPLEMENTED IN HOMOGENNODE")
        return None
    
class AddNode(HomogenOperator):
    def __init__(self, *terms):
        super().__init__("+", *terms)

    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval(), self.terms))

    def merge_two(self, term, node):
        if isinstance(node, intnode.IntNode) and isinstance(term, intnode.IntNode):
            intnode.IntNode(term.n+node.n)
        if isinstance(node, unitnode.UnitNode) and isinstance(term, unitnode.UnitNode):
            if node.unit==term.unit:
                return unitnode.UnitNode(term.unit, (node.value+term.value).simplifyed())
        return None


class MulNode(HomogenOperator):
    def __init__(self, *terms):
        super().__init__("*", *terms)

    def eval(self):
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval(), self.terms))

    def merge_two(self, term, node):
        if isinstance(term, unitnode.UnitNode) or isinstance(node, unitnode.UnitNode):
            if isinstance(term, unitnode.UnitNode) and isinstance(node, unitnode.UnitNode):
                print("TODO operators unit*unit")
                raise NotImplemented
                #if term.unit == node.unit:
                    #return unitNode.UnitNode()
            if isinstance(term, unitnode.UnitNode):
                unit_node=term
                other_node=node
            elif isinstance(node, unitnode.UnitNode):
                unit_node=node
                other_node=term
            else:
                raise ValueError("um dafuq")
            return_val=unitnode.UnitNode(unit_node.unit, (unit_node.value*other_node).simplifyed())
            return return_val
        return None


                

class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()-self.right.eval()

    def formatted(self):
        return "({}-{})".format(self.left, self.right)




class DivNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()/self.right.eval()

    def formatted(self):
        return "({}/{})".format(self.left, self.right)


class PowNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval()**self.right.eval()

    def formatted(self):
        return "({}^{})".format(self.left, self.right)



from . import simplifyer
from . import unitnode
