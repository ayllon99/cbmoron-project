import psycopg2
import pandas as pd
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
######################
conn = psycopg2.connect(
    host=os.getenv('PG_HOST'),
    database=os.getenv('PG_DATABASE_NAME'),
    user=os.getenv('PG_USER_NAME'),
    password=os.getenv('PG_DATABASE_PASSWORD'),
    port=os.getenv('PG_PORT')
)
cur=conn.cursor()
cur.execute('SELECT match_id FROM public.shooting_chart_availability WHERE availability=true')
match_ids=pd.DataFrame(cur.fetchall())[0].tolist()


client=MongoClient(host=os.getenv('MONGO_HOST'),
                   port=int(os.getenv('MONGO_PORT')))
db=client.shootings_json
collection=db.CBM


headers={'Host': 'intrafeb.feb.es',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImQzOWE5MzlhZTQyZmFlMTM5NWJjODNmYjcwZjc1ZDc3IiwidHlwIjoiSldUIn0.eyJuYmYiOjE3MTg1NDYyNjksImV4cCI6MTcxODYzMjY2OSwiaXNzIjoiaHR0cHM6Ly9pbnRyYWZlYi5mZWIuZXMvaWRlbnRpdHkuYXBpIiwiYXVkIjpbImh0dHBzOi8vaW50cmFmZWIuZmViLmVzL2lkZW50aXR5LmFwaS9yZXNvdXJjZXMiLCJsaXZlc3RhdHMuYXBpIl0sImNsaWVudF9pZCI6ImJhbG9uY2VzdG9lbnZpdm9hcHAiLCJpZGFtYml0byI6IjEiLCJyb2xlIjpbIk92ZXJWaWV3IiwiVGVhbVN0YXRzIiwiU2hvdENoYXJ0IiwiUmFua2luZyIsIktleUZhY3RzIiwiQm94U2NvcmUiXSwic2NvcGUiOlsibGl2ZXN0YXRzLmFwaSJdfQ.GgvDkRih-hELUQVzXn3muglOOlaX77RinvZZL1PYqEK_mgEMSzMdF4WyGH9rEh2tVlPNjozaDQkXfBB6v_KgmFSb5L56qaRj_pqbuYlmqpr7cgvER_YX9bozNF_jTr96sb2KxlR8zAb55CZeItTuwkNRfnabSErf4d9TQsgE2C67ae9ZEsH35aSqgus3Cjnew0W8e7lizxH9RrBmLfrD0_AP3vwypzk3_8z69xq0g7vCutumFmKWrIsstDIjXR8_2sfnVKzZfkHdUYUov0M0TrpQYfOl8_bm0VpaQDFxrQFXNgvTLqBnCFpGTm4hj7_Kw_ZKrPXLRH4zWdtNnMrmtQ',
    'Origin': 'https://baloncestoenvivo.feb.es',
    'Connection': 'keep-alive',
    'Referer': 'https://baloncestoenvivo.feb.es/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'}


ids_done=[]
for match in collection.find():
    di=list(match.keys())[1]
    #print(di)
    ids_done.append(int(di))

len(match_ids)
len(ids_done)
match_ids=list(set(match_ids)-set(ids_done))
len(match_ids)

for match_id in match_ids:
    try:
        response=requests.get(f'https://intrafeb.feb.es/LiveStats.API/api/v1/ShotChart/{match_id}?_=1718555921778',headers=headers)
        print(response,match_id)
        if response.status_code==200:
            file=response.json()
            tomongo={f'{match_id}':file['SHOTCHART']['SHOTS']}
            collection.insert_one(tomongo)
        else:
            with open('shootings_time_errors.txt','a') as file:
                file.write(f'Status error in {match_id}\n')
        #time.sleep(1)
    except Exception as e:
        print(f'Error in match_id={match_id} response={response} error={type(e)}')
        with open('shootings_time_errors.txt','a') as file:
            file.write(f'Error in match_id={match_id} response={response} error={type(e)}\n')

cur.close()
conn.close()
client.close()





