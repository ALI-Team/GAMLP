from src.intnode import IntNode
from src.varnode import VarNode
print(((IntNode(5)*IntNode(2)*VarNode("x"))*(IntNode(3)+IntNode(2))).simplifyed().terms[1].n)
