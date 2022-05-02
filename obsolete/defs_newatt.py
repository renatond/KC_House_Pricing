# THIS FUNCION WILL BE SAVED AS A .PY FILE NAMED 'defs'

import time
import geopy.geocoders
from geopy.geocoders import Nominatim
import certifi
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim( user_agent='geopyExercises')

def get_data(x):
    index, row = x
    time.sleep(10)
   
    #API request
    response = geolocator.reverse( row['latlong'] )
    address = response.raw['address']

    neighbourhood = address['neighbourhood'] if 'neighbourhood' in address else 'NA'
    city = address['city'] if 'city' in address else 'NA'
    state = address['state'] if 'state' in address else 'NA'

    return neighbourhood, city, state
