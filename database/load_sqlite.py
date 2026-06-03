import sqlite3
import pandas as pd

def load_to_sqlite(df, db_path, table_name):
    conn = sqlite3.connect(db_path)

    df.to_sql(
        table_name,
        conn,
        if_exists='replace',
        index=False
        )
    conn.close()