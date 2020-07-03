
import gdb

class BasePrinter:
    def __init__(self, val, prefix="{}"):
        self.val = val
        self.prefix = prefix
        self.name = str(self.val.type)
        for expr in ("ngstd::", "ngcomp::", "ngbla::", "ngla::","ngfem::", "std::",
                     "netgen::", "ngcore::"):
            self.name = self.name.replace(expr, "")
        self.name.replace("__cxx11::basic_string<char, char_traits<char>, allocator<char> >", "string")
        template_arguments = []
        nargs = 0
        while True:
            try:
                template_arguments.append(val.type.template_argument(nargs))
            except RuntimeError:
                break
            nargs += 1
        self.template_types = template_arguments

    def to_string(self):
        if hasattr(self, "info"):
            info = ": " + self.info()
        else:
            info = ""
        return self.prefix.format(self.name) + info

    def memberprint(self, name):
        return "\n" + name, self.val[name]

    def arrayprint(self, name):
        from .core import ArrayPrinter
        return "\n" + name, ArrayPrinter(self.val[name]).to_string()

def process_kids(state, PF):
    for field in PF.type.fields():
        if field.artificial or field.type == gdb.TYPE_CODE_FUNC or \
        field.type == gdb.TYPE_CODE_VOID or field.type == gdb.TYPE_CODE_METHOD or \
        field.type == gdb.TYPE_CODE_METHODPTR or field.type == None: continue
        key = field.name
        if key is None: continue
        if field.is_base_class:
            for k, v in process_kids(state, field):
                yield k, v
        else:
            try: val = state[key]
            except RuntimeError: continue
            yield key, val

def printing(key, val):
    if val.type.code == gdb.TYPE_CODE_PTR or val.type.code == gdb.TYPE_CODE_MEMBERPTR:
        if not val: return key, "NULL"
        else:
            try:
                return key, val.dereference()
            except RuntimeError:
                return key, "Cannot access memory at address " + str(val.address)
    else:
        return key, val

class DefaultPrinter(BasePrinter):
    def children(self):
        for key, val in process_kids(self.val, self.val):
            k,v = printing(key, val)
            try:
                printer = gdb.default_visualizer(v)
            except:
                printer = None
            yield "\n" + k, v if printer is None else printer.to_string()

class PointerPrinter:
    def __init__(self, val, printer):
        prefix = "{}"
        try:
            val = val.dereference()
            prefix = "*{}"
        except:
            pass

        if str(val.type).startswith("std::shared_ptr<") or str(val.type).startswith("std::_Sp_counted_ptr_inplace"):
            print("is shared ptr")
            val = val["_M_ptr"].dereference()
            prefix = "shared_ptr<{}>"

        if str(val.type).startswith("std::unique_ptr<"):
            val = val["_M_ptr"].dereference()
            prefix = "unique_ptr<{}>"

        if prefix == "{}":
            raise Exception("Something's wrong")
        try:
            valstr = str(val)
            self.is_nullptr = False
        except MemoryError:
            self.is_nullptr = True
        self.val = val
        self.prefix = prefix
        self.printer = printer

    def to_string(self):
        if self.is_nullptr:
            return self.prefix.format(self.val.type) + ": nullptr"
        return self.prefix.format(self.val.type) + ": " + printer.info()

class DummyPrinter:
    def __init__(self, val):
        self.val = val
    def to_string(self):
        return str(self.val)

class StdStringPrinter:
    "Print a std::string"
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return self.val['_M_dataplus']['_M_p']

    def display_hint(self):
        return 'string'
