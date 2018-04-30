from .operators import *
from .varnode import VarNode
from .unitnode import UnitNode
from .intnode import IntNode
from .equation import Equation
def parse(data):
    def build_node(node):
        symbol=node[0]
        args=node[1:]
        if symbol not in ["#","$"]:
            args=list(map(build_node, args))
        return symbol_converter[symbol](args)
    reading_symbol=True
    symbol=None
    stack=[]
    data_tree=[]
    current_node=data_tree
    current_data=""
    for c in data:
        if c in symbol_converter:
            reading_symbol=False
            symbol=c
            node=[symbol]
            stack.append(node)
            current_node.append(node)
            current_node=node
        elif c=="|":
            pass
            #reading_symbol=True
        elif c=="}":
            if current_data != "":
                current_node.append(current_data)
                current_data=""
            stack.pop()
            if len(stack)>0:
                current_node=stack[-1]
        else:
            current_data+=c
    return build_node(data_tree[0])

            
            
symbol_converter={
    "+":lambda x:AddNode(*x),
    "*":lambda x:MulNode(*x),
    "-":lambda x:SubNode(*x),
    "/":lambda x:DivNode(*x),
    "^":lambda x:PowNode(*x),
    "@":lambda x:UnitNode(*x),
    "=":lambda x:Equation(*x),
    "#":lambda x:IntNode(float(x[0]) if "." in x[0] else int(x[0])),
    "$":lambda x:VarNode(*x)
}
