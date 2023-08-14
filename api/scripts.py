import sqlite3 as sql
import geopy.distance

con = sql.connect('../db.sqlite3')
cur = con.cursor()


def get_coords(icao):
    """
    Takes and ICAO and uses the SQL db to lookup lat/lon
    :param icao: airport identifier from airports db
    :return: latitude and longitude of airport
    """
    lat = cur.execute(f"SELECT lat FROM api_airport WHERE icao='{icao}'").fetchone()[0]
    lon = cur.execute(f"SELECT lon FROM api_airport WHERE icao='{icao}'").fetchone()[0]
    return lat, lon


def get_distance(to_icao, from_icao):
    """
    Takes two airport ICAOs, runs the get_oords function
    :param to_icao: airport assignment goes to
    :param from_icao: airport assignment is from
    :return: distance in nautical miles between two airports
    """
    to_lat, to_lon = get_coords(to_icao)
    from_lat, from_lon = get_coords(from_icao)
    distance = geopy.distance.geodesic((to_lat, to_lon), (from_lat, from_lon)).nm
    return round(distance, 0)
