
from .base import *

class NetgenMeshPrinter(BasePrinter):
    def __init__(self, val, **kwargs):
        super().__init__(val, **kwargs)

    def children(self):
        yield self.memberprint("dimension")
        for val in ("segments", "surfelements", "volelements", "facedecoding", "materials", "bcnames"):
            yield self.arrayprint(val)
        yield "topology", "MeshTopology"
        yield "geometry", "shared_ptr<NetgenGeometry>"

class SegmentPrinter(BasePrinter):
    def info(self):
        return "[{} - {}]".format(*[PointIndexPrinter(self.val["pnums"][i]).info() for i in range(2)])

    def children(self):
        for c in "si", "edgenr", "domin", "domout", "surfnr1", "surfnr2":
            yield "\n" + c, self.val[c]

class Element2dPrinter(BasePrinter):
    def info(self):
        typ = "TRIG" if int(self.val["np"]) == 3 else "QUAD"
        return "{} [{}]".format(typ, " - ".join([PointIndexPrinter(self.val["pnum"][i]).info() for i in range(int(self.val["np"]))]))

    def children(self):
        for val in ("typ", "pnum", "is_curved", "refflag", "next", "np"):
            yield self.memberprint(val)

class Element3dPrinter(BasePrinter):
    def info(self):
        return "[{}]".format(" - ".join([PointIndexPrinter(self.val["pnum"][i]).info() for i in range(int(self.val["np"]))]))

    def children(self):
        for val in ("typ", "pnum", "index", "is_curved", "flags"):
            yield self.memberprint(val)

class PointIndexPrinter(BasePrinter):
    def info(self):
        return "INVALID" if int(self.val["i"]) == 0 else str(self.val["i"])

class NgElementPrinter(BasePrinter):
    def children(self):
        for val in ("type", "index", "mat", "points", "edges", "faces", "facets", "is_curved"):
            yield self.memberprint(val)
