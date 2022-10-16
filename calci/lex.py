# The Calci Programming language Lexer
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

from enum import Enum
from . import tools
from .errors.rterror import RuntimeError

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
    WHILE = 108
    REPEAT = 109
    END = 110
    ELSE = 111
    FOR = 112
    TO = 113
    BY = 114
    DO = 115

    # Types
    NAT = 116
    INT = 117
    REAL = 118
    STR = 119

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
    MODSIGN = 213


class Token:
    def __init__(self, tokText: str, tokKind: TokType) -> None:
        self.text: str = tokText
        self.kind: str = tokKind

    @staticmethod
    def checkIfKeyword(tokText: str) -> TokType:
        for kind in TokType:
            if kind.name.lower() == tokText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

class Lexer:
    def __init__(self, input: str) -> None:
        self.src: str = input + "\n"
        self.src_lines: str = self.src.splitlines()
        self.lineno: int = 1
        self.curChar: str = ''
        self.curPos: int = -1
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
        tools.throwError(RuntimeError(
            'LexError',
            message,
            self.src_lines[self.lineno-1],
            self.lineno
        ))
    
    # Skips whitespaces except newlines
    def skipWS(self) -> None:
        while self.curChar in [' ', '\t', '\r']:
            self.nextChar()

    # Skips Comments
    def skipComment(self) -> None:
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()
            self.lineno += 1

    # Returns the next token
    def getToken(self) -> Token:
        self.skipWS()
        self.skipComment()
        token: Token = None

        if self.curChar == "+":
            token = Token(self.curChar, TokType.PLUS)

        elif self.curChar == "-":
            token = Token(self.curChar, TokType.MINUS)

        elif self.curChar == "*":
            token = Token(self.curChar, TokType.ASTERISK)

        elif self.curChar == "/":
            token = Token(self.curChar, TokType.SLASH)
        
        elif self.curChar == "%":
            token = Token(self.curChar, TokType.MODSIGN)
        
        elif self.curChar == "=":
            token = Token(self.curChar, TokType.EQ)

        elif self.curChar == ":":
            if self.peek() == "=":
                lastChar: str = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.COLONEQ)
            else:
                token = Token(self.curChar, TokType.COLON)
        
        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar: str = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.NOTEQ)
            else:
                self.abort(f"Expected != got !{self.peek()}")
        
        elif self.curChar == ">":
            if self.peek() == "=":
                lastChar: str = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.GTEQ)
            else:
                token = Token(self.curChar, TokType.GT)
        
        elif self.curChar == "<":
            if self.peek() == "=":
                lastChar: str = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokType.LTEQ)
            else:
                token = Token(self.curChar, TokType.LT)
        
        elif self.curChar == '\"':
            self.nextChar()
            startPos: int = self.curPos
            
            while self.curChar != '\"':
                self.nextChar()
            
            tokText: str = self.src[startPos : self.curPos]
            token = Token(tokText, TokType.STRING)
        
        elif self.curChar.isdigit():
            startPos: int = self.curPos
            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == ".":
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort("Illegal Character in Number")
                while self.peek().isdigit():
                    self.nextChar()
            
            tokText: str = self.src[startPos : self.curPos + 1]
            token = Token(tokText, TokType.NUMBER)
        
        elif self.curChar.isalpha():
            startPos: int = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            
            tokText: str = self.src[startPos : self.curPos + 1]
            keyword: str = Token.checkIfKeyword(tokText)
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