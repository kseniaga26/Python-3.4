import pandas as pd
import sqlite3

def get_sql_from_csv(file_name: str) -> None:
    data = pd.read_csv(file_name)
    conn_db = sqlite3.connect('currencies_db')
    c = conn_db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS currencies (date text, RUR number, USD number, KZT number, BYR number,'
              'UAH number, EUR number)')
    conn_db.commit()
    data.to_sql('currencies', conn_db, if_exists='replace', index=False)

get_sql_from_csv('dataframe51.csv')