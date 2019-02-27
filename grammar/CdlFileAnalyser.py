#!/usr/bin/env python3

__author__ = 'smr'


# Utilities
#


from sys import stdin, stdout, stderr, exit, argv
from io import StringIO
from antlr4 import *
from antlr4.InputStream import InputStream
from CdlLexer import CdlLexer
from CdlParser import CdlParser

from CdlVisitor import CdlVisitor
from CdlParser import CdlParser

from geolocator import CachedGeoLocator
import simplekml
from model import Location, Person, Vessel, VesselSeason, Cruise, Visitation, CrewEvent, Leg

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

locator = CachedGeoLocator()
locator.load()

def remove_quotes(aString : str):
    if aString.startswith('"') and aString.endswith('"'):
        return aString[1:-1]
    else:
        return aString

def get_text(ctx):
    if ctx is not None:
        return ctx.getText()
    return None

class StaySpec(object):
    def __init__(self, period, units):
        self.period = period
        self.units = units

    def get_duration_days(self):
        # only support days at the moment
        return self.period

    def __str__(self):
        return "%s: period=%s units=%s" % (type(self).__name__, str(self.period), self.units)

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

    def get_person(self, person_id):
        if person_id is not None:
            if person_id not in self.persons:
                raise ValueError("Unknown person %s" % (person_id, ))
            return self.persons[person_id]

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

    def get_location(self, location_id : str):
        if location_id is not None:
            if location_id not in self.locations:
                raise ValueError("%s not a defined location" % (location_id, ))
            return self.locations[location_id]

class VesselVisitor(CdlVisitor):
    def __init__(self):
        super(VesselVisitor, self).__init__()

    def visitVessel_spec(self, ctx:CdlParser.Vessel_specContext):
        return Vessel(
            ctx.identifier().getText(),
            ctx.name().getText(),
            remove_quotes(ctx.flag().getText()),
            remove_quotes(ctx.rego().getText()),
            float(ctx.speed().getText()))

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

class PersonVisitor(CdlVisitor):
    def __init__(self):
        super(PersonVisitor, self).__init__()

    def visitPerson_spec(self, ctx:CdlParser.Person_specContext):
        person_id = ctx.identifier().getText()
        name = remove_quotes(ctx.name().getText())
        return Person(person_id, name)

class PositionVisitor(CdlVisitor):
    def __init__(self):
        super(PositionVisitor, self).__init__();

    def visitPosition(self, ctx:CdlParser.PositionContext):
        return (
            LongLatVisitor().visit(ctx.lng()).value,
            LongLatVisitor().visit(ctx.lat()).value)

class LongLatVisitor(CdlVisitor):
    def __init__(self):
        super(LongLatVisitor, self).__init__();
        self.value = 0.0

    def visit(self, ctx):
        super(LongLatVisitor, self).visit(ctx);
        return self


    def visitDec_deg(self, ctx:CdlParser.Dec_degContext):
        self.value = float(ctx.number().getText())

    def visitDegrees(self, ctx:CdlParser.DegreesContext):
        self.value += int(ctx.getText())

    def visitDecimal_minutes(self, ctx:CdlParser.Decimal_minutesContext):
        text = ctx.getText().replace('\'', '')
        self.value += float(text)/60.0

    def visitEw_hemisphere(self, ctx:CdlParser.Ew_hemisphereContext):
        if ctx.getText() == "W":
            self.value = -self.value

    def visitNs_hemisphere(self, ctx:CdlParser.Ns_hemisphereContext):
        if ctx.getText() == "S":
            self.value = -self.value


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

        # handle person list
        visitor = PersonVisitor()
        for person_spec in ctx.person_list().person_spec():
            self.result.add_person(visitor.visit(person_spec))

        # hand vessel_season_specs

        visitor = VesselSeasonVisitor(self.result)
        for vsc in ctx.vessel_season_spec():
            vs = visitor.visit(vsc)
            self.result.add_vessel_season(vs)

        

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
        cruise =  Cruise(name=remove_quotes(ctx.title().getText()),
            departure_date=ctx.date().getText(),
            departure_port=self.cdl_file.get_location(ctx.location_identifier().getText())
            )

        # events
       
        eventVisitor = EventVisitor(self.cdl_file, cruise)
        for event_line in ctx.event_line():
            eventVisitor.visit(event_line)

        # build the legs for this cruise
         
        current_leg = None
        for event in cruise.events:
            if isinstance(event, CrewEvent):
                continue
            if current_leg is None:
                current_leg = Leg(cruise)
                current_leg.visitations.append(event)
            else:
                current_leg.visitations.append(event)
                if event.is_stopover():   # which ends this leg
                    cruise.legs.append(current_leg)
                    current_leg = Leg(cruise)
                    current_leg.visitations.append(event)
        return cruise

