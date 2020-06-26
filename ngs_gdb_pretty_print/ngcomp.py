
from .netgen import *

class Ngs_ElementPrinter(NgElementPrinter):
    def children(self):
        yield self.memberprint("ei")
        super().children()

