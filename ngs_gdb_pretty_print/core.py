
from .base import *

class ArrayPrinter(BasePrinter):
    def __init__(self, val, **kwargs):
        super().__init__(val, **kwargs)
        self.size = int(val["size"])
        self.values = "["
        if self.size > 0:
            def printval(val):
                p = gdb.default_visualizer(val)
                if p is None:
                    return str(val)
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
register_printer(ArrayPrinter, 'ngcore::FlatArray<.*>',
                 'ngcore::Array<.*>', 'ngcore::ArrayMem<.*>',
                 'netgen::NgFlatArray<.*>','netgen::NgArray<.*>',
                 "ngfem::IntegrationRule")

class BitArrayPrinter(BasePrinter):
    def children(self):
        yield self.memberprint("size")
        yield "data", "{}".format("".join(str(1 if (int(self.val["data"][i/8]) & 1<<i%8) else 0) for i in range(self.val["size"])))
register_printer(BitArrayPrinter, "ngcore::BitArray")


class SymbolTablePrinter(BasePrinter):
    def children(self):
        names = gdb.default_visualizer(self.val["names"]).children()
        data = gdb.default_visualizer(self.val["data"]).children()
        for n, d in zip(names, data):
            yield "\n" + str(n[1]), d[1]
register_printer(SymbolTablePrinter, "ngcore::SymbolTable<.*>")

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
register_printer(FlagPrinter, "ngcore::Flags")
