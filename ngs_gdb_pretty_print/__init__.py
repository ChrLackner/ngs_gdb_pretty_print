
import re
import gdb

from .base import *
from .core import *
from .netgen import *
from .comp import *
from .fem import *

# pretty_printers_dict['std::_Sp_counted_ptr_inplace.*'] = PointerPrinter
# pretty_printers_dict["^std::basic_string<char,.*>$"] = StdStringPrinter

#default visualizer
# pretty_printers_dict[".*"] = DefaultPrinter

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
