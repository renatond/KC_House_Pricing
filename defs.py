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
   
    #API request
    response = geolocator.reverse( row['latlong'] )
    address = response.raw['address']

    place_id = response.raw['place_id'] if 'place_id' in response.raw else 'NA'
    osm_type = response.raw['osm_type'] if 'osm_type' in response.raw else 'NA'
    country = address['country'] if 'country' in address else 'NA'
    country_code = address['country_code'] if 'country_code' in address else 'NA'

    return place_id, osm_type, country, country_code