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


images=[]
for year in years:
    fig=analysis.draw_court(dic_stats=stats,year=year)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    images.append(buf)


df = pd.DataFrame({
    'years': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
    'points_per_game': [20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
    'assists_per_game': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    'rebounds_per_game': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
})


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


def name_scraper(state):
    input=state.value
    print(input)
    results=fuzzy_search(my_list,input)
    for result in results:
        print(f"Found {result[0]} with similarity {result[1]}")


value=None

def create_fig(df,stat):
    fig = px.line(data_frame=df,x='years', y=stat)
    return fig


stat=['points_per_game','assists_per_game','rebounds_per_game']

figg = create_fig(df,'points_per_game')


def on_selector(state):
    print('printing-----------',state.stat)
    df=state.df
    column=state.stat
    state.figg = create_fig(df,column)

with tgb.Page() as root_page:
    tgb.navbar(class_name='m-auto')


with tgb.Page() as player_home:
    tgb.text(' ',mode='pre')
    tgb.text("Player analysis",class_name="h1 text-center")
    tgb.text(' ',mode='pre')
    with tgb.layout(1):
        with tgb.layout(class_name='d-inline-block m-auto'):
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.input('{value}',type='search',properties={'args':my_list},label='Player name',class_name='d-inline',on_change=name_scraper,change_delay=10)
            with tgb.part(class_name='d-inline-block m-auto d-flex justify-content-center'):
                tgb.button('Select')
    tgb.text(' ',mode='pre')
    tgb.text(player_info['player_name'],class_name="h2 text-center text-underline")
    tgb.text(' ',mode='pre')
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
    with tgb.layout("1 225px"):
        tgb.chart(figure="{figg}")
        tgb.selector(value='{stat}',lov=['points_per_game','assists_per_game','rebounds_per_game'],
                    dropdown=False,
                    multiple=False,
                    mode='radio',
                    label="Select stat",
                    class_name="fullwidth",
                    on_change=on_selector)
    tgb.text(' ',mode='pre')
    tgb.table("{df}")
    #table=tgb.table("{player_career_stats}")
    #table.align = "center"

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

pages = {
    "/": root_page,
    "home": player_home,
    "about":second
}

gui = Gui(pages=pages)
gui.run(title='Player analysis',port=2425)
