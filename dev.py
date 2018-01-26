from src.intnode import IntNode
from src.variable import var
print((IntNode(5)*IntNode(2)*var("x")).simplifyed())
print(((IntNode(5)*IntNode(2)*var("x"))+((IntNode(3)+IntNode(2))*var("x"))).simplifyed())
#print(IntNode(5)*var("x")-IntNode(2))
