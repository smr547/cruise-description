
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
        r = self.gmaps.geocode(place_name)
        return r[0]['geometry']['location']

class CachedGeoLocator(GeoLocator):
    cache_filename = Path('locator_cache.json')

    def save(self):
        with open(self.cache_filename, 'w') as outfile:
            json.dump(self.cache, outfile)

    def load(self):
        if self.cache_filename.is_file():
            with open(self.cache_filename, 'r') as infile:
                self.cache = json.load(infile)

    def __init__(self):
        self.cache = {}
        super(CachedGeoLocator, self).__init__()

    def get_location(self, place_name: str):
        if place_name not in self.cache:
            self.cache[place_name] = super(CachedGeoLocator, self).get_location(place_name)
        return self.cache[place_name]
