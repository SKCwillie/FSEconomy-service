import sqlite3
from os import listdir
import pandas as pd


def create_dbs():
    file_names = [file for file in listdir('.') if file.endswith('.csv')]
    con = sqlite3.connect("../db.sqlite3")
    for file_name in file_names:
        table_name = f"api_{file_name.split('.')[0]}"
        df = pd.read_csv(f'./{file_name}')
        df.to_sql(table_name, con, if_exists='replace', index=False)
    con.close()
    pass


create_dbs()
