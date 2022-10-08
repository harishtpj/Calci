# Calci Compiler Error

import sys
from . import Error

class CompilerError(Error):  
    def run(self) -> Error:
        sys.stderr.write("Calci - Compile Time Error:\n")
        sys.stderr.write(f"\t{self.errname} : {self.errmsg}\n")
        sys.stderr.write("Compilation terminated\n")
        sys.exit(-1)