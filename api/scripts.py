import sqlite3 as sql
import geopy.distance
import pandas as pd
import requests
from io import StringIO
import json
import os.path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(BASE_DIR, "db.sqlite3")
con = sql.connect(db_path, check_same_thread=False)
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


def get_assignments(user_key, icao):
    """
    Takes an airport ICAO and fetches the assignments available at it
    Groups assignments with the same to and from ICAO
    Returns info in JSON format
    :param user_key: key from FSEconomy datafeed
    :param icao: 3 or 4 digit string
    """
    df = pd.DataFrame()
    headers = {}
    payload = {}
    url = f'https://server.fseconomy.net/data?userkey={user_key}' \
          f'&format=csv&query=icao&search=jobsfrom&icaos={icao.upper()}'
    response = requests.request("GET", url, headers=headers, data=payload)
    if '<Error>' in response.text:
        print(f'{response.status_code}: {response.text}')
        pass
    else:
        df = pd.concat([df, pd.read_csv(StringIO(response.text), sep=',')])

    assignments = df.groupby(['FromIcao', 'ToIcao', 'UnitType', 'Type'], as_index=False).agg(
        {'Amount': 'sum', 'Pay': 'sum'})
    assignments = assignments[['FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay']]
    assignments['Distance'] = assignments.apply(lambda x: get_distance(x['ToIcao'], x['FromIcao']), axis=1)
    assignments.to_sql('api_assignment', con, if_exists='append')
    pass

