# Calci Language Tools
import os, shutil
from .errors import Error
from .fileutils import dlfName

def throwError(err: Error) -> Error:
    err.run()

def runProgram(fname: str, dlang: str) -> None:
    if dlang == "java":
        pass
    else:
        cc: str = os.getenv("CC", "tcc")
        cfname: str = dlfName(fname, "c")
        exe: str = dlfName(fname)
        if os.name == 'nt':
            exe += ".exe"
        if os.system(f"{cc} {cfname} -o {exe}") != 0:
            os.remove(cfname)
            exit(0)

def clearTemp(tempf: str, fname: str):
    os.remove(dlfName(tempf.name, "c"))
    tempexe = os.path.basename(os.path.realpath(tempf.name))
    tempexe = tempexe[:-3]
    fexe = os.path.basename(os.path.realpath(fname))
    fexe = fexe[:-3]
    if os.name == 'nt':
        tempexe += ".exe"
        fexe += ".exe"
    shutil.move(tempexe,fexe)

def gencFmt(vtype: str, forfunc: str="num") -> str:
    if vtype == "nat" or vtype == "int":
        return "%d"
    elif vtype == "real":
        return "%lf"
    elif vtype == "str" and forfunc == "i":
        return "%[^\\n]%*c"
    else:
        return "%s"

def getcType(vtype: str) -> str:
    return {
        "nat": "unsigned int",
        "int" : "int",
        "real" : "double",
        "str": "char[100]"
    }[vtype]