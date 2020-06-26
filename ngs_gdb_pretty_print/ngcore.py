
from .base import *

class ArrayPrinter(BasePrinter):
    def __init__(self, val, **kwargs):
        super().__init__(val, **kwargs)
        self.size = int(val["size"])
        self.values = "["
        if self.size > 0:
            printer = gdb.default_visualizer(val["data"][0])
            if printer is None:
                printer = DummyPrinter
            else:
                printer = printer.__class__
            def printval(val):
                p = printer(val)
                if hasattr(p, "info"):
                    return p.info()
                return p.to_string()
        if self.size > 20:
            self.values += ", ".join(printval(val["data"][i]) for i in range(5)) + ", ..., " + ", ".join(printval(val["data"][i]) for i in range(self.size-5, self.size))
        else:
            self.values += ", ".join(printval(val["data"][i]) for i in range(self.size))
        self.values += "]"

    def children(self):
        yield "\ndata", self.values

    def info(self):
        return "size({})".format(self.size)
