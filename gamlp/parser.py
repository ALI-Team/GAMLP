import re

from purplex import Lexer, TokenDef
from purplex import Parser, attach
from purplex import LEFT, RIGHT

from . import node
from .operators import *
from .intnode import IntNode
from .variable import var
from . import equation
from .unitnode import UnitNode
from .varnode import VarNode


class LibLexer(Lexer):

    INTEGER = TokenDef(r'\d+')
    FLOAT = TokenDef(r'(?:\d+)?\.\d+')

    LPAREN = TokenDef(r'\(')
    RPAREN = TokenDef(r'\)')

    TIMES = TokenDef(r'\*')
    DIVIDE = TokenDef(r'/')
    PLUS = TokenDef(r'\+')
    MINUS = TokenDef(r'-')
    POW = TokenDef(r'\^')

    EQ = TokenDef(r'=')

    VAR = TokenDef(r'[a-zA-Z]+')
    UNIT = TokenDef(r'[0-9]+[a-zA-Z]+')

    WHITESPACE = TokenDef(r'[\s\n]+', ignore=True)


class LibParser(Parser):

    LEXER = LibLexer
    START = 'e'

    PRECEDENCE = (
        (RIGHT, 'UMINUS'),
        (LEFT, 'POW'),
        (LEFT, 'TIMES', 'DIVIDE'),
        (LEFT, 'PLUS', 'MINUS'),
        (LEFT, 'EQ'),
    )

    @attach('e : LPAREN e RPAREN')
    def brackets(self, lparen, expr, rparen):
        return expr

    @attach('e : e PLUS e')
    def addition(self, left, op, right):
        return left + right

    @attach('e : e MINUS e')
    def subtract(self, left, op, right):
        return SubNode(left,right)

    @attach('e : e TIMES e')
    def multiply(self, left, op, right):
        return MulNode(left,right)

    @attach('e : e DIVIDE e')
    def division(self, left, op, right):
        return DivNode(left,right)

    @attach('e : e POW e')
    def power(self, left, op, right):
        return PowNode(left,right)

    @attach('e : MINUS e', prec_symbol='UMINUS')
    def negate(self, minus, expr):
        if isinstance(expr, IntNode):
            return IntNode(-expr.n)
        else:
            return MulNode(expr, IntNode(-1))

    @attach('e : INTEGER')
    def number(self, num):
        return IntNode(int(num))

    @attach('e : FLOAT')
    def float(self, num):
        return IntNode(float(num))

    @attach('e : VAR')
    def variable(self, name):
        return var(name)
    @attach('e : UNIT')
    def unit(self, unit):
        match=re.match("([0-9]+)([a-z]+)",unit)
        return UnitNode(VarNode(match.group(2)),IntNode(int(match.group(1))))

    @attach('e : e EQ e')
    def eq(self, left, eq, right):
        return equation.Equation(left,right)
def parse(s):
    return parser.parse(s)

def parse(s):
    return parser.parse(s)


parser = LibParser()
