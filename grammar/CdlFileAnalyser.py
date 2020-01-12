#!/usr/bin/env python3

__author__ = 'smr'

from sys import stdin, stdout, stderr, exit, argv
from io import StringIO
from cdl_preprocessor import preprocess
from antlr4 import *
from antlr4.InputStream import InputStream
from CdlLexer import CdlLexer
from CdlParser import CdlParser

from CdlVisitor import CdlVisitor
from CdlParser import CdlParser
from datetime import datetime

import simplekml
from grammar_model import CdlFile, Location, Person, Vessel, VesselSeason, Cruise, Visitation, CrewEvent, Leg, Crew, CrewRole, Cabin

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

date_format = "%d/%m/%y"
time_format = "%H%M"

# keep track of changing crew compliment as the file is processed

crew = None

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

class VesselVisitor(CdlVisitor):
    def __init__(self):
        super(VesselVisitor, self).__init__()

    def visitVessel_spec(self, ctx:CdlParser.Vessel_specContext):
        vessel = Vessel(
            ctx.identifier().getText(),
            ctx.name().getText(),
            remove_quotes(ctx.flag().getText()),
            remove_quotes(ctx.rego().getText()),
            float(ctx.speed().getText()))

        visitor = CabinSpecVisitor()
        for cabin_ctx in ctx.cabin_list().cabin_spec():
            vessel.add_cabin(visitor.visit(cabin_ctx))
        return vessel
            

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

        # handle vessel_season_specs

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
        global crew
        vessel_id = ctx.vessel_identifier().getText()
        if vessel_id in self.cdl_file.vessels:
            vessel = self.cdl_file.vessels[vessel_id]
        else:
            raise ValueError("Vessel %s is not defined" % (vessel_id, ))

        season_id = ctx.season_identifier().getText()

        crew = Crew() 
        cruises = []
        vessel_season = VesselSeason(vessel, season_id, cruises)
        visitor = CruiseVisitor(self.cdl_file, vessel_season)
        for c in ctx.cruise():
            cruise = visitor.visit(c)
            cruises.append(cruise)

        return vessel_season

class CruiseVisitor(CdlVisitor):

    def __init__(self, cdl_file : CdlFile, vessel_season: VesselSeason):
        super(CruiseVisitor, self).__init__();
        self.cdl_file = cdl_file
        self.vessel_season = vessel_season

    def visitCruise(self, ctx:CdlParser.CruiseContext):
        dep_date = datetime.strptime(ctx.date().getText(), date_format)
        dep_time = datetime.strptime(ctx.time().getText(), time_format)
        cruise =  Cruise(vesselSeason=self.vessel_season,
            name=remove_quotes(ctx.title().getText()),
            departure_date=dep_date.date(),
            departure_time=dep_time.time(),
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
        global crew
        person = self.cdl_file.get_person(ctx.identifier().getText())
        location = self.cdl_file.get_location(get_text(ctx.location_identifier()))
  
        # cabin allocation in a 'join'

        cabin = None
        ca = ctx.cabin_allocation()
        if ca is not None:
            cabin_id = ca.identifier().getText()
            # print("cabin_id=%s" % (cabin_id))
            try:
                cabin = self.cruise.vesselSeason.vessel.cabins[cabin_id]
            except KeyError:
                raise Exception("Cabin %s is undefined for vessel %s" % 
                    (cabin_id, self.cruise.vesselSeason.vessel.identifier))

        # role

        role =  get_text(ctx.role_spec())

        # create a CrewEvent object and add to this cruise

        e = CrewEvent(person, join_not_leave=True,
            role=role,
            scheduled=datetime.strptime(get_text(ctx.date()), date_format),
            location=location,
            cabin=cabin)
        self.cruise.add_event(e)

        # why do we need this global?

        crew = crew.add_crewRole(CrewRole(person, role))
        return

    def visitLeaving_spec(self, ctx:CdlParser.Leaving_specContext):
        global crew
        person = self.cdl_file.get_person(ctx.identifier().getText())
        location = self.cdl_file.get_location(get_text(ctx.location_identifier()))

        e = CrewEvent(person, join_not_leave=False,
            scheduled=datetime.strptime(get_text(ctx.date()), date_format),
            location=location)
        self.cruise.add_event(e)
        crew = crew.del_crewRole(CrewRole(person))

    def visitVia_waypoints(self, ctx:CdlParser.Via_waypointsContext):
        for lid_ctx in ctx.location_identifier():
            location = self.cdl_file.get_location(get_text(lid_ctx))
            self.cruise.add_event(Visitation(location, crew, stay_spec=None))
        return

    def visitVisitation_spec(self, ctx:CdlParser.Visitation_specContext):
        location = self.cdl_file.get_location(ctx.location_identifier().getText())

        # stay spec
        
        stay_spec = None
        visitor = StaySpecVisitor()
        if ctx.stay_spec() is not None:
            stay_spec = visitor.visit(ctx.stay_spec())
        else:
            stay_spec = StaySpec(1, "night")
        
        self.cruise.add_event(Visitation(location, crew, stay_spec=stay_spec))
        return

class StaySpecVisitor(CdlVisitor):

    def __init__(self):
        super(StaySpecVisitor, self).__init__();

    def visitStay_spec(self, ctx:CdlParser.Stay_specContext):
        return StaySpec(int(ctx.stay_duration().getText()), ctx.duration_units().getText())

class CabinSpecVisitor(CdlVisitor):

    def __init__(self):
        super(CabinSpecVisitor, self).__init__();

    def visitCabin_spec(self, ctx:CdlParser.Cabin_specContext):
        return Cabin(ctx.identifier().getText(), int(ctx.max_occupants().getText()))

class CdlFileAnalyser(object):
    def __init__(self):
        pass

    def analyse(self, fin):
        '''
        Build a CdlFile instance from the CDL file-like object fin
        '''
        lexer = CdlLexer(InputStream(fin.read()))
        token_stream = CommonTokenStream(lexer)
        parser = CdlParser(token_stream)
        tree = parser.cdl_file()
    
        visitor = CdlFileVisitor()
        cdl_file = visitor.visit(tree)
        Location.save_cache()
        return cdl_file

if __name__ == '__main__':
    fin = stdin
    try:
        if len(argv) > 1:
            fin = open(argv[1], 'r')
        analyser = CdlFileAnalyser()
        tree = analyser.analyse(fin)
    except ValueError as e:
        Location.save_cache()
        die(e)
    # import pdb; pdb.set_trace()
    #
