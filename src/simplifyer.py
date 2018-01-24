import copy

def separate(node):
    numbers=[]
    term_list=copy.deepcopy(node.terms)
    terms=[]
    for term in term_list:
        print(term)
        simplifyed_term=term.simplifyed()
        print(simplifyed_term)
        if isinstance(simplifyed_term, node.__class__):
            term_list.extend(simplifyed_term.terms)
        elif isinstance(simplifyed_term, intnode.IntNode):
            print("number!")
            print(simplifyed_term.n)
            numbers.append(simplifyed_term.n)
        else:
            terms.append(simplifyed_term)
    return terms, numbers

def simplify_homogen(node):
    terms, numbers=separate(node)
    if len(numbers) > 0:
        terms.append(intnode.IntNode(node.__class__(*list(map(lambda x:intnode.IntNode(x), numbers))).eval()))
        print("t")
        print(terms[-1])
        print(terms[-1].n)
    print("debug")
    print(node)
    print(terms)
    if len(terms)==1 and isinstance(terms[0], intnode.IntNode):
        print("int")
        print(terms[0].n)
        return terms[0]
    
    else:
        return node.__class__(*terms)

from . import intnode
