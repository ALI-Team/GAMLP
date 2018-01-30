class Solver:
    def __init__(self):
        self.methods=[]

    def method(self, grade=None):
        def decorator(f):
            self.methods.append(Method(f, grade=grade))
            return f
        return decorator
    def solve(self, equation):
        print("running solver")
        method=self.find_method(grade=equation.grade)
        if method==None:
            print("NO METHOD FOUND")
            raise ValueError
        print(method.function)
        return method.function(equation)

    def find_method(self, grade=None):
        for method in self.methods:
            if method.matches(grade):
                return method
        return None

class Method:
    def __init__(self, function, grade=None):
        self.grade=grade
        self.function=function
    def matches(self, grade):
        if self.grade==grade:
            return True
        return False
    
        
solver=Solver()
from . import equation_methods

#print(solver.methods)
#solver.solve([])
