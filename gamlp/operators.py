import math

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
        
    def formatted(self, parent):
        return util.parentheses(self,parent,self.symbol.join(map(lambda x:x.formatted(self), self.terms)))

    def merge_in(self, *nodes, target=None, context=None):
        for node in nodes:
            merged=False
            for term in self.terms:
                merged_term=self.merge_two(term, node, target=target, context=context)
                if None != merged_term:
                    self.terms.remove(term)
                    self.terms.append(merged_term)
                    merged=True
                    break
            if not merged:
                self.terms.append(node)

    def flattend(self):
        children=[]
        for term in self.terms:
            if isinstance(term, self.__class__):
                children.extend(term.flattend().terms)
            else:
                children.append(term.flattend())
        return self.__class__(*children)
            

    def merge_two(self, term, node, target=None, context=None):
        print("WARNING MERGE_TWO NOT IMPLEMENTED IN HOMOGENNODE")
        raise NotImplemented

    #def contains(self, value):
        #return True in list(map(lambda x:x.contains(value),self.terms))

    def compact_format(self):
        return "{sym}{terms}}}".format(sym=self.symbol, terms="".join(map(lambda x:x.compact_format(),self.terms)))

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
        self.priority=1

    def eval(self):
        return functools.reduce(lambda x,y:x+y, map(lambda z:z.eval(), self.terms))

    def merge_two(self, term, node, target=None, context=None):
        if isinstance(node, intnode.IntNode) and isinstance(term, intnode.IntNode):
            return intnode.IntNode(term.n+node.n)
        if isinstance(node, unitnode.UnitNode) and isinstance(term, unitnode.UnitNode):
            if node.unit.eq(term.unit):
                return unitnode.UnitNode(term.unit, (node.value+term.value)).simplifyed(target=target, context=context)
        return None

    def simplifyed(self, target=None, context=None):
        if self.get_int_value()!=None:
            return self.get_int_value()
        term=simplifyer.simplify_homogen(self, target=target, context=context)
        if isinstance(term,AddNode):
            if len(list(filter(lambda x:x==None or (not x.eq(intnode.IntNode(0))),map(lambda x:x.get_int_value(),term.terms))))==1:
                #Only non 0 element
                return list(filter(lambda x:x[1]==None or (not x[1].eq(intnode.IntNode(0))),map(lambda x:(x,x.get_int_value()),term.terms)))[0][0]
        return term

    def latex(self, parent):
        return latex.parentheses(self, parent, "+".join(map(lambda x:x.latex(self), self.terms)))


        

