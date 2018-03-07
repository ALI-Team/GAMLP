from gamlp.parser import parse
from gamlp import dot
import os
import re
commands=[]
def command(regex):
    def decorator(f):
        commands.append((f,regex))
        return f
    return decorator

@command("set ([a-z]+) (on|off)")
def set(flag,val):
    flags[flag]=val=="on"

@command("(?:exit|quit)")
def exit():
    global go
    go=False

@command("flag ([a-z]+)")
def flag_command(f):
    for c in f:
        flags[c]=True

@command("get ([a-z]+)")
def flag_command(f):
    print(flags.get(f))

flags={}
go=True

while go:
    try:
        expr=input(">>> ")
    except EOFError:
        break
    for c in commands:
        match=re.match(c[1], expr)
        if match != None:
            c[0](*match.groups())
            break
    else:
        tree=parse(expr)
        if flags.get("s"):
            tree=tree.simplifyed()
        if flags.get("l"):
            print(tree.latex())
        else:
            print(tree)

        if flags.get("d") or flags.get("b"):
            with open("/tmp/dot.dot", "w") as f:
                f.write(dot.dot_code(tree, debug=flags.get("debug", False)))
        if flags.get("b"):
            os.system("cat /tmp/dot.dot | dot -Tpng > dot.png")
