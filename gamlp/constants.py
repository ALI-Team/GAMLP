import math
class Constant:
    def __init__(self,name, value, symbol):
        self.value=value
        self.symbol=symbol
        self.name=name
        constants_list[name]=self

constants_list = {}

Constant("pi",math.pi,"π")

get = constants_list.get
