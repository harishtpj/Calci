# The Calci Programming language parser

import sys
from typing import Tuple
from .lex import Lexer, TokType

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
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

    # Grammar Parsing Rules (see Calci.g for rules)

    # Calci.g => line [6]:
    def program(self) -> None:
        print("PROGRAM")

        while self.checkToken(TokType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokType.EOF):
            self.statement()
    
    # Calci.g => line [10]:
    def statement(self) -> None:
        # Calci.g => Subrule {1}
        if self.checkToken(TokType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokType.STRING):
                self.nextToken() # String
            else:
                self.expression() # Expression
        
        # Calci.g => Subrule {2}
        elif self.checkToken(TokType.PRINTLN):
            print("STATEMENT-PRINTLN")
            self.nextToken()

            if self.checkToken(TokType.STRING):
                self.nextToken() # String
            else:
                self.expression() # Expression
        
        # Calci.g => Subrule {3}
        elif self.checkToken(TokType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()

            if self.curToken.text not in self.vars:
                self.vars.add(self.curToken.text)

            self.match(TokType.IDENTIFIER)
        
        # Calci.g => Subrule {4}
        elif self.checkToken(TokType.VAR):
            print("STATEMENT-VAR")
            self.nextToken()

            if self.curToken.text not in self.vars:
                self.vars.add(self.curToken.text)

            self.match(TokType.IDENTIFIER)
            self.match(TokType.COLONEQ)
            self.expression()
        
        # Calci.g => Subrule {5}
        elif self.checkToken(TokType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokType.THEN)
            self.nl()

            while not self.checkToken(TokType.ENDIF):
                self.statement()
            
            self.match(TokType.ENDIF)
        
        # Calci.g => Subrule {6}
        elif self.checkToken(TokType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokType.REPEAT)
            self.nl()

            while not self.checkToken(TokType.ENDWHILE):
                self.statement()
            
            self.match(TokType.ENDWHILE)
        
        else:
            self.abort(f"Invalid statement at {self.curToken.text} ({self.curToken.kind.name})")
            
        # Newline
        self.nl()
    
    # Calci.g => line [19]:
    def comparison(self) -> None:
        print("COMPARISON")

        self.expression()
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort(f"Expected comparison operator at: {self.curToken.text}")

        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    # Calci.g => line [23]:
    def expression(self) -> None:
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokType.PLUS) or self.checkToken(TokType.MINUS):
            self.nextToken()
            self.term()
    
    # Calci.g => line [27]:
    def term(self) -> None:
        print("TERM")

        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokType.ASTERISK) or self.checkToken(TokType.SLASH):
            self.nextToken()
            self.unary()
    
    # Calci.g => line [31]:
    def unary(self) -> None:
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokType.PLUS) or self.checkToken(TokType.MINUS):
            self.nextToken()        
        self.primary()
    
    # Calci.g => line [35]:
    def primary(self) -> None:
        print(f"PRIMARY ({self.curToken.text})")

        if self.checkToken(TokType.NUMBER): 
            self.nextToken()
        elif self.checkToken(TokType.IDENTIFIER):
            if self.curToken.text not in self.vars:
                self.abort(f"Referencing variable before assignment: {self.curToken.text}")
            self.nextToken()
        else:
            # Error!
            self.abort(f"Unexpected token at {self.curToken.text}")
    
    # Calci.g => line [38]:
    def nl(self) -> None:
        print("NEWLINE")
        self.match(TokType.NEWLINE)
        while self.checkToken(TokType.NEWLINE):
            self.nextToken()
