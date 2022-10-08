# Calci Runtime Error

import sys
from . import Error

class RuntimeError(Error):
    def __init__(self, errname: str, errmsg: str) -> None:
        super().__init__(errname, errmsg)

    def run(self) -> Error:
        sys.stderr.write("Calci - Runtime Error:\n")
        sys.stderr.write(f"{self.errname} : {self.errmsg}\n")
        sys.exit(-1)