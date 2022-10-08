# Calci language commandline interface

import argparse
from . import __ver_str__

arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="calci",
                                    description="The Calci programming language compiler")

arg_parser.add_argument('File',
                        metavar='file',
                        type=str,
                        help="The File to compile")

arg_parser.add_argument("-l",
                        "--lang",
                        action="store",
                        type=str,
                        help="the Language to Transpile")

arg_parser.add_argument("-S",
                        "--source",
                        action="store_true",
                        help="only Compiles Calci File to Given Language")

arg_parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=__ver_str__,
                        help="shows version info of Calci compiler")