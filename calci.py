# The Calci Programming language Interpreter

import sys
from calci.lex import Lexer
from calci.parse import Parser

def main():
    print("Calci Interpreter")

    if len(sys.argv) < 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as progfile:
        input = progfile.read()

    lexer = Lexer(input)
    parser = Parser(lexer)

    parser.program()
    print("Parsing completed")

if __name__ == "__main__":
    main()