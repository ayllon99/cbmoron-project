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


conn=psycopg2.connect(dbname='cbmoron_database',host='localhost',user='root',password='root')
cur = conn.cursor()

#Shootings query
cur.execute("""SELECT CASE
                WHEN EXTRACT(MONTH FROM date) < 8 THEN EXTRACT(YEAR FROM date)-1
                WHEN EXTRACT(MONTH FROM date) >= 8 THEN EXTRACT(YEAR FROM date)
                END AS season,date,category,player_id,player_name,success,quarter,shoot_time,top_top,left_left,shooting_type 
                FROM shootings
                LEFT JOIN results
                ON shootings.match_id=results.match_id
                WHERE player_id = 2274861
                ORDER BY season""")
df=pd.DataFrame(cur.fetchall())
df.columns=['season','date','category','player_id','player_name','success','quarter','shoot_time','top_top','left_left','shooting_type']


cur.close()
conn.close()




images=[]
for year in range(2020,2023):
    fig=draw_court(year=year)             
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    images.append(buf)


with tgb.Page() as player_home:
    tgb.text("Análisis de jugador",class_name="h1 text-center")
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
            tgb.input(value='', label='Nombre del jugador')
        with tgb.part():
            tgb.button('Analizar',class_name="center")
    with tgb.layout("1 1 1 1 1 1 1"):
        with tgb.part():
            tgb.text('.')
    tgb.text("Jose Luis Ayllon Sanchez",class_name="h2 text-center")
    tgb.text('--------------------------------------',class_name="h1 text-center")
    with tgb.layout("1 1 1 1 1"):
        with tgb.part():
            tgb.text(f'Edad',class_name="h3 text-center")
            tgb.text(f'{25} años',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Última temporada',class_name="h3 text-center")
            tgb.text(f'{2018}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Última liga',class_name="h3 text-center")
            tgb.text(f'{'1 provincial'}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Posición',class_name="h3 text-center")
            tgb.text(f'{'alero'}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Nacionalidad',class_name="h3 text-center")
            tgb.text(f'{'españa'}',class_name="h3 text-center")
    
    tgb.text('--------------------------------------',class_name="h1 text-center")
    #tgb.table("{path}")
    with tgb.layout("1 1 1"):
        for i, image_buffer in enumerate(images):
            with tgb.part():
                tgb.image(image_buffer.getvalue(), width=10, label='Shootings')
                image_buffer.seek(0)  # Reset the buffer for the next iteration
    #tgb.chart(figure="{fig_line_chart}",)
    #table=tgb.table("{player_career_stats}")
    #table.align = "center"



gui = Gui(player_home)
gui.run(title='Player analysis',port=2425)
