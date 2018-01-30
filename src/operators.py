from .operatornode import OperatorNode
import functools
from . import intnode
import itertools
import copy
from . import latex
# issubclass

class HomogenOperator(OperatorNode):
    def __init__(self, symbol, *terms):
        self.terms=list(terms)
        self.symbol=symbol

    def __hash__(self):
        terms_hash = 0
        for term in self.terms:
            terms_hash += hash(term)

        return hash(str(terms_hash) + str(hash(self.symbol)))
        
    def formatted(self):
        print(self.terms)
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
        raise NotImplemented

    #def contains(self, value):
        #return True in list(map(lambda x:x.contains(value),self.terms))

    def get_children(self):
        return self.terms
    
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

    def simplifyed(self):
        term=simplifyer.simplify_homogen(self)
        return term

    def latex(self):
        return latex.parentheses("+".join(map(lambda x:x.latex(), self.terms)))


        

class MulNode(HomogenOperator):
    def __init__(self, *terms):
        super().__init__("*", *terms)

    def eval(self):
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval(), self.terms))

    def merge_two(self, term, node):
        if isinstance(term, unitnode.UnitNode) or isinstance(node, unitnode.UnitNode):
            if isinstance(term, unitnode.UnitNode) and isinstance(node, unitnode.UnitNode):
                if term.unit == node.unit:
                    return unitnode.UnitNode(PowNode(term.unit,intnode.IntNode(2)), (term.value*node.value).simplifyed())
                else:
                    return unitnode.UnitNode(term.unit*node.unit, (term.value*node.value).simplifyed())
            else:
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

    def simplifyed(self):
        node=simplifyer.simplify_homogen(self)
        if isinstance(node, MulNode):
            add_nodes=[]
            other=MulNode()
            for term in node.terms:
                if isinstance(term, AddNode):
                    add_nodes.append(term.terms)
                elif isinstance(term, SubNode):
                    add_nodes.append([term.left, term.right*intnode.IntNode(-1)])
                else:
                    other.merge_in(term)
            resulting_node=AddNode()
            for selection in itertools.product(*add_nodes):
                resulting_node.merge_in(MulNode(*other.terms,*selection))
            return resulting_node.simplifyed()

        return node

    def latex(self):
        return latex.parentheses("\\times".join(map(lambda x:x.latex(), self.terms)))


class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def __hash__(self):
        return hash(str(str(hash(self.left))+str(hash(self.right))+str(hash("-"))))
        
    def eval(self):
        return self.left.eval()-self.right.eval()

    def formatted(self):
        return "({}-{})".format(self.left, self.right)

    def simplifyed(self):
        return self

    #def contains(self, value):
    #    return True in [self.left.contains(value), self.right.contains(value)]
    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return latex.parentheses("{}-{}".format(self.left.latex(),self.right.latex()))


class DivNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def __hash__(self):
        return hash(str(str(hash(self.left))+str(hash(self.right))+str(hash("/"))))

    def eval(self):
        return self.left.eval()/self.right.eval()

    def formatted(self):
        return "({}/{})".format(self.left, self.right)

    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return "\\frac{{{}}}{{{}}}".format(self.left.latex(),self.right.latex())

class PowNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def __hash__(self):
        return hash(str(str(hash(self.left))+str(hash(self.right))+str(hash("^"))))
        
    def eval(self):
        return self.left.eval()**self.right.eval()

    def formatted(self):
        return "({}^{})".format(self.left, self.right)

    def contains(self, value):
        return True in [self.left.contains(value), self.right.contains(value)]

    def simplifyed(self):
        if isinstance(self.left, unitnode.UnitNode):
            return unitnode.UnitNode(copy.deepcopy(self.left.unit)**copy.deepcopy(self.right), copy.deepcopy(self.left.value)**copy.deepcopy(self.right)).simplifyed()
        elif isinstance(self.left, MulNode):
            return MulNode(*list(map(lambda x:x**copy.deepcopy(self.right),copy.deepcopy(self.left.terms)))).simplifyed()

        elif isinstance(self.left, AddNode):
            return AddNode(*list(map(lambda x:x**copy.deepcopy(self.right).simplifyed(),copy.deepcopy(self.left.terms)))).simplifyed()
        elif isinstance(self.left, intnode.IntNode) and (self.right, intnode.IntNode):
            if self.right.n == 1:
                return intnode.IntNode(self.right.n)
            elif self.left.n == 1:
                return intnode.IntNode(1)
        return self

    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return "{}^{}".format(self.left.latex(),self.right.latex())
from . import simplifyer
from . import unitnode
