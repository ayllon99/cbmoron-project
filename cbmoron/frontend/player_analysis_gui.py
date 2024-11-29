from taipy.gui import Gui,notify
import taipy as tp
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
############################3
from dotenv import load_dotenv
import os
from scraping_phase.pipeline import PostgreSQLConnection,DataPipeline
import io
import analysis_phase.analysis as analysis
from datetime import datetime



def create_line_chart(dff):
    dff=pd.DataFrame(dff.groupby('season')['n_matches'].sum()).reset_index()
    fig=px.line(dff,'season','n_matches',title='Analizando n_matches')
    return fig
############################

#Lista de elementos que puedo añadir:
#https://docs.taipy.io/en/latest/manuals/gui/viselements/controls/

def draw_court(color="black", lw=1, outer_lines=True, dic_stats=None ,year=None):
    """if ax is None:
        ax = plt.gca()"""
    fig, ax = plt.subplots()

    # Basketball Hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)
    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)
    # The paint
    # outer box
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # inner box
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Free Bottom Top Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    # Three Point Line
    corner_three_a = Rectangle((-220.2, -47.5), 0, 136.4, linewidth=lw, color=color)
    corner_three_b = Rectangle((220.2, -47.5), 0, 136.4, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
    #painting
    color_front='#f9cb9c'
    color_sides='#e58b2f'
    color_corners='#f9cb9c'
    three_point_line_wedge_right = Wedge((0, 0), 238, 22, 75, width=70, facecolor=color_sides)
    three_point_line_wedge_left = Wedge((0, 0), 238, 95, 158, width=70, facecolor=color_sides)
    three_point_line_wedge_front = Wedge((0, 0), 238, 70.5, 109.8, width=50, facecolor=color_front)
    front_rect=Rectangle((-80, 142.5), 160, 81, linewidth=1, color=color_front,fill=True)
    left_side_rect=Rectangle((-80, 88.9), -90, 60, linewidth=1, color=color_sides,fill=True)
    right_side_rect=Rectangle((80, 88.9), 90, 60, linewidth=1, color=color_sides,fill=True)
    right_corner_rect = Rectangle((220.2, -47.5), -140, 136.4, linewidth=1, color=color_corners,fill=True)
    left_corner_rect = Rectangle((-220.2, -47.5), 140, 136.4, linewidth=1, color=color_corners,fill=True,)
    # list of court shapes
    court_elements = [three_point_line_wedge_left,three_point_line_wedge_right,three_point_line_wedge_front,right_side_rect,right_corner_rect,left_side_rect,left_corner_rect,front_rect,hoop,outer_box ,backboard, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc,]
    #outer_lines=True
    if outer_lines:
        outer_lines = Rectangle((-275, -47.5), 550, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

    right_corner_three=dic_stats['right_corner_three']['in']        #CALCULAR IN / OUT Y PORCENTAJE Y AÑADIRLO A LA IMAGEN
    right_corner_middle=dic_stats['right_corner_middle']['in']
    right_side_three=dic_stats['right_side_three']['in']
    right_side_middle=dic_stats['right_side_middle']['in']
    front_three=dic_stats['front_three']['in']
    front_middle=dic_stats['front_middle']['in']
    left_side_three=dic_stats['left_side_three']['in']
    left_side_middle=dic_stats['left_side_middle']['in']
    left_corner_three=dic_stats['left_corner_three']['in']
    left_corner_middle=dic_stats['left_corner_middle']['in']
    zone=dic_stats['Zone']['in']


    ax.text(0, 185, front_middle, ha="center", va="center", fontsize=10)    #AÑADIR AQUI EL IN / OUT
    ax.text(0, 60, zone, ha="center", va="center", fontsize=10)
    ax.text(145, 140, right_side_middle, ha="center", va="center", fontsize=10)
    ax.text(-145, 140, left_side_middle, ha="center", va="center", fontsize=10)
    ax.text(-150, 20, left_corner_middle, ha="center", va="center", fontsize=10)
    ax.text(150, 20, right_corner_middle, ha="center", va="center", fontsize=10)
    ax.text(0, 260, front_three, ha="center", va="center", fontsize=10)
    ax.text(190, 180, right_side_three, ha="center", va="center", fontsize=10)
    ax.text(-190, 180, left_side_three, ha="center", va="center", fontsize=10)
    ax.text(-260, 0, left_corner_three, fontsize=10)
    ax.text(230, 0, right_corner_three, fontsize=10)

    ax.set_title(f'Shootings stats in {year}',color='white')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.patch.set_facecolor('white')
    fig.patch.set_facecolor('none')
    ax.plot()
    #plt.show()
    return fig


def on_selector(state):
    filtered_data = state.data.loc[
        state.data["City"].isin(state.city)
    ]

    state.fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
    state.fig_city_perc = create_perc_fig(filtered_data, 'City')
    state.fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
    state.fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')


player_career_stats=analysis.get_players_stats_career(player_id=2493108)
fig_line_chart=create_line_chart(player_career_stats)

dic_stats=analysis.get_shooting_info(player_id=2338790)
years=list(dic_stats.keys())

images=[]
for year in years:
    fig=draw_court(dic_stats=dic_stats[year],year=year)             
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    images.append(buf)



path=analysis.get_players_path(player_id=2493108)
player_info=analysis.get_player_info(player_id=2493108)
player_name=player_info.loc[0].player_name
edad=datetime.today().year - player_info.loc[0].birthday.year
ult_temp=path.loc[0].Temporada
ult_liga=path.loc[0].Categoría
position=player_info.loc[0].position
nacionalidad=player_info.loc[0].nationality


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
    tgb.text(player_name,class_name="h2 text-center")
    tgb.text('--------------------------------------',class_name="h1 text-center")
    with tgb.layout("1 1 1 1 1"):
        with tgb.part():
            tgb.text(f'Edad',class_name="h3 text-center")
            tgb.text(f'{edad} años',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Última temporada',class_name="h3 text-center")
            tgb.text(f'{ult_temp}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Última liga',class_name="h3 text-center")
            tgb.text(f'{ult_liga}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Posición',class_name="h3 text-center")
            tgb.text(f'{position}',class_name="h3 text-center")
        with tgb.part():
            tgb.text(f'Nacionalidad',class_name="h3 text-center")
            tgb.text(f'{nacionalidad}',class_name="h3 text-center")
    
    tgb.text('--------------------------------------',class_name="h1 text-center")
    tgb.table("{path}")
    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.image(images[0].getvalue(),width=10,label='Shootings')
        with tgb.part():
            tgb.image(images[1].getvalue(),width=10,label='Shootings')
        with tgb.part():
            tgb.image(images[2].getvalue(),width=10,label='Shootings')
    tgb.chart(figure="{fig_line_chart}",)
    table=tgb.table("{player_career_stats}")
    table.align = "center"
"""
        with tgb.part():
            tgb.text("Average Sales", class_name="h2")
            tgb.text("{int(data['Total'].mean())}", class_name="h3")

        with tgb.part():
            tgb.text("Mean Rating", class_name="h2")
            tgb.text("{int(data['Rating'].mean())}", class_name="h3")
#
    #tgb.image(buf.getvalue())
    tgb.chart(figure="{fig_line_chart}")
#
    #tgb.chart(figure="{fig_map}")

    with tgb.layout("1 1 1"):
        tgb.chart(figure="{fig_product_line}")
        tgb.chart(figure="{fig_city}")
        tgb.chart(figure="{fig_customer_type}")
    
    tgb.chart(figure="{fig_time}")
    tgb.chart(figure="{fig_date}")

    tgb.text("Analysis", class_name="h2")

    tgb.selector(value="{city}", lov=["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang", "Yangon", "Naypyitaw"],
                 dropdown=True,
                 multiple=True,
                 label="Select cities",
                 class_name="fullwidth",
                 on_change=on_selector)

    with tgb.layout("1 1 1"):
        tgb.image(buf.getvalue(),width=1000,label='Shootings')
        tgb.chart(figure="{fig_product_line_perc}")
        tgb.chart(figure="{fig_gender_perc}")
        tgb.chart(figure="{fig_customer_type_perc}")

    tgb.table("{data}")

"""

gui = Gui(player_home)
gui.run(title='Sales',port=2425)

