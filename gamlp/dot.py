from . import node
from . import operatornode
from . import unitnode
from . import intnode
from . import equation
def dot_code(tree, debug=False, child_label_amount=1, direction="V"):
    edges=[]
    def build_edge_list(node):
        nonlocal edges
        #nonlocal nodes

        if isinstance(node, unitnode.UnitNode) and node.value.eq(intnode.IntNode(1)):
            node=node.unit
        children=node.get_children()
        if children==None:
            nodes.add(node)
            return
        child_labels=node.child_labels(amount=child_label_amount)
        have_child_labels = not child_labels==None
        if have_child_labels and isinstance(child_labels, str):
            individual_child_labels=False
        else:
            individual_child_labels=True
        nodes.add(node)
        for i,child in enumerate(children):
            if have_child_labels:
                if individual_child_labels:
                    child_label=child_labels[i]
                else:
                    child_label=child_labels
            else:
                child_label=None
            if isinstance(child, unitnode.UnitNode) and child.value.eq(intnode.IntNode(1)):

                edges.append((node,child.unit, child_label))
                build_edge_list(child.unit)
                continue
            edges.append((node,child,child_label))
            build_edge_list(child)
    nodes=set()
    build_edge_list(tree)
    
    #if len(edges) == 0:
    #    nodes.add(tree)
    for f,t,_ in edges:
        nodes.add(f)
        nodes.add(t)
    code=""
    if direction == "H":
        code+="rankdir=\"LR\";\n"
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

    for f,t,child_label in edges:
        child_label_code=""
        if child_label != None:
            child_label_code="label={} fontsize=9".format(child_label)
        else:
            child_label_code=""

        code+="{} -- {}[{}];\n".format(f.dot_name,t.dot_name,child_label_code)
    
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
        
        
