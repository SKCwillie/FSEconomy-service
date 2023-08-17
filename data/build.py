import sqlite3
from os import listdir
import pandas as pd
from api.scripts import *
import datetime
import time
from dotenv import load_dotenv

load_dotenv('../api/.env')
FSE_KEY=os.getenv('FSE_KEY')

def create_dbs():
    file_names = [file for file in listdir('.') if file.endswith('.csv')]
    con = sqlite3.connect("../db.sqlite3")
    for file_name in file_names:
        table_name = f"api_{file_name.split('.')[0]}"
        df = pd.read_csv(f'./{file_name}')
        df.to_sql(table_name, con, if_exists='replace', index=False)
    con.close()
    pass


def get_assignments():
    icao_strings = stringify_icao_list(get_icao_list())
    df = pd.DataFrame()
    headers = {}
    payload = {}
    for i in icao_strings:
        url = f'https://server.fseconomy.net/data?userkey={FSE_KEY}' \
              f'&format=csv&query=icao&search=jobsfrom&icaos={i}'
        print(datetime.datetime.now().strftime('%H:%M:%S'))
        response = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(60)
        if '<Error>' in response.text:
            print(f'{response.status_code}: {response.text}')
            pass
        else:
            df = pd.concat([df, pd.read_csv(StringIO(response.text), sep=',')])

    assignments = df.groupby(['FromIcao', 'ToIcao', 'UnitType', 'Type'], as_index=False).agg(
        {'Amount': 'sum', 'Pay': 'sum'})
    assignments = assignments[['FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay']]
    assignments['Distance'] = assignments.apply(lambda x: get_distance(x['ToIcao'], x['FromIcao']), axis=1)
    assignments = assignments.sort_values(by=['Pay'], ascending=False)
    assignments.to_sql('api_assignments', con, if_exists='replace', index=True)


if __name__ == '__main__':
    # create_dbs()
    get_assignments()
