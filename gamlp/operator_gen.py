class Operator:
    def __init__(self,name,operator, multi=False):
        self.name=name
        self.operator=operator
        self.multi=multi
    def gen(self):
        print("Generating {}".format(self.name))
        return (node_code if not self.multi else multi_node_code).format(name=self.name, operator=self.operator)

node_code="""
class {name}Node(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval(){operator}self.right.eval()
"""

multi_node_code="""
class {name}Node(OperatorNode):
    def __init__(self, *terms):
        self.terms=terms

    def eval(self):
        return functools.reduce(lambda x,y:x{operator}y, map(lambda z:z.eval()))
"""
operators=[
    Operator("Add","+", multi=True),
    Operator("Sub","-"),
    Operator("Mul","*", multi=True),
    Operator("Div","/"),
    Operator("Pow","**")
]
text="from .operatornode import OperatorNode\nimport functools"
for operator in operators:
    text+=operator.gen()+"\n"
f=open("operators.py","w")
f.write(text)
f.close()
    
