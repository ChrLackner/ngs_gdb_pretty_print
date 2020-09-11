
from .base import register_printer, BasePrinter
from .netgen import PointPrinter

class IntegrationPoint(BasePrinter):
    def info(self):
        pi = self.val["pi"]
        return "[" + "(" + ", ".join([str(pi[i]) for i in range(3)]) + "), " + str(self.val["weight"]) + ", " + str(self.val["vb"]).replace("ngfem::","") + "]"

    def children(self):
        for field in ("nr", "facetnr"):
            yield self.memberprint(field)

register_printer(IntegrationPoint, "ngfem::IntegrationPoint")

class FiniteElement(BasePrinter):
    def info(self):
        return "(ndof: {}, order: {})".format(self.val["ndof"], self.val["order"])
register_printer(FiniteElement, "ngfem::FiniteElement")

class CompoundFiniteElement(FiniteElement):
    def info(self):
        fea = self.val["fea"]
        fels = [FiniteElement(fea["data"][i].dereference()) for i in range(fea["size"])]
        return super().info() + "[" + ", ".join([fel.name if fel.dynamic_type is None else fel.dynamic_type + fel.info() for fel in fels]) + "]"
register_printer(CompoundFiniteElement, "ngfem::CompoundFiniteElement")
