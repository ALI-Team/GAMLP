from src.intnode import IntNode
#from gamlp.intnode import IntNode

print("Testing addnode hash")
print(hash((IntNode(5) + IntNode(5)) + IntNode(10)))
print(hash((IntNode(5) + IntNode(5)) + IntNode(10)))

print("Testing mulnode hash")
print(hash((IntNode(2) * IntNode(3)) * IntNode(10)))
print(hash((IntNode(2) * IntNode(3)) * IntNode(10)))

print("Testing addnode and mulnode hash")
print(hash((IntNode(2) * IntNode(3)) + IntNode(4)))
print(hash((IntNode(2) * IntNode(3)) + IntNode(4)))

print("Testing subnode")
print(hash((IntNode(10) - IntNode(5))))
print(hash((IntNode(10) - IntNode(5))))

print("Testing divnode")
print(hash((IntNode(10) / IntNode(5))))
print(hash((IntNode(10) / IntNode(5))))

print("Testing pownode")
print(hash((IntNode(10) ** IntNode(5))))
print(hash((IntNode(10) ** IntNode(5))))

print("Testing all of them")
print(hash(((IntNode(10)+IntNode(5))*IntNode(3))**((IntNode(10)-IntNode(3)/IntNode(7)))))
print(hash(((IntNode(10)+IntNode(5))*IntNode(3))**((IntNode(10)-IntNode(3)/IntNode(7)))))
