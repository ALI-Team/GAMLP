from .unitnode import UnitNode
from .varnode import VarNode

def var(name):
    return UnitNode(VarNode(name), intnode.IntNode(1))

from . import intnode
