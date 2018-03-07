from .node import Node
from . import operators
from . import unitnode
from . import varnode
from . import intnode

class Equation(Node):
    def __init__(self, left, right):
        #TODO
        self.node=left.simplifyed()
        self.find_parts()
        print("Detected {n}:th grade equation".format(n=self.grade))

    def find_parts(self):
        def add_unknown(name, power, value):
            if not name in self.unknowns:
                self.unknowns[name]={}
            self.unknowns[name][power]=value
        self.unknowns={}
        if isinstance(self.node, operators.AddNode):
            self.constant=0
            for term in self.node.terms:
                print(term.__class__)
                if isinstance(term, unitnode.UnitNode):
                    if isinstance(term.unit, varnode.VarNode):
                        add_unknown(term.unit.name,1,term.value.n)
                        #self.unknowns[term.unit.name][0]=term.value.n
                    elif isinstance(term.unit, operators.PowNode):
                        add_unknown(term.unit.left.name,term.unit.right.n,term.value.n)

                if isinstance(term, intnode.IntNode):
                    self.constant=term.n
        else:
            print("UNSUPPORTED WITH A * NODE IN EQ")
            raise NotImplemented
        self.number_unknowns=len(self.unknowns)
        if self.number_unknowns == 1:
            self.unknown=list(self.unknowns)[0]
            self.grade=max(self.unknowns[self.unknown])
            self.exponents=self.unknowns[self.unknown]
            self.exponents[0]=self.constant
        if self.number_unknowns > 1:
            print("UNSUPPORTED WITH MULIPLE UNKNOWNS")
            raise NotImplemented

        if self.number_unknowns == 0:
            print("UNSUPPORTED WITH NO UNKNOWNS")
            raise ValueError
                    
                        

            
        
