# The Calci Programming language Lexer
import sys
from enum import Enum
from typing import Union

class TokType(Enum):
    # Basic Tokens
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENTIFIER = 2
    STRING = 3

    # Keywords
    PRINT = 101
    PRINTLN = 102
    INPUT = 103
    LET = 104
    VAR = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Types
    NAT = 112
    INT = 113
    REAL = 114
    STR = 115

    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    COLONEQ = 206
    LT = 207
    LTEQ = 208
    GT = 209
    GTEQ = 210
    NOTEQ = 211
    COLON = 212


class Token:
    def __init__(self, tokText: str, tokKind: TokType) -> None:
        self.text = tokText
        self.kind = tokKind

    @staticmethod
    def checkIfKeyword(tokText: str) -> Union[TokType, None]:
        for kind in TokType:
            if kind.name.lower() == tokText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

class Lexer:
    def __init__(self, input: str) -> None:
        self.src = input + "\n"
        self.curChar = ''
        self.curPos = -1
        self.nextChar()
    
    # Processes the next character for lexing
    def nextChar(self) -> None:
        self.curPos += 1
        if self.curPos >= len(self.src):
            self.curChar = '\0'
        else:
            self.curChar = self.src[self.curPos]
    
    # Returns the next character without modifying anything
    def peek(self) -> str:
        if self.curPos + 1 >= len(self.src):
            return '\0'
        return self.src[self.curPos + 1]


    def abort(self, message: str) -> None:
        sys.exit(f"Calci - LexError: \n\t{message}")
    
    # Skips whitespaces except newlines
    def skipWS(self) -> None:
        while self.curChar in [' ', '\t', '\r']:
            self.nextChar()

    # Skips Comments
    def skipComment(self) -> None:
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Returns the next token
    def getToken(self) -> Union[Token, None]:
        self.skipWS()
        self.skipComment()
        token = None

        if self.curChar == "+":
            token = Token(self.curChar, TokType.PLUS)

        elif self.curChar == "-":
            token = Token(self.curChar, TokType.MINUS)

        elif self.curChar == "*":
            token = Token(self.curChar, TokType.ASTERISK)

        elif self.curChar == "/":
            token = Token(self.curChar, TokType.SLASH)
        
        elif self.curChar == "=":
            token = Token(self.curChar, TokType.EQ)

        elif self.curChar == ":":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.COLONEQ)
            else:
                token = Token(self.curChar, TokType.COLON)
        
        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.NOTEQ)
            else:
                self.abort(f"Expected != got !{self.peek()}")
        
        elif self.curChar == ">":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.GTEQ)
            else:
                token = Token(self.curChar, TokType.GT)
        
        elif self.curChar == "<":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.LTEQ)
            else:
                token = Token(self.curChar, TokType.LT)
        
        elif self.curChar == '\"':
            self.nextChar()
            startPos = self.curPos
            
            while self.curChar != '\"':
                self.nextChar()
            
            tokText = self.src[startPos : self.curPos]
            token = Token(tokText, TokType.STRING)
        
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == ".":
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort("Illegal Character in Number")
                while self.peek().isdigit():
                    self.nextChar()
            
            tokText = self.src[startPos : self.curPos + 1]
            token = Token(tokText, TokType.NUMBER)
        
        elif self.curChar.isalpha():
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            
            tokText = self.src[startPos : self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:
                token = Token(tokText, TokType.IDENTIFIER)
            else:
                token = Token(tokText, keyword)

        elif self.curChar == "\n":
            token = Token(self.curChar, TokType.NEWLINE)

        elif self.curChar == "\0":
            token = Token('', TokType.EOF)

        else:
            # Invalid Token
            self.abort(f"Invalid Token: {self.curChar}")

        self.nextChar()
        return token