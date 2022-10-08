# Calci Language Tools
#
# BSD 3-Clause License
# 
# Copyright (c) 2022, Harish Kumar
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
        exe += ".exe" if os.name == 'nt' else ""
        if os.system(f"{cc} {cfname} -o {exe}") != 0:
            os.remove(cfname)
            exit(-1)

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

def gencFmt(vtype: str, forfunc: str="_") -> str:
    return {
        "_nat": "%d",
        "_int": "%d",
        "_real": "%lf",
        "_str": "%s",
        "istr": "%[^\\n]%*c"
    }[forfunc+vtype]

def getcType(vtype: str) -> str:
    return {
        "nat": "unsigned int",
        "int" : "int",
        "real" : "double",
        "str": "char[100]"
    }[vtype]