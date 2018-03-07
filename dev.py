
from gamlp import dot
from gamlp.intnode import IntNode
from gamlp.variable import var
from gamlp.equation import Equation
from gamlp.solvers import solver
from gamlp.operators import *
i=IntNode
v=var

def simplify_expr(expr):
    print(expr)
    print("    <=>")
    print(expr.simplifyed())

def gdot(tree):
    with open("/tmp/dot.dot", "w") as f:
        f.write(dot.dot_code(tree))

        


#simplify_expr((var("x")*IntNode(5)*IntNode(2)+var("x")*IntNode(8)+IntNode(2)))
#simplify_expr(IntNode(5)+IntNode(3))
#simplify_expr(IntNode(5)-IntNode(3))
#simplify_expr((var("x")+IntNode(2))*(var("x")+IntNode(5))*IntNode(2))
#simplify_expr((var("x")*IntNode(5)+var("x")*IntNode(8)))
#print(solver.solve(Equation((var("x")-IntNode(2))*(var("x")+IntNode(5))*IntNode(2), None)))
#simplify_expr((var("x")+IntNode(2))*(var("x")-IntNode(3)))
#print(solver.solve(Equation((var("x")+IntNode(2))*(var("x")-IntNode(3)), None)))

#print(((var("x")-IntNode(2))*(var("x")+IntNode(5))/IntNode(2)).latex())

#simplify_expr(IntNode(5)-IntNode(3))
#simplify_expr((var("x")*IntNode(5)*IntNode(2)-var("x")*IntNode(8)+IntNode(2)))
#print((IntNode(50)*var("x"))/IntNode(10))
#simplify_expr((i(10)**i(-1))*i(50))
#(((10^-1)*50))

#simplify_expr((IntNode(50)*var("x"))/IntNode(10))
#print(dot.dot_code(AddNode(var,i(2),i(3),i(4),i(5))))
#print(solver.solve(Equation(((IntNode(50)*var("x"))/IntNode(10))+i(10),None)))


#gdot((v("a")*v("b")*v("c")*i(3)*i(5)))
gdot((v("a")*v("b")*v("c")*i(3)*i(5)).simplifyed())
#gdot(((v("a")*v("b")*v("c")).simplifyed()*(i(3)*i(5))))
#gdot((v("a")*v("b")*v("c")).simplifyed())
