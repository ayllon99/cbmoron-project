from taipy.gui import Gui,notify
import taipy as tp
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
import io
from datetime import datetime




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

    """right_corner_three=dic_stats['right_corner_three']['in']        #CALCULAR IN / OUT Y PORCENTAJE Y AÑADIRLO A LA IMAGEN
    right_corner_middle=dic_stats['right_corner_middle']['in']
    right_side_three=dic_stats['right_side_three']['in']
    right_side_middle=dic_stats['right_side_middle']['in']
    front_three=dic_stats['front_three']['in']
    front_middle=dic_stats['front_middle']['in']
    left_side_three=dic_stats['left_side_three']['in']
    left_side_middle=dic_stats['left_side_middle']['in']
    left_corner_three=dic_stats['left_corner_three']['in']
    left_corner_middle=dic_stats['left_corner_middle']['in']
    zone=dic_stats['Zone']['in']"""

    #######Delete####
    right_corner_three=1        #CALCULAR IN / OUT Y PORCENTAJE Y AÑADIRLO A LA IMAGEN
    right_corner_middle=2
    right_side_three=3
    right_side_middle=4
    front_three=5
    front_middle=6
    left_side_three=7
    left_side_middle=8
    left_corner_three=9
    left_corner_middle=10
    zone=11
    ################################

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
    plt.show()
    return fig



draw_court()