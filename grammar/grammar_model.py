#!/usr/bin/env python3

# A data model for the Cruise Description Language
#

__author__ = 'smr'

from geolocator import CachedGeoLocator
from geopy.distance import great_circle
from datetime import timedelta, datetime
from timezonefinder import TimezoneFinder
import pytz
from math import ceil


class Location(object):

    _locator = CachedGeoLocator().load()
    _tf = TimezoneFinder()

    @classmethod
    def save_cache(cls):
        if cls._locator is not None:
            cls._locator.save()

    def __init__(self, identifier, name, coords):
        self.identifier = identifier
        self.name = name
        if coords is None:
            loc = self._locator.get_location(name)
            self.coords = (loc['lng'],  loc['lat'])
        else:
            self.coords = coords
        self.timezone = None

    def lat(self):
        return self.coords[1]

    def lng(self):
        return self.coords[0]

    def asLatLongTuple(self):
        return (self.lat(), self.lng())

    def timezone_name(self):
        return self._tf.timezone_at(lng=self.lng(), lat=self.lat())

    def get_timezone(self):
        if self.timezone is None:
            self.timezone = pytz.timezone(self.timezone_name())
        return self.timezone

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

class Person(object):
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name 

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

class Vessel(object):
    def __init__(self, identifier, name, flag, rego, speed_kts):
        self.identifier = identifier
        self.name = name
        self.flag = flag
        self.rego = rego
        self.speed_kts = speed_kts
        # todo: expand attributes

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

class VesselSeason(object):
    def __init__(self, vessel, season, cruises):
        self.vessel = vessel
        self.season = season
        self.cruises = cruises

    def key(self):
        return "%s/%s" % (self.vessel.identifier, self.season)

    def identifier(self):
        return "%s" % (self.key(), )

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier())

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

class VisitedLocation(Location):
    def __init__(self, identifier, name, coords):
        super(self, VisitedLocation).__init__(identifier, name, coords)    

class PointOfInterest(Location):
    def __init__(self, identifier, name, coords):
        super(self, VisitedLocation).__init__(identifier, name, coords)    

class Season(object):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "%s: identifier=%s" % (type(self).__name__, self.identifier)

class CrewRole(object):
    def __init__(self, person : Person, role : str=None):
        self.person = person
        self.role = role

    def key(self):
        return self.person.identifier

    def __str__(self):
        result = self.person.identifier
        if self.role is not None:
          result += " (" + self.role + ")"
        return result

class Crew(object):
    '''
    An immutable collection of CrewRoles
    '''
    def __init__(self, crewRoles:dict=None):
        if crewRoles is None:
            self._crewRoles = {}
        else:
            self._crewRoles = crewRoles

    def add_crewRole(self, crewRole: CrewRole):
        if crewRole.key() in self._crewRoles.keys() :
            raise ValueError("% s is already in Crew" % (crewRole.key(), ))

        d = self._crewRoles.copy()  # duplicate the crewRoles
        d[crewRole.key()] = crewRole  # add the new crewRole
        return Crew(d)  

    def del_crewRole(self, crewRole: CrewRole):
        if crewRole.key() not in self._crewRoles.keys() :
            raise ValueError("%s is not in Crew" % (crewRole.key(), ))

        d = self._crewRoles.copy()  # duplicate the crewRoles
        d.pop(crewRole.key()) # delete the new crewRole
        return Crew(d)  

    def __str__(self):
        result = ""
        for cr in self._crewRoles.values():
            result += ", " + str(cr)
        return result[2:]

class Cruise(object):
    def __init__(self, vesselSeason=None, name=None, shortname=None, description=None, departure_date=None,
            departure_time=None, departure_port=None):
        self.vesselSeason = vesselSeason
        self.name = name 
        self.shortname = shortname    # not defined in grammar yet
        self.description = description   # not defined in grammar yet
        self._departure_date = departure_date  # should be datetime.date
        self._departure_time = departure_time  # should be datetime.time
        self.departure_port = departure_port
        self.legs = []   # not defined in grammar yet
        self.events = [] # ordered list of events - An Event is a Visitation or Crew movement

    def add_event(self, event):
        self.events.append(event)

    def distance_NM(self):
        dist = 0.0
        for leg in self.legs:
            dist += leg.distance_NM()
        return dist

    def elapsed_time_td(self):
        # the cruise ``elapsed_time`` includes the duration of the stay at the destination port
        visits = self.get_visitations()
        return visits[-1].get_arrival_dt() - visits[0].get_departure_dt() + visits[-1].get_computed_duration()

    def get_destination_stay_dt(self):
        visits = self.get_visitations()
        return visits[-1].get_computed_duration()

    def get_arrival_dt(self):
        visits = self.get_visitations()
        return visits[-1].get_arrival_dt()

    def get_visitations(self):
        visitations = []
        for e in self.events:
            if isinstance(e, Visitation):
                visitations.append(e)
        return visitations

    def get_destination_port(self):
        return self.get_visitations()[-1].location

    def cruising_speed_KTS(self):
        return self.vesselSeason.vessel.speed_kts

    def distance_NM(self):
        dist = 0.0 
        for leg in self.legs:
            dist += leg.distance_NM()
        return dist
    
    def get_departure_dt(self):
        '''
        Return the user specified departure date/time as a timezone aware datetime object
        localised to the local timezone of the departure port
        '''

        if self._departure_date is None or self._departure_time is None:
            raise ValueError("Departure date/time has not been specified for %s" % (self.name, ))
        dt = datetime.combine(self._departure_date , self._departure_time)
        dt = self.departure_port.get_timezone().localize(dt)
        return dt
            
    def get_description(self):
        return "Cruise from %s to %s departs %s distance %d NM" % (
            self.departure_port.identifier, 
            self.get_destination_port().identifier,
            self._departure_date, round(self.distance_NM()))

    def __str__(self):
        return "%s: name=%s departs %s on %s %d events, distance %d NM" % (type(self).__name__, self.name,
            self.departure_port, self._departure_date, len(self.events), round(self.distance_NM()))

