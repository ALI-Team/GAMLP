from .solvers import solver
import math
@solver.method(grade=2)
def pq_solver(equation):
    #UGLY AF
    exps=equation.exponents
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
