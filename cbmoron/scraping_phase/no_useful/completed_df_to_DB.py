import psycopg2
import pandas as pd
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


def to_database_teams(team_id,team_name,a):
    try:
        cur.execute(f"""INSERT INTO teams (team_id,team_name)
                VALUES ({team_id},'{team_name}');""")
    except:
            cur.execute("ROLLBACK")
            print(f'Error row={a} team_id={team_id}, team_name={team_name}')


def to_database_stages(stage_id,stage_name,year,a):
    try:
        cur.execute(f"""INSERT INTO stages (stage_id,stage_name,year)
                VALUES ({stage_id},'{stage_name}',{year});""")
    except:
            cur.execute("ROLLBACK")
            print(f'Error row={a} stage_id={stage_id}, stage_name={stage_name}, year={year}')


def to_database_results(match_id,home_team_id,away_team_id,stage_id,matchday,home_score,away_score,date,match_link,time,category,a):
    try:
        cur.execute(f"""INSERT INTO results (match_id,home_team_id,away_team_id,stage_id,matchday,home_score,away_score,date,match_link,time,category)
                VALUES ({match_id},{home_team_id},{away_team_id},{stage_id},{matchday},{home_score},{away_score},'{date}','{match_link}','{time}','{category}');""")
    except:
            cur.execute("ROLLBACK")
            print(f'Error row={a} match_id={match_id}')
    

#Insert teams dataframe into database
df=pd.read_pickle('scraping_phase/teams_eba.pkl')
for a in range(len(df)):
    team_id=df.loc[a].team_id
    team_name=df.loc[a].team_name.strip()
    to_database_teams(team_id,team_name,a)


#Insert stages dataframe into database
dff=pd.read_pickle('scraping_phase/stages_eba.pkl')
for a in range(len(dff)):
    stage_id=dff.loc[a].stage_id
    stage_name=dff.loc[a].stage_name.strip()
    year=dff.loc[a].year
    to_database_stages(stage_id,stage_name,year,a)


#Insert results dataframe into database
data=pd.read_pickle('scraping_phase/results_eba.pkl')
for a in range(len(data)):
    match_id=data.loc[a].match_id
    home_team_id=data.loc[a].home_team_id
    away_team_id=data.loc[a].away_team_id
    stage_id=data.loc[a].stage_id
    matchday=data.loc[a].matchday
    home_score=data.loc[a].home_score
    away_score=data.loc[a].away_score
    date=data.loc[a].date
    time=data.loc[a].time
    match_link=data.loc[a].match_link
    category=data.loc[a].category
    to_database_results(match_id,home_team_id,away_team_id,stage_id,matchday,home_score,away_score,date,match_link,time,category,a)
