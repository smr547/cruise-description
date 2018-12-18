__author__ = 'smr'

from CdlVisitor import CdlVisitor
from CdlParser import CdlParser


class MyVisitor(CdlVisitor):

    # Visit a parse tree produced by CdlParser#cruise.
    def visitCruise(self, ctx:CdlParser.CruiseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#location_definition.
    def visitLocation_definition(self, ctx:CdlParser.Location_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#location.
    def visitLocation(self, ctx:CdlParser.LocationContext):
        print("%s=%s"%(ctx.identifier().getText(),ctx.placename().getText()))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#placename.
    def visitPlacename(self, ctx:CdlParser.PlacenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#identifier.
    def visitIdentifier(self, ctx:CdlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#cruise_definition.
    def visitCruise_definition(self, ctx:CdlParser.Cruise_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#destination_line.
    def visitDestination_line(self, ctx:CdlParser.Destination_lineContext):
        print(ctx.identifier().getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CdlParser#title.
    def visitTitle(self, ctx:CdlParser.TitleContext):
        return self.visitChildren(ctx)



del CdlParser
