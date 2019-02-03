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

from geolocator import CachedGeoLocator
import simplekml

def die(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)

locator = CachedGeoLocator()
locator.load()

class Location(object):

    def __init__(self, identifier, name, coords):
        self.identifier = identifier
        self.name = name
        if coords is None:
            loc = locator.get_location(name)
            self.coords = (loc['lng'],  loc['lat'])
        else:
            self.coords = coords

    def __str__(self):
        return "Location: identifier=%s, name=%s" % (self.identifier, self.name)

class MyVisitor(CdlVisitor):

    def __init__(self):
        self.locations = {}
        self.title = None
        self.visitations = []

    def visitTitle(self, ctx:CdlParser.TitleContext):
        self.title = ctx.getText()
        return self.visitChildren(ctx)


    def visitLocation(self, ctx:CdlParser.LocationContext):
        positionVisitor = PositionVisitor()
        positionVisitor.visitChildren(ctx)
        loc = Location(ctx.identifier().getText(), ctx.placename().getText(), positionVisitor.coords_tuple())
        self.locations[loc.identifier] = loc
        return

    # Visit a parse tree produced by CdlParser#destination_line.
    def visitVisitation_spec(self, ctx:CdlParser.Visitation_specContext):
        loc = None
        if ctx.location_identifier().getText() not in self.locations:
            loc = Location(ctx.location_identifier().getText(), ctx.location_identifier().getText(), None)
            self.locations[loc.identifier] = loc
        else:
            loc = self.locations[ctx.location_identifier().getText()]

        self.visitations.append(loc)
        return self.visitChildren(ctx)

class PositionVisitor(CdlVisitor):
    def __init__(self):
        self.coords = []

    def visitNumber(self, ctx:CdlParser.NumberContext):
        self.coords.append(float(ctx.getText()))
        return 

    def coords_tuple(self):
        if len(self.coords) > 1:
            return tuple(self.coords)
        else:
            return None
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    lexer = CdlLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CdlParser(token_stream)
    tree = parser.cdl_file()

    visitor = MyVisitor()

    try:
        visitor.visit(tree)
    except ValueError as e:
        locator.save()
        die(str(e))

    # create simple KML file

    kml = simplekml.Kml()


    for loc in visitor.locations.values():
        pnt = kml.newpoint(name=loc.identifier, description=loc.name, coords=[loc.coords])

    route = []
    for loc in visitor.visitations:
        route.append(loc.coords)

    ls = kml.newlinestring(name=visitor.title)
    ls.coords = route
    # ls.extrude = 1
    # ls.altitudemode = simplekml.AltitudeMode.relativetoground
    ls.style.linestyle.width = 10
    ls.style.linestyle.color = simplekml.Color.red
    ls.description = '<![CDATA[This is a description of the planned cruise<br/><hr /><a href="http://doc.trolltech.com/3.3/qstylesheet.html">Here is a link</a> to something interesting<hr />]]>'

    print(kml.kml())
    locator.save()

