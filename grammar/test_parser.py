#!/usr/bin/env python3

import sys
from antlr4 import *
from CdlLexer import CdlLexer
from CdlParser import CdlParser
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CdlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CdlParser(stream)
    tree = parser.cdl_file()
    element = tree.fleet_spec().vessel_spec()[0].cabin_list().cabin_spec()[0]
    print("Contents of type %s:\n%s\n" % (type(element), dir((element))))
    print(element.getText()) 
    print(element.identifier().getText())
    print(element.max_persons().getText())
if __name__ == '__main__':
    main(sys.argv)