class MulNode(HomogenOperator):
    def __init__(self, *terms):
        super().__init__("*", *terms)
        self.priority=2

    def eval(self):
        return functools.reduce(lambda x,y:x*y, map(lambda z:z.eval(), self.terms))

    def merge_two(self, term, node, target=None, context=None):
        def strip_unit(x):
            if isinstance(x, unitnode.UnitNode) and x.value.eq(intnode.IntNode(1)):
                return (x.unit,True)
            return (x, False)
        def unit_wrap(x):
            if is_unit:
                return unitnode.UnitNode(x, intnode.IntNode(1))
            else:
                return x

        term,term_unit=strip_unit(term)
        node,node_unit=strip_unit(node)
        is_unit=term_unit or node_unit
        """
        if isinstance(term, unitnode.UnitNode) or isinstance(node, unitnode.UnitNode):
            if isinstance(term, unitnode.UnitNode) and isinstance(node, unitnode.UnitNode):
                if term.unit.eq(node.unit):
                    return unitnode.UnitNode(PowNode(term.unit,intnode.IntNode(2)), (term.value*node.value).simplifyed(target=target, context=context))
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
                return_val=unitnode.UnitNode(unit_node.unit, (unit_node.value*other_node)).simplifyed(target=target, context=context)
                return return_val
        """
        if term.eq(node):
            return unit_wrap(PowNode(term, intnode.IntNode(2)).simplifyed(target=target, context=context))
        if isinstance(term, PowNode) or isinstance(node, PowNode):
            if isinstance(term, PowNode) and isinstance(node, PowNode) and term.left.eq(node.left):
                return unit_wrap(PowNode(term.left, AddNode(term.right,node.right)).simplifyed(target=target, context=context))
            if isinstance(term, PowNode):
                pownode=term
                other=node
            else:
                pownode=node
                other=term
            if pownode.left.eq(other):
                return unit_wrap(PowNode(pownode.left,AddNode(pownode.right+intnode.IntNode(1)).simplifyed(target=target, context=context)).simplifyed(target=target, context=context))
        return None
    def label(self, debug=False):
        return "×"

    def simplifyed(self, target=None, context=None):
        if self.get_int_value()!=None:
            return self.get_int_value()
        node=simplifyer.simplify_homogen(self, target=target, context=context)
        if isinstance(node, MulNode):
            unitnodes=[]
            others=[]
            for child_node in node.terms:
                iv=child_node.get_int_value()
                if iv != None and iv.eq(intnode.IntNode(1)):
                    continue
                elif isinstance(child_node, unitnode.UnitNode):
                    unitnodes.append(child_node)
                else:
                    others.append(child_node)
            if len(unitnodes) == len(others) == 1:
                if not others[0].contains_unknowns():
                    node=unitnode.UnitNode(unitnodes[0].unit, MulNode(unitnodes[0].value, others[0])).simplifyed(target=target, context=target)
        if target=="FACTOR":
            return node
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
                    other.merge_in(term, target=target, context=context)
            resulting_node=AddNode()
            for selection in itertools.product(*add_nodes):
                resulting_node.merge_in(MulNode(*other.terms,*selection), target=target, context=context)
            if len(resulting_node.terms)==1:
                if issubclass(resulting_node.terms[0].__class__,HomogenOperator) and len(resulting_node.terms[0].terms)==1:
                    return resulting_node.terms[0].terms[0]
                    
                return resulting_node.terms[0]
            return resulting_node.simplifyed(target=target, context=target)
        return node

    def latex(self, parent):
        return latex.parentheses(self, parent, " \\times ".join(map(lambda x:x.latex(self), self.terms)))


class SubNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
        self.priority=1

    def hash_node(self):
        return hash(str(str(self.left.hash_node())+str(self.right.hash_node())+str(hash("-"))))
        
    def eval(self):
        return self.left.eval()-self.right.eval()

    def formatted(self, parent):
        return util.parentheses(self,parent,"{}-{}".format(self.left.formatted(self), self.right.formatted(self)))

    def simplifyed(self, target=None, context=None):
        if self.get_int_value()!=None:
            return self.get_int_value()
        return AddNode(self.left, (self.right*intnode.IntNode(-1))).simplifyed(target=target, context=context)

    #def contains(self, value):
    #    return True in [self.left.contains(value), self.right.contains(value)]
    def get_children(self):
        return [self.left, self.right]

    def latex(self, parent):
        return latex.parentheses(self, parent,"{}-{}".format(self.left.latex(self),self.right.latex(self)))

    def label(self, debug=False):
        return "-"
    def child_labels(self, amount=1):
        if amount > 0:
            return ["left","right"]
        else:
            return None

    def flattend(self):
        return SubNode(self.left.flattend(), self.right.flattend())

    def compact_format(self):
        return "-{left}{right}}}".format(left=self.left.compact_format(), right=self.right.compact_format())

class DivNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
        self.priority=2

    def hash_node(self):
        return hash(str(str(self.left.hash_node())+str(self.right.hash_node())+str(hash("/"))))

    def eval(self):
        return self.left.eval()/self.right.eval()

    def formatted(self, parent):
        return util.parentheses(self,parent,"{}/{}".format(self.left.formatted(self), self.right.formatted(self)))
    
    def get_children(self):
        return [self.left, self.right]

    def latex(self, parent):
        return "\\frac{{{}}}{{{}}}".format(self.left.latex(self),self.right.latex(self))

    def simplifyed(self, target=None, context=None):
        if self.get_int_value()!=None:
            return self.get_int_value()
        return MulNode(self.left, (PowNode(self.right, intnode.IntNode(-1)))).simplifyed(target=target, context=context)

    def label(self, debug=False):
        return "/"

    def child_labels(self, amount=1):
        if amount > 0:
            return ["Numerator","Denominator"]
        else:
            return None

    def flattend(self):
        return DivNode(self.left.flattend(), self.right.flattend())

    def compact_format(self):
        return "|{left}{right}}}".format(left=self.left.compact_format(), right=self.right.compact_format())
    
