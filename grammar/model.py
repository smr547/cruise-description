#!/usr/bin/env python3

# A data model for the Cruise Description Language
#

__author__ = 'smr'

from geolocator import CachedGeoLocator

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
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

class VisitedLocation(Location):
    def __init__(self, identifier, name, coords):
        super(self, VisitedLocation).__init__(identifier, name, coords)    

class PointOfInterest(Location):
    def __init__(self, identifier, name, coords):
        super(self, VisitedLocation).__init__(identifier, name, coords)    

class Vessel(object):
    def __init__(self, identifier, name, flag, rego):
        self.identifier = identifier
        self.name = name 
        self.flag = flag
        self.rego = rego
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

    def __str__(self):
        return "%s: name=%s departs %s on %s" % (type(self).__name__, self.name,
            self.departure_port, self.departure_date)

class Leg(object):
    def __init__(self, cruise, identifier, name, description):
        self.cruise = cruise
        self.identifier = identifier
        self.name = name 
        self.description = description
        self.visitations = []

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

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


if __name__ == '__main__':
    pass

