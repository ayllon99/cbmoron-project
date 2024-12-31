from taipy.gui import Gui,notify
import plotly.express as px
import taipy.gui.builder as tgb
import io
import analysis
from fuzzywuzzy import fuzz
import pandas as pd


def fuzzy_search(my_list, target, threshold=50):
    results = []
    for item in my_list:
        ratio = fuzz.ratio(target, item)
        if ratio >= threshold:
            results.append((item, ratio))
    return results


def name_scraper(state):
    try:
        input=state.value
        print(input)
        results=fuzzy_search(list_of_players_total,input)
        #print(results)
        if len(results)>0:
            state.list_of_players=[result[0].upper() for result in results]
        else:
            state.list_of_players=['No players','with that','name']
    except:
        print('Error in name_scraper')


def proccess_column_weighted(stat,n_matches):
    return (n_matches * stat).sum() / n_matches.sum()


def proccess_df_avg(df):
    dff=df.groupby('SEASON').apply(lambda x: pd.Series({'N_MATCHES': x['N_MATCHES'].sum(),
                                                        'POINTS': proccess_column_weighted(x['POINTS'],x['N_MATCHES']), 
                                                        'TWOS_IN': proccess_column_weighted(x['TWOS_IN'],x['N_MATCHES']),
                                                        'TWOS_TRIED':proccess_column_weighted(x['TWOS_TRIED'],x['N_MATCHES']), 
                                                        'TWOS_PERC':proccess_column_weighted(x['TWOS_PERC'],x['N_MATCHES']), 
                                                        'THREES_IN':proccess_column_weighted(x['THREES_IN'],x['N_MATCHES']), 
                                                        'THREES_TRIED':proccess_column_weighted(x['THREES_TRIED'],x['N_MATCHES']), 
                                                        'THREES_PERC':proccess_column_weighted(x['THREES_PERC'],x['N_MATCHES']), 
                                                        'FIELD_GOALS_IN':proccess_column_weighted(x['FIELD_GOALS_IN'],x['N_MATCHES']), 
                                                        'FIELD_GOALS_TRIED':proccess_column_weighted(x['FIELD_GOALS_TRIED'],x['N_MATCHES']), 
                                                        'FIELD_GOALS_PERC':proccess_column_weighted(x['FIELD_GOALS_PERC'],x['N_MATCHES']), 
                                                        'FREE_THROWS_IN':proccess_column_weighted(x['FREE_THROWS_IN'],x['N_MATCHES']), 
                                                        'FREE_THROWS_TRIED':proccess_column_weighted(x['FREE_THROWS_TRIED'],x['N_MATCHES']), 
                                                        'FREE_THROWS_PERC':proccess_column_weighted(x['FREE_THROWS_PERC'],x['N_MATCHES']), 
                                                        'OFFENSIVE_REBOUNDS':proccess_column_weighted(x['OFFENSIVE_REBOUNDS'],x['N_MATCHES']), 
                                                        'DEFFENSIVE_REBOUNDS':proccess_column_weighted(x['DEFFENSIVE_REBOUNDS'],x['N_MATCHES']), 
                                                        'TOTAL_REBOUNDS':proccess_column_weighted(x['TOTAL_REBOUNDS'],x['N_MATCHES']), 
                                                        'ASSISTS':proccess_column_weighted(x['ASSISTS'],x['N_MATCHES']), 
                                                        'TURNOVERS':proccess_column_weighted(x['TURNOVERS'],x['N_MATCHES']), 
                                                        'BLOCKS_FAVOR':proccess_column_weighted(x['BLOCKS_FAVOR'],x['N_MATCHES']), 
                                                        'BLOCKS_AGAINST':proccess_column_weighted(x['BLOCKS_AGAINST'],x['N_MATCHES']), 
                                                        'DUNKS':proccess_column_weighted(x['DUNKS'],x['N_MATCHES']), 
                                                        'PERSONAL_FOULS':proccess_column_weighted(x['PERSONAL_FOULS'],x['N_MATCHES']), 
                                                        'FOULS_RECEIVED':proccess_column_weighted(x['FOULS_RECEIVED'],x['N_MATCHES']), 
                                                        'EFFICIENCY':proccess_column_weighted(x['EFFICIENCY'],x['N_MATCHES']),
                                                        }),include_groups=False)
    return dff


