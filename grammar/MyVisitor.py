__author__ = 'smr'

from CdlVisitor import CdlVisitor
from CdlParser import CdlParser

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

del CdlParser
