def dot_code(tree):
    edges=[]
    def build_edge_list(node):
        nonlocal edges
        children=node.get_children()
        if children==None:
            return
        for child in children:
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
        code+="{} [label=\"{}\"];\n".format(name, node.label())
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
        
        
