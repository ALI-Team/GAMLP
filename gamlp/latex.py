from . import operators
def parentheses(node, parent, s):
    if parent.__class__ in [operators.DivNode, operators.SqrtNode]:
        return s
    if parent==None or parent.priority < node.priority:
        return s
    else:
        return "\\left({}\\right)".format(s)
