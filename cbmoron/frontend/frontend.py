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
import cbmoron.frontend.analysis


conn=psycopg2.connect(dbname='cbmoron_database',host='localhost',user='root',password='root')
cur = conn.cursor()

#Shootings query
cur.execute("""SELECT season,shoot_from,success,COUNT(*)
                FROM shootings
                LEFT JOIN results
                ON shootings.match_id=results.match_id
                WHERE player_id = 2274861
                GROUP BY season,shoot_from,success
                ORDER BY season,shoot_from""")
df=pd.DataFrame(cur.fetchall())
df.columns=['season','shoot_from','success','total']

stats={}

for year in df['season'].unique():
    stats[year]={}
    stats[year]['Zone']={'in':0,'out':0}
    stats[year]['Right Corner Three']={'in':0,'out':0}
    stats[year]['Right Corner Middle']={'in':0,'out':0}
    stats[year]['Right Side Three']={'in':0,'out':0}
    stats[year]['Right Side Middle']={'in':0,'out':0}
    stats[year]['Front Three']={'in':0,'out':0}
    stats[year]['Front Middle']={'in':0,'out':0}
    stats[year]['Left Side Three']={'in':0,'out':0}
    stats[year]['Left Side Middle']={'in':0,'out':0}
    stats[year]['Left Corner Three']={'in':0,'out':0}
    stats[year]['Left Corner Middle']={'in':0,'out':0}


for row in range(len(df)):
    
    success=df.loc[row].success
    if success==True:
        stats[df.loc[row].season][df.loc[row].shoot_from]['in']=df.loc[row].total
    else:
        stats[df.loc[row].season][df.loc[row].shoot_from]['out']=df.loc[row].total

new_stats = {}
for year, values in stats.items():
    new_values = {}
    for key, value in values.items():
        new_values[key] = {
            'in': value['in'],
            'out': value['out'],
            'tried': value['in'] + value['out']
        }
    new_stats[year] = new_values

for year in new_stats.keys():
    cbmoron.frontend.analysis.draw_court(dic_stats=new_stats,year=year)

cur.close()
conn.close()


images=[]
for year in range(2020,2023):
    fig=analysis.draw_court(year=year)             
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
