#!/usr/bin/env python3

# A data model for the Cruise Description Language
#

__author__ = 'smr'

from geolocator import CachedGeoLocator
from geopy.distance import great_circle
from datetime import timedelta

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

    def lat(self):
        return self.coords[0]

    def lng(self):
        return self.coords[1]

    def asLatLongTuple(self):
        return (self.lat(), self.lng())

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

class VisitedLocation(Location):
    def __init__(self, identifier, name, coords):
        super(self, VisitedLocation).__init__(identifier, name, coords)    

class PointOfInterest(Location):
    def __init__(self, identifier, name, coords):
        super(self, VisitedLocation).__init__(identifier, name, coords)    

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

class Person(object):
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name 

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

class Season(object):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "%s: identifier=%s" % (type(self).__name__, self.identifier)

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

class Cruise(object):
    def __init__(self, vesselSeason=None, name=None, shortname=None, description=None, departure_date=None,        departure_port=None):
        self.vesselSeason = vesselSeason
        self.name = name 
        self.shortname = shortname    # not defined in grammar yet
        self.description = description   # not defined in grammar yet
        self.departure_date = departure_date 
        self.departure_port = departure_port
        self.legs = []   # not defined in grammar yet
        self.events = [] # ordered list of events - An Event is a Visitation or Crew movement

    def add_event(self, event):
        # print("adding:  %s %s" % (type(event), str(event), ))
        self.events.append(event)

    def distance_NM(self):
        dist = 0.0
        for leg in self.legs:
            dist += leg.distance_NM()
        return dist

    def cruising_speed_KTS(self):
        return self.vesselSeason.vessel.speed_kts
            
    def __str__(self):
        return "%s: name=%s departs %s on %s %d events, distance %d NM" % (type(self).__name__, self.name,
            self.departure_port, self.departure_date, len(self.events), round(self.distance_NM()))

class Leg(object):
    def __init__(self, cruise):
        self.cruise = cruise
        self.visitations = []
        self._hops = None

    def origin(self):
        return self.visitations[0].location

    def destination(self):
        return self.visitations[-1].location

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

    def __str__(self):
        return "%s: from %s to %s dist_NM=%f time=%s" % (type(self).__name__, self.origin().identifier, self.destination().identifier, self.distance_NM(), str(self.sailing_time()))

class Hop(object):
    def __init__(self, from_location : Location, to_location : Location):
        self.from_location = from_location
        self.to_location = to_location

    def distance_NM(self):
        return great_circle(self.from_location.asLatLongTuple(), self.to_location.asLatLongTuple()).miles


class Visitation(object):
    def __init__(self, location, stay_spec=None, description=None):
        self.location = location
        self.description = description
        self.stay_spec = stay_spec
        self.duration_days= 0
        if stay_spec is not None:
            self.duration_days= stay_spec.get_duration_days()
       
        

    def is_stopover(self):
        return self.duration_days > 0

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
     

if __name__ == '__main__':
    pass