def proccess_df_total(df):
    dff=df.groupby('SEASON').apply(lambda x: pd.Series({'N_MATCHES': x['N_MATCHES'].sum(),
                                                    'POINTS':  x['POINTS'].sum(), 
                                                    'TWOS_IN': x['TWOS_IN'].sum(),
                                                    'TWOS_TRIED':x['TWOS_TRIED'].sum(), 
                                                    'TWOS_PERC':proccess_column_weighted(x['TWOS_PERC'],x['N_MATCHES']), 
                                                    'THREES_IN':x['THREES_IN'].sum(), 
                                                    'THREES_TRIED':x['THREES_TRIED'].sum(), 
                                                    'THREES_PERC':proccess_column_weighted(x['THREES_PERC'],x['N_MATCHES']), 
                                                    'FIELD_GOALS_IN':x['FIELD_GOALS_IN'].sum(), 
                                                    'FIELD_GOALS_TRIED':x['FIELD_GOALS_TRIED'].sum(), 
                                                    'FIELD_GOALS_PERC':proccess_column_weighted(x['FIELD_GOALS_PERC'],x['N_MATCHES']), 
                                                    'FREE_THROWS_IN':x['FREE_THROWS_IN'].sum(), 
                                                    'FREE_THROWS_TRIED':x['FREE_THROWS_TRIED'].sum(), 
                                                    'FREE_THROWS_PERC':proccess_column_weighted(x['FREE_THROWS_PERC'],x['N_MATCHES']), 
                                                    'OFFENSIVE_REBOUNDS':x['OFFENSIVE_REBOUNDS'].sum(), 
                                                    'DEFFENSIVE_REBOUNDS':x['DEFFENSIVE_REBOUNDS'].sum(), 
                                                    'TOTAL_REBOUNDS':x['TOTAL_REBOUNDS'].sum(), 
                                                    'ASSISTS':x['ASSISTS'].sum(), 
                                                    'TURNOVERS':x['TURNOVERS'].sum(), 
                                                    'BLOCKS_FAVOR':x['BLOCKS_FAVOR'].sum(), 
                                                    'BLOCKS_AGAINST':x['BLOCKS_AGAINST'].sum(), 
                                                    'DUNKS':x['DUNKS'].sum(), 
                                                    'PERSONAL_FOULS':x['PERSONAL_FOULS'].sum(), 
                                                    'FOULS_RECEIVED':x['FOULS_RECEIVED'].sum(), 
                                                    'EFFICIENCY':x['EFFICIENCY'].sum(),
                                                    }),include_groups=False)
    return dff


def create_fig(df,stat,stat_mode):
    try:
        if len(stat)>1:
            stats=', '.join([f'{col}' for col in stat])
        else:
            stats=stat[0]
        title=f'{stats} IN {stat_mode} BY SEASON'
        #print(title)
        title=title.upper()
        if stat_mode == 'AVERAGE':
            dff = proccess_df_avg(df)
        elif stat_mode == 'TOTAL':
            dff = proccess_df_total(df)

        dff=dff.reset_index()
        dff=dff.sort_values("SEASON")
        if len(dff)>1:
            fig = px.line(data_frame=dff,x='SEASON', y=stat, title=title)
        else:
            fig = px.bar(data_frame=dff,x='SEASON', y=stat, title=title)
    except:
        print('Error in create_fig')
    return fig


#Marc Gasol id
player_id=360978
player_stats = analysis.PlayerStats(player_id)

#Input
value=None

