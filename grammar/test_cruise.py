#!/usr/bin/env python3

# List all the locations mentioned in a cruise description
#

__author__ = 'smr'

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from CdlLexer import CdlLexer
from CdlParser import CdlParser

from CdlVisitor import CdlVisitor
from CdlParser import CdlParser

from geolocator import GeoLocator

class Location(object):
    def __init__(self, identifier, name, lat_long):
        self.identifier = identifier
        self.name = name
        self.lat_long = lat_long

    def __str__(self):
        return "Location: identifier=%s, name=%s" % (self.identifier, self.name)

class MyVisitor(CdlVisitor):

    def __init__(self):
        self.locations = {}

    def visitLocation(self, ctx:CdlParser.LocationContext):
        loc = Location(ctx.identifier().getText(), ctx.placename().getText(), None)
        self.locations[loc.identifier] = loc
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CdlParser#destination_line.
    def visitDestination_line(self, ctx:CdlParser.Destination_lineContext):
        if ctx.identifier().getText() not in self.locations:
            loc = Location(ctx.identifier().getText(), ctx.identifier().getText(), None)
            self.locations[loc.identifier] = loc
        return self.visitChildren(ctx)

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

    locator = GeoLocator()

    for loc in visitor.locations.values():
        print(loc, locator.get_location(loc.name))
