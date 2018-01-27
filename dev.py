from src.intnode import IntNode
from src.variable import var
def simplify_expr(expr):
    print(expr)
    print("    <=>")
    print(expr.simplifyed())

simplify_expr((var("x")*IntNode(5)+var("x")*IntNode(8)))
simplify_expr((var("x")*IntNode(5)*IntNode(2)+var("x")*IntNode(8)+IntNode(2)))
simplify_expr((var("x")*IntNode(5)+var("x")*IntNode(8)))
simplify_expr((var("x")*IntNode(5)+var("x")*IntNode(8)))
