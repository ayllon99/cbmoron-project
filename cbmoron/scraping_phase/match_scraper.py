import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
from datetime import datetime
from scraping_phase.pipeline import PostgreSQLConnection,DataPipeline
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def partials_scraper(soup,match_id): #return df
    home_partials=[ a.text for a in soup.find('div',{'class':'fila parciales'}).find('div',{'class':'columna equipo local'}).find_all('span')]
    away_partials=[ a.text for a in soup.find('div',{'class':'fila parciales'}).find('div',{'class':'columna equipo visitante'}).find_all('span')]
    df=pd.DataFrame({'match_id':match_id,'q1_home':[home_partials[0]],'q2_home':[home_partials[1]],'q3_home':[home_partials[2]],'q4_home':[home_partials[3]],'q1_away':[away_partials[0]],'q2_away':[away_partials[1]],'q3_away':[away_partials[2]],'q4_away':[away_partials[3]],})
    return df


def dictionary_team_names(soup): #return teams_dict
    teams_dict={}

    home_team_link=soup.find('div',{'class':'box-marcador tableLayout de tres columnas'}).find('div',{'class':'columna equipo local'}).find('span',{'class':'nombre'}).find('a').get('href')
    home_team_id=home_team_link.split('=')[1]
    home_team_name=soup.find('div',{'class':'box-marcador tableLayout de tres columnas'}).find('div',{'class':'columna equipo local'}).find('span',{'class':'nombre'}).find('a').text.strip()
    teams_dict[home_team_id]={'team_name':home_team_name,'home_away':'Home'}
    
    away_team_link=soup.find('div',{'class':'box-marcador tableLayout de tres columnas'}).find('div',{'class':'columna equipo visitante'}).find('span',{'class':'nombre'}).find('a').get('href')
    away_team_id=away_team_link.split('=')[1]
    away_team_name=soup.find('div',{'class':'box-marcador tableLayout de tres columnas'}).find('div',{'class':'columna equipo visitante'}).find('span',{'class':'nombre'}).find('a').text.strip()
    teams_dict[away_team_id]={'team_name':away_team_name,'home_away':'Away'}

    return teams_dict


