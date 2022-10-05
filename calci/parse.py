# The Calci Programming language parser

import sys
from .lex import Lexer, TokType
from .emit import Emitter

class Parser:
    def __init__(self, lexer: Lexer, emitter: Emitter) -> None:
        self.lexer = lexer
        self.emitter = emitter

        self.vars = set()        # Variables declared so far.
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()            # Two calls to initialize current & peek

    def checkToken(self, kind) -> bool:
        return kind == self.curToken.kind

    def checkPeek(self, kind) -> bool:
        return kind == self.peekToken.kind

    def match(self, kind) -> None:
        if not self.checkToken(kind):
            self.abort(f"Expected {kind.name}, got {self.curToken.kind.name}")
        self.nextToken()

    # Advances the current token
    def nextToken(self) -> None:
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message) -> None:
        sys.exit(f"Calci - ParseError: \n\t{message}")
    
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
    
    def gencFmt(self, vtype: str, forfunc="num") -> str:
        if vtype == "nat" or vtype == "int":
            return "%d"
        elif vtype == "real":
            return "%lf"
        elif vtype == "str" and forfunc == "i":
            return "%[^\\n]%*c"
        else:
            return "%s"
    
    def getcType(self, vtype: str) -> str:
        return {
            "nat": "unsigned int",
            "int" : "int",
            "real" : "double",
            "str": "char[100]"
        }[vtype]
        


    # Grammar Parsing Rules (see Calci.g for rules)

    # Calci.g => line [6]:
    def program(self) -> None:
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        while self.checkToken(TokType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokType.EOF):
            self.statement()
        
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
    
    # Calci.g => line [10]:
    def statement(self) -> None:
        # Calci.g => Subrule {1}
        if self.checkToken(TokType.PRINT):
            self.nextToken()

            if self.checkToken(TokType.STRING):
                self.emitter.emitLine(f"printf(\"{self.curToken.text}\");")
                self.nextToken() # String
            else:
                self.emitter.emit(f"printf(\"{self.gencFmt(self.curToken.text)}\",")
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
                self.emitter.emit(f"printf(\"{self.gencFmt(self.curToken.text)}\",")
                self.nextToken()
                self.expression() # Expression
                self.emitter.emitLine(");")
            self.emitter.emitLine("printf(\"\\n\");")
        
        # Calci.g => Subrule {3}
        elif self.checkToken(TokType.INPUT):
            self.nextToken()
            fmt = self.gencFmt(self.curToken.text, "i")
            self.nextToken()

            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before declaration: {self.curToken.text}")
            
            self.emitter.emitLine(f"scanf(\"{fmt}\", &{self.curToken.text});")
            self.match(TokType.IDENTIFIER)
        
        # Calci.g => Subrule {4}
        elif self.checkToken(TokType.VAR):
            self.nextToken()

            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before declaration: {self.curToken.text}")
            
            self.emitter.emit(self.curToken.text + " = ")
            self.match(TokType.IDENTIFIER)
            self.match(TokType.COLONEQ)
            self.expression()
            self.emitter.emitLine(";")
        
        # Calci.g => Subrule {5}
        elif self.checkToken(TokType.LET):
            vars_decl = []
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
                self.emitter.headerLine(f"{self.getcType(self.curToken.text)} {vals};")
                self.nextToken()
            else:
                self.abort(f"Expected type name at: {self.curToken.text}")
        
        # Calci.g => Subrule {6}
        elif self.checkToken(TokType.IF):
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokType.THEN)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokType.ENDIF):
                self.statement()
            
            self.match(TokType.ENDIF)
            self.emitter.emitLine("}")
        
        # Calci.g => Subrule {7}
        elif self.checkToken(TokType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokType.REPEAT)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokType.ENDWHILE):
                self.statement()
            
            self.match(TokType.ENDWHILE)
            self.emitter.emitLine("}")
        
        else:
            self.abort(f"Invalid statement at {self.curToken.text} ({self.curToken.kind.name})")
            
        # Newline
        self.nl()
    
    # Calci.g => line [19]:
    def comparison(self) -> None:

        self.expression()
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        else:
            self.abort(f"Expected comparison operator at: {self.curToken.text}")

        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
    
    # Calci.g => line [23]:
    def expression(self) -> None:
        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokType.PLUS) or self.checkToken(TokType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()
    
    # Calci.g => line [27]:
    def term(self) -> None:
        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokType.ASTERISK) or self.checkToken(TokType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()
    
    # Calci.g => line [31]:
    def unary(self) -> None:
        # Optional unary +/-
        if self.checkToken(TokType.PLUS) or self.checkToken(TokType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()        
        self.primary()
    
    # Calci.g => line [35]:
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
    
    # Calci.g => line [38]:
    def nl(self) -> None:
        self.match(TokType.NEWLINE)
        while self.checkToken(TokType.NEWLINE):
            self.nextToken()