#Menu
list_of_players_df=player_stats.list_of_players()
list_of_players_dict=list_of_players_df.set_index('player_name').to_dict()['player_id']
list_of_players_total=[ a.lower() for a in list_of_players_df['player_name'].to_list()]
list_of_players=list_of_players_df['player_name'].to_list()[:10] 

#Personal info + path
player_info=player_stats.info_query()
player_path=player_stats.path()
player_image,player_image_width,player_image_height=analysis.get_player_image(player_id)
player_image_height=f"{player_image_height}px"
player_image_width=f"{player_image_width}px"
name=player_info['player_name']
age=player_info['age']
try:
    last_season=player_path.loc[0].SEASON
    last_league=player_path.loc[0].LEAGUE
except:
    print('Error in SEASON or LEAGUE')
position=player_info['position']
nationality=player_info['nationality']

#Shootings
stats, years = player_stats.get_shooting_stats()
images=[]
for year in years:
    fig=analysis.draw_court(dic_stats=stats,year=year)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    images.append(buf)
final_images=[]
for i, image_buffer in enumerate(images):
    final_images.append(image_buffer.getvalue())
    image_buffer.seek(0)
image_1=final_images[0]
image_2=final_images[1]
image_3=final_images[2]

#Table stats
stat_mode='AVERAGE'
player_stats_table=player_stats.stats_avg_table()
my_list=list(player_stats_table.columns)
stats_columns=[x for x in my_list if x not in ['MIN', 'SEASON','TEAM_NAME_EXTENDED','STAGE_NAME_EXTENDED']]

#Chart
stat=['POINTS']
figg = create_fig(player_stats_table,['POINTS'],'AVERAGE')


def menu_clicked(state,id,payload):
    player_id = list_of_players_dict[payload['args'][0]]
    new_player(state,player_id)

def new_player(state,player_id):
    try:
        state.player_id=player_id
        player_stats = analysis.PlayerStats(player_id)
        state.value = None

        player_info=player_stats.info_query()
        player_path=player_stats.path()
        player_image,player_image_width,player_image_height=analysis.get_player_image(player_id)
        state.player_path=player_path
        state.name=player_info['player_name']
        state.player_image_height=f"{player_image_height}px"
        state.player_image_width=f"{player_image_width}px"
        state.player_image=player_image
        state.age=player_info['age']

        try:
            state.last_season=player_path.loc[0].SEASON
            state.last_league=player_path.loc[0].LEAGUE
        except:
            print('Error getting SEASON or LEAGUE')

        state.position=player_info['position']
        state.nationality=player_info['nationality']

        stats, years = player_stats.get_shooting_stats()
        
        images=[]
        for year in years:
            fig=analysis.draw_court(dic_stats=stats,year=year)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            images.append(buf)
        final_images=[]
        for i, image_buffer in enumerate(images):
            final_images.append(image_buffer.getvalue())
            image_buffer.seek(0)
        state.image_1=final_images[0]
        state.image_2=final_images[1]
        state.image_3=final_images[2]
        state.stat_mode='AVERAGE'
        player_stats_table=player_stats.stats_avg_table()
        state.stats_columns=list(player_stats_table.columns)
        state.player_stats_table=player_stats_table

        #Chart
        state.stat=['POINTS']
        #print('player_id passed is:',player_id)
        on_mode(state)
    except Exception as e:
        print('Error in new_player---- ',e)
        notify(state=state,message='ERROR IN THIS PLAYER')


def on_mode(state):
    try:
        player_id=state.player_id
        player_stats = analysis.PlayerStats(player_id)
        mode=state.stat_mode
        #print(mode)
        if mode=='AVERAGE':
            table=player_stats.stats_avg_table()
            state.player_stats_table=table
            
        elif mode=='TOTAL':
            table=player_stats.stats_total_table()
            state.player_stats_table=table
        on_selector(state)
    except:
        print('Error in on_mode')


def on_selector(state):
    try:
        column=state.stat
        mode=state.stat_mode
        #print('printing-----------',state.stat)
        df=state.player_stats_table
        state.figg = create_fig(df,column,mode)
    except:
        print('Error in on_selector')


