from src.intnode import IntNode
from src.variable import var
from src.equation import Equation
from src.solvers import solver
def simplify_expr(expr):
    print(expr)
    print("    <=>")
    print(expr.simplifyed())


simplify_expr((var("x")*IntNode(5)+var("x")*IntNode(8)))
simplify_expr((var("x")*IntNode(5)*IntNode(2)+var("x")*IntNode(8)+IntNode(2)))
simplify_expr((var("x")+IntNode(2))*(var("x")+IntNode(5)))
simplify_expr((var("x")+IntNode(2))*(var("x")+IntNode(5))*IntNode(2))
simplify_expr((var("x")*IntNode(5)+var("x")*IntNode(8)))
print(solver.solve(Equation((var("x")-IntNode(2))*(var("x")+IntNode(5))*IntNode(2), None)))
simplify_expr((var("x")+IntNode(2))*(var("x")-IntNode(3)))
print(solver.solve(Equation((var("x")+IntNode(2))*(var("x")-IntNode(3)), None)))

simplify_expr((var("x")**IntNode(2)))

print(((var("x")-IntNode(2))*(var("x")+IntNode(5))/IntNode(2)).latex())