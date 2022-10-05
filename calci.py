# The Calci Programming language Compiler

import sys
from calci.lex import Lexer
from calci.parse import Parser
from calci.emit import Emitter

def main():
    print("Calci Compiler")

    if len(sys.argv) < 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as progfile:
        input = progfile.read()

    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.writeFile()
    print("Program Compiled")

if __name__ == "__main__":
    main()