def submit_stats(state):
    print("clicked_second")
    season=state.season
    n_matches=state.n_matches
    min_avg=state.min_avg
    points_avg=state.points_avg
    twos_in_avg=state.twos_in_avg
    twos_tried_avg=state.twos_tried_avg
    twos_perc=state.twos_perc
    threes_in_avg=state.threes_in_avg
    threes_tried_avg=state.threes_tried_avg
    threes_perc=state.threes_perc
    field_goals_in_avg=state.field_goals_in_avg
    field_goals_tried_avg=state.field_goals_tried_avg
    field_goals_perc=state.field_goals_perc
    free_throws_in_avg=state.free_throws_in_avg
    free_throws_tried_avg=state.free_throws_tried_avg
    free_throws_perc=state.free_throws_perc
    offensive_rebounds_avg=state.offensive_rebounds_avg
    deffensive_rebounds_avg=state.deffensive_rebounds_avg
    total_rebounds_avg=state.total_rebounds_avg
    assists_avg=state.assists_avg
    turnovers_avg=state.turnovers_avg
    blocks_favor_avg=state.blocks_favor_avg
    blocks_against_avg=state.blocks_against_avg
    dunks_avg=state.dunks_avg
    personal_fouls_avg=state.personal_fouls_avg
    fouls_received_avg=state.fouls_received_avg
    efficiency_avg=state.efficiency_avg
    print(season,n_matches,min_avg,points_avg,twos_in_avg,twos_tried_avg,twos_perc,threes_in_avg,threes_tried_avg,threes_perc,field_goals_in_avg,field_goals_tried_avg,field_goals_perc,free_throws_in_avg,free_throws_tried_avg,free_throws_perc,offensive_rebounds_avg,deffensive_rebounds_avg,total_rebounds_avg,assists_avg,turnovers_avg,blocks_favor_avg,blocks_against_avg,dunks_avg,personal_fouls_avg,fouls_received_avg,efficiency_avg)




season=None
n_matches=None
min_avg=None
points_avg=None
twos_in_avg=None
twos_tried_avg=None
twos_perc=None
threes_in_avg=None
threes_tried_avg=None
threes_perc=None
field_goals_in_avg=None
field_goals_tried_avg=None
field_goals_perc=None
free_throws_in_avg=None
free_throws_tried_avg=None
free_throws_perc=None
offensive_rebounds_avg=None
deffensive_rebounds_avg=None
total_rebounds_avg=None
assists_avg=None
turnovers_avg=None
blocks_favor_avg=None
blocks_against_avg=None
dunks_avg=None
personal_fouls_avg=None
fouls_received_avg=None
efficiency_avg=None


league_selected='ORO'
leagues_list=['ORO','PLATA','EBA']

season_selected=None
seasons_list=['2023/24', '2022/23', '2021/22', '2020/21', '2019/20', '2018/19', '2017/18', '2016/17', '2015/16']

team_ids_dict=''
player_ids_dict=''

team_selected=None
teams_list=[]

player_id_selected=None
player_selected=None
players_list=[]

def league_function(state):
    state.players_list=[]
    state.teams_list=[]
    state.player_selected=None
    state.team_selected=None
    state.season_selected=None

def season_function(state):
    state.teams_list=[]
    searching=analysis.search_player()
    league=state.league_selected
    season=state.season_selected[2:]
    print('league: ',league,', season: ',season)
    team_ids_dict,teams_list=searching.on_change_season(league=league,season=season)
    #print(teams_list)
    state.team_ids_dict=team_ids_dict
    state.teams_list=teams_list
    
def team_function(state):
    searching=analysis.search_player()
    team_ids_dict=dict(dict(state.team_ids_dict)['team_id'])
    team_selected=state.team_selected
    team_id=team_ids_dict[team_selected]
    player_ids_dict,players_list=searching.on_change_team(team_id)
    state.players_list=players_list
    state.player_ids_dict=player_ids_dict

