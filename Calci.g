// A Grammar specification file for Calci programming language
// Written in ANTLR grammar syntax
//
// BSD 3-Clause License
// 
// Copyright (c) 2022, Harish Kumar
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
// 
// 1. Redistributions of source code must retain the above copyright notice, this
//    list of conditions and the following disclaimer.
// 
// 2. Redistributions in binary form must reproduce the above copyright notice,
//    this list of conditions and the following disclaimer in the documentation
//    and/or other materials provided with the distribution.
// 
// 3. Neither the name of the copyright holder nor the names of its
//    contributors may be used to endorse or promote products derived from
//    this software without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

grammar Calci;

program
    : statement *
    ;

statement
    : 'PRINT' (type expression | string) nl
    | 'PRINTLN' (type expression | string) nl
    | 'INPUT' identifier nl
    | 'VAR' identifier ':=' expression nl
    | 'LET' (identifier)+ ':' type nl
    | 'IF' comparison 'THEN' nl statement* 'ELSE' nl statement* 'END' nl
    | 'IF' comparison 'THEN' nl statement* 'END' nl
    | 'WHILE' comparison 'REPEAT' nl statement* 'END' nl
    ;

comparison
    : expression (('=' | '!=' | '>' | '>=' | '<' | '<=') expression)+
    ;

expression
    : term (( '-' | '+' | '%' ) term)*
    ;

term
    : unary (( '/' | '*' ) unary)*
    ;

unary
    : ('+' | '-')? primary
    ;

primary
    : number | identifier
    ;

nl
    : '\n'+
    ;

number
    : ('0'..'9')+ ('.' ('0'..'9')+)?
    ;

identifier
    : ('a'..'z''A'..'Z''0'..'9')+
    ;

string
    : '"' .+ '"'
    ;

type
    : 'nat' | 'int' | 'real' | 'str'
    ;