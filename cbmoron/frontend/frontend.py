from taipy.gui import Gui,notify
import taipy as tp
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
import io
from datetime import datetime
from PIL import Image
import matplotlib.image as mpimg
import psycopg2
#import cbmoron.frontend.analysis as analysis
import analysis

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



with tgb.Page() as player_home:
    tgb.text("Player analysis",class_name="h1 text-center")
    with tgb.layout("1 1 1 1 1 1 1"):
        with tgb.part():
            tgb.text('.')
    with tgb.layout("1 1 1 1 1 1 1"):
        with tgb.part():
            tgb.text('')
        with tgb.part():
            tgb.text('')
        with tgb.part():
            tgb.text('')
        with tgb.part():
            tgb.input(value='', label='Player name')
        with tgb.part():
            tgb.button('Select',class_name="center")
    with tgb.layout("1 1 1 1 1 1 1"):
        with tgb.part():
            tgb.text('.')
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
    
    tgb.text('--------------------------------------',class_name="h1 text-center")
    tgb.text('PLAYER CAREER IN THE COUNTRY',class_name="h2 text-center")
    tgb.table("{player_path}")
    with tgb.layout("1 1 1"):
        for i, image_buffer in enumerate(images):
            with tgb.part():
                tgb.image(image_buffer.getvalue(), width=10, label='')
                image_buffer.seek(0)  # Reset the buffer for the next iteration
    #tgb.chart(figure="{chart}",)
    #table=tgb.table("{player_career_stats}")
    #table.align = "center"



gui = Gui(player_home)
gui.run(title='Player analysis',port=2425)
