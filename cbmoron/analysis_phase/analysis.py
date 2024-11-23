from dotenv import load_dotenv
import os
from scraping_phase.pipeline import PostgreSQLConnection,DataPipeline
import pandas as pd

load_dotenv()
conn = PostgreSQLConnection(os.getenv('PG_HOST'), os.getenv('PG_DATABASE_NAME'), os.getenv('PG_USER_NAME'), os.getenv('PG_DATABASE_PASSWORD'))
conn.connect()


def get_players_stats_career(player_id=None):
    global conn
    with open('analysis_phase/players_stats_career.sql','r') as f:
        file=f.read()

    query=file.format(player_id)

    pipeline=DataPipeline(conn,'')
    df=pd.DataFrame(pipeline.query(query))
    cols=list(range(48))
    colss=['year', 'player_id', 'season', 'team_name', 'n_matches', 'total_mins', 6, 'pts_total', 'pts_avg', 'twos_in', 'twos_tried', 'twos_perc', 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,47]

    df.columns=colss
    dff=df[['year', 'player_id', 'season', 'team_name', 'n_matches', 'total_mins', 'pts_total', 'pts_avg', 'twos_in', 'twos_tried', 'twos_perc']]

    return dff


def get_players_path(player_id=None):
    global conn
    with open('analysis_phase/players_path.sql','r') as f:
        file=f.read()

    query=file.format(player_id,player_id)
    pipeline=DataPipeline(conn,'')
    df=pd.DataFrame(pipeline.query(query))
    df.columns=['Temporada','Categoría','Equipo','Nº de partidos']
    df['Nº de partidos']=df['Nº de partidos'].astype(int)
    return df


def get_player_info(player_id=None):
    global conn
    with open('analysis_phase/player_info.sql','r') as f:
        file=f.read()
    query=file.format(player_id)
    pipeline=DataPipeline(conn,'')
    df=pd.DataFrame(pipeline.query(query))
    df.columns=['player_id','player_name','position','height','weight','birthday','nationality','player_link']
    return df


def get_shooting_info(player_id):
    global conn
    with open('analysis_phase/years_of_shooting_data.sql','r') as f:
        file=f.read()
    query=file.format(player_id)
    pipeline=DataPipeline(conn,'')
    df=pd.DataFrame(pipeline.query(query))
    df.columns=['n_years']
    years=[int(year) for year in df['n_years']]
    with open('analysis_phase/shooting_query.sql','r') as f:
        file=f.read()
    query2=file.format(player_id)
    pipeline=DataPipeline(conn,'')
    df=pd.DataFrame(pipeline.query(query2))
    df.columns=['year','identifier','player_id','match_id','success','quarter','shoot_time','top_top','left_left','shooting_type','date']
    dic_stats=getting_percentages(years,df)
    return dic_stats



