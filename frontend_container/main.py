from taipy.gui import Gui,notify
import plotly.express as px
import taipy.gui.builder as tgb
import io
import analysis as analysis
#import analysis
from fuzzywuzzy import fuzz


def fuzzy_search(my_list, target, threshold=50):
    results = []
    for item in my_list:
        ratio = fuzz.ratio(target, item)
        if ratio >= threshold:
            results.append((item, ratio))
    return results


def name_scraper(state):
    input=state.value
    print(input)
    results=fuzzy_search(list_of_players_total,input)
    print(results)
    if len(results)>0:
        state.list_of_players=[result[0].upper() for result in results]
    else:
        state.list_of_players=['No players','with that','name']


def create_fig(df,stat,stat_mode):
    if len(stat)>1:
        stats=', '.join([f'{col}' for col in stat])
    else:
        stats=stat[0]
    title=f'{stats} IN {stat_mode} BY SEASON'
    print(title)
    title=title.upper()
    df=df.sort_values("SEASON")
    if len(df)>1:
        fig = px.line(data_frame=df,x='SEASON', y=stat, title=title)
    else:
        fig = px.bar(data_frame=df,x='SEASON', y=stat, title=title)
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
stats_columns=list(player_stats_table.columns)

#Chart
stat=['POINTS']
figg = create_fig(player_stats_table,['POINTS'],'AVERAGE')


def new_player(state,id,payload):
    
    player_id = list_of_players_dict[payload['args'][0]]
    state.player_id=player_id
    player_stats = analysis.PlayerStats(player_id)
    state.value = None

    player_info=player_stats.info_query()
    player_path=player_stats.path()
    player_image,player_image_width,player_image_height=analysis.get_player_image(player_id)
    state.player_path=player_path
    state.name=player_info['player_name']
    player_image_height=f"{player_image_height}px"
    player_image_width=f"{player_image_width}px"
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
    print('player_id passed is:',player_id)
    on_mode(state)


def on_mode(state):
    player_id=state.player_id
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


with tgb.Page() as player_analysis:
    tgb.text(' ',mode='pre')
    tgb.text('{player_id}',mode='pre',class_name='d-none')
    tgb.text("Player analysis",class_name="h1 text-center")
    tgb.text(' ',mode='pre')
    tgb.text('Use the searcher bar to type the name of the player and select the player in the left menu',mode='pre',class_name='text-center')
    with tgb.layout(1):
        with tgb.layout(class_name='d-inline-block m-auto'):
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.input('{value}',type='search',label='Player name',class_name='d-inline',on_change=name_scraper,change_delay=10)
            """with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.button('Select')"""
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.menu('{list_of_players}',on_action=new_player)
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
    

pages = {
    "/": root_page,
    "home": player_analysis,
    "about": second
}

gui = Gui(pages=pages)
gui.run(title='Player analysis',port=5000)
