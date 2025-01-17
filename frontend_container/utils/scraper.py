from utils.show_data import new_player
from utils.analysis import PlayerScraper, SearchPlayer
from taipy.gui import notify


# Player Scraping
def submit_stats(state):
    notify(state, notification_type='I',
           message='Matching players with those stats or higher')
    
    stats_dict = {
        'n_matches': state.n_matches,
        'min_avg': state.min_avg,
        'points_avg': state.points_avg,
        'twos_in_avg': state.twos_in_avg,
        'twos_tried_avg': state.twos_tried_avg,
        'twos_perc': state.twos_perc,
        'threes_in_avg': state.threes_in_avg,
        'threes_tried_avg': state.threes_tried_avg,
        'threes_perc': state.threes_perc,
        'field_goals_in_avg': state.field_goals_in_avg,
        'field_goals_tried_avg': state.field_goals_tried_avg,
        'field_goals_perc': state.field_goals_perc,
        'free_throws_in_avg': state.free_throws_in_avg,
        'free_throws_tried_avg': state.free_throws_tried_avg,
        'free_throws_perc': state.free_throws_perc,
        'offensive_rebounds_avg': state.offensive_rebounds_avg,
        'deffensive_rebounds_avg': state.deffensive_rebounds_avg,
        'total_rebounds_avg': state.total_rebounds_avg,
        'assists_avg': state.assists_avg,
        'turnovers_avg': state.turnovers_avg,
        'blocks_favor_avg': state.blocks_favor_avg,
        'blocks_against_avg': state.blocks_against_avg,
        'dunks_avg': state.dunks_avg,
        'personal_fouls_avg': state.personal_fouls_avg,
        'fouls_received_avg': state.fouls_received_avg,
        'efficiency_avg': state.efficiency_avg
    }

    season = state.season_scraping
    league = state.league_scraping

    player_scraper = PlayerScraper(stats_dict, season, league)
    
    try:
        players_scraped = player_scraper.querying()
        state.players_scraped = players_scraped
        state.scraper_instructions = 'Click a row to select the player'
        notify(state, notification_type='success',
           message='Some players found!')
    except:
        state.scraper_instructions = ''
        notify(state, notification_type='error',
           message='No players with those stats were found')


def clear_button(state):
    state.n_matches = None
    state.min_avg = None
    state.points_avg = None
    state.twos_in_avg = None
    state.twos_tried_avg = None
    state.twos_perc = None
    state.threes_in_avg = None
    state.threes_tried_avg = None
    state.threes_perc = None
    state.field_goals_in_avg = None
    state.field_goals_tried_avg = None
    state.field_goals_perc = None
    state.free_throws_in_avg = None
    state.free_throws_tried_avg = None
    state.free_throws_perc = None
    state.offensive_rebounds_avg = None
    state.deffensive_rebounds_avg = None
    state.total_rebounds_avg = None
    state.assists_avg = None
    state.turnovers_avg = None
    state.blocks_favor_avg = None
    state.blocks_against_avg = None
    state.dunks_avg = None
    state.personal_fouls_avg = None
    state.fouls_received_avg = None
    state.efficiency_avg = None


def scraper_triggered(state, var_name, payload):
    table = state.players_scraped
    player_id = int(table.loc[payload['index'],'player_id'])
    notify(state, notification_type='I',
           message='Analyzing selected player')
    new_player(state, player_id)


#Player Analysis
def league_function(state):
    state.teams_list = []
    state.players_list = []
    state.season_analysis = None
    state.team_analysis = None
    state.player_analysis = None
    

def season_function(state):
    state.teams_list = []
    state.players_list = []
    state.team_analysis = None
    state.player_analysis = None
    searching = SearchPlayer()
    league = state.league_analysis
    season = state.season_analysis[2:]
    
    team_ids_dict, teams_list = searching.on_change_season(league=league,
                                                           season=season)
    state.team_ids_dict = team_ids_dict
    state.teams_list = teams_list


def team_function(state):
    state.player_analysis = None
    searching = SearchPlayer()
    team_ids_dict = dict(dict(state.team_ids_dict)['team_id'])
    team_selected = state.team_analysis
    team_id = team_ids_dict[team_selected]
    player_ids_dict, players_list = searching.on_change_team(team_id)
    state.players_list = players_list
    state.player_ids_dict = player_ids_dict


def player_function(state):
    player_name = state.player_analysis
    player_ids_dict = dict(dict(state.player_ids_dict)['player_id'])
    player_id = player_ids_dict[player_name]
    notify(state, notification_type='I',
           message='Analyzing selected player')
    new_player(state, player_id)
