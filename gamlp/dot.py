from . import node
from . import operatornode
from . import unitnode
from . import intnode
from . import equation
def dot_code(tree, debug=False):
    edges=[]
    def build_edge_list(node):
        nonlocal edges

        if isinstance(node, unitnode.UnitNode) and node.value.eq(intnode.IntNode(1)):
            node=node.unit
        children=node.get_children()
        if children==None:
            return
        for child in children:
            if isinstance(child, unitnode.UnitNode) and child.value.eq(intnode.IntNode(1)):
                #print("one unit")
                edges.append((node,child.unit))
                build_edge_list(child.unit)
                continue
            edges.append((node,child))
            build_edge_list(child)
    build_edge_list(tree)
    nodes=set()
    for f,t in edges:
        nodes.add(f)
        nodes.add(t)
    code=""
    i=0
    for node in nodes:
        name=int2base(i, len(digs))
        node.dot_number=i
        node.dot_name=name
        if issubclass(node.__class__,operatornode.OperatorNode) or isinstance(node,unitnode.UnitNode) or isinstance(node, equation.Equation):
            node_style="shape=box "
        else:
            node_style=""
        code+="{} [{}label=\"{}\"];\n".format(name, node_style,node.label(debug=debug))
        i=i+1

    for f,t in edges:
        code+="{} -- {};\n".format(f.dot_name,t.dot_name)
    
    return "graph tree {{\n{}}}".format(code) 
digs="".join(map(chr,range(ord("a"),ord("z")+1)))

def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x //= base

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)
        
        
