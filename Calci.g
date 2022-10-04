// A Grammar specification file for Calci programming language
// Written in ANTLR grammar syntax

grammar Calci;

program
    : statement *
    ;

statement
    : 'PRINT' (expression | string) nl
    | 'PRINTLN' (expression | string) nl
    | 'INPUT' identifier nl
    | 'VAR' identifier ':=' expression nl
    | 'IF' comparison 'THEN' nl statement* 'ENDIF' nl
    | 'WHILE' comparison 'REPEAT' nl statement* 'ENDWHILE' nl
    ;

comparison
    : expression (('=' | '!=' | '>' | '>=' | '<' | '<=') expression)+
    ;

expression
    : term (( '-' | '+' ) term)*
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