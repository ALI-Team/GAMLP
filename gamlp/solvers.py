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
                return Solutions(equation.unknown,ans)

        else:
            return None


class Solutions:
    def __init__(self, unknown, solutions):
        self.unknown=unknown
        self.solutions=solutions


    def __str__(self):
        if len(self.solutions) == 1:
            return "{} = {}".format(self.unknown, self.solutions[0])
        elif len(self.solutions) == 0:
            return "No solutions found"
        else:
            return "\n".join(map(lambda x:"{u}{i} = {val}".format(u=self.unknown, i=x[0], val=x[1]), enumerate(self.solutions)))

class Method:
    def __init__(self, function, grade=None):
        self.grade=grade
        self.function=function
    def matches(self, grade):
        if self.grade==None or self.grade==grade:
            return True
        return False


def factor_solver(tree):
    pass
    
        
solver=Solver()
from . import equation_methods

#print(solver.methods)
#solver.solve([])