def table_scraper(teams_dict,rows,match_id,home_away): #return df and players_dict
    players_dict={'Home':{},'Away':{}}
    match_ids=[]
    team_ids=[]
    team_names=[]
    vs_team_ids=[]
    vs_team_names=[]
    home_aways=[]
    player_ids=[]
    player_links=[]
    startings=[]
    numbers=[]
    player_names=[]
    mins=[]
    points=[]
    twos=[]
    twos_in=[]
    twos_tried=[]
    twos_perc=[]
    threes=[]
    threes_in=[]
    threes_tried=[]
    threes_perc=[]
    field_goals=[]
    field_goals_in=[]
    field_goals_tried=[]
    field_goals_perc=[]
    free_throws=[]
    free_throws_in=[]
    free_throws_tried=[]
    free_throws_perc=[]
    offensive_rebounds=[]
    deffensive_rebounds=[]
    total_rebounds=[]
    assists=[]
    steals=[]
    turnovers=[]
    blocks_favor=[]
    blocks_against=[]
    dunks=[]
    personal_fouls=[]
    fouls_received=[]
    efficiencies=[]
    balances=[]

    for row in rows[:-1]:
        try:
            tds=row.find_all('td')
            starting=True if tds[0].text=='*' else False
            number=int(tds[1].text)
            player_name=tds[2].text.strip()
            player_data_link=[a.replace('&c','').replace('&med','') for a in tds[2].find('a').get('href').split('=')]
            team_id= int([a for a,b in teams_dict.items() if teams_dict[a]['home_away']==home_away][0])
            team_name=teams_dict[f'{team_id}']['team_name']
            vs_team_id=int([a for a,b in teams_dict.items() if teams_dict[a]['home_away']!=home_away][0])
            vs_team_name=teams_dict[f'{vs_team_id}']['team_name']
            player_id=int(player_data_link[2])
            player_link=f'https://baloncestoenvivo.feb.es/jugador/{team_id}/{player_id}'
            players_dict[teams_dict[f'{team_id}']['home_away']][number]={'player_id':player_id,'player_name':player_name}
            try:
                min=datetime.strptime(tds[3].text, '%M:%S').time()
            except:
                min=datetime.strptime('00:00', '%M:%S').time()
            point=int(tds[4].text)
            two=tds[5].text.split(' ')[0]
            two_in=int(two.split('/')[0])
            two_tried=int(two.split('/')[1])
            two_perc=round(float(tds[5].text.split(' ')[1].replace(',','.').replace('%','')),2)
            three=tds[6].text.split(' ')[0]
            three_in=int(three.split('/')[0])
            three_tried=int(three.split('/')[1])
            three_perc=round(float(tds[6].text.split(' ')[1].replace(',','.').replace('%','')),2)
            field_goal=tds[7].text.split(' ')[0]
            field_goal_in=int(field_goal.split('/')[0])
            field_goal_tried=int(field_goal.split('/')[1])
            field_goal_perc=round(float(tds[7].text.split(' ')[1].replace(',','.').replace('%','')),2)
            free_throw=tds[8].text.split(' ')[0]
            free_throw_in=int(free_throw.split('/')[0])
            free_throw_tried=int(free_throw.split('/')[1])
            free_throw_perc=round(float(tds[8].text.split(' ')[1].replace(',','.').replace('%','')),2)
            offensive_rebound=int(tds[9].text)
            deffensive_rebound=int(tds[10].text)
            total_rebound=offensive_rebound+deffensive_rebound
            assist=int(tds[12].text)
            steal=int(tds[13].text)
            turnover=int(tds[14].text)
            block_favor=int(tds[15].text)
            block_against=int(tds[16].text)
            dunk=int(tds[17].text)
            personal_foul=int(tds[18].text)
            foul_received=int(tds[19].text)
            efficiency=int(tds[20].text)
            balance=int(tds[21].text)

            match_ids.append(int(match_id))
            team_ids.append(team_id)
            team_names.append(team_name)
            vs_team_ids.append(vs_team_id)
            vs_team_names.append(vs_team_name)
            home_aways.append(home_away)
            player_ids.append(player_id)
            player_links.append(player_link)
            startings.append(starting)
            numbers.append(number)
            player_names.append(player_name)
            mins.append(min)
            points.append(point)
            twos.append(two)
            twos_in.append(two_in)
            twos_tried.append(two_tried)
            twos_perc.append(two_perc)
            threes.append(three)
            threes_in.append(three_in)
            threes_tried.append(three_tried)
            threes_perc.append(three_perc)
            field_goals.append(field_goal)
            field_goals_in.append(field_goal_in)
            field_goals_tried.append(field_goal_tried)
            field_goals_perc.append(field_goal_perc)
            free_throws.append(free_throw)
            free_throws_in.append(free_throw_in)
            free_throws_tried.append(free_throw_tried)
            free_throws_perc.append(free_throw_perc)
            offensive_rebounds.append(offensive_rebound)
            deffensive_rebounds.append(deffensive_rebound)
            total_rebounds.append(total_rebound)
            assists.append(assist)
            steals.append(steal)
            turnovers.append(turnover)
            blocks_favor.append(block_favor)
            blocks_against.append(block_against)
            dunks.append(dunk)
            personal_fouls.append(personal_foul)
            fouls_received.append(foul_received)
            efficiencies.append(efficiency)
            balances.append(balance)
        except:
            pass
    df=pd.DataFrame({'match_id':match_ids,'team_id':team_ids,'vs_team_id':vs_team_ids,'player_id':player_ids,'player_link':player_links,'starting':startings,'number':numbers,'player_name':player_names,'minutes':mins,'points':points,'two_points_in':twos_in,'two_points_tried':twos_tried,'two_points_perc':twos_perc,'three_points_in':threes_in,'three_points_tried':threes_tried,'three_points_perc':threes_perc,'field_goals_in':field_goals_in,'field_goals_tried':field_goals_tried,'field_goals_perc':field_goals_perc,'free_throws_in':free_throws_in,'free_throws_tried':free_throws_tried,'free_throws_perc':free_throws_perc,'offensive_rebounds':offensive_rebounds,'deffensive_rebounds':deffensive_rebounds,'total_rebounds':total_rebounds,'assists':assists,'steals':steals,'turnovers':turnovers,'blocks_favor':blocks_favor,'blocks_against':blocks_against,'dunks':dunks,'personal_fouls':personal_fouls,'fouls_received':fouls_received,'efficiency':efficiencies,'balance':balances})
    return df, players_dict


