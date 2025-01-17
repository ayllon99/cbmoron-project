from utils.analysis import *
from utils.scraper import *
from utils.show_data import *


# Player Scraper default ------------------------------------------------------
season_scraping = "2023/24"
league_scraping = "LEB ORO"
n_matches = None
min_avg = None
points_avg = None
twos_in_avg = None
twos_tried_avg = None
twos_perc = None
threes_in_avg = None
threes_tried_avg = None
threes_perc = None
field_goals_in_avg = None
field_goals_tried_avg = None
field_goals_perc = None
free_throws_in_avg = None
free_throws_tried_avg = None
free_throws_perc = None
offensive_rebounds_avg = None
deffensive_rebounds_avg = None
total_rebounds_avg = None
assists_avg = None
turnovers_avg = None
blocks_favor_avg = None
blocks_against_avg = None
dunks_avg = None
personal_fouls_avg = None
fouls_received_avg = None
efficiency_avg = None

stats_dict = {
        "n_matches": 15,
        "points_avg": 12,
        'min_avg': 12,
        "twos_in_avg": 1,
        "twos_tried_avg": 5}


player_scraper = PlayerScraper(stats_dict, season_scraping, league_scraping)
players_scraped = player_scraper.querying()
players_scraped = players_scraped
scraper_instructions = ''
# Lists used in Scraper AND Analysis ------------------------------------------
leagues_list = ['LEB ORO', 'LEB PLATA', 'LIGA EBA']
seasons_list = ['2023/24', '2022/23', '2021/22', '2020/21', '2019/20',
                '2018/19', '2017/18', '2016/17', '2015/16']

# Player Analysis default -----------------------------------------------------
league_analysis = 'LEB ORO'
season_analysis = None
team_analysis = None
player_analysis = None
player_id_selected = None
teams_list = []
players_list = []

# Empty by default
team_ids_dict = ''
player_ids_dict = ''

# Player Analysis by default = Marc Gasol -------------------------------------
# Marc Gasol id
player_id = 360978
player_stats = PlayerStats(player_id)

# Personal info + path
player_stats.info()
name = player_stats.player_name
age = player_stats.age
position = player_stats.position
nationality = player_stats.nationality

player_path = player_stats.path()

last_season = player_stats.last_season
last_league = player_stats.last_league

player_image = player_stats.player_image()
player_image_width = player_stats.player_image_width
player_image_height = player_stats.player_image_height


# Shootings
image_1, image_2, image_3 = player_stats.shootings_images()

# Table stats
stat_mode = 'AVERAGE'
player_stats_table = player_stats.stats_avg_table()

# Chart
list_of_stats = list(player_stats_table.columns)
stats_columns = [x for x in list_of_stats if x not in
                 ['MIN', 'SEASON', 'TEAM_NAME_EXTENDED',
                  'STAGE_NAME_EXTENDED']]
# Stat to show by default
stats_to_show = ['POINTS']
figg = create_fig(player_stats_table, stats_to_show, stat_mode)

