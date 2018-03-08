import os

import configparser

def reset_config():
    global config
    config = configparser.ConfigParser()
    config["INIT"] = {
        "flags":"se"
    }
    config["EXPORT"] = {
        "dot_path":"/tmp/dot.dot",
        "png_path":"dot.png"
    }
    write_file()
def write_file():
    global config

    with open(config_path,"w") as f:
        config.write(f)

def check_dirs():
    os.makedirs(config_base, exist_ok=True)

def read_config():
    config.read(config_path)
    
config=configparser.ConfigParser()

config_base=os.path.expanduser("~")+"/.config/gamlp/"
config_path=config_base+"command.conf"

check_dirs()
if not os.path.isfile(config_path):
    reset_config()
read_config()
