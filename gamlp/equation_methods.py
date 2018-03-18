from .solvers import solver
import math
@solver.method(grade=2)
def pq_solver(equation):
    #UGLY AF
    exps=equation.exponents

    if not 1 in exps:
        return None
    
    sqrt_part=math.sqrt(exps[1]**2-(4*exps[2]*exps[0]))
    eq=lambda x:(-exps[1]+x)/(2*exps[2])
    return [eq(sqrt_part), eq(-sqrt_part)]
    #equation.unknowns

@solver.method(grade=1)
def grade_one_solver(equation):
    #UGLY AF
    exps=equation.exponents
    return [(-exps[0])/exps[1]]
    #equation.unknowns

@solver.method(grade=None)
def easy_exp_solver(equation):
    exps = equation.exponents
    
    exponent = 0
    coefficient = 0

    if 0 in exps:
        otherval = exps[0]
    else:
        otherval = 0
        
    for exp,val in exps.items():
        if exp != 0 and exponent == 0:
            exponent = exp
            coefficient = val
        elif exp != 0 and exponent != 0:
            return None
            
    if exponent == 0 or coefficient < 0:
        return None
    
    return [((-otherval/coefficient)**(1/exponent))]
