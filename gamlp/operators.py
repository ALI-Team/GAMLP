from .operatornode import OperatorNode
import functools
from . import intnode
import itertools
import copy
from . import latex
from . import util

# issubclass

class HomogenOperator(OperatorNode):
    def __init__(self, symbol, *terms):
        self.terms=list(terms)
        self.symbol=symbol

    def hash_node(self):
        terms_hash = 0
        for term in self.terms:
            terms_hash += term.hash_node()

        return hash(str(terms_hash) + str(hash(self.symbol)))
        
    def formatted(self):
        #print(self.terms)
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

    def label(self, debug=False):
        return self.symbol

    def child_labels(self, amount=1):
        if amount > 1:
            return "Term"
        else:
            return None
        
    
class AddNode(HomogenOperator):
    def __init__(self, *terms):
        super().__init__("+", *terms)

    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval(), self.terms))

    def merge_two(self, term, node):
        if isinstance(node, intnode.IntNode) and isinstance(term, intnode.IntNode):
            return intnode.IntNode(term.n+node.n)
        if isinstance(node, unitnode.UnitNode) and isinstance(term, unitnode.UnitNode):
            if node.unit.eq(term.unit):
                return unitnode.UnitNode(term.unit, (node.value+term.value)).simplifyed()
        return None

    def simplifyed(self):
        if self.get_int_value()!=None:
            return self.get_int_value()
        term=simplifyer.simplify_homogen(self)
        if isinstance(term,AddNode):
            if len(term.terms)==1:
                return term.terms[0]
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
                if term.unit.eq(node.unit):
                    return unitnode.UnitNode(PowNode(term.unit,intnode.IntNode(2)), (term.value*node.value).simplifyed())
                else:
                    pass
                    #return unitnode.UnitNode((term.unit*node.unit).simplifyed(), (term.value*node.value).simplifyed())
            else:
                if isinstance(term, unitnode.UnitNode):
                    unit_node=term
                    other_node=node
                elif isinstance(node, unitnode.UnitNode):
                    unit_node=node
                    other_node=term
                else:
                    raise ValueError("um dafuq")
                return_val=unitnode.UnitNode(unit_node.unit, (unit_node.value*other_node)).simplifyed()
                return return_val
        if isinstance(term, PowNode) or isinstance(node, PowNode):
            if isinstance(term, PowNode):
                pownode=term
                other=node
            else:
                pownode=node
                other=term
            if pownode.left.eq(other):
                return PowNode(pownode.left,AddNode(pownode.right+intnode.IntNode(1)).simplifyed()).simplifyed()
        return None
    def label(self, debug=False):
        return "×"

    def simplifyed(self):
        if self.get_int_value()!=None:
            return self.get_int_value()
        node=simplifyer.simplify_homogen(self)
        if isinstance(node, MulNode):
            add_nodes=[]
            other=MulNode()
            for term in node.terms:
                term_int_val=term.get_int_value()
                if  term_int_val != None and term_int_val.eq(intnode.IntNode(1)):
                    continue
                if isinstance(term, AddNode):
                    add_nodes.append(term.terms)
                elif isinstance(term, SubNode):
                    add_nodes.extend([term.left, term.right*intnode.IntNode(-1)])
                else:
                    other.merge_in(term)
            resulting_node=AddNode()
            for selection in itertools.product(*add_nodes):
                resulting_node.merge_in(MulNode(*other.terms,*selection))
            if len(resulting_node.terms)==1:
                if issubclass(resulting_node.terms[0].__class__,HomogenOperator) and len(resulting_node.terms[0].terms)==1:
                    return resulting_node.terms[0].terms[0]

                    
                return resulting_node.terms[0]
            return resulting_node.simplifyed()

        return node

    def latex(self):
        return latex.parentheses("\\times".join(map(lambda x:x.latex(), self.terms)))


