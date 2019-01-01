
import os
import googlemaps

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
