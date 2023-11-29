import sqlite3
import sys

sys.path.insert(0, '/home/skcwillie/FSEconomyV2')
from dotenv import load_dotenv
from os import listdir
import sqlite3 as sql
import pandas as pd
import time
import requests
import os
from io import StringIO
from api.scripts import get_icao_list, get_distance, stringify_icao_list, get_return_pax, db_path

load_dotenv('../api/.env')
FSE_KEY = os.getenv('FSE_KEY')
DELAY = 61
con = sql.connect(db_path, check_same_thread=False)
cur = con.cursor()


def create_dbs():
    file_names = [file for file in listdir('.') if file.endswith('.csv')]
    for file_name in file_names:
        table_name = f"api_{file_name.split('.')[0]}"
        df = pd.read_csv(f'./{file_name}', sep=';')
        df.to_sql(table_name, con, if_exists='replace', index=False)
    print('Successfully built starting dbs')
    pass


def get_aircraft_list():
    aircraft_list = []
    query = 'SELECT * FROM api_availableaircraft'
    query_results = con.execute(query).fetchall()
    for result in query_results:
        aircraft_list.append(result[1])
    return aircraft_list


def get_data(url, df, headers={}, payload={}, error_count=0):
    errors_allowed = 10
    response = requests.request("GET", url, headers=headers, data=payload)
    if error_count == errors_allowed:
        print('Skipping')
        return df
    elif '<Error>' in response.text and error_count < 10:
        print(response.text)
        print(f'Trying Again: {errors_allowed - error_count} attempts left before skipping')
        error_count += 1
        time.sleep(DELAY)
        get_data(url, df, error_count=error_count)
    else:
        df = pd.concat([df, pd.read_csv(StringIO(response.text), sep=',')])
        time.sleep(DELAY)
    return df


def get_jobs():
    table_name = 'api_job'
    icao_strings = stringify_icao_list(get_icao_list())
    df = pd.DataFrame()
    count = 1
    for i in icao_strings:
        print(f'Gathering data: {int(round(count * 100 / 30, 0))}%')
        url = f'https://server.fseconomy.net/data?userkey={FSE_KEY}' \
              f'&format=csv&query=icao&search=jobsfrom&icaos={i}'
        df = get_data(url, df)
        count += 1

    print('Grouping data...')
    try:
        assignments = df.groupby(['FromIcao', 'ToIcao', 'UnitType', 'Type'], as_index=False).agg(
            {'Amount': 'sum', 'Pay': 'sum'})
        assignments = assignments[['FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay']]
        print('Calculating distance...')
        assignments['Distance'] = assignments.apply(lambda x: get_distance(x['ToIcao'], x['FromIcao']), axis=1)
        print('Writing to database...')
    except KeyError:
        print('Error: could not retrieve data')
        return
    try:
        assignments = assignments.loc[:, ~assignments.columns.str.contains('^Unnamed')]
    except KeyError:
        pass
    assignments.to_sql('api_job', con, if_exists='replace', index=False)
    print('Finding return passengers...')
    helper = pd.read_sql_query('SELECT * FROM api_job', con)
    helper['ReturnPax'] = helper.apply(lambda row: get_return_pax(row['FromIcao'], row['ToIcao']), axis=1)
    helper.to_sql(table_name, con, if_exists='replace', index=True)
    print('Finished getting data!')


def get_aircraft_rentals(aircraft_list):
    table_name = "api_aircraftrental"
    df = pd.DataFrame()
    for aircraft in aircraft_list:
        url = f'https://server.fseconomy.net/data?userkey={FSE_KEY}' \
              f'&format=csv&query=aircraft&search=makemodel&makemodel={aircraft.replace(" ", "%20")}'
        print(f'Gathering aircraft data for {aircraft}...')
        df = get_data(url, df)
        time.sleep(DELAY)

    df = df[(df['RentalDry'] > 0) | (df['RentalWet'] > 0)]
    try:
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    except KeyError:
        pass
    df.to_sql(table_name, con, if_exists='replace', index=True)


def create_jobs_by_aircraft():
    create_query = """
        CREATE TABLE api_aircraftjob AS 
        SELECT * FROM api_job 
        LEFT JOIN api_aircraftrental 
        ON api_job.FromIcao = api_aircraftrental.Location 
        WHERE ReturnPax > 0 and MakeModel IS NOT NULL
        """
    delete_query = "DROP TABLE api_aircraftjob"
    print('Deleting aircraftjob db')
    try:
        cur.execute(delete_query)
    except:
        print('Could not delete. Skipping')
    print('Creating aircraftjob db')
    try:
        cur.execute(create_query)
        print('aircraftjob db created')
    except:
        print("Could not create db. Skipping")


if __name__ == '__main__':
    create_dbs()
    AVAILABLE_AIRCRAFT = get_aircraft_list()
    get_aircraft_rentals(AVAILABLE_AIRCRAFT)
    create_jobs_by_aircraft()
    get_jobs()
    con.close()
