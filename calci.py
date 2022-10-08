# The Calci Programming language Compiler

# Python imports
import tempfile

# Language imports
from calci.lex import Lexer
from calci.parse import Parser
from calci.emit import Emitter
from calci.cmdargs import argparse, arg_parser
from calci.fileutils import readFile, dlfName
from calci.tools import runProgram, clearTemp

class Calci:
    def transpile(self, fname: str, dlang: str, forcomp: bool = False) -> tempfile._TemporaryFileWrapper:
        progsrc: str = readFile(fname)
        lexer: Lexer = Lexer(progsrc)

        tempf: tempfile._TemporaryFileWrapper = tempfile.NamedTemporaryFile()

        if dlang == "java":
            pass
        else:
            emitter: Emitter = Emitter(dlfName(tempf.name, "c")) if forcomp else Emitter(dlfName(fname, "c"))
            parser: Parser = Parser(lexer, emitter)

            parser.program()
            emitter.writeFile()
        
        return tempf


    def compile(self, fname: str, dlang: str) -> None:
        tempf: tempfile._TemporaryFileWrapper = self.transpile(fname, dlang, forcomp=True)
        runProgram(tempf.name, dlang)
        clearTemp(tempf, fname)

    def run(self) -> None:
        args: argparse.ArgumentParser = arg_parser.parse_args()
        if args.source:
            self.transpile(args.File, args.lang)
        else:
            self.compile(args.File, args.lang)

if __name__ == "__main__":
    calci = Calci()
    calci.run()