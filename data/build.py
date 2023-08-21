# When running on pythonanywhere, sys path will need to be added to be able to import scripts
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
from api.scripts import get_icao_list, get_distance, stringify_icao_list, get_return_pax

load_dotenv('../api/.env')
FSE_KEY = os.getenv('FSE_KEY')
con = sql.connect('../db.sqlite3', check_same_thread=False)
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
    helper.to_sql('api_job', con, if_exists='replace', index=True)
    print('Finished getting data!')


def get_aircraft_rentals():
    aircrafts = ['Beechcraft 18', 'Beechcraft King Air 350' 'Cessna Citation CJ4 (MSFS)', 'Cessna 208 Caravan',
                 'Cessna 414A Chancellor', 'DeHavilland DHC-6 Twin Otter', 'Douglas DC-6B (PMDG)',
                 'Socata TBM 930 (MSFS)']
    headers = {}
    payload = {}
    df = pd.DataFrame()
    for aircraft in aircrafts:
        url = f'https://server.fseconomy.net/data?userkey={FSE_KEY}' \
              f'&format=csv&query=aircraft&search=makemodel&makemodel={aircraft}'
        print(f'Gathering aircraft data for {aircraft}...')
        response = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(60)
        if '<Error>' in response.text:
            print(f'{response.status_code}: {response.text}')
            pass
        else:
            df = pd.concat([df, pd.read_csv(StringIO(response.text), sep=',')])
        time.sleep(6)
    df.drop(df[(df['RentalDry'] == 0) & (df['RentalWet'] == 0)].index, inplace=True)
    try:
        df.drop(["Unnamed: 24"])
    except KeyError:
        pass
    df.to_sql('api_aircraft_rentals', con, if_exists='replace', index=False)


if __name__ == '__main__':
    create_dbs()
    get_aircraft_rentals()
    get_jobs()
