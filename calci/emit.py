# The Calci Programming language C code emitter

class Emitter:
    def __init__(self, fullpath: str) -> None:
        self.fullPath = fullpath
        self.header = ""
        self.code = ""

    def emit(self, code: str) -> None:
        self.code += code
    
    def emitLine(self, code: str) -> None:
        self.code += code + '\n'
    
    def headerLine(self, code: str):
        self.header += code + '\n'

    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)