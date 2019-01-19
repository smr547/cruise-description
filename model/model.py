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
    def __init__(self, identifier, name, shortname, country_of_rego, rego_number):
        self.identifier = identifier
        self.name = name 
        self.shortname = shortname 
        self.country_of_rego = country_of_rego
	self.rego_number = rego_number
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
    def __init__(self, vessel, season):
        self.vessel = vessel
        self.season = season
        self.locations = []
        self.cruises = []

    def identifier(self):
        return "%s/%s" % (self.vessel.identifier, self.season.identifier)

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier())

class Cruise(object):
    def __init__(self, vesselSeason, identifier, name, shortname, description):
        self.vesselSeason = vesselSeason
        self.identifier = identifier
        self.name = name 
        self.shortname = shortname 
        self.description = description
        self.legs = []

    def __str__(self):
        return "%s: identifier=%s, name=%s" % (type(self).__name__, self.identifier, self.name)

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
    def __init__(self, leg, location, identifier, description, duration_days=0):
        self.leg = leg
        self.location = location
        self.identifier = identifier
        self.description = description
        self.duration _days= duration_days

    def is_stopover(self):
        return self.duration_days > 0

    def __str__(self):
        return "%s: identifier=%s, location=%s" % (type(self).__name__, self.identifier, self.location.name)


if __name__ == '__main__':
    pass

