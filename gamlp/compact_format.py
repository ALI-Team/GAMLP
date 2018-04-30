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
    stack=[]
    data_tree=[]
    current_node=data_tree
    current_data=""
    for c in data:
        if c in number_charset and current_data=="":
            symbol="#"
            node=[symbol]
            stack.append(node)
            current_node.append(node)
            current_node=node
            current_data=c
        elif c in var_charset and current_data=="":
            symbol="$"
            node=[symbol]
            stack.append(node)
            current_node.append(node)
            current_node=node
            current_data=c
        elif c in symbol_converter:
            symbol=c
            node=[symbol]
            stack.append(node)
            current_node.append(node)
            current_node=node
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

number_charset=set(map(str,range(10))).union(["_","."])
var_charset=set(map(chr,range(ord("a"),ord("z")+1))).union(map(chr,range(ord("A"),ord("Z")+1)))

def create_unitnode(x):
    if len(x)==1:
        return UnitNode(x[0], IntNode(1))
    else:
        return UnitNode(*x)
            
symbol_converter={
    "+":lambda x:AddNode(*x),
    "*":lambda x:MulNode(*x),
    "-":lambda x:SubNode(*x),
    "|":lambda x:DivNode(*x),
    ";":lambda x:SqrtNode(*x),
    "^":lambda x:PowNode(*x),
    "@":create_unitnode,
    "=":lambda x:Equation(*x),
    "#":lambda x:IntNode(float(x[0].replace("_","-")) if "." in x[0] else int(x[0].replace("_","-"))),
    "$":lambda x:VarNode(*x)
}
