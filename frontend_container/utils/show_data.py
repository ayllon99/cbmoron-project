from taipy.gui import notify
import plotly.express as px
from utils.analysis import *
from utils.processer import *


def new_player(state, player_id):
    try:
        # New player id
        state.player_id = player_id
        player_stats = PlayerStats(player_id)

        # Personal info + path -------------------------------------------------------
        player_stats.info()
        state.name = player_stats.player_name
        state.age = player_stats.age
        state.position = player_stats.position
        state.nationality = player_stats.nationality

        state.player_path = player_stats.path()

        state.last_season = player_stats.last_season
        state.last_league = player_stats.last_league
        
        state.player_image = player_stats.player_image()
        state.player_image_height = player_stats.player_image_height
        state.player_image_width = player_stats.player_image_width

        # Shootings images ----------------------------------------------------
        image_1, image_2, image_3 = player_stats.shootings_images()
        
        state.image_1 = image_1
        state.image_2 = image_2
        state.image_3 = image_3

        # Table stats ---------------------------------------------------------
        # Stat mode return to default
        state.stat_mode = 'AVERAGE'
        player_stats_table = player_stats.stats_avg_table()
        state.player_stats_table = player_stats_table

        # Chart ---------------------------------------------------------------
        list_of_stats = list(player_stats_table.columns)

        state.stats_columns = [x for x in list_of_stats if x not in
                               ['MIN', 'SEASON', 'TEAM_NAME_EXTENDED',
                               'STAGE_NAME_EXTENDED']]
        #Stat to show return to default
        state.stats_to_show = ['POINTS']
        state.figg = create_fig(player_stats_table, ['POINTS'], 'AVERAGE')
        notify(state, notification_type='success',
           message=f'Stats available!')
    except Exception as e:
        print('Error in new_player---- ', e)
        notify(state=state, notification_type='error',
               message='Error getting the data of this player')


def on_mode(state):
    try:
        player_id = state.player_id
        player_stats = PlayerStats(player_id)
        mode = state.stat_mode

        if mode == 'AVERAGE':
            state.player_stats_table = player_stats.stats_avg_table()

        elif mode == 'TOTAL':
            state.player_stats_table = player_stats.stats_total_table()
        # Modify chart figure to show info with the current mode
        on_stats_selector(state)
    except Exception:
        print('Error in on_mode')


def on_stats_selector(state):
    try:
        stats_to_show = state.stats_to_show
        mode = state.stat_mode
        df = state.player_stats_table

        state.figg = create_fig(df, stats_to_show, mode)
    except Exception as e:
        print('Error in on_selector ',e)


def create_fig(df, stats_to_show, stat_mode):
    try:
        if len(stats_to_show) > 1:
            stats = ', '.join([f'{col}' for col in stats_to_show])
        else:
            stats = stats_to_show[0]
        title = f'{stats} IN {stat_mode} BY SEASON'
        
        title = title.upper()
        if stat_mode == 'AVERAGE':
            dff = proccess_df_avg(df)
        elif stat_mode == 'TOTAL':
            dff = proccess_df_total(df)

        dff = dff.reset_index()
        dff = dff.sort_values("SEASON")
        
        if len(dff) > 1:
            fig = px.line(data_frame=dff, x='SEASON',
                          y=stats_to_show, title=title)
        else:
            season = dff.loc[0].SEASON
            title = f'{stats} IN {stat_mode} BY 20{season}'
            melted_df = pd.melt(dff, id_vars=[], value_vars=stats_to_show)
            fig = px.bar(data_frame=melted_df, x='variable', y='value',
                         title=title)
    except Exception as e:
        print('Error in create_fig ',e)
        # Return empty figure to show no data
    return fig
