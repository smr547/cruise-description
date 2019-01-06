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
import simplekml

class Location(object):
    locator = GeoLocator()

    def __init__(self, identifier, name, coords):
        self.identifier = identifier
        self.name = name
        if coords is None:
            loc = self.locator.get_location(name)
            self.coords = (loc['lng'],  loc['lat'])
        else:
            self.coords = coords

    def __str__(self):
        return "Location: identifier=%s, name=%s" % (self.identifier, self.name)

class MyVisitor(CdlVisitor):

    def __init__(self):
        self.locations = {}
        self.title = None

    def visitTitle(self, ctx:CdlParser.TitleContext):
        self.title = ctx.getText()
        return self.visitChildren(ctx)


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

    # create simple KML file

    kml = simplekml.Kml()


    route = []
    for loc in visitor.locations.values():
        pnt = kml.newpoint(name=loc.identifier, description=loc.name, coords=[loc.coords])
        route.append(loc.coords)

    ls = kml.newlinestring(name=visitor.title)
    ls.coords = route
    # ls.extrude = 1
    # ls.altitudemode = simplekml.AltitudeMode.relativetoground
    ls.style.linestyle.width = 10
    ls.style.linestyle.color = simplekml.Color.red

    print(kml.kml())