class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def hash_node(self):
        return hash(str(str(self.left.hash_node())+str(self.right.hash_node())+str(hash("-"))))
        
    def eval(self):
        return self.left.eval()-self.right.eval()

    def formatted(self):
        return "({}-{})".format(self.left, self.right)

    def simplifyed(self):
        if self.get_int_value()!=None:
            return self.get_int_value()
        return AddNode(self.left, (self.right*intnode.IntNode(-1))).simplifyed()

    #def contains(self, value):
    #    return True in [self.left.contains(value), self.right.contains(value)]
    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return latex.parentheses("{}-{}".format(self.left.latex(),self.right.latex()))

    def label(self, debug=False):
        return "-"
    def child_labels(self, amount=1):
        if amount > 0:
            return ["left","right"]
        else:
            return None

class DivNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def hash_node(self):
        return hash(str(str(self.left.hash_node())+str(self.right.hash_node())+str(hash("/"))))

    def eval(self):
        return self.left.eval()/self.right.eval()

    def formatted(self):
        return "({}/{})".format(self.left, self.right)
    
    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return "\\frac{{{}}}{{{}}}".format(self.left.latex(),self.right.latex())

    def simplifyed(self):
        if self.get_int_value()!=None:
            return self.get_int_value()
        return MulNode(self.left, (PowNode(self.right, intnode.IntNode(-1)))).simplifyed()

    def label(self, debug=False):
        return "/"

    def child_labels(self, amount=1):
        if amount > 0:
            return ["Numerator","Denominator"]
        else:
            return None
    
class PowNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def hash_node(self):
        return hash(str(str(self.left.hash_node())+str(self.right.hash_node())+str(hash("^"))))
        
    def eval(self):
        return self.left.eval()**self.right.eval()

    def formatted(self):
        return "(({})^({}))".format(self.left, self.right)

    def contains(self, value):
        return True in [self.left.contains(value), self.right.contains(value)]

    def simplifyed(self):
        if self.get_int_value() != None:
            return self.get_int_value()
        if self.right.get_int_value()==0:
            return intnode.IntNode(1)
        left=self.left.simplifyed()
        right=self.right.simplifyed()
        if isinstance(left, unitnode.UnitNode):
            return unitnode.UnitNode(copy.deepcopy(left.unit)**copy.deepcopy(right), copy.deepcopy(left.value)**copy.deepcopy(right)).simplifyed()
        elif isinstance(left, MulNode):
            return MulNode(*list(map(lambda x:x**copy.deepcopy(self.right),copy.deepcopy(left.terms)))).simplifyed()

        elif isinstance(left, AddNode) and right.get_int_value() != None:
            l = len(left.terms)
            exponent = right.get_int_value().n
            if l == 0:
                return intnode.IntNode(0)
            
            combs = itertools.combinations_with_replacement(range(l), exponent)
            exp_factorial = util.factorial(exponent)
            result_terms = []
    
            for comb in combs:
                exponents = [0] * l
                for factor in comb:
                    exponents[factor] += 1
            
                denominator = 1
                for exp in exponents:
                    denominator *= util.factorial(exp)

                multinomial_factor = intnode.IntNode(int(exp_factorial / denominator))
                factors = []
                for i in range(l):
                    if exponents[i] == 0:
                        continue
                    
                    if exponents[i] == 1:
                        factor = left.terms[i]
                    else:
                        factor = PowNode(left.terms[i], intnode.IntNode(exponents[i]))
                        
                    factors.append(factor)
                term = MulNode(*[multinomial_factor, *factors]).simplifyed()
                result_terms.append(term)
            return AddNode(*result_terms)
                
            
        right_value=self.right.get_int_value()
        if right_value.eq(intnode.IntNode(1)):
            return self.left.simplifyed()
        elif right_value.eq(intnode.IntNode(0)):
            return intnode.IntNode(1)
        return PowNode(left, right) 

    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return "{{{}}}^{{{}}}".format(self.left.latex(),self.right.latex())
    def label(self, debug=False):
        return "^"
    def child_labels(self, amount=1):
        if amount > 0:
            return ["Base","Exponent"]
        else:
            return None
from . import simplifyer
from . import unitnode
