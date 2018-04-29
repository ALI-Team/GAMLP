from operators import *
from varnode import VarNode
from unitnode import UnitNode
def parse(data):
    reading_symbol=True
    symbol=None

    for c in data:
        if reading_symbol:
            symbol=symbol
        else:
            if 
symbol_converter={
    "+":lambda x:AddNode(*x),
    "*":lambda x:MulNode(*x),
    "-":lambda x:SubNode(*x),
    "/":lambda x:DivNode(*x),
    "^":lambda x:PowNode(*x),
    "@":lambda x:UnitNode(*x),
    "#":lambda x:IntNode(float(x[0]) if "." in x[0] else int(x[0])),
    "$":lambda x:VarNode(*x)
}
