#!/usr/bin/env python3

# Utilities
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
from model import Person, VesselSeason, Cruise

def die(message):
    sys.stderr.write(str(message) + "\n")
    sys.exit(1)

locator = CachedGeoLocator()
locator.load()

def remove_quotes(aString : str):
    if aString.startswith('"') and aString.endswith('"'):
        return aString[1:-1]
    else:
        return aString

class Vessel(object):
    def __init__(self, identifier, name, flag, rego):
        self.identifier = identifier
        self.name = name
        self.flag = flag 
        self.rego = rego
        # todo: expand attributes

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)
class Location(object):

    def __init__(self, identifier, name, coords):
        print("construction location: %s \n" % (name, ))
        self.identifier = identifier
        self.name = name
        if coords is None:
            loc = locator.get_location(name)
            self.coords = (loc['lng'],  loc['lat'])
        else:
            self.coords = coords

    def __str__(self):
        return "Location: identifier=%s, name=%s" % (self.identifier, self.name)

class CdlFile(object):
    def __init__(self):
        self.vessels = {}  # dict of all vessels in the fleet
        self.persons = {}  # dict of all people  
        self.vesselSeasons = {} # dict of all VesselSeasons in the file
        self.locations = {} # dict of all locations in the file

    def add_vessel(self, vessel : Vessel):
        key = vessel.identifier
        if key in self.vessels:
            raise ValueError("Duplicate definitions for Vessel %s" % (key, ))
        else:
            self.vessels[key] = vessel

    def add_person(self, person : Person):
        key = person.identifier
        if key in self.persons:
            raise ValueError("Duplicate definitions for Person %s" % (key, ))
        else:
            self.persons[key] = person

    def add_location(self, location : Location):
        key = location.identifier
        if key in self.locations:
            raise ValueError("Duplicate definitions for Location %s" % (key, ))
        else:
            self.locations[key] = location

    def add_vessel_season(self, vessel_season : VesselSeason):
        key = vessel_season.key()
        if key in self.vesselSeasons:
            raise ValueError("Duplicate definitions for VesselSeason %s" % (key, ))
        else:
            self.vesselSeasons[key] = vessel_season


class VesselVisitor(CdlVisitor):
    def __init__(self):
        super(VesselVisitor, self).__init__()

    def visitVessel_spec(self, ctx:CdlParser.Vessel_specContext):
        return Vessel(
            ctx.identifier().getText(),
            ctx.name().getText(),
            remove_quotes(ctx.flag().getText()),
            remove_quotes(ctx.rego().getText()))

class LocationVisitor(CdlVisitor):
    def __init__(self):
        super(LocationVisitor, self).__init__()

    def visitLocation(self, ctx:CdlParser.LocationContext):
        coords = None
        if ctx.position() is not None:
            coords = PositionVisitor().visit(ctx.position())
        return Location(ctx.identifier().getText(),
            remove_quotes(ctx.placename().getText()),
            coords)

class PositionVisitor(CdlVisitor):
    def __init__(self):
        super(PositionVisitor, self).__init__();

    def visitPosition(self, ctx:CdlParser.PositionContext):
        return (float(ctx.lng().getText()), float(ctx.lat().getText()))

class CdlFileVisitor(CdlVisitor):

    def __init__(self):
        super(CdlFileVisitor, self).__init__();
        self.result = CdlFile()

    def visitCdl_file(self, ctx:CdlParser.Cdl_fileContext):

        # hand fleet spec
        visitor = VesselVisitor()        
        for vsc in ctx.fleet_spec().vessel_spec():
            self.result.add_vessel(visitor.visit(vsc))

        # handle location list
        visitor = LocationVisitor()
        for loc_spec in ctx.location_list().location():
            self.result.add_location(visitor.visit(loc_spec))

        # hand vessel_season_specs

        visitor = VesselSeasonVisitor(self.result)
        for vsc in ctx.vessel_season_spec():
            self.result.add_vessel_season(visitor.visit(vsc))

        return self.result

class VesselSeasonVisitor(CdlVisitor):

    def __init__(self, cdl_file : CdlFile):
        super(VesselSeasonVisitor, self).__init__();
        self.cdl_file = cdl_file

    def visitVessel_season_spec(self, ctx:CdlParser.Vessel_season_specContext):
        vessel_id = ctx.vessel_identifier().getText()
        if vessel_id in self.cdl_file.vessels:
            vessel = self.cdl_file.vessels[vessel_id]
        else:
            raise ValueError("Vessel %s is not defined" % (vessel_id, ))

        season_id = ctx.season_identifier().getText()
 
        cruises = []
        result = VesselSeason(vessel, season_id, cruises)
        visitor = CruiseVisitor(self.cdl_file)
        for c in ctx.cruise():
            cruise = visitor.visit(c)
            cruise.vesselSeason = result
            cruises.append(cruise)

        return result

class CruiseVisitor(CdlVisitor):

    def __init__(self, cdl_file : CdlFile):
        super(CruiseVisitor, self).__init__();
        self.cdl_file = cdl_file

    def visitCruise(self, ctx:CdlParser.CruiseContext):
        result =  Cruise(remove_quotes(ctx.title().getText()))

        # events
       
        eventVisitor = EventVisitor(self.cdl_file)
        for event_line in ctx.event_line():
            result.add_event(eventVisitor.visit(event_line))

        return result

class EventVisitor(CdlVisitor):

    def __init__(self, cdl_file : CdlFile):
        super(EventVisitor, self).__init__();
        self.cdl_file = cdl_file

    def visitJoining_spec(self, ctx:CdlParser.Joining_specContext):
        print("ignored event: %s joining\n" % (ctx.identifier().getText(),))
        return


    def visitLeaving_spec(self, ctx:CdlParser.Leaving_specContext):
        print(ignored event: "%s leaving\n" % (ctx.identifier().getText(),))
        return 

    def visitVisitation_spec(self, ctx:CdlParser.Visitation_specContext):
        location_id = ctx.location_identifier().getText()
        if location_id not in self.cdl_file.locations:
            raise ValueError("%s not a defined location" % (location_id, ))

        # stay spec
        
        stay_spec = None
        visitor = StaySpecVisitor()
        if ctx.stay_spec() is not None:
            stay_spec = visitor.visit(ctx.stay_spec())
        
            
        return Visitation(location, stay_spec=stay_spec)
    
def build_objects(cdl_filename=None):
    '''
    Build a VesselSeason instance from the CDL file
    '''

    if cdl_filename is None:
        input_stream = InputStream(sys.stdin.readline())
    else:
        input_stream = FileStream(cdl_filename)
    lexer = CdlLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CdlParser(token_stream)
    tree = parser.cdl_file()
    
    visitor = CdlFileVisitor()
    cdl_file = visitor.visit(tree)
    locator.save()
    return cdl_file

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    try:
        tree = build_objects(sys.argv[1])
    except ValueError as e:
        locator.save()
        die(e)
    # import pdb; pdb.set_trace()
    print(type(tree))
