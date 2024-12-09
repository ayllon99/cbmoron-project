from taipy.gui import Gui,notify
import taipy as tp
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import taipy.gui.builder as tgb
import taipy.gui.state as state
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
import io
from datetime import datetime
from PIL import Image
import matplotlib.image as mpimg
import psycopg2
#import cbmoron.frontend.analysis as analysis
import analysis
from fuzzywuzzy import fuzz


player_id=2274861
player_stats = analysis.PlayerStats(player_id)
stats, years = player_stats.get_shooting_stats()
player_info=player_stats.info_query()
player_path=player_stats.path()
last_season=player_path.loc[0].SEASON
last_league=player_path.loc[0].LEAGUE
player_stats_total=player_stats.stats_total_table()
player_stats_avg=player_stats.stats_avg_table()
##

#SELECT identifier,player_id,season,team_name_extended,stage_abbrev,stage_name_extended,n_matches,min_total,points_total,twos_in_total,twos_tried_total,twos_perc,threes_in_total,threes_tried_total,threes_perc,field_goals_in_total,field_goals_tried_total,field_goals_perc,free_throws_in_total,free_throws_tried_total,free_throws_perc,offensive_rebounds_total,deffensive_rebounds_total,total_rebounds_total,assists_total,turnovers_total,blocks_favor_total,blocks_against_total,dunks_total,personal_fouls_total,fouls_received_total,efficiency_total 

#SELECT season,team_name_extended,stage_name_extended,SUM(n_matches) AS n_matches,MIN(min_total) AS min_total,SUM(points_total) AS points_total ,SUM(twos_in_total) AS twos_in_total,SUM(twos_tried_total) AS twos_tried_total,SUM(twos_perc) AS twos_perc,SUM(threes_in_total) AS threes_in_total,SUM(threes_tried_total) AS threes_tried_total,SUM(threes_perc) AS threes_perc,SUM(field_goals_in_total) AS field_goals_in_total,SUM(field_goals_tried_total) AS field_goals_tried_total,SUM(field_goals_perc) AS field_goals_perc,SUM(free_throws_in_total) AS free_throws_in_total,SUM(free_throws_tried_total) AS free_throws_tried_total,SUM(free_throws_perc) AS free_throws_perc,SUM(offensive_rebounds_total) AS offensive_rebounds_total,SUM(deffensive_rebounds_total) AS deffensive_rebounds_total,SUM(total_rebounds_total) AS total_rebounds_total,SUM(assists_total) AS assists_total,SUM(turnovers_total) AS turnovers_total,SUM(blocks_favor_total) AS blocks_favor_total,SUM(blocks_against_total) AS blocks_against_total,SUM(dunks_total)AS dunks_total,SUM(personal_fouls_total) AS personal_fouls_total,SUM(fouls_received_total) AS fouls_received_total,SUM(efficiency_total) AS efficiency_total 


images=[]
for year in years:
    fig=analysis.draw_court(dic_stats=stats,year=year)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    images.append(buf)


def fuzzy_search(my_list, target, threshold=60):
    results = []
    for item in my_list:
        ratio = fuzz.ratio(target, item)
        if ratio >= threshold:
            results.append((item, ratio))
    return results

my_list = ["apple", "banana", "cherry", "date", "elderberry"]
target = "chery"
threshold = 60  # 60% similarity threshold

value=None


def name_scraper(state):
    input=state.value
    print(input)
    results=fuzzy_search(my_list,input)
    for result in results:
        print(f"Found {result[0]} with similarity {result[1]}")


def create_fig(df,stat,stat_mode):
    if len(stat)>1:
        stats=', '.join([f'{col}' for col in stat])
    else:
        stats=stat[0]
    title=f'{stats} IN {stat_mode} BY SEASON'
    print(title)
    title=title.upper()
    df=df.sort_values("SEASON")
    fig = px.line(data_frame=df,x='SEASON', y=stat, title=title)
    return fig

player_stats_table=player_stats.stats_avg_table()
stat_mode='AVERAGE'
stats_columns=list(player_stats_table.columns)

figg = create_fig(player_stats_table,['POINTS'],'AVERAGE')
stat=['POINTS']


def on_mode(state):
    player_id=2274861
    player_stats = analysis.PlayerStats(player_id)
    mode=state.stat_mode
    print(mode)
    if mode=='AVERAGE':
        table=player_stats.stats_avg_table()
        state.player_stats_table=table
        
    elif mode=='TOTAL':
        table=player_stats.stats_total_table()
        state.player_stats_table=table
    on_selector(state)


def on_selector(state):
    column=state.stat
    mode=state.stat_mode
    print('printing-----------',state.stat)
    df=state.player_stats_table
    state.figg = create_fig(df,column,mode)


