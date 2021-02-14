'''
Module for finding coordinates and distance.
'''

import math
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderUnavailable

geolocator = Nominatim(user_agent="Geo Helper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def calculate_distance(point1: tuple, point2: tuple) -> float:
    '''
    Calculate distance between two points on the globe.

    >>> calculate_distance((49.81812780411789, 24.023804536291237),\
 (49.816988598548434, 24.023516882652373))
    0.12834404504864394
    >>> calculate_distance((48.63606646315562, 34.95913939497848),\
 (49.89303026581707, 24.09021802341345))
    800.2137219129796
    '''
    earth_radius = 6371

    lattitude1 = math.radians(point1[0])
    longitude1 = math.radians(point1[1])
    lattitude2 = math.radians(point2[0])
    longitude2 = math.radians(point2[1])

    delta_lon = longitude2 - longitude1
    delta_lat = lattitude2 - lattitude1

    distance = 2*earth_radius * math.asin(math.sqrt(math.sin(
        delta_lat/2)**2 + math.cos(lattitude1)*math.cos(lattitude2)*math.sin(delta_lon/2)**2))
    return distance


def get_coordinates(address: str) -> tuple:
    '''
    Get coordinates of location.

    >>> get_coordinates('Lviv')
    (49.841952, 24.0315921)
    >>> get_coordinates('New York')
    (40.7127281, -74.0060152)
    '''
    try:
        location = try_geocode_until_failure(address)
    except GeocoderUnavailable:
        return 0, 0

    if location is None:
        return 0, 0

    return location.latitude, location.longitude


def try_geocode_until_failure(address: str, attempt=1, max_attempts=3):
    '''
    Check if geopy can find location of address.
    '''
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return try_geocode_until_failure(address, attempt=attempt+1)
        raise


def get_movies_coordinates(movies: list):
    '''
    Get coordinates of movies filming locations.

    >>> get_movies_coordinates([['The Office', 'Scranton, Pennsylvania, USA'],\
['How To Get Away With Murder', 'Los Angeles, California, USA']])
    [['The Office', (41.4086874, -75.6621294)], ['How To Get Away With Murder',\
 (34.0536909, -118.242766)]]
    '''
    coordinates = []
    for movie in movies:
        location = get_coordinates(movie[1])
        if location != (0, 0):
            coordinates.append([movie[0], location])

    return coordinates


def get_movies_coordinates_with_distance(movies: list, location: tuple) -> list:
    '''
    Get a list of movies with relative distance to certain location.

    >>> get_movies_coordinates_with_distance([['The Office', (41.4086874, -75.6621294)],\
 ['How To Get Away With Murder', (34.0536909, -118.242766)]],\
 (49.81808054050804, 24.025798406573227))
    [['The Office', (41.4086874, -75.6621294), 7218.698217414779],\
 ['How To Get Away With Murder', (34.0536909, -118.242766), 9975.48942473333]]
    '''
    movies_with_distance = []
    for movie in movies:
        if movie[1] != (0, 0):
            movies_with_distance.append(
                [movie[0], movie[1], calculate_distance(location, movie[1])])

    return movies_with_distance
