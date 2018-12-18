__author__ = 'smr'

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from CdlLexer import CdlLexer
from CdlParser import CdlParser
from MyVisitor import MyVisitor

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    lexer = CdlLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CdlParser(token_stream)
    tree = parser.cruise()

    visitor = MyVisitor()
    visitor.visit(tree)

    # list all unique locations

    for loc in visitor.locations.values():
        print(loc)
