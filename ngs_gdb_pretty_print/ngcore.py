
from .base import *

class ArrayPrinter(BasePrinter):
    def __init__(self, val, **kwargs):
        super().__init__(val, **kwargs)
        self.size = int(val["size"])
        self.values = "["
        if self.size > 0:
            def printval(val):
                p = gdb.default_visualizer(val)
                if hasattr(p, "info"):
                    return p.info()
                return p.to_string()
            if self.size > 10:
                self.values += ", ".join(printval(val["data"][i]) for i in range(2)) + ", ..., {}".format(printval(val["data"][self.size-1]))
            else:
                self.values += ", ".join(printval(val["data"][i]) for i in range(self.size))
        self.values += "]"

    def children(self):
        yield "\ndata", self.values

    def info(self):
        return " size({})".format(self.size)

class SymbolTablePrinter(BasePrinter):
    def children(self):
        names = gdb.default_visualizer(self.val["names"]).children()
        data = gdb.default_visualizer(self.val["data"]).children()
        for n, d in zip(names, data):
            yield "\n" + str(n[1]), d[1]

class FlagPrinter(BasePrinter):
    def children(self):
        for flag in ("defflags", "numflags", "strflags","flaglistflags"):
            val = SymbolTablePrinter(self.val[flag])
            for n, d in val.children():
                yield n, d
        for flag in ("numlistflags", "strlistflags"):
            val = SymbolTablePrinter(self.val[flag])
            for n, d in val.children():
                array = ArrayPrinter(d["_M_ptr"].dereference())
                yield n, array.values



