from .node import Node
from . import operators
from . import unitnode
from . import varnode
from . import intnode
from . import solvers

class Equation(Node):
    def __init__(self, left, right):
        self.left=left
        self.right=right
        self.priority=0

    def simplifyed(self, target=None, context=None):
        return Equation((self.left-self.right).simplifyed(target=target, context=context),intnode.IntNode(0))

    def solve(self):
        factor_node=self.clone()
        self.find_parts()
        sol=solvers.solver.solve(self)
        if sol != None:
            return sol
        factor_sol=solvers.factor_solver(factor_node)


    
    def formatted(self, parent):
        #print(self.terms)
        return "{}={}".format(self.left.formatted(self), self.right.formatted(self))
    def label(self, debug=False):
        return "="

    def child_labels(self, amount=1):
        if amount > 1:
            return ["Left","Right"]
        else:
            return None

    def get_children(self):
        return [self.left, self.right]

    def latex(self):
        return "{} \eq {}".format(self.left.latex(), self.right.latex())
        

    def find_parts(self):
        self.node=self.simplifyed().left
        def add_unknown(name, power, value):
            if not name in self.unknowns:
                self.unknowns[name]={}
            self.unknowns[name][power]=value
        self.unknowns={}
        if isinstance(self.node, operators.AddNode):
            self.constant=0
            for term in self.node.terms:
                if not term.contains_unknowns():
                    self.constant+=term.eval()
                elif isinstance(term, unitnode.UnitNode):
                    if term.value.contains_unknowns():
                        print("Unknowns in value of unitnode in eq solver equation.py WTF")
                        raise ValueError
                    amount=term.value.eval()
                    if isinstance(term.unit, varnode.VarNode):
                        add_unknown(term.unit.name,1,amount)
                    elif isinstance(term.unit, operators.PowNode):
                        if term.unit.right.contains_unknowns():
                            print("Var in exp not supported")
                            raise ValueError 

                        add_unknown(term.unit.left.name,term.unit.right.eval(),amount)
        else:
            print("UNSUPPORTED WITH A * NODE IN EQ")
            raise NotImplementedError
        self.number_unknowns=len(self.unknowns)
        if self.number_unknowns == 1:
            self.unknown=list(self.unknowns)[0]
            self.grade=max(self.unknowns[self.unknown])
            self.exponents=self.unknowns[self.unknown]
            self.exponents[0]=self.constant
        if self.number_unknowns > 1:
            print("UNSUPPORTED WITH MULIPLE UNKNOWNS")
            raise NotImplementedError

        if self.number_unknowns == 0:
            print("UNSUPPORTED WITH NO UNKNOWNS")
            raise ValueError
                    
                        

            
        
