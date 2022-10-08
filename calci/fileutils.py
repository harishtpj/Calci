# Calci Language File utilities

import os
from .errors.comperror import CompilerError
from . import tools

def checkIfFile(fname: str) -> None:
    if not os.path.exists(fname):
        tools.throwError(CompilerError(
            "IOError",
            f"Cannot open file {fname}"
        ))

def dlfName(fname: str, dlang: str = "_") -> str:
    fname = os.path.basename(os.path.realpath(fname))
    return {
        "_": fname[:-3],
        "c": fname[:-3] + ".c"
    }[dlang]

def readFile(fname: str) -> str:
    checkIfFile(fname)
    with open(fname, 'r') as progfile:
        progsrc: str = progfile.read()
    return progsrc