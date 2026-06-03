import sqlite3
import pandas as pd

conn = sqlite3.connect("database/health_data.db")

query = "SELECT * FROM pacientes LIMIT 5;"

df = pd.read_sql_query(query, conn)

print(df)

conn.close()