with tgb.Page() as root_page:
    tgb.navbar(class_name='m-auto')


with tgb.Page() as player_home:
    tgb.text(' ',mode='pre')
    tgb.text("Player analysis",class_name="h1 text-center")
    tgb.text(' ',mode='pre')
    with tgb.layout(1):
        with tgb.layout(class_name='d-inline-block m-auto'):
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.input('{value}',type='search',label='Player name',class_name='d-inline',on_change=name_scraper,change_delay=10)
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.button('Select')
    tgb.text(' ',mode='pre')
    tgb.text(player_info['player_name'],class_name="h2 text-center text-underline")
    tgb.text(' ',mode='pre')
    with tgb.layout("1 1 1 1 1"):
        with tgb.part():
            tgb.text(f'Age',class_name="h3 text-center text-underline")
            tgb.text(f'{player_info['age']} years old',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Last season',class_name="h3 text-center text-underline")
            tgb.text(last_season,class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Last league',class_name="h3 text-center text-underline")
            tgb.text(last_league,class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Position',class_name="h3 text-center text-underline")
            tgb.text(f'{player_info['position']}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Nationality',class_name="h3 text-center text-underline")
            tgb.text(f'{player_info['nationality']}',class_name="h3 text-center")
    
    tgb.text(' ',mode='pre')
    tgb.text('PLAYER CAREER IN THE COUNTRY',class_name="h2 text-center")
    tgb.table("{player_path}")
    with tgb.layout("1 1 1"):
        for i, image_buffer in enumerate(images):
            with tgb.part():
                tgb.image(image_buffer.getvalue(), width=10, label='')
                image_buffer.seek(0)
    tgb.selector(value='{stat_mode}',lov=['AVERAGE','TOTAL'],
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select mode",
                    class_name="fullwidth",
                    on_change=on_mode)
    tgb.text(' ',mode='pre')
    tgb.text('PLAYER CAREER STATS',class_name="h2 text-center")
    tgb.text(' ',mode='pre')
    tgb.table("{player_stats_table}")
    tgb.text(' ',mode='pre')
    with tgb.layout("1 225px"):
        tgb.chart(figure="{figg}")
        tgb.selector(value='{stat}',lov=stats_columns,
                    dropdown=True,
                    multiple=True,
                    mode='selector',
                    label="Select stat",
                    class_name="fullwidth",
                    on_change=on_selector)

with tgb.Page() as second:
    
    tgb.text("Player analysis",class_name="h1 text-center")
    tgb.text(' ',mode='pre')
    tgb.text(player_info['player_name'],class_name="h2 text-center")
    tgb.text('--------------------------------------',class_name="h1 text-center")
    with tgb.layout("1 1 1 1 1 1 1"):
        with tgb.part():
            tgb.text('')
        with tgb.part():
            tgb.text('')
        with tgb.part():
            tgb.text('')
        with tgb.part():
            tgb.input(value='', label='Player name',class_name='align-columns-center')
        with tgb.part():
            tgb.button('Select',class_name='align-columns-center')
    tgb.text(' ',mode='pre')
    tgb.text(player_info['player_name'],class_name="h2 text-center")
    tgb.text('--------------------------------------',class_name="h1 text-center")
    with tgb.layout("1 1 1 1 1"):
        with tgb.part():
            tgb.text(f'Age',class_name="h3 text-center")
            tgb.text(f'{player_info['age']} years old',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Last season',class_name="h3 text-center")
            tgb.text(last_season,class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Last league',class_name="h3 text-center")
            tgb.text(last_league,class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Position',class_name="h3 text-center")
            tgb.text(f'{player_info['position']}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Nationality',class_name="h3 text-center")
            tgb.text(f'{player_info['nationality']}',class_name="h3 text-center")
    
    tgb.text(' ',mode='pre')
    tgb.text('PLAYER CAREER IN THE COUNTRY',class_name="h2 text-center")
    tgb.table("{player_path}")
    with tgb.layout("1 1 1"):
        for i, image_buffer in enumerate(images):
            with tgb.part():
                tgb.image(image_buffer.getvalue(), width=10, label='')
                image_buffer.seek(0)
    tgb.selector(value='{stat}',lov=['points_per_game','assists_per_game','rebounds_per_game'],
                 dropdown=True,
                 multiple=False,
                 label="Select stat",
                 class_name="fullwidth",
                 on_change=on_selector)
    tgb.chart(figure="{figg}")
    tgb.table("{df}")
    tgb.table("{player_stats_avg}")

pages = {
    "/": root_page,
    "home": player_home,
    "about":second
}

gui = Gui(pages=pages)
gui.run(title='Player analysis',port=2425)
