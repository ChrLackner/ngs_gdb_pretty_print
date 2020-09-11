
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

register_printer(NetgenMeshPrinter, 'netgen::Mesh')

class SegmentPrinter(BasePrinter):
    def info(self):
        return "[{} - {}]".format(*[PointIndexPrinter(self.val["pnums"][i]).info() for i in range(2)])

    def children(self):
        for c in "si", "edgenr", "domin", "domout", "surfnr1", "surfnr2":
            yield "\n" + c, self.val[c]
register_printer(SegmentPrinter, "netgen::Segment")


class Element2dPrinter(BasePrinter):
    def info(self):
        typ = "TRIG" if int(self.val["np"]) == 3 else "QUAD"
        return "{} [{}]".format(typ, " - ".join([PointIndexPrinter(self.val["pnum"][i]).info() for i in range(int(self.val["np"]))]))

    def children(self):
        for val in ("index", "is_curved"):
            yield self.memberprint(val)
register_printer(Element2dPrinter, 'netgen::Element2d')

class Element3dPrinter(BasePrinter):
    def info(self):
        return "[{}]".format(" - ".join([PointIndexPrinter(self.val["pnum"][i]).info() for i in range(int(self.val["np"]))]))

    def children(self):
        for val in ("typ", "pnum", "index", "is_curved", "flags"):
            yield self.memberprint(val)
register_printer(Element3dPrinter, "netgen::Element")

class PointIndexPrinter(BasePrinter):
    def info(self):
        return "INVALID" if int(self.val["i"]) == 0 else str(self.val["i"])
register_printer(PointIndexPrinter, "netgen::PointIndex")

class IndexPrinter(BasePrinter):
    def info(self):
        return "INVALID" if int(self.val["i"]) == -1 else str(self.val["i"])
register_printer(IndexPrinter, "netgen::SegmentIndex", "netgen::SurfaceElementIndex")

class NgElementPrinter(BasePrinter):
    def children(self):
        for val in ("type", "index", "mat", "points", "edges", "faces", "facets", "is_curved"):
            yield self.memberprint(val)
register_printer(NgElementPrinter, "netgen::Ng_Element")

class PointPrinter(BasePrinter):
    def info(self):
        size = int(self.template_types[0])
        return "(" + ", ".join(str(self.val["x"][i]) for i in range(size)) + ")"
register_printer(PointPrinter, "netgen::Point<.*>")

class FaceDescriptorPrinter(BasePrinter):
    def children(self):
        for val in ("surfnr", "domin", "domout", "bcprop", "domin_singular",
                    "domout_singular", "tlosurf"):
            yield self.memberprint(val)
        yield "\nbcname", self.val["bcname"].dereference()
register_printer(FaceDescriptorPrinter, "netgen::FaceDescriptor")