class Leg(object):
    def __init__(self, cruise):
        self.cruise = cruise
        self.visitations = []
        self._hops = None
        self._warnings = []

    def origin_visitation(self):
        return self.visitations[0]

    def destination_visitation(self):
        return self.visitations[-1]

    def origin(self):
        return self.visitations[0].location

    def destination(self):
        return self.visitations[-1].location

    def name(self):
        return "%s to %s" % (self.origin().identifier, self.destination().identifier)

    def destination_stay_description(self):

        def hours(td : timedelta):
            secs = td.total_seconds()
            hours = round(secs/3600.0)
            return hours

        to_v = self.destination_visitation()
        return "stay in %s is  %s hours (expected %d)" % (
                    self.destination().identifier,
                    hours(to_v.get_computed_duration()),
                    hours(to_v.get_planned_duration_td()))

    def distance_NM(self):
        dist = 0.0
        for hop in self.hops():
            dist += hop.distance_NM()
        return dist

    def sailing_time(self):
        return timedelta(hours=self.distance_NM()/self.cruise.cruising_speed_KTS())

    def hops(self):
        if self._hops is None:
            self._hops = []
            for i in range(1,len(self.visitations)):
                self._hops.append(Hop(self.visitations[i-1].location, self.visitations[i].location))
        return self._hops

    def get_warnings(self):
        return self._warnings

    def clear_warnings(self):
        self._warnings = []
        return

    def add_warning(self, warning : Warning):
        self._warnings.append(warning)
        return

    def __str__(self):
        return "%s: from %s to %s dist_NM=%f time=%s" % (type(self).__name__, self.origin().identifier, self.destination().identifier, self.distance_NM(), str(self.sailing_time()))

class Hop(object):
    def __init__(self, from_location : Location, to_location : Location):
        self.from_location = from_location
        self.to_location = to_location

    def distance_NM(self):
        return great_circle(self.from_location.asLatLongTuple(), self.to_location.asLatLongTuple()).miles


class Visitation(object):
    def __init__(self, location : Location, crew : Crew, stay_spec=None, description=None):
        self.location = location
        self.description = description
        self.crew = crew
        self.stay_spec = stay_spec
        self.duration_days= 0
        self._arrival_dt = None
        self._computed_duration = None
        self._warnings = []

        if stay_spec is not None:
            self.duration_days= stay_spec.get_duration_days()
       
    def get_planned_duration_td(self):
        return timedelta(days=self.stay_spec.get_duration_days())
        
   
    def get_arrival_dt(self):
        return self._arrival_dt 
       
    def get_departure_dt(self):
        if self._arrival_dt is not None and self._computed_duration is not None:
            return self._arrival_dt + self._computed_duration

    def set_arrival_dt(self, a_dt : datetime):
        self._arrival_dt = a_dt

    def set_computed_duration(self, duration : timedelta):
        self._computed_duration = duration

    def get_computed_duration(self):
        return self._computed_duration

    def get_duration_description(self):
        cd = self.get_computed_duration()
        hours = int(ceil(cd.total_seconds()/3600.0))
        return "%d hours" % (hours, )

    def is_stopover(self):
        return self.duration_days > 0

    def get_warnings(self):
        return self._warnings

    def clear_warnings(self):
        self._warnings = []
        return

    def add_warning(self, warning : Warning):
        self._warnings.append(warning)
        return


    def __str__(self):
        return "%s: location=%s (stay %d days)" % (type(self).__name__, self.location.identifier, self.duration_days)

class CrewEvent(object):
    def __init__(self, person, join_not_leave=True, role=None, scheduled=None, location=None):
        self.person = person
        self.join_not_leave = join_not_leave
        self.role = role
        self.scheduled = scheduled
        self.location = location

    def event_name(self):
        if self.join_not_leave:
            return "joins"
        return "leaves"

    def __str__(self):
        loc_id = None
        if self.location is not None:
            loc_id = self.location.identifier
        return "%s: %s %s (role: %s, scheduled: %s, location: %s)" % (type(self).__name__, self.person.identifier,
            self.event_name(), self.role, self.scheduled, loc_id)

class Warning(object):
    def __init__(self, message : str):
        self._message = message


    def get_message(self):
        return "WARNING: %s" % (self._message, )

    
     

if __name__ == '__main__':
    pass

