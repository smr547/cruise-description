#!/usr/bin/env python3

from sys import argv
import os
import googlemaps
import json
from pathlib import Path

class GeoLocator(object):
    '''
    Use GoogleMaps Geolocation API to return placename information
    '''

    def __init__(self):
        secret_key = os.environ['GOOGLE_API_KEY']
        self.gmaps = googlemaps.Client(key=secret_key)

    def get_location(self, place_name:str):
        '''
        Uses the Google Maps geocode service to
        return the  location of the supplied place name as a dict like
        {'lng': 2.1734035, 'lat': 41.3850639}
        '''
        r = self.gmaps.geocode(place_name)
        if len(r) > 0:
            return r[0]['geometry']['location']
        else:
            raise ValueError("Unknown location %s" % (place_name, ))

class CachedGeoLocator(GeoLocator):
    cache_filename = Path('locator_cache.json')

    def save(self):
        # print("Saving GeoLocator cache with %d items" % (len(self.cache), ))
        with open(str(self.cache_filename), 'w') as outfile:
            json.dump(self.cache, outfile)

    def load(self):
        if self.cache_filename.is_file():
            with open(str(self.cache_filename), 'r') as infile:
                self.cache = json.load(infile)
        return self

    def __init__(self):
        self.cache = {}
        super(CachedGeoLocator, self).__init__()

    def get_location(self, place_name: str):
        '''
        Returns location of the supplied place name as a dict like
        {'lng': 2.1734035, 'lat': 41.3850639}
        '''
        if place_name not in self.cache:
            self.cache[place_name] = super(CachedGeoLocator, self).get_location(place_name)
            # print("Adding '%s' to cache which now has %d items" % (place_name, len(self.cache)))
        return self.cache[place_name]

if __name__ == "__main__":
    locator = CachedGeoLocator()
    locator.load()
    print(locator.get_location(argv[1]))
    locator.save()

    