def totals_scraper(teams_dict,rows,match_id,home_away): #return a 1 row df
    team_id= int([a for a,b in teams_dict.items() if teams_dict[a]['home_away']==home_away][0])
    vs_team_id=int([a for a,b in teams_dict.items() if teams_dict[a]['home_away']!=home_away][0])
    tds=rows[-1].find_all('td')
    try:
        min=tds[3].text.strip()
    except:
        min='0:00'
    point=int(tds[4].text)
    two=tds[5].text.split(' ')[0].strip()
    two_in=int(two.split('/')[0])
    two_tried=int(two.split('/')[1])
    two_perc=round(float(tds[5].text.split(' ')[1].replace(',','.').replace('%','')),2)
    three=tds[6].text.split(' ')[0].strip()
    three_in=int(three.split('/')[0])
    three_tried=int(three.split('/')[1])
    three_perc=round(float(tds[6].text.split(' ')[1].replace(',','.').replace('%','')),2)
    field_goal=tds[7].text.split(' ')[0].strip()
    field_goal_in=int(field_goal.split('/')[0])
    field_goal_tried=int(field_goal.split('/')[1])
    field_goal_perc=round(float(tds[7].text.split(' ')[1].replace(',','.').replace('%','')),2)
    free_throw=tds[8].text.split(' ')[0].strip()
    free_throw_in=int(free_throw.split('/')[0])
    free_throw_tried=int(free_throw.split('/')[1])
    free_throw_perc=round(float(tds[8].text.split(' ')[1].replace(',','.').replace('%','')),2)
    offensive_rebound=int(tds[9].text)
    deffensive_rebound=int(tds[10].text)
    total_rebound=offensive_rebound+deffensive_rebound
    assist=int(tds[12].text)
    steal=int(tds[13].text)
    turnover=int(tds[14].text)
    block_favor=int(tds[15].text)
    block_against=int(tds[16].text)
    dunk=int(tds[17].text)
    personal_foul=int(tds[18].text)
    foul_received=int(tds[19].text)
    efficiency=int(tds[20].text)
    df=pd.DataFrame({'match_id':[match_id],'team_id':[team_id],'vs_team_id':[vs_team_id],'minutes':[min],'points':[point],'two_points_in':[two_in],'two_points_tried':[two_tried],'two_points_perc':[two_perc],'three_points_in':[three_in],'three_points_tried':three_tried,'three_points_perc':[three_perc],'field_goals_in':[field_goal_in],'field_goals_tried':field_goal_tried,'field_goals_perc':[field_goal_perc],'free_throws_in':[free_throw_in],'free_throws_tried':free_throw_tried,'free_throws_perc':[free_throw_perc],'offensive_rebounds':[offensive_rebound],'deffensive_rebounds':[deffensive_rebound],'total_rebounds':[total_rebound],'assists':[assist],'steals':[steal],'turnovers':[turnover],'blocks_favor':[block_favor],'blocks_against':[block_against],'dunks':[dunk],'personal_fouls':[personal_foul],'fouls_received':[foul_received],'efficiency':[efficiency]})
    return df


def is_two_or_three(top_point,left_point): #return string
    proportion=647.39/361.89
    center_top=50
    center_left=10
    center_top_scaled=center_top/proportion
    top_point_scaled=top_point/proportion
    
    if (top_point>=11.8 and top_point<20) or (top_point>=80 and top_point<=88.2):
        radius=21.5
    elif (top_point>=20 and top_point<30) or (top_point>=70 and top_point<80):
        radius=20
    elif top_point>=30 and top_point<70:
        radius=19
    else:
        return 'three'
    d=np.sqrt(((top_point_scaled-center_top_scaled)**2)+((left_point-center_left)**2))
    if d>radius:
        return 'three'
    elif d<radius:
        return 'two'


