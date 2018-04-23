from . import operators
from . import equation
from . import intnode

class Solver:
    def __init__(self):
        self.methods=[]

    def method(self, grade=None):
        def decorator(f):
            self.methods.append(Method(f, grade=grade))
            return f
        return decorator
    def solve(self, equation):
        for method in self.methods:
            if method.matches(equation.grade):
                ans=method.function(equation)
                if ans==None:
                    continue
                return Solutions({equation.unknown:ans})

        else:
            return None


class Solutions:
    def __init__(self, solutions):
        #self.unknown=unknown
        self.solutions={}
        self.__iadd__(solutions)
        #self.solutions=solutions


    def __iadd__(self, other):
        if isinstance(other,Solutions):
            solutions=other.solutions
        else:
            solutions=other
        for unknown, solutions in solutions.items():
            if unknown in self.solutions:
                self.solutions[unknown].union(solutions)
            else:
                self.solutions[unknown]=set(solutions)
        return self

    def __str__(self):
        if len(self.solutions) == 0:
            return "No solutions found"
        lines=[]
        for unknown, solution in self.solutions.items():
            if len(solution) == 1:
                lines.append("{} = {}".format(unknown, list(solution)[0]))
            elif len(solution) == 0:
                continue
            else:
                lines.extend(list(map(lambda x:"{u}{i} = {val}".format(u=unknown, i=x[0], val=x[1]), enumerate(solution))))
        return "\n".join(lines)

class Method:
    def __init__(self, function, grade=None):
        self.grade=grade
        self.function=function
    def matches(self, grade):
        if self.grade==None or self.grade==grade:
            return True
        return False


def factor_solver(tree):
    tree=tree.simplifyed(target="FACTOR")
    if not isinstance(tree.left, operators.MulNode):
        return None
    roots=list(filter(lambda x:len(x.unknowns())==1, tree.left.terms))
    solutions=Solutions({})
    for root in roots:
        sol=equation.Equation(root, intnode.IntNode(0)).solve()
        if sol != None:
            solutions+=sol
    return solutions
    
        
solver=Solver()
from . import equation_methods

#print(solver.methods)
#solver.solve([])
