from taipy.gui import notify
import plotly.express as px
from utils import analysis
from utils import processer
from utils import shootings


def new_player(state, player_id):
    try:
        # New player id
        state.player_id = player_id
        player_stats = analysis.PlayerStats(player_id)

        # Personal info -------------------------------------------------------
        player_info = player_stats.info_query()
        player_name = player_info['player_name'].upper()
        state.name = player_name
        state.age = player_info['age']
        state.position = player_info['position']
        state.nationality = player_info['nationality']
        
        player_image, player_image_width, player_image_height = analysis\
            .get_player_image(player_id)
        
        state.player_image_height = player_image_height
        state.player_image_width = player_image_width
        state.player_image = player_image

        player_path = player_stats.path()
        try:
            state.last_season = player_path.loc[0].SEASON
            state.last_league = player_path.loc[0].LEAGUE
        except Exception:
            state.last_season = '-'
            state.last_league = '-'

        # Player Path ---------------------------------------------------------
        state.player_path = player_path
        
        # Shootings images ----------------------------------------------------
        image_1, image_2, image_3 = shootings.shootings_images(player_stats)
        
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
        player_stats = analysis.PlayerStats(player_id)
        mode = state.stat_mode

        if mode == 'AVERAGE':
            state.player_stats_table = player_stats.stats_avg_table()

        elif mode == 'TOTAL':
            state.player_stats_table = player_stats.stats_total_table()
        # Modify chart figure to show info with the current mode
        on_selector(state)
    except Exception:
        print('Error in on_mode')


def on_selector(state):
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
            dff = processer.proccess_df_avg(df)
        elif stat_mode == 'TOTAL':
            dff = processer.proccess_df_total(df)

        dff = dff.reset_index()
        dff = dff.sort_values("SEASON")
        print('len dff is: ',len(dff))
        if len(dff) > 1:
            fig = px.line(data_frame=dff, x='SEASON',
                          y=stats_to_show, title=title)
        else:
            fig = px.bar(data_frame=dff, x='SEASON',
                         y=stats_to_show, title=title)
    except Exception as e:
        print('Error in create_fig ',e)
    return fig