def is_paint(top_point,left_point): #return boolean
    if top_point>38 and top_point<62 and left_point<20:
        return True
    else: 
        return False


def twos_middle_stats(id,dictionary): #return string: '2/4'
    try:
        middle_in= dictionary[(id,'Middle',True)]
    except:
        middle_in=0
    try:
        middle_out=dictionary[(id,'Middle',False)]
    except:
        middle_out=0
    total_middle=middle_in+middle_out
    stats=f'{middle_in}/{total_middle}'
    return stats


def twos_zone_stats(id,dictionary): #return string: '2/4'
    try:
        zone_in=dictionary[(id,'Zone',True)]
    except:
        zone_in=0
    try:
        zone_out=dictionary[(id,'Zone',False)]
    except:
        zone_out=0
    total_zone=zone_in+zone_out
    stats=f'{zone_in}/{total_zone}'
    return stats


def shooting_scraper(soup_shooting_chart,match_id,players_dict,teams_dict): #return df, dict_to_procces
    shoots=soup_shooting_chart.find('div',{'class':'court-shoots'}).find_all('div')

    match_ids=[match_id]*len(shoots)
    team_ids=[]
    team_names=[]
    vs_team_ids=[]
    vs_team_names=[]
    home_aways=[]
    numbers=[]
    player_ids=[]
    player_names=[]
    successes=[]
    quarters=[]
    tops=[]
    lefts=[]
    shootings_type=[]

    for shoot in shoots:
        home_away='Home' if shoot.get('class')[1]=='t0' else 'Away'
        team_id=int([id for id,dic in teams_dict.items() if dic['home_away']==home_away][0])
        team_name=teams_dict[f'{team_id}']['team_name']
        vs_team_id=int([id for id,dic in teams_dict.items() if dic['home_away']!=home_away][0])
        vs_team_name=teams_dict[f'{vs_team_id}']['team_name']
        number=int(shoot.get('class')[2].split('-')[1])
        player_id=players_dict[home_away][number]['player_id']
        player_name=players_dict[home_away][number]['player_name']
        success=True if shoot.get('class')[3]=='success1' else False
        if shoot.get('class')[4]=='q-1':
            quarter=1
        elif shoot.get('class')[4]=='q-2':
            quarter=2
        elif shoot.get('class')[4]=='q-3':
            quarter=3
        elif shoot.get('class')[4]=='q-4':
            quarter=4
        else:
            quarter=0

        position=shoot.get('style').split(';')
        top=float(position[0].split(':')[1].strip().replace('%',''))
        left=float(position[1].split(':')[1].strip().replace('%',''))
        if left>50:
            left=100-left
        two_or_three=is_two_or_three(top,left)
        if two_or_three=='three':
            shootings_type.append('Three')
        elif two_or_three=='two' and is_paint(top,left)==True:
            shootings_type.append('Zone')
        elif two_or_three=='two' and is_paint(top,left)==False:
                shootings_type.append('Middle')

        team_ids.append(team_id)
        team_names.append(team_name)
        vs_team_ids.append(vs_team_id)
        vs_team_names.append(vs_team_name)
        home_aways.append(home_away)
        numbers.append(number)
        player_ids.append(player_id)
        player_names.append(player_name)
        successes.append(success)
        quarters.append(quarter)
        tops.append(round(top,2))
        lefts.append(round(left,2))
    df=pd.DataFrame({'player_id':player_ids,'match_id':match_ids,'team_id':team_ids,'home_away':home_aways,'vs_team_id':vs_team_ids,'number':numbers,'player_name':player_names,'success':successes,'quarter':quarters,'top_top':tops,'left_left':lefts,'shooting_type':shootings_type})
    dict_to_process=df[df['shooting_type']!='Three'].groupby(['player_id','shooting_type'])['success'].value_counts().to_dict()
    
    return df,dict_to_process


