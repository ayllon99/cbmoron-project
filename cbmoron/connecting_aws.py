import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()
######################
conn = psycopg2.connect(
    host='database-1.cli64meq2e42.us-east-1.rds.amazonaws.com',
    database='initial_database',
    user='postgres',
    password='CBMproject.123',
    port=5432
)
cur=conn.cursor()
cur.execute("SELECT * FROM mytable")
df=pd.DataFrame(cur.fetchall())

with open('cbmoron_dumping.sql','r',encoding='utf-8') as f:
    file=f.read()

cur.execute("INSERT INTO mytable (name, email) VALUES ('John Doe', 'john@example.com');")
