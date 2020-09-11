
from .netgen import *
from .base import *

class Ngs_ElementPrinter(NgElementPrinter):
    def children(self):
        yield self.memberprint("ei")
        super().children()
register_printer(Ngs_ElementPrinter, "ngcomp::Ngs_Element")
