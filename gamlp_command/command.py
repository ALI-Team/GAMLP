import os
import re
import logging
import copy

from gamlp.parser import parse
from gamlp import dot
from gamlp import equation
from gamlp import intnode
import purplex
from PIL import Image
import PIL.ImageOps 

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
    print("GAMLP version {} released under GPLv3".format(version))
    print("'help' for help")
    print("'flags' for avalible flags")
    print("'commands' for avalible commands")
    start_flags=command_config.config["INIT"]["flags"]
    for c in start_flags:
        flags.set(c,True)
    

    dot_path=command_config.config["EXPORT"]["dot_path"]
    png_path=command_config.config["EXPORT"]["png_path"]
    global go
    go=True
    while go:
        try:
            expr=input(">>> ")
        except EOFError:
            break
        res=commands.parse_command(expr)
        if not res:
            try:
                tree=parse(expr)
                input_tree=copy.deepcopy(tree)
            except purplex.exception.NoMatchingTokenFoundError:
                print("syntax error")
                continue
            except Exception as e:
                print(e)
                print("Error in parsing")
                continue
            if flags.get("s"):
                try:
                    if flags.get("c"):
                        tree=tree.simplifyed(target="FACTOR")
                    else:
                        tree=tree.simplifyed()
                except Exception as e:
                    print(e)
                    logging.getLogger().error("Error in simplifying", exc_info=True)
                    #print("Error in simplifying")
                    continue

            if flags.get("n") and not tree.contains_unknowns():
                tree=intnode.IntNode(tree.eval())
            if flags.get("e") and isinstance(tree, equation.Equation):
                try:
                    print(input_tree.solve())
                except Exception as e:
                    print(e)
                    print("Error in solving")
                    continue
            else:
                if flags.get("l"):
                    output(tree.latex(None))
                else:
                    output(tree)
                if flags.get("d") or flags.get("b"):
                    with open(dot_path, "w") as f:
                        if flags.get("c"):
                            if flags.get("x",False):
                                child_label_amount=2
                            else:
                                child_label_amount=1
                        else:
                            child_label_amount=0
                        f.write(dot.dot_code(tree, debug=flags.get("x", False), child_label_amount=child_label_amount, direction=["V","H"][flags.get("h",False)]))
                if flags.get("b"):
                    os.system("dot -Tpng > {png} < {dot}".format(png=png_path, dot=dot_path))
                    if flags.get("p"):
                        image = Image.open(png_path)
                        image = image.convert("RGBA")
                        img_data = image.getdata()
                        new_img_data = []
                        for item in img_data:
                            color=(255-item[0])
                            new_img_data.append((255, 255, 255, color))

                        image.putdata(new_img_data)

                        image.save(png_path)


                if flags.get("f"):
                    os.system("feh {png}".format(png=png_path))
