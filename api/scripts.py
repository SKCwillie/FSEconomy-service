import sqlite3 as sql
import geopy.distance
import pandas as pd
import requests
from io import StringIO
import os.path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(BASE_DIR, "db.sqlite3")
con = sql.connect(db_path, check_same_thread=False)
cur = con.cursor()
FUEL_PRICE = 4.50
LANDING_TIME = .25


def get_icao_list():
    """
    Function that takes no argument but will query the database for all large US and CAN airports
    :return: list of icaos
    """
    query = "SELECT icao FROM api_airport WHERE (country = 'United States' or country = 'Canada') AND size >=3000"
    query_results = cur.execute(query).fetchall()
    return [i[0] for i in query_results]


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


def stringify_icao_list(icao_list, n=30):
    """
    function to take a list and breaks the list into a subset of n strings
    this allows to hit the endpoint n times as to not error out with too many requests
    :param icao_list: list of icaos
    :param n: how many strings to divide the list into. i.e. how many times to hit the endpoint
    :return: a list of strings formatted to easily hit the datafeed
    """
    return_list = []
    icao_list = [icao_list[i::n] for i in range(n)]
    for sublist in icao_list:
        return_list.append('-'.join(sublist))
    return return_list


def get_return_pax(FromIcao, ToIcao):
    """
    Goes and hits the api_assignments db to find how many return pax exist for given assignment
    :param FromIcao: ICAO of original assignment
    :param ToIcao: ICAO of original assignment
    :return: how passengers are available for return leg
    """
    query = f"SELECT Amount, UnitType FROM api_job WHERE FromIcao ='{ToIcao}' AND ToIcao ='{FromIcao}' AND UnitType='passengers'"
    try:
        results = cur.execute(query).fetchone()[0]
        return results
    except TypeError:
        return None


def get_alias_dict():
    """
    Reads the CSV with aircraft aliases to format the aliases more digestable for the datafeed
    :return: A dict with aliases (with removed spaces) as keys and the actuaal makeModel as values
    """
    df = pd.read_csv(f'{BASE_DIR}/data/aircraftalias.csv')
    alias_dict = {}
    for index, row in df.iterrows():
        try:
            alias_dict[row['Alias'].replace(' ', '')] = row['MakeModel']
        except AttributeError:
            alias_dict[row['Alias']] = row['MakeModel']
    return alias_dict


aliases = get_alias_dict()


def get_financials(instance):
    """
    Takes an instance of the AircraftJobsSerializer class to calculate cost and profits for job
    :param instance: instance of class
    :return:
    """
    query = f"""
    SELECT GPH, CruiseSpeed, Seats, Crew
    FROM api_aircraft 
    WHERE MakeModel = '{instance.MakeModel}'"""
    fuel_burn, cruise_speed, seats, crew = cur.execute(query).fetchone()
    job_time = 2 * instance.Distance / cruise_speed + LANDING_TIME
    dry_cost = job_time * (instance.RentalDry + fuel_burn + FUEL_PRICE)
    wet_cost = job_time * instance.RentalWet
    # This is clunky but there needs to be checks incase the owner doesn't allow for dry and wet rental
    if instance.RentalWet == 0:
        rental_cost = dry_cost
    elif instance.RentalDry == 0:
        rental_cost = wet_cost
    elif dry_cost > wet_cost:
        rental_cost = wet_cost
    else:
        rental_cost = dry_cost

    max_pax = seats - crew - 1
    dollar_per_pax = round(instance.Pay / instance.Amount, 2)
    if instance.Amount > max_pax:
        pax_to = max_pax
    else:
        pax_to = instance.Amount
    if instance.ReturnPax > max_pax:
        pax_from = max_pax
    else:
        pax_from = instance.ReturnPax
    net_pay = (pax_to + pax_from) * dollar_per_pax
    ground_crew_fee = net_pay * .10
    if pax_to > 4:
        booking_fee_to = round(pax_to * .01, 2) * net_pay
    else:
        booking_fee_to = 0
    if pax_from > 4:
        booking_fee_from = round(pax_from * .01, 2) * net_pay
    else:
        booking_fee_from = 0
    earnings = round(net_pay - rental_cost - booking_fee_from - booking_fee_to - ground_crew_fee, 2)
    instance.NetPay = round(net_pay, 2)
    instance.PaxTo = int(round(pax_to, 0))
    instance.PaxFrom = int(round(pax_from, 0))
    instance.RentalCost = round(rental_cost, 2)
    instance.RentalDryCost = round(dry_cost, 2)
    instance.RentalWetCost = round(wet_cost, 2)
    instance.BookingFeeTo = round(booking_fee_to, 2)
    instance.BookingFeeFrom = round(booking_fee_from, 2)
    instance.Earnings = round(earnings, 2)
    instance.EarningsPerHr = int(round(earnings / job_time, 0))
    return instance