class EventVisitor(CdlVisitor):

    def __init__(self, cdl_file : CdlFile, cruise : Cruise):
        super(EventVisitor, self).__init__();
        self.cdl_file = cdl_file
        self.cruise = cruise
    def visitJoining_spec(self, ctx:CdlParser.Joining_specContext):
        person = self.cdl_file.get_person(ctx.identifier().getText())
        location = self.cdl_file.get_location(get_text(ctx.location_identifier()))

        e = CrewEvent(person, join_not_leave=True,
            role=get_text(ctx.role_spec()),
            scheduled=get_text(ctx.date()),
            location=location)
        self.cruise.add_event(e)
        return

    def visitLeaving_spec(self, ctx:CdlParser.Leaving_specContext):
        person = self.cdl_file.get_person(ctx.identifier().getText())
        location = self.cdl_file.get_location(get_text(ctx.location_identifier()))

        e = CrewEvent(person, join_not_leave=False,
            scheduled=get_text(ctx.date()),
            location=location)
        self.cruise.add_event(e)

    def visitVia_waypoints(self, ctx:CdlParser.Via_waypointsContext):
        for lid_ctx in ctx.location_identifier():
            location = self.cdl_file.get_location(get_text(lid_ctx))
            self.cruise.add_event(Visitation(location, stay_spec=None))
        return

    def visitVisitation_spec(self, ctx:CdlParser.Visitation_specContext):
        location = self.cdl_file.get_location(ctx.location_identifier().getText())

        # stay spec
        
        stay_spec = None
        visitor = StaySpecVisitor()
        if ctx.stay_spec() is not None:
            stay_spec = visitor.visit(ctx.stay_spec())
        
        self.cruise.add_event(Visitation(location, stay_spec=stay_spec))
        return

class StaySpecVisitor(CdlVisitor):

    def __init__(self):
        super(StaySpecVisitor, self).__init__();

    def visitStay_spec(self, ctx:CdlParser.Stay_specContext):
        return StaySpec(int(ctx.stay_duration().getText()), ctx.duration_units().getText())
        return

    

class CdlFileAnalyser(object):
    def __init__(self):
        pass

    def analyse(self, cdl_filename=None):
        '''
        Build a CdlFile instance from the CDL file
        '''

        # select input stream

        output = StringIO()
        if cdl_filename is None:
            fin = stdin
        else:
            fin = open(cdl_filename, 'r')

        # read source into memory, including files where specified

        for line in fin:
            if line.startswith("$include "):
                filename = line[8:-1].strip()
                with open(filename) as f:
                    for rec in f:
                        output.write(rec)
            else:
                output.write(line)
        fin.close()

        # now process CDL source from memory 

        lexer = CdlLexer(InputStream(output.getvalue()))
        token_stream = CommonTokenStream(lexer)
        parser = CdlParser(token_stream)
        tree = parser.cdl_file()
    
        visitor = CdlFileVisitor()
        cdl_file = visitor.visit(tree)
        locator.save()
        return cdl_file

if __name__ == '__main__':
    filename = None
    if len(argv) > 1:
        filename = argv[1]
    try:
        analyser = CdlFileAnalyser()
        tree = analyser.analyse(filename)
    except ValueError as e:
        locator.save()
        die(e)
    # import pdb; pdb.set_trace()
    #
