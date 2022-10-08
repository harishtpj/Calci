# Calci Error Template

class Error:
    """
    Base Error Class for Calci Compiler
    Error Types:
    IOError - Error on Input/Output Operations
    LexError - Error encountered during Lexing
    ParseError - Error encountered during Parsing
    """
    def __init__(self, errname: str, errmsg: str) -> None:
        self.errname: str = errname
        self.errmsg: str = errmsg