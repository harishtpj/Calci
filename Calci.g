// A Grammar specification file for Calci programming language
// Written in ANTLR grammar syntax

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