import copy

def separate(node):
    numbers=[]
    term_list=copy.deepcopy(node.terms)
    terms=[]
    vset=variable.VariableSet()
    for term in term_list:
        simplifyed_term=term.simplifyed()
        if isinstance(simplifyed_term, unitnode.UnitNode):
            vset.append(simplifyed_term)
        elif isinstance(simplifyed_term, node.__class__):
            term_list.extend(simplifyed_term.terms)
        elif isinstance(simplifyed_term, intnode.IntNode):
            numbers.append(simplifyed_term.n)
        else:
            terms.append(simplifyed_term)
    return terms, numbers, vset

def simplify_homogen(node):
    terms, numbers, vset=separate(node)
    print(vset)
    if len(numbers) > 0:
        terms.append(intnode.IntNode(node.__class__(*list(map(lambda x:intnode.IntNode(x), numbers))).eval()))
    terms.extend(vset.nodes())
    if len(terms)==1 and isinstance(terms[0], intnode.IntNode):
        return terms[0]
    else:
        return node.__class__(*terms)

from . import intnode
from . import variable
from . import unitnode
