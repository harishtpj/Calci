# The Calci Programming language Compiler
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