class PowNode(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
        self.priority=3

    def hash_node(self):
        return hash(str(str(self.left.hash_node())+str(self.right.hash_node())+str(hash("^"))))
        
    def eval(self):
        return self.left.eval()**self.right.eval()

    def formatted(self, parent):
        return util.parentheses(self,parent,"{}^{}".format(self.left.formatted(self), self.right.formatted(self)))

    def contains(self, value):
        return True in [self.left.contains(value), self.right.contains(value)]

    def simplifyed(self, target=None, context=None):
        if self.get_int_value() != None:
            return self.get_int_value()
        if self.right.get_int_value()==0:
            return intnode.IntNode(1)
        left=self.left.simplifyed(target=target, context=context)
        right=self.right.simplifyed(target=target, context=context)
        if isinstance(left, unitnode.UnitNode):
            return unitnode.UnitNode(copy.deepcopy(left.unit)**copy.deepcopy(right), copy.deepcopy(left.value)**copy.deepcopy(right)).simplifyed(target=target, context=context)
        elif isinstance(left, MulNode):
            return MulNode(*list(map(lambda x:x**copy.deepcopy(self.right),copy.deepcopy(left.terms)))).simplifyed(target=target, context=context)
        elif isinstance(left, PowNode):
            return PowNode(left.left, MulNode(left.right,right)).simplifyed(target=target, context=context)

        elif isinstance(left, AddNode) and right.get_int_value() != None and target!="FACTOR":
            l = len(left.terms)
            exponent = right.get_int_value().n
            if l == 0:
                return intnode.IntNode(0)

            if exponent < 0:
                return PowNode(left, right) 
            
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
                term = MulNode(*[multinomial_factor, *factors]).simplifyed(target=target, context=context)
                result_terms.append(term)
            return AddNode(*result_terms)
                
            
        right_value=self.right.get_int_value()
        if right_value != None and right_value.eq(intnode.IntNode(1)):
            return self.left.simplifyed(target=target, context=context)
        elif right_value != None and right_value.eq(intnode.IntNode(0)):
            return intnode.IntNode(1)
        return PowNode(left, right) 

    def get_children(self):
        return [self.left, self.right]

    def latex(self, parent):
        return "{{{}}}^{{{}}}".format(latex.parentheses(self,parent, self.left.latex(self)),self.right.latex(self))
    def label(self, debug=False):
        return "^"
    def child_labels(self, amount=1):
        if amount > 0:
            return ["Base","Exponent"]
        else:
            return None

    def flattend(self):
        return PowNode(self.left.flattend(), self.right.flattend())

    def compact_format(self):
        return "^{left}{right}}}".format(left=self.left.compact_format(), right=self.right.compact_format())

class SqrtNode(OperatorNode):
    def __init__(self, term):
        self.term=term
        self.priority=4

    def hash_node(self):
        return hash(str(self.term.hash_node())+"sqrt")

    def eval(self):
        return math.sqrt(self.term.eval())

    def formatted(self, parent):
        return util.parentheses(self,parent,"√({})".format(self.term.formatted(self)))
    
    def get_children(self):
        return [self.term]

    def latex(self, parent):
        return "\\sqrt{{{}}}".format(self.term.latex(self))

    def simplifyed(self, target=None, context=None):
        if self.get_int_value()!=None:
            return self.get_int_value()
        return PowNode(self.term,intnode.IntNode(0.5)).simplifyed(target=target, context=context)

    def label(self, debug=False):
        return "√"

    def child_labels(self, amount=1):
        if amount > 1:
            return ["Term"]
        else:
            return None

    def flattend(self):
        return SqrtNode(self.term.flattend())

    def compact_format(self):
        return ";{term}}}".format(term=self.term.compact_format())

from . import simplifyer
from . import unitnode
