def set(flag,state):
    char=find_char(flag)
    if char==None:
        return False
    flag_state[char]=state
    return True
def get(flag, *args):
    char=find_char(flag)
    if char==None:
        return None
    if not char in flag_state:
        if len(args) > 0:
            return args[0]
        return False
    return flag_state[char]

def find_char(s):
    if s in flags:
        return s
    for flag in flags.values():
        if flag.name==s:
            return flag.char
    else:
        return None
class Flag:
    def __init__(self, char, name, text, default):
        self.char=char
        self.name=name
        self.text=text
        self.default=default
        flags[char]=self

flags={}
Flag("d","dot","Generate a .dot in /tmp/dot.dot for the output node", False)
Flag("b","builddot","Build the dot file and place it in currect dir as dot.png", False)
Flag("s","simplify","Simplify input",True)
Flag("l","latex","Output in latex",False)
Flag("f","feh","Open outputed dot image with feh",False)
Flag("e","equation","Solve equations",True)
Flag("x","debug","Debug",True)
Flag("c","childlabel","Show childlabels in dot",False)
Flag("h","horizontal","Horizontal dot files",False)
Flag("p","presentation","Make rendered images white with transparent background",False)

flag_state={}
