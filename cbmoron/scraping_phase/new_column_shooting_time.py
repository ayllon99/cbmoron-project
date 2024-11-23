import psycopg2
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime


def to_database(identifier,time_shoot):
    try:
        cur.execute(f"""INSERT INTO temporal_new_time_column (identifier,time)
                VALUES ({identifier},'{time_shoot}');""")
        cur.execute('COMMIT')
    except:
            cur.execute("ROLLBACK")
            print(f'Error inserting into database in identifier={identifier}, time_shoot={time_shoot}')
            with open('new_column_time.txt','a') as file:
                file.write(f'Error inserting into database in identifier={identifier}, time_shoot={time_shoot}\n')


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
cur.execute('SELECT identifier,match_id,number,success,quarter,left_left,top_top FROM public.shootings WHERE shoot_time IS NULL')
shootings_df=pd.DataFrame(cur.fetchall())
shootings_df.columns=['identifier','match_id','number','success','quarter','left_left','top_top']

client=MongoClient(host=os.getenv('MONGO_HOST'),
                   port=int(os.getenv('MONGO_PORT')))
db=client.shootings_json
collection=db.CBM

cur.execute('SELECT identifier FROM public.temporal_new_time_column')
identifiers_done=pd.DataFrame(cur.fetchall())[0].tolist()
len(identifiers_done)
shootings_ids=shootings_df['identifier'].tolist()
len(shootings_ids)

tobe_done=list(set(shootings_ids)-set(identifiers_done))
len(tobe_done)

for id in tobe_done:
    identifier=id
    match_id=shootings_df[shootings_df['identifier']==identifier]['match_id'].tolist()[0]
    number=shootings_df[shootings_df['identifier']==identifier]['number'].tolist()[0]
    success=1 if shootings_df[shootings_df['identifier']==identifier]['success'].tolist()[0]==True else 0
    quarter=shootings_df[shootings_df['identifier']==identifier]['quarter'].tolist()[0]
    left_left=shootings_df[shootings_df['identifier']==identifier]['left_left'].tolist()[0]
    top_top=shootings_df[shootings_df['identifier']==identifier]['top_top'].tolist()[0]

    result = collection.find_one({ f'{match_id}': { '$exists': 'true' } })

    time_list=[a['t'] for a in result[f'{match_id}'] if a['player']==f'{number}'and a['m']==f'{success}' and a['quarter']==f'{quarter}' and round(float(a['y']),2)==round(top_top,2) and (round(float(a['x']),2)==round(left_left,2) or round(float(a['x']),2)==round(100-left_left,2))]
    
    if len(time_list)==1 and len(time_list[0].split(':'))==2:
        time_shoot=datetime.strptime(time_list[0],"%M:%S").time()
        to_database(identifier,time_shoot)
    elif len(time_list)==1 and len(time_list[0].split(':'))==3:
        min_sec=time_list[0].split(':')[1:]
        time_shoot=datetime.strptime(f'{min_sec[0]}:{min_sec[1]}',"%M:%S").time()
        to_database(identifier,time_shoot)
    elif len(time_list)==0:
         print(f'No shoot found in identifier={identifier}')
         with open('new_column_time.txt','a') as file:
            file.write(f'No shoot found in identifier={identifier}\n')
    elif len(time_list)==2 and time_list[0]==time_list[1]:
        time_shoot=datetime.strptime(time_list[0],"%M:%S").time()
        to_database(identifier,time_shoot)
    elif len(time_list)==3 and time_list[0]==time_list[1]==time_list[2]:
        time_shoot=datetime.strptime(time_list[0],"%M:%S").time()
        to_database(identifier,time_shoot)
    else:
        print(f'More than 1 unique shoots matches ={len(time_list)}')
        with open('new_column_time.txt','a') as file:
            file.write(f'More than 1 different shoot matches={len(time_list)} in identifier={identifier}\n')