def player_function(state):
    player_name=state.player_selected
    player_ids_dict=dict(dict(state.player_ids_dict)['player_id'])
    player_id=player_ids_dict[player_name]
    state.player_id_selected=player_id
    print(player_id)

def submit_player(state):
    player_id=state.player_id_selected
    new_player(state,player_id)


with tgb.Page() as root_page:
    tgb.navbar(class_name='m-auto')


with tgb.Page() as player_analysis:
    tgb.text(' ',mode='pre')
    tgb.text('{player_id}',mode='pre',class_name='d-none')
    tgb.text('{player_id_selected}',mode='pre',class_name='d-none')
    tgb.text("Player analysis",class_name="h1 text-center")
    #tgb.text(' ',mode='pre')
    #tgb.text('Use the searcher bar to type the name of the player and select the player in the left menu',mode='pre',class_name='text-center')
    """with tgb.layout(1):
        with tgb.layout(class_name='d-inline-block m-auto'):
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.input('{value}',type='search',label='Player name',class_name='d-inline',on_change=name_scraper,change_delay=10)
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.menu('{list_of_players}',on_action=new_player)"""
    tgb.text('{team_ids_dict}',mode='pre',class_name='d-none')
    tgb.text('{player_ids_dict}',mode='pre',class_name='d-none')
    tgb.text(' ', mode='pre')
    with tgb.layout("1 1 1 1"):
        with tgb.part():
            tgb.selector(value='{league_selected}',lov='{leagues_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select league",
                    class_name="fullwidth",
                    on_change=league_function)
        with tgb.part():
            tgb.selector(value='{season_selected}',lov='{seasons_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select year",
                    class_name="fullwidth",
                    on_change=season_function)
        with tgb.part():
            tgb.selector(value='{team_selected}',lov='{teams_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select team",
                    class_name="fullwidth",
                    on_change=team_function)
        with tgb.part():
            tgb.selector(value='{player_selected}',lov='{players_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select player",
                    class_name="fullwidth",
                    on_change=player_function)
    with tgb.layout("1"):
        with tgb.part(class_name='m-auto'):
            tgb.button("Submit", on_action=submit_player)
    tgb.text(' ',mode='pre')
    with tgb.layout("1 1 1"):
        with tgb.part(class_name='m-auto'):
            tgb.image('{player_image}',height='{player_image_height}',width='{player_image_width}')
        with tgb.part(class_name='m-auto'):
            tgb.text('{name}',class_name="h2 text-center text-underline")
    tgb.text(' ',mode='pre')
    with tgb.layout("1 1 1 1 1"):
        with tgb.part():
            tgb.text(f'Age',class_name="h3 text-center text-underline")
            tgb.text('{age} years old',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Last season',class_name="h3 text-center text-underline")
            tgb.text('{last_season}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Last league',class_name="h3 text-center text-underline")
            tgb.text('{last_league}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Position',class_name="h3 text-center text-underline")
            tgb.text('{position}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Nationality',class_name="h3 text-center text-underline")
            tgb.text('{nationality}',class_name="h3 text-center")
    
    tgb.text(' ',mode='pre')
    tgb.text('PLAYER CAREER IN THE COUNTRY',class_name="h2 text-center")
    tgb.table("{player_path}")
    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.image('{image_1}', width=10, label='')
        with tgb.part():
            tgb.image('{image_2}', width=10, label='')
        with tgb.part():
            tgb.image('{image_3}', width=10, label='')
                
    tgb.toggle(value='{stat_mode}',lov=['AVERAGE','TOTAL'],
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="",
                    class_name="fullwidth",
                    on_change=on_mode)
    tgb.text(' ',mode='pre')
    tgb.text('PLAYER CAREER STATS',class_name="h2 text-center")
    tgb.text(' ',mode='pre')
    tgb.table("{player_stats_table}")
    tgb.text(' ',mode='pre')
    with tgb.layout("225px 1"):
        tgb.selector(value='{stat}',lov=stats_columns,
                    dropdown=True,
                    multiple=True,
                    mode='selector',
                    label="Select stat",
                    class_name="fullwidth",
                    on_change=on_selector)
        tgb.chart(figure="{figg}",class_name='fullwidth')


with tgb.Page() as second:
    
    tgb.text(' ',mode='pre')
    tgb.text("Player scraper",class_name="h1 text-center")
    tgb.text('{team_ids_dict}',mode='pre',class_name='d-none')
    tgb.text('{player_ids_dict}',mode='pre',class_name='d-none')
    tgb.text(' ', mode='pre')
    with tgb.layout("1 1 1 1"):
        with tgb.part():
            tgb.selector(value='{league_selected}',lov='{leagues_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select league",
                    class_name="fullwidth",
                    on_change=league_function)
        with tgb.part():
            tgb.selector(value='{season_selected}',lov='{seasons_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select year",
                    class_name="fullwidth",
                    on_change=season_function)
        with tgb.part():
            tgb.selector(value='{team_selected}',lov='{teams_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select team",
                    class_name="fullwidth",
                    on_change=team_function)
        with tgb.part():
            tgb.selector(value='{player_selected}',lov='{players_list}',
                    dropdown=True,
                    multiple=False,
                    mode='selector',
                    label="Select player",
                    class_name="fullwidth",
                    on_change=player_function)
    tgb.text(' ', mode='pre')
    tgb.text("Enter player stats:", class_name="h3 text-center")
    tgb.text(' ', mode='pre')
    with tgb.layout("1"):
        with tgb.part(class_name='m-auto'):
            tgb.button("Submit", on_action=submit_stats)
    tgb.text(' ', mode='pre')
    with tgb.layout("1 1 1 1 1 1"):
        with tgb.part():
            tgb.text("Season:")
            tgb.input("{season}", type="text", class_name="form-control")
        with tgb.part():
            tgb.text("N matches:")
            tgb.input("{n_matches}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Min avg:")
            tgb.input("{min_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Points avg:")
            tgb.input("{points_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Twos in avg:")
            tgb.input("{twos_in_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Twos tried avg:")
            tgb.input("{twos_tried_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Twos perc:")
            tgb.input("{twos_perc}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Threes in avg:")
            tgb.input("{threes_in_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Threes tried avg:")
            tgb.input("{threes_tried_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Threes perc:")
            tgb.input("{threes_perc}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Field goals in avg:")
            tgb.input("{field_goals_in_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Field goals tried avg:")
            tgb.input("{field_goals_tried_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Field goals perc:")
            tgb.input("{field_goals_perc}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Free throws in avg:")
            tgb.input("{free_throws_in_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Free throws tried avg:")
            tgb.input("{free_throws_tried_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Free throws perc:")
            tgb.input("{free_throws_perc}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Offensive rebounds avg:")
            tgb.input("{offensive_rebounds_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Deffensive rebounds avg:")
            tgb.input("{deffensive_rebounds_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Total rebounds avg:")
            tgb.input("{total_rebounds_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Assists avg:")
            tgb.input("{assists_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Turnovers avg:")
            tgb.input("{turnovers_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Blocks favor avg:")
            tgb.input("{blocks_favor_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Blocks against avg:")
            tgb.input("{blocks_against_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Dunks avg:")
            tgb.input("{dunks_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Personal fouls avg:")
            tgb.input("{personal_fouls_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Fouls received avg:")
            tgb.input("{fouls_received_avg}", type="number", class_name="form-control")
        with tgb.part():
            tgb.text("Efficiency avg:")
            tgb.input("{efficiency_avg}", type="number", class_name="form-control")
        

pages = {
    "/": root_page,
    "home": player_analysis,
    "about": second
}

gui = Gui(pages=pages)
gui.run(title='Player analysis',port=5000)
