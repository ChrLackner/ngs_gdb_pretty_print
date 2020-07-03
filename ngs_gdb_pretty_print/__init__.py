
import re
import gdb

from .base import *
from .core import *
from .netgen import *
from .comp import *

regexp_dict = {}
pretty_printers_dict = {}
pretty_printers_dict['ngcore::FlatArray<.*>'] = ArrayPrinter
pretty_printers_dict['ngcore::Array<.*>'] = ArrayPrinter
pretty_printers_dict['ngcore::ArrayMem<.*>'] = ArrayPrinter
pretty_printers_dict['netgen::NgFlatArray<.*>'] = ArrayPrinter
pretty_printers_dict['netgen::NgArray<.*>'] = ArrayPrinter
pretty_printers_dict['netgen::Mesh'] = NetgenMeshPrinter
pretty_printers_dict['std::_Sp_counted_ptr_inplace.*'] = PointerPrinter
pretty_printers_dict["netgen::Segment"] = SegmentPrinter
pretty_printers_dict['netgen::Element2d'] = Element2dPrinter
pretty_printers_dict['netgen::Element'] = Element3dPrinter
pretty_printers_dict["netgen::PointIndex"] = PointIndexPrinter
pretty_printers_dict["netgen::Point<.*>"] = PointPrinter
pretty_printers_dict["netgen::SurfaceElementIndex"] = SurfaceElementIndexPrinter
pretty_printers_dict["netgen::Ng_Element"] = NgElementPrinter
pretty_printers_dict["ngcore::SymbolTable<.*>"] = SymbolTablePrinter
pretty_printers_dict["ngcore::Flags"] = FlagPrinter
pretty_printers_dict["^std::basic_string<char,.*>$"] = StdStringPrinter

#default visualizer
# pretty_printers_dict[".*"] = DefaultPrinter

for key in pretty_printers_dict:
    regexp_dict[key] = re.compile(key)

def ngs_lookup_function(val):
    type = val.type

    # If it points to a reference, get the reference.
    if type.code == gdb.TYPE_CODE_REF:
        type = type.target()
    # type = type.unqualified().strip_typedefs()
    typename = type.tag
    if typename == None:
        return None
    for tn, printer in pretty_printers_dict.items():
       if regexp_dict[tn].fullmatch(typename):
           return printer(val)
    return None

gdb.pretty_printers.append(ngs_lookup_function)
