import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBT0wk5hoASyd3WI6aq22Psq8vfv5BYpLY')

now = datetime(2021, 7, 19, 9)
directions = gmaps.directions("Klinkenbergerweg 34, 6711 ML Ede", "Station Lage Zwaluwe", mode="driving", departure_time=now)

print("done")