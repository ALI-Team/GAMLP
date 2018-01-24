class Operator:
    def __init__(self,name,operator):
        self.name=name
        self.operator=operator
    def gen(self):
        print("Generating {}".format(self.name))
        return node_code.format(name=self.name, operator=self.operator)

node_code="""
class {name}Node(OperatorNode):
    def __init__(self, left, right):
        self.left=left
        self.right=right
    def eval(self):
        return self.left.eval(){operator}self.right.eval()
"""

operators=[
    Operator("Add","+"),
    Operator("Sub","-"),
    Operator("Mul","*"),
    Operator("Div","/"),
    Operator("Pow","**")
]
text="from operatornode import OperatorNode"
for operator in operators:
    text+=operator.gen()+"\n"
f=open("operators.py","w")
f.write(text)
f.close()
    