def getting_percentages(years,df):
    stats={}
    n_images=len(years)
    i=0
    while i<n_images:
        if i<3:
            stats[f'{years[i]}']={}
            stats[f'{years[i]}']['Zone']={'in':0,'tried':0}
            stats[f'{years[i]}']['right_corner_three']={'in':0,'tried':0}
            stats[f'{years[i]}']['right_corner_middle']={'in':0,'tried':0}
            stats[f'{years[i]}']['right_side_three']={'in':0,'tried':0}
            stats[f'{years[i]}']['right_side_middle']={'in':0,'tried':0}
            stats[f'{years[i]}']['front_three']={'in':0,'tried':0}
            stats[f'{years[i]}']['front_middle']={'in':0,'tried':0}
            stats[f'{years[i]}']['left_side_three']={'in':0,'tried':0}
            stats[f'{years[i]}']['left_side_middle']={'in':0,'tried':0}
            stats[f'{years[i]}']['left_corner_three']={'in':0,'tried':0}
            stats[f'{years[i]}']['left_corner_middle']={'in':0,'tried':0}

            dff=df[df['year']==years[i]].reset_index(drop=True)
            for a in range(len(dff)):
                top_top=dff.loc[a].top_top
                left_left=dff.loc[a].left_left
                shooting_type=dff.loc[a].shooting_type
                success=dff.loc[a].success
                if shooting_type == 'Zone' and success == True:
                    stats[f'{years[i]}']['Zone']['in']+=1
                    stats[f'{years[i]}']['Zone']['tried']+=1
                elif shooting_type == 'Zone' and success == False:
                    stats[f'{years[i]}']['Zone']['tried']+=1
                elif shooting_type == 'Middle':
                    if top_top>10 and top_top<38 and left_left<10 and success == True:
                        stats[f'{years[i]}']['left_corner_middle']['in']+=1
                        stats[f'{years[i]}']['left_corner_middle']['tried']+=1
                    elif top_top>10 and top_top<38 and left_left<10 and success == False:
                        stats[f'{years[i]}']['left_corner_middle']['tried']+=1
                    elif top_top>62 and top_top<90 and left_left<10 and success == True:
                        stats[f'{years[i]}']['right_corner_middle']['in']+=1
                        stats[f'{years[i]}']['right_corner_middle']['tried']+=1
                    elif top_top>62 and top_top<90 and left_left<10 and success == False:
                        stats[f'{years[i]}']['right_corner_middle']['tried']+=1
                    elif top_top>38 and top_top<62 and success == True:
                        stats[f'{years[i]}']['front_middle']['in']+=1
                        stats[f'{years[i]}']['front_middle']['tried']+=1
                    elif top_top>38 and top_top<62 and success == False:
                        stats[f'{years[i]}']['front_middle']['tried']+=1
                    elif top_top<50 and success == True:
                        stats[f'{years[i]}']['left_side_middle']['in']+=1
                        stats[f'{years[i]}']['left_side_middle']['tried']+=1
                    elif top_top<50 and success == False:
                        stats[f'{years[i]}']['left_side_middle']['tried']+=1
                    elif top_top>50 and success == True:
                        stats[f'{years[i]}']['right_side_middle']['in']+=1
                        stats[f'{years[i]}']['right_side_middle']['tried']+=1
                    elif top_top>50 and success == False:
                        stats[f'{years[i]}']['right_side_middle']['tried']+=1
                elif shooting_type == 'Three':
                    if top_top>90 and left_left<10 and success == True:
                        stats[f'{years[i]}']['right_corner_three']['in']+=1
                        stats[f'{years[i]}']['right_corner_three']['tried']+=1
                    elif top_top>90 and left_left<10 and success == False:
                        stats[f'{years[i]}']['right_corner_three']['tried']+=1
                    elif top_top>90 and left_left<10 and success == True:
                        stats[f'{years[i]}']['left_corner_three']['in']+=1
                        stats[f'{years[i]}']['left_corner_three']['tried']+=1
                    elif top_top>90 and left_left<10 and success == False:
                        stats[f'{years[i]}']['left_corner_three']['tried']+=1
                    elif top_top>38 and top_top<62 and success == True:
                        stats[f'{years[i]}']['front_three']['in']+=1
                        stats[f'{years[i]}']['front_three']['tried']+=1
                    elif top_top>38 and top_top<62 and success == False:
                        stats[f'{years[i]}']['front_three']['tried']+=1
                    elif top_top<50 and success == True:
                        stats[f'{years[i]}']['left_side_three']['in']+=1
                        stats[f'{years[i]}']['left_side_three']['tried']+=1
                    elif top_top<50 and success == False:
                        stats[f'{years[i]}']['left_side_three']['tried']+=1
                    elif top_top>50 and success == True:
                        stats[f'{years[i]}']['right_side_three']['in']+=1
                        stats[f'{years[i]}']['right_side_three']['tried']+=1
                    elif top_top>50 and success == False:
                        stats[f'{years[i]}']['right_side_three']['tried']+=1
        i+=1
    return stats



