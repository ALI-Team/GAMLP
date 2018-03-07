import re

from . import flags
from .util import output
commands=[]
def command(regex, text):
    def decorator(f):
        commands.append((f,regex, text))
        return f
    return decorator

@command("set ([a-z]+) (on|off)","Set a flag")
def set(flag,val):
    status=flags.set(flag,val=="on")
    if not status:
        output("Unknown flag")

@command("(?:exit|quit)", "Exit")
def exit():
    global go
    go=False

@command("flag ([a-z]+)", "Set multiple flags to True")
def flag_command(f):
    for c in f:
        flags.set(c,True)

@command("get ([a-z]+)", "Get value of flag")
def flag_command(f):
    res=flags.get(f)
    if res == None:
        output("Unknown flag")
    else:
        return(res)

@command("help", "Show help")
def help_command():
    output("Type a command or a expression, exit with exit quit or C-d")

@command("flags", "show flags")
def flags_command():
    output("\n".join(map(lambda x:"{name}({char}) - {text}".format(name=x.name, char=x.char, text=x.text), flags.flags.values())))

@command("commands", "show commands")
def flags_command():
    output("\n".join(map(lambda x:"{regex} - {text}".format(regex=x[1], text=x[2]), commands)))
def parse_command(line):
    for c in commands:
        match=re.match(c[1], line)
        if match != None:
            c[0](*match.groups())
            return True
    return False

