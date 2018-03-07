import os
import re

from gamlp.parser import parse
from gamlp import dot

from . import flags
from . import commands
from . import command_config
from .util import output

def execute():
    try:
        import pkg_resources
    except ImportError:
        version="?"
    else:
        try:
            version=pkg_resources.require("GAMLP")[0].version
        except pkg_resources.DistributionNotFound:
            version="?"
    print("GAMLP version {}".format(version))
    print("'help' for help")
    print("'flags' for avalible flags")
    print("'commands' for avalible commands")
    start_flags=command_config.config["INIT"]["flags"]
    for c in start_flags:
        flags.set(c,True)
    

    dot_path=command_config.config["EXPORT"]["dot_path"]
    png_path=command_config.config["EXPORT"]["png_path"]
    go=True
    while go:
        try:
            expr=input(">>> ")
        except EOFError:
            break
        res=commands.parse_command(expr)
        if not res:
            tree=parse(expr)
            if flags.get("s"):
                tree=tree.simplifyed()
            if flags.get("l"):
                output(tree.latex())
            else:
                output(tree)
            if flags.get("d") or flags.get("b"):
                with open(dot_path, "w") as f:
                    f.write(dot.dot_code(tree, debug=flags.get("debug", False)))
            if flags.get("b"):
                os.system("dot -Tpng > {png} < {dot}".format(png=png_path, dot=dot_path))
