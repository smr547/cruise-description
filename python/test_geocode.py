#!/usr/bin/env python3

# A simple test of the geolocation API
#
# Assumes env variable GOOGLE_API_KEY has been intialised
#

import os
import googlemaps


secret_key = os.environ['GOOGLE_API_KEY']
gmaps = googlemaps.Client(key=secret_key)

places = ["Sant Carles de la Rapita", 
   "Kembla Heights, NSW, Australia", 
   "7 Gooreen Steet, Reid, ACT", 
   "Port of Barcelona, Spain", 
   "Toulon, France",
   "St. Tropez, France",
   "St. Tropez",
   "Point de Colombier, France",
   "Cape Cepet, France"]

for place in places:
    r = gmaps.geocode(place)
    
    loc = (r[0]['geometry']['location'])
    # p =  {'lat': loc['lat'], 'lng': loc['lng']}
    p =  (loc['lat'], loc['lng'])
    print(type(p))
    e = gmaps.elevation(p)
    print(place, r[0]['geometry']['location'], e)

