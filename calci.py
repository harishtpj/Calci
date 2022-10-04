# The Calci Programming language Interpreter

from calci.lex import Lexer, TokType

def main():
    input = "IF+-123 foo*THEN/"
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.kind != TokType.EOF:
        print(token.kind)
        token = lexer.getToken()

if __name__ == "__main__":
    main()