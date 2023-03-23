# The Calci Programming language parser
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

from . import tools
from .errors.rterror import RuntimeError
from .lex import Lexer, TokType
from .emit import Emitter

class Parser:
    def __init__(self, lexer: Lexer, emitter: Emitter) -> None:
        self.lexer: Lexer = lexer
        self.emitter: Emitter = emitter

        self.vars: set = set()        # Variables declared so far.
        self.curToken: str = None
        self.peekToken: str = None
        self.nextToken()
        self.nextToken()              # Two calls to initialize current & peek

    def checkToken(self, kind: TokType) -> bool:
        return kind == self.curToken.kind

    def checkPeek(self, kind: TokType) -> bool:
        return kind == self.peekToken.kind

    def match(self, kind: TokType) -> None:
        if not self.checkToken(kind):
            self.abort(f"Expected {kind.name}, got {self.curToken.kind.name}")
        self.nextToken()

    # Advances the current token
    def nextToken(self) -> None:
        if self.peekToken is not None:
            if self.peekToken.kind == TokType.NEWLINE:
                self.lexer.lineno += 1
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message) -> None:
        tools.throwError(RuntimeError(
            "ParseError",
            message,
            self.lexer.src_lines[self.lexer.lineno-1],
            self.lexer.lineno
        ))
    
    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self) -> bool:
        return self.checkToken(TokType.GT) or \
               self.checkToken(TokType.GTEQ) or \
               self.checkToken(TokType.LT) or \
               self.checkToken(TokType.LTEQ) or \
               self.checkToken(TokType.EQ) or \
               self.checkToken(TokType.NOTEQ)
    
    def isType(self) -> bool:
        return self.checkToken(TokType.NAT) or \
               self.checkToken(TokType.INT) or \
               self.checkToken(TokType.REAL) or \
               self.checkToken(TokType.STR)
    
    def parseIF(self, type="") -> None:
        if type == "elsif":
            self.match(TokType.ELSIF)
            self.emitter.emit("}else ")

        self.emitter.emit("if(")
        self.comparison()
        self.match(TokType.THEN)
        self.nl()
        self.emitter.emitLine("){")

        while not (self.checkToken(TokType.ELSE) or self.checkToken(TokType.END) or self.checkToken(TokType.ELSIF)):
            self.statement()
        
        if self.checkToken(TokType.ELSE):
            self.match(TokType.ELSE)
            self.emitter.emit("} else ")
            self.nl()
            self.emitter.emitLine("{")
            while not self.checkToken(TokType.END):
                self.statement()
        
        if self.checkToken(TokType.ELSIF):
            self.parseIF("elsif")

    # Grammar Parsing Rules (see Calci.g for rules)

    # Calci.g => rule program:
    def program(self) -> None:
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        while self.checkToken(TokType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokType.EOF):
            self.statement()
        
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
    
    # Calci.g => rule statement:
    def statement(self) -> None:
        # Calci.g => Subrule {1}
        if self.checkToken(TokType.PRINT):
            self.nextToken()

            if self.checkToken(TokType.STRING):
                self.emitter.emitLine(f"printf(\"{self.curToken.text}\");")
                self.nextToken() # String
            else:
                self.emitter.emit(f"printf(\"{tools.gencFmt(self.curToken.text)}\",")
                self.nextToken()
                self.expression() # Expression
                self.emitter.emitLine(");")
        
        # Calci.g => Subrule {2}
        elif self.checkToken(TokType.PRINTLN):
            self.nextToken()

            if self.checkToken(TokType.STRING):
                self.emitter.emitLine(f"printf(\"{self.curToken.text}\");")
                self.nextToken() # String
            else:
                self.emitter.emit(f"printf(\"{tools.gencFmt(self.curToken.text)}\",")
                self.nextToken()
                self.expression() # Expression
                self.emitter.emitLine(");")
            self.emitter.emitLine("printf(\"\\n\");")
        
        # Calci.g => Subrule {3}
        elif self.checkToken(TokType.FMTPRINT):
            self.nextToken()
            self.emitter.emit(f"printf(\"{self.curToken.text}\"")

            fmt_vars: list[str] = []
            self.nextToken()

            while not self.checkToken(TokType.NEWLINE):
                if self.curToken.text not in self.vars:
                    self.abort(f"Referencing variable before declaration: {self.curToken.text}")
                    
                fmt_vars.append(self.curToken.text)
                self.match(TokType.IDENTIFIER)
            
            for fvars in fmt_vars:
                self.emitter.emit(f", {fvars}")
            
            self.emitter.emitLine(");")
        
        # Calci.g => Subrule {4}
        elif self.checkToken(TokType.INPUT):
            self.nextToken()
            fmt = tools.gencFmt(self.curToken.text, "i")
            self.nextToken()

            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before declaration: {self.curToken.text}")
            
            self.emitter.emitLine(f"scanf(\"{fmt}\", &{self.curToken.text});")
            self.match(TokType.IDENTIFIER)
        
        # Calci.g => Subrule {5}
        elif self.checkToken(TokType.VAR):
            self.nextToken()

            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before declaration: {self.curToken.text}")
            
            self.emitter.emit(self.curToken.text + " = ")
            self.match(TokType.IDENTIFIER)
            self.match(TokType.COLONEQ)
            self.expression()
            self.emitter.emitLine(";")
        
        # Calci.g => Subrule {6}
        elif self.checkToken(TokType.LET):
            vars_decl: list[str] = []
            self.nextToken()

            while not self.checkToken(TokType.COLON):
                if self.curToken.text not in self.vars:
                    self.vars.add(self.curToken.text)
                else:
                    self.abort(f"Redeclaring variable: {self.curToken.text}")

                vars_decl.append(self.curToken.text)
                self.match(TokType.IDENTIFIER)
    
            
            self.match(TokType.COLON)
            if self.isType():
                vals = ",".join(vars_decl)
                self.emitter.headerLine(f"{tools.getcType(self.curToken.text)} {vals};")
                self.nextToken()
            else:
                self.abort(f"Expected type name at: {self.curToken.text}")
        
        # Calci.g => Subrule {7}
        elif self.checkToken(TokType.IF):
            self.nextToken()
            self.parseIF()

            self.match(TokType.END)
            self.emitter.emitLine("}")
        
        # Calci.g => Subrule {8}
        elif self.checkToken(TokType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokType.REPEAT)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokType.END):
                self.statement()
            
            self.match(TokType.END)
            self.emitter.emitLine("}")
        
        # Calci.g => Subrule {9}
        elif self.checkToken(TokType.FOR):
            self.nextToken()
            self.emitter.emit("for(")
            ctr: str = self.curToken.text
            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before declaration: {self.curToken.text}")
            self.match(TokType.IDENTIFIER)
            self.match(TokType.COLONEQ)
            self.emitter.emit(ctr + " = ")
            self.expression()
            self.emitter.emit(";")

            self.match(TokType.TO)
            self.emitter.emit(ctr + "<")
            self.expression()
            self.emitter.emit(";")

            self.match(TokType.BY)
            self.emitter.emit(ctr + "+=")
            self.expression()
            self.match(TokType.DO)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokType.END):
                self.statement()

            self.match(TokType.END)
            self.emitter.emitLine("}")

        
        else:
            self.abort(f"Invalid statement at {self.curToken.text} ({self.curToken.kind})")
            
        # Newline
        self.nl()
    
    # Calci.g => rule comparison:
    def comparison(self) -> None:
        self.expression()
        if self.isComparisonOperator():
            if self.checkToken(TokType.EQ):
                self.curToken.text = "=="
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        else:
            self.abort(f"Expected comparison operator at: {self.curToken.text}")

        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
    
    # Calci.g => rule expression:
    def expression(self) -> None:
        self.term()
        # Can have 0 or more +/-/% and expressions.
        while self.checkToken(TokType.PLUS) or self.checkToken(TokType.MINUS) or self.checkToken(TokType.MODSIGN):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()
    
    # Calci.g => rule term:
    def term(self) -> None:
        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokType.ASTERISK) or self.checkToken(TokType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()
    
    # Calci.g => rule unary:
    def unary(self) -> None:
        # Optional unary +/-
        if self.checkToken(TokType.PLUS) or self.checkToken(TokType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()        
        self.primary()
    
    # Calci.g => rule primary:
    def primary(self) -> None:
        if self.checkToken(TokType.NUMBER):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.checkToken(TokType.IDENTIFIER):
            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before declaration: {self.curToken.text}")
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            # Error!
            self.abort(f"Unexpected token at {self.curToken.text}")
    
    # Calci.g => rule nl:
    def nl(self) -> None:
        self.match(TokType.NEWLINE)
        while self.checkToken(TokType.NEWLINE):
            self.nextToken()
