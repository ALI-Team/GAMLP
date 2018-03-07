import copy

def separate(node):
    numbers=[]
    term_list=copy.deepcopy(node.terms)
    terms=[]
    for term in term_list:
        simplifyed_term=term.simplifyed()
        if isinstance(simplifyed_term, node.__class__):
            term_list.extend(simplifyed_term.terms)
        elif isinstance(simplifyed_term, intnode.IntNode):
            numbers.append(simplifyed_term.n)
        else:
            terms.append(simplifyed_term)
    return terms, numbers

def simplify_homogen(node):
    terms, numbers=separate(node)
    if len(numbers) > 0:
        terms.append(intnode.IntNode(node.__class__(*list(map(lambda x:intnode.IntNode(x), numbers))).eval()))
    #terms.extend(vset.nodes())
    if len(terms)==1:
        return terms[0]
    else:
        return_node=node.__class__()
        return_node.merge_in(*terms)
        if len(return_node.terms) == 1:
            return return_node.terms[0]
        return return_node


from . import intnode
from . import variable
from . import unitnode
