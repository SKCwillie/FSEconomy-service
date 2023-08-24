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
con = sql.connect(db_path, check_same_thread=False)
cur = con.cursor()


def create_dbs():
    file_names = [file for file in listdir('.') if file.endswith('.csv')]
    for file_name in file_names:
        table_name = f"api_{file_name.split('.')[0]}"
        df = pd.read_csv(f'./{file_name}')
        df.to_sql(table_name, con, if_exists='replace', index=False)
    print('Successfully built starting dbs')
    pass


def get_jobs():
    table_name = 'api_job'
    icao_strings = stringify_icao_list(get_icao_list())
    df = pd.DataFrame()
    headers = {}
    payload = {}
    count = 0
    for i in icao_strings:
        url = f'https://server.fseconomy.net/data?userkey={FSE_KEY}' \
              f'&format=csv&query=icao&search=jobsfrom&icaos={i}'
        response = requests.request("GET", url, headers=headers, data=payload)
        count += 1
        print(f'Gathering data: {round(count * 100 / 30, 0)}%')
        time.sleep(60)
        if '<Error>' in response.text:
            print(f'{response.status_code}: {response.text}')
            pass
        else:
            df = pd.concat([df, pd.read_csv(StringIO(response.text), sep=',')])

    print('Grouping data...')
    assignments = df.groupby(['FromIcao', 'ToIcao', 'UnitType', 'Type'], as_index=False).agg(
        {'Amount': 'sum', 'Pay': 'sum'})
    assignments = assignments[['FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay']]
    print('Calculating distance...')
    assignments['Distance'] = assignments.apply(lambda x: get_distance(x['ToIcao'], x['FromIcao']), axis=1)
    print('Writing to database...')
    assignments.to_sql('api_job', con, if_exists='replace', index=True)
    print('Finding return passengers...')
    helper = pd.read_sql_query('SELECT * FROM api_job', con)
    helper['ReturnPax'] = helper.apply(lambda row: get_return_pax(row['FromIcao'], row['ToIcao']), axis=1)
    helper.to_sql(table_name, con, if_exists='replace', index=True)
    print('Finished getting data!')


def get_aircraft_rentals():
    aircrafts = ['Beechcraft 18', 'Beechcraft King Air 350', 'Cessna Citation CJ4 (MSFS)', 'Cessna 208 Caravan',
                 'Cessna 414A Chancellor', 'DeHavilland DHC-6 Twin Otter', 'Douglas DC-6B (PMDG)',
                 'Socata TBM 930 (MSFS)']
    table_name = "api_aircraftrental"
    headers = {}
    payload = {}
    df = pd.DataFrame()
    for aircraft in aircrafts:
        url = f'https://server.fseconomy.net/data?userkey={FSE_KEY}' \
              f'&format=csv&query=aircraft&search=makemodel&makemodel={aircraft.replace(" ", "%20")}'
        print(f'Gathering aircraft data for {aircraft}...')
        time.sleep(60)
        response = requests.request("GET", url, headers=headers, data=payload)
        if '<Error>' in response.text:
            print(f'{response.status_code}: {response.text}')
            pass
        else:
            df = pd.concat([df, pd.read_csv(StringIO(response.text), sep=',')])
    df = df[(df['RentalDry'] > 0) | (df['RentalWet'] > 0)]
    try:
        df.drop(["Unnamed: 24"])
    except KeyError:
        pass
    df.to_sql(table_name, con, if_exists='replace', index=False)


def create_jobs_by_aircraft():
    create_query = """
        CREATE TABLE api_aircraftjob AS 
        SELECT * FROM api_job 
        LEFT JOIN api_aircraftrental 
        ON api_job.FromIcao = api_aircraftrental.Location 
        WHERE ReturnPax > 0 and MakeModel IS NOT NULL
        """
    delete_query = "DELETE FROM api_aircraftjob"
    insert_query = """
        INSERT INTO api_aircraftjob
        SELECT * FROM api_job
        LEFT JOIN api_aircraftrental
        ON api_job.FromIcao = api_aircraftrental.Location
        WHERE ReturnPax > 0 and MakeModel IS NOT NULL
        """
    try:
        cur.execute(create_query)
    except sqlite3.OperationalError:
        cur.execute(delete_query)
        cur.execute(insert_query)
    con.commit()


if __name__ == '__main__':
    create_dbs()
    get_jobs()
    get_aircraft_rentals()
    create_jobs_by_aircraft()
    con.close()
