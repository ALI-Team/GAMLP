import copy

def separate(node,target=None, context=None):
    numbers=[]
    if isinstance(node, operators.MulNode):
        expanded_terms=[]
        for term in node.terms:
            if isinstance(term, unitnode.UnitNode):
                expanded_terms.append(unitnode.UnitNode(term.unit, intnode.IntNode(1)))
                expanded_terms.append(term.value)
            else:
                expanded_terms.append(term)
    else:
        expanded_terms=node.terms
            
        
    term_list=copy.deepcopy(expanded_terms)
    terms=[]
    for term in term_list:
        simplifyed_term=term.simplifyed(target=target, context=context)
        int_val=simplifyed_term.get_int_value()
        if int_val != None:
            numbers.append(int_val.n)
        elif isinstance(simplifyed_term, node.__class__):
            term_list.extend(simplifyed_term.terms)
        elif isinstance(simplifyed_term, intnode.IntNode):
            numbers.append(simplifyed_term.n)
        else:
            terms.append(simplifyed_term)
    return terms, numbers

def simplify_homogen(node,target=None, context=None):
    terms, numbers=separate(node,target=target, context=context)
    if len(numbers) > 0:
        terms.append(intnode.IntNode(node.__class__(*list(map(lambda x:intnode.IntNode(x), numbers))).eval()))
    #terms.extend(vset.nodes())
    if len(terms)==1:
        return terms[0]
    else:
        return_node=node.__class__()
        return_node.merge_in(*terms, target=target, context=context)
        if len(return_node.terms) == 1:
            return return_node.terms[0]
        return return_node


from . import intnode
from . import variable
from . import unitnode
from . import operators
