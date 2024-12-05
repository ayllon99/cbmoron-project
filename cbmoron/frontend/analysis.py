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


data_not_found_path=r'C:\Users\Jose\Desktop\New folder\Proyectos_Python\cbmoron-project\cbmoron\frontend\data_not_found.png'


def draw_court(color="black", lw=1, outer_lines=True, dic_stats=None ,year=None):
    
    fig, ax = plt.subplots()
    if year in dic_stats.keys():
        # Basketball Hoop
        hoop = Circle((0,-20), radius=7.5, linewidth=lw, color=color, fill=False)
        # Backboard
        backboard = Rectangle((-30, -32.5), 60, 0, linewidth=lw, color=color)
        # The paint
        # Outer box
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
        # Inner box
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
        # Free Throw Top Arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
        # Free Bottom Top Arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
        # Restricted Zone
        restricted = Arc((0, -20), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
        # Three Point Line
        corner_three_a = Rectangle((-220.2, -47.5), 0, 136.4, linewidth=lw, color=color)
        corner_three_b = Rectangle((220.2, -47.5), 0, 136.4, linewidth=lw, color=color)
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
        # Center Court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
        # Painting
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
    
        court_elements = [three_point_line_wedge_left,three_point_line_wedge_right,three_point_line_wedge_front,right_side_rect,right_corner_rect,left_side_rect,left_corner_rect,front_rect,hoop,outer_box ,backboard, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc,]
        
        if outer_lines:
            outer_lines = Rectangle((-275, -47.5), 550, 470, linewidth=lw, color='white', fill=False)
            court_elements.append(outer_lines)

        for element in court_elements:
            ax.add_patch(element)
        
        try:
            right_corner_three_total=f"{dic_stats[year]['Right Corner Three']['in']}/{dic_stats[year]['Right Corner Three']['tried']}"
            right_corner_three=f'{round((int(dic_stats[year]['Right Corner Three']['in'])/int(dic_stats[year]['Right Corner Three']['tried']))*100,2)}%'
        except:
            right_corner_three_total=f"{dic_stats[year]['Right Corner Three']['in']}/{dic_stats[year]['Right Corner Three']['tried']}"
            right_corner_three='0%'
        try:
            right_corner_middle_total=f"{dic_stats[year]['Right Corner Middle']['in']}/{dic_stats[year]['Right Corner Middle']['tried']}"
            right_corner_middle=f'{round((int(dic_stats[year]['Right Corner Middle']['in'])/int(dic_stats[year]['Right Corner Middle']['tried']))*100,2)}%'
        except:
            right_corner_middle_total=f"{dic_stats[year]['Right Corner Middle']['in']}/{dic_stats[year]['Right Corner Middle']['tried']}"
            right_corner_middle='0%'
        try:
            right_side_three_total=f"{dic_stats[year]['Right Side Three']['in']}/{dic_stats[year]['Right Side Three']['tried']}"
            right_side_three=f'{round((int(dic_stats[year]['Right Side Three']['in'])/int(dic_stats[year]['Right Side Three']['tried']))*100,2)}%'
        except:
            right_side_three_total=f"{dic_stats[year]['Right Side Three']['in']}/{dic_stats[year]['Right Side Three']['tried']}"
            right_side_three='0%'
        try:
            right_side_middle_total=f"{dic_stats[year]['Right Side Middle']['in']}/{dic_stats[year]['Right Side Middle']['tried']}"
            right_side_middle=f'{round((int(dic_stats[year]['Right Side Middle']['in'])/int(dic_stats[year]['Right Side Middle']['tried']))*100,2)}%'
        except:
            right_side_middle_total=f"{dic_stats[year]['Right Side Middle']['in']}/{dic_stats[year]['Right Side Middle']['tried']}"
            right_side_middle='0%'
        try:
            front_three_total=f"{dic_stats[year]['Front Three']['in']}/{dic_stats[year]['Front Three']['tried']}"
            front_three=f'{round((int(dic_stats[year]['Front Three']['in'])/int(dic_stats[year]['Front Three']['tried']))*100,2)}%'
        except:
            front_three_total=f"{dic_stats[year]['Front Three']['in']}/{dic_stats[year]['Front Three']['tried']}"
            front_three='0%'
        try:
            front_middle_total=f"{dic_stats[year]['Front Middle']['in']}/{dic_stats[year]['Front Middle']['tried']}"
            front_middle=f'{round((int(dic_stats[year]['Front Middle']['in'])/int(dic_stats[year]['Front Middle']['tried']))*100,2)}%'
        except:
            front_middle_total=f"{dic_stats[year]['Front Middle']['in']}/{dic_stats[year]['Front Middle']['tried']}"
            front_middle='0%'
        try:
            left_side_three_total=f"{dic_stats[year]['Left Side Three']['in']}/{dic_stats[year]['Left Side Three']['tried']}"
            left_side_three=f'{round((int(dic_stats[year]['Left Side Three']['in'])/int(dic_stats[year]['Left Side Three']['tried']))*100,2)}%'
        except:
            left_side_three_total=f"{dic_stats[year]['Left Side Three']['in']}/{dic_stats[year]['Left Side Three']['tried']}"
            left_side_three='0%'
        try:
            left_side_middle_total=f"{dic_stats[year]['Left Side Middle']['in']}/{dic_stats[year]['Left Side Middle']['tried']}"
            left_side_middle=f'{round((int(dic_stats[year]['Left Side Middle']['in'])/int(dic_stats[year]['Left Side Middle']['tried']))*100,2)}%'
        except:
            left_side_middle_total=f"{dic_stats[year]['Left Side Middle']['in']}/{dic_stats[year]['Left Side Middle']['tried']}"
            left_side_middle='0%'
        try:
            left_corner_three_total=f"{dic_stats[year]['Left Corner Three']['in']}/{dic_stats[year]['Left Corner Three']['tried']}"
            left_corner_three=f'{round((int(dic_stats[year]['Left Corner Three']['in'])/int(dic_stats[year]['Left Corner Three']['tried']))*100,2)}%'
        except:
            left_corner_three_total=f"{dic_stats[year]['Left Corner Three']['in']}/{dic_stats[year]['Left Corner Three']['tried']}"
            left_corner_three='0%'
        try:
            left_corner_middle_total=f"{dic_stats[year]['Left Corner Middle']['in']}/{dic_stats[year]['Left Corner Middle']['tried']}"
            left_corner_middle=f'{round((int(dic_stats[year]['Left Corner Middle']['in'])/int(dic_stats[year]['Left Corner Middle']['tried']))*100,2)}%'
        except:
            left_corner_middle_total=f"{dic_stats[year]['Left Corner Middle']['in']}/{dic_stats[year]['Left Corner Middle']['tried']}"
            left_corner_middle='0%'
        try:
            zone_total=f"{dic_stats[year]['Zone']['in']}/{dic_stats[year]['Zone']['tried']}"
            zone=f'{round((int(dic_stats[year]['Zone']['in'])/int(dic_stats[year]['Zone']['tried']))*100,2)}%'
        except:
            zone_total=f"{dic_stats[year]['Zone']['in']}/{dic_stats[year]['Zone']['tried']}"
            zone='0%'
        
        ax.text(0, 60, zone, ha="center", va="center", fontsize=10)
        ax.text(0,40,zone_total,ha="center", va="center", fontsize=10)

        ax.text(0, 185, front_middle, ha="center", va="center", fontsize=10)
        ax.text(0,165,front_middle_total,ha="center", va="center", fontsize=10)

        ax.text(145, 140, right_side_middle, ha="center", va="center", fontsize=10)
        ax.text(145,120,right_side_middle_total,ha="center", va="center", fontsize=10)

        ax.text(-145, 140, left_side_middle, ha="center", va="center", fontsize=10)
        ax.text(-145,120,left_side_middle_total,ha="center", va="center", fontsize=10)

        ax.text(-150, 20, left_corner_middle, ha="center", va="center", fontsize=10)
        ax.text(-150,0,left_corner_middle_total,ha="center", va="center", fontsize=10)

        ax.text(150, 20, right_corner_middle, ha="center", va="center", fontsize=10)
        ax.text(150,0,right_corner_middle_total,ha="center", va="center", fontsize=10)

        ax.text(0, 280, front_three, ha="center", va="center", fontsize=10)
        ax.text(0, 260, front_three_total, ha="center", va="center", fontsize=10)

        ax.text(210, 180, right_side_three, ha="center", va="center", fontsize=10)
        ax.text(210, 160, right_side_three_total, ha="center", va="center", fontsize=10)

        ax.text(-210, 180, left_side_three, ha="center", va="center", fontsize=10)
        ax.text(-210, 160, left_side_three_total, ha="center", va="center", fontsize=10)

        ax.text(-280, 0, left_corner_three, fontsize=10)
        ax.text(-280, -20, left_corner_three_total, fontsize=10)

        ax.text(230, 0, right_corner_three, fontsize=10)
        ax.text(230, -20, right_corner_three_total, fontsize=10)
        
        ax.set_title(f'Shootings stats in {year}/{year+1}',color='white')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.patch.set_facecolor('white')
        fig.patch.set_facecolor('none')
        ax.plot()
        #plt.show()
    else:
        img = mpimg.imread(data_not_found_path)
        ax.imshow(img)
        ax.set_title(f'Shootings stats in {year}/{year+1}',color='white')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.patch.set_facecolor('white')
        fig.patch.set_facecolor('none')
        ax.plot()
        
    return fig






class PlayerStats:
    def __init__(self, player_id):
        self.player_id = player_id
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname='cbmoron_database',
            host='localhost',
            user='root',
            password='root'
        )
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def get_shooting_query(self):
        self.connect()
        params = [self.player_id]
        self.cur.execute("""
            SELECT season, shoot_from, success, COUNT(*)
            FROM shootings
            LEFT JOIN results
            ON shootings.match_id = results.match_id
            WHERE player_id = %s
            GROUP BY season, shoot_from, success
            ORDER BY season, shoot_from DESC
        """, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['season', 'shoot_from', 'success', 'total']
        self.close_connection()
        return df

    def get_shooting_stats(self):
        df = self.get_shooting_query()
        stats = {}
        for year in df['season'].unique():
            stats[year] = {}
            stats[year]['Zone'] = {'in': 0, 'out': 0}
            stats[year]['Right Corner Three'] = {'in': 0, 'out': 0}
            stats[year]['Right Corner Middle'] = {'in': 0, 'out': 0}
            stats[year]['Right Side Three'] = {'in': 0, 'out': 0}
            stats[year]['Right Side Middle'] = {'in': 0, 'out': 0}
            stats[year]['Front Three'] = {'in': 0, 'out': 0}
            stats[year]['Front Middle'] = {'in': 0, 'out': 0}
            stats[year]['Left Side Three'] = {'in': 0, 'out': 0}
            stats[year]['Left Side Middle'] = {'in': 0, 'out': 0}
            stats[year]['Left Corner Three'] = {'in': 0, 'out': 0}
            stats[year]['Left Corner Middle'] = {'in': 0, 'out': 0}
        for row in range(len(df)):
            success = df.loc[row].success
            if success:
                stats[df.loc[row].season][df.loc[row].shoot_from]['in'] = df.loc[row].total
            else:
                stats[df.loc[row].season][df.loc[row].shoot_from]['out'] = df.loc[row].total
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
        keys = list(new_stats.keys())
        keys.sort(reverse=True)
        if len(keys) > 0:
            years = [keys[0], keys[0] - 1, keys[0] - 2]
        else:
            years = [datetime.today().year, datetime.today().year - 1, datetime.today().year - 2]
        return new_stats, years

    def info_query(self):
        self.connect()
        params = [self.player_id]
        self.cur.execute("""
            SELECT player_id, player_name, position, birthday, nationality FROM public.players_info
            WHERE player_id = %s
        """, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['player_id', 'player_name', 'position', 'birthday','nationality']
        birthday=df.loc[0].birthday
        today = datetime.today()  
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        dict_df={'player_id': df.loc[0].player_id, 'player_name': df.loc[0].player_name, 'position': df.loc[0].position, 'age': age, 'nationality': df.loc[0].nationality}
        self.close_connection()
        return dict_df
    

# Example usage:
player_stats = PlayerStats(2274861)
stats, years = player_stats.get_shooting_stats()
player_info=player_stats.info_query()