def new_columns_players(table_df): #return table_df
    table_df['middle_shootings']=table_df['player_id'].apply(twos_middle_stats,dictionary=dict_to_process)
    table_df['middle_shootings_in']=table_df['middle_shootings'].apply(lambda x: int(x.split('/')[0]))
    table_df['middle_shootings_tried']=table_df['middle_shootings'].apply(lambda x: int(x.split('/')[1]))
    table_df['middle_shootings_perc']=table_df['middle_shootings'].apply(lambda x:round(float(int(x.split('/')[0])/int(x.split('/')[1])),2) if int(x.split('/')[1]) !=0 else float(0))

    table_df['zone_shootings']=table_df['player_id'].apply(twos_zone_stats,dictionary=dict_to_process)
    table_df['zone_shootings_in']=table_df['zone_shootings'].apply(lambda x: int(x.split('/')[0]))
    table_df['zone_shootings_tried']=table_df['zone_shootings'].apply(lambda x: int(x.split('/')[1]))
    table_df['zone_shootings_perc']=table_df['zone_shootings'].apply(lambda x:round(float(int(x.split('/')[0])/int(x.split('/')[1])),2) if int(x.split('/')[1]) !=0 else float(0))
    table_df.drop(columns=['middle_shootings','zone_shootings'],inplace=True)
    return table_df


def new_columns_teams(players_matches_stats,totals_df): #return 2 rows df
    team_ids=[int(a) for a in totals_df['team_id'].tolist()]
    home_middle_in=players_matches_stats[players_matches_stats['team_id']==team_ids[0]]['middle_shootings_in'].sum()
    home_middle_tried=players_matches_stats[players_matches_stats['team_id']==team_ids[0]]['middle_shootings_tried'].sum()
    home_middle_perc=round(float(home_middle_in/home_middle_tried),2) if int(home_middle_tried) !=0 else float(0)
    away_middle_in=players_matches_stats[players_matches_stats['team_id']==team_ids[1]]['middle_shootings_in'].sum()
    away_middle_tried=players_matches_stats[players_matches_stats['team_id']==team_ids[1]]['middle_shootings_tried'].sum()
    away_middle_perc=round(float(away_middle_in/away_middle_tried),2) if int(away_middle_tried) !=0 else float(0)
    totals_df['middle_shootings_in']=[home_middle_in,away_middle_in]
    totals_df['middle_shootings_tried']=[home_middle_tried,away_middle_tried]
    totals_df['middle_shootings_perc']=[home_middle_perc,away_middle_perc]
    home_zone_in=players_matches_stats[players_matches_stats['team_id']==team_ids[0]]['zone_shootings_in'].sum()
    home_zone_tried=players_matches_stats[players_matches_stats['team_id']==team_ids[0]]['zone_shootings_tried'].sum()
    home_zone_perc=round(float(home_zone_in/home_zone_tried),2) if int(home_zone_tried) !=0 else float(0)
    away_zone_in=players_matches_stats[players_matches_stats['team_id']==team_ids[1]]['zone_shootings_in'].sum()
    away_zone_tried=players_matches_stats[players_matches_stats['team_id']==team_ids[1]]['zone_shootings_tried'].sum()
    away_zone_perc=round(float(away_zone_in/away_zone_tried),2) if int(away_zone_tried) !=0 else float(0)
    totals_df['zone_shootings_in']=[home_zone_in,away_zone_in]
    totals_df['zone_shootings_tried']=[home_zone_tried,away_zone_tried]
    totals_df['zone_shootings_perc']=[home_zone_perc,away_zone_perc]
    return totals_df

'''
def getting_match_ids():
    global conn
    load_dotenv()

    conn = PostgreSQLConnection(os.getenv('PG_HOST'), os.getenv('PG_DATABASE_NAME'), os.getenv('PG_USER_NAME'), os.getenv('PG_DATABASE_PASSWORD'))
    conn.connect()

    conn.execute('SELECT match_id,date FROM public.results ORDER BY date DESC')
    data_total=pd.DataFrame(conn.fetchall())
    match_ids_total=data_total[0].tolist()
    conn.execute('SELECT match_id FROM public.shooting_chart_availability')
    match_ids_done=pd.DataFrame(conn.fetchall())[0].tolist()

    with open('match_scraper_errors.txt','r')as f:
        fi=f.read()
    fi=fi.replace('\n',"").replace('Error in ',",")
    errors_ids=[int(a) for a in fi[1:].split(',')]

    match_ids=list(set(match_ids_total)-set(match_ids_done)-set(errors_ids))
    dataframe_left=data_total[data_total[0].isin(match_ids)]

    tuples_left=[tuple(x) for x in dataframe_left.itertuples(index=False)]

    print(f'New match_ids to scrape:{len(tuples_left)}')
    return tuples_left
'''

brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path
driver = webdriver.Chrome(options=options)

tuples_left=getting_match_ids()

for match_id,year in tuples_left:
    year=int(year.year)
    try:
        shooting_charts=[]
        charts_availability=[]
        driver.get(f'https://baloncestoenvivo.feb.es/partido/{match_id}')
        wait = WebDriverWait(driver, 2)
        waiting=wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[4]/div[2]/div[2]/div[4]")))
        time.sleep(0.5)
        soup=bs(driver.page_source)
        try:
            match_partials=partials_scraper(soup,match_id)
        except:
            pass
        teams_dict=dictionary_team_names(soup)

        home_rows=soup.find_all('div',{'class':'responsive-scroll'})[0].find('tbody').find_all('tr')
        away_rows=soup.find_all('div',{'class':'responsive-scroll'})[1].find('tbody').find_all('tr')

        home_df,home_players_dict=table_scraper(teams_dict,home_rows,match_id,'Home')
        away_df,away_players_dict=table_scraper(teams_dict,away_rows,match_id,'Away')
        home_totals_df=totals_scraper(teams_dict,home_rows,match_id,'Home')
        away_totals_df=totals_scraper(teams_dict,away_rows,match_id,'Away')

        players_matches_stats=pd.concat([home_df,away_df]).reset_index(drop=True)
        teams_match_stats=pd.concat([home_totals_df,away_totals_df]).reset_index(drop=True)

        players_dict={'Home':home_players_dict['Home'],'Away':away_players_dict['Away']}
        if year>2020:
            try:
                print(f'Clicking shooting year={year}')
                driver.find_element(By.XPATH,'/html/body/form/div[4]/div[2]/div[1]/div[1]/a[4]').click()
                wait = WebDriverWait(driver, 2)
                waiting=wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[4]/div[2]/div[1]/div[2]/div[4]/div[2]/div[1]/div/div")))
                time.sleep(0.5)
                soup_shooting_chart=bs(driver.page_source)
                shooting_df,dict_to_process=shooting_scraper(soup_shooting_chart,match_id,players_dict,teams_dict)
                shooting_charts.append(match_id)
                charts_availability.append(True)
                players_matches_stats=new_columns_players(players_matches_stats)
                teams_match_stats=new_columns_teams(players_matches_stats,teams_match_stats)
                print(f'Shooting chart available in match_id={match_id}')
            except:
                print(f'No shooting chart available in match_id={match_id}')
                shooting_charts.append(match_id)
                charts_availability.append(False)
        else:
            print('No shooting chart available (no greater than 2019)')
            shooting_charts.append(match_id)
            charts_availability.append(False)
        shooting_charts_availability=pd.DataFrame({'match_id':shooting_charts,'availability':charts_availability})

        pipeline_match_partials = DataPipeline(conn, 'match_partials')
        try:
            pipeline_match_partials.insert_data(match_partials)
        except:
            pass
        pipeline_shooting_chart_availability = DataPipeline(conn, 'shooting_chart_availability')
        pipeline_shooting_chart_availability.insert_data(shooting_charts_availability)
        pipeline_shootings = DataPipeline(conn, 'shootings')
        try:
            pipeline_shootings.insert_data(shooting_df)
        except:
            pass
        pipeline_players_matches_stats= DataPipeline(conn, 'players_matches_stats')
        pipeline_players_matches_stats.insert_data(players_matches_stats)
        pipeline_teams_matches_stats= DataPipeline(conn, 'teams_matches_stats')
        pipeline_teams_matches_stats.insert_data(teams_match_stats)
    except Exception as e:
        print(f'Error in match_scraper match_id= {match_id}')
        print(e,type(e))
        with open('match_scraper_errors.txt','a') as file:
            file.write(f'Error in {match_id}\n')
    
conn.close()


