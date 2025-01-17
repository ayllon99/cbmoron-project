import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from minio import Minio
from PIL import Image
import io
from utils.shootings import generate_image
from utils.variables import config


class PlayerScraper:
    """
    Connected to postgres database to return players based on a stats inputted 
    """
    def __init__(self, stats_dict, season, league):
        # Variables to access to data
        self.postgres_database = config['postgres_database']
        self.postgres_host = config['postgres_host']
        self.postgres_user = config['postgres_user']
        self.postgres_pass = config['postgres_pass']
        self.conn = None
        self.cur = None
        # Data
        self.stats_dict = stats_dict
        self.season = season[2:]
        self.league = league

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.postgres_database,
            host=self.postgres_host,
            user=self.postgres_user,
            password=self.postgres_pass
        )
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def _create_query(self):
        
        if self.stats_dict['min_avg'] is not None:
            min_avg = int(self.stats_dict['min_avg'])
            clause = f"min_avg >= %s AND "
            min_param = timedelta(hours=0, minutes=min_avg, seconds=0)
        else:
            clause = ''
            min_param = None

        stats_dict = {key: value for key, value in self.stats_dict.items()
                    if value is not None and key != 'min_avg'}

        query = " AND ".join(f"{key} >= %s" for key in stats_dict.keys())
        where_clause = clause + query
        params = list(stats_dict.values())
        params.insert(0, self.season)
        if where_clause:
            where_clause = "WHERE " + where_clause

        if min_param is not None:
            params.insert(1, min_param)

        if self.league is not None:
            league_clause = "WHERE pcp.league = %s"
            params.append(self.league)
        else:
            league_clause = ""

        return where_clause, league_clause, params

    def _get_query(self, where_clause, league_clause, params):
            
        full_query = f"""
            WITH temporal AS(
                SELECT season, player_id,
                SUM(n_matches) AS n_matches,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN '00:00'
                    WHEN SUM(n_matches)!=0
                        THEN DATE_TRUNC('second', '00:00:00' +
                                        (SUM(EXTRACT(EPOCH FROM min_avg)
                                            * n_matches) / SUM(n_matches))
                                        * INTERVAL '1 second')
                END AS min_avg,
                CASE
                WHEN SUM(n_matches)=0
                        THEN 0
                WHEN SUM(n_matches)!=0
                        THEN SUM(points_avg*n_matches)/SUM(n_matches)
                END AS points_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(twos_in_avg*n_matches)/SUM(n_matches)
                END AS twos_in_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(twos_tried_avg*n_matches)/SUM(n_matches)
                END AS twos_tried_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(twos_perc*n_matches)/SUM(n_matches)
                END AS twos_perc,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(threes_in_avg*n_matches)/SUM(n_matches)
                END AS threes_in_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(threes_tried_avg*n_matches)/SUM(n_matches)
                END AS threes_tried_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(threes_perc*n_matches)/SUM(n_matches)
                END AS threes_perc,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(field_goals_in_avg*n_matches)/SUM(n_matches)
                END AS field_goals_in_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(field_goals_tried_avg*n_matches) /
                            SUM(n_matches)
                END AS field_goals_tried_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(field_goals_perc*n_matches)/SUM(n_matches)
                END AS field_goals_perc,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(free_throws_in_avg*n_matches)/SUM(n_matches)
                END AS free_throws_in_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(free_throws_tried_avg*n_matches) /
                            SUM(n_matches)
                END AS free_throws_tried_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(free_throws_perc*n_matches)/SUM(n_matches)
                END AS free_throws_perc,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(offensive_rebounds_avg*n_matches) /
                            SUM(n_matches)
                END AS offensive_rebounds_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(deffensive_rebounds_avg*n_matches) /
                            SUM(n_matches)
                END AS deffensive_rebounds_avg,
                CASE
                    WHEN SUM(n_matches)=0
                        THEN 0
                    WHEN SUM(n_matches)!=0
                        THEN SUM(total_rebounds_avg*n_matches)/SUM(n_matches)
                END AS total_rebounds_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(assists_avg*n_matches)/SUM(n_matches)
                END AS assists_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(turnovers_avg*n_matches)/SUM(n_matches)
                END AS turnovers_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(blocks_favor_avg*n_matches)/SUM(n_matches)
                END AS blocks_favor_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(blocks_against_avg*n_matches)/SUM(n_matches)
                END AS blocks_against_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(dunks_avg*n_matches)/SUM(n_matches)
                END AS dunks_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(personal_fouls_avg*n_matches)/SUM(n_matches)
                END AS personal_fouls_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(fouls_received_avg*n_matches)/SUM(n_matches)
                END AS fouls_received_avg,
                CASE
                    WHEN SUM(n_matches)=0
                    THEN 0
                    WHEN SUM(n_matches)!=0
                    THEN SUM(efficiency_avg*n_matches)/SUM(n_matches)
                END AS efficiency_avg
                FROM players_stats_career
                WHERE season = %s
                GROUP BY season, player_id
                ORDER BY season, player_id DESC),
            stats_table AS(
                SELECT *
                FROM temporal
                {where_clause} ),
            stats_path_table AS(
                SELECT pcp.league,pcp.team_name,st.season,st.player_id AS player_id,
                        st.n_matches,st.min_avg,
                        st.points_avg,st.twos_in_avg,
                        st.twos_tried_avg,st.twos_perc,
                        st.threes_in_avg,st.threes_tried_avg,
                        st.threes_perc,st.field_goals_in_avg,
                        st.field_goals_tried_avg,st.field_goals_perc,
                        st.free_throws_in_avg,st.free_throws_tried_avg,
                        st.free_throws_perc,st.offensive_rebounds_avg,
                        st.deffensive_rebounds_avg,st.total_rebounds_avg,
                        st.assists_avg,st.turnovers_avg,st.blocks_favor_avg,
                        st.blocks_against_avg,st.dunks_avg,
                        st.personal_fouls_avg,st.fouls_received_avg,st.efficiency_avg
                FROM stats_table AS st
                LEFT JOIN players_career_path AS pcp
                ON st.player_id = pcp.player_id AND st.season = pcp.season
                {league_clause})

            SELECT spt.player_id,player_name,season,team_name,n_matches,min_avg,points_avg,
                twos_in_avg,twos_tried_avg,twos_perc,threes_in_avg,
                threes_tried_avg,threes_perc,field_goals_in_avg,
                field_goals_tried_avg,field_goals_perc,free_throws_in_avg,
                free_throws_tried_avg,free_throws_perc,offensive_rebounds_avg,
                deffensive_rebounds_avg,total_rebounds_avg,assists_avg,
                turnovers_avg,blocks_favor_avg,blocks_against_avg,dunks_avg,
                personal_fouls_avg,fouls_received_avg,efficiency_avg
            FROM stats_path_table AS spt
            LEFT JOIN players_info as pi
            ON spt.player_id = pi.player_id
            """

        self.cur.execute(full_query, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['player_id', 'player_name', 'season', 'team_name',
                    'n_matches', 'min_avg', 'points_avg',
                    'twos_in_avg', 'twos_tried_avg', 'twos_perc',
                    'threes_in_avg', 'threes_tried_avg', 'threes_perc',
                    'field_goals_in_avg', 'field_goals_tried_avg',
                    'field_goals_perc', 'free_throws_in_avg',
                    'free_throws_tried_avg', 'free_throws_perc',
                    'offensive_rebounds_avg',	'deffensive_rebounds_avg',
                    'total_rebounds_avg', 'assists_avg', 'turnovers_avg',
                    'blocks_favor_avg', 'blocks_against_avg', 'dunks_avg',
                    'personal_fouls_avg', 'fouls_received_avg',
                    'efficiency_avg']
        return df

    def _proccess_df(self, df):
        df['player_name'] = df['player_name'].apply(lambda x: x.upper())
        df['n_matches'] = df['n_matches'].apply(lambda x: int(x))
        df['min_avg'] = df['min_avg']\
            .apply(lambda x: (datetime(1900, 1, 1) + x).time()
                   .strftime("%M:%S"))
        df['points_avg'] = df['points_avg'].apply(lambda x: round(x, 2))
        df['twos_in_avg'] = df['twos_in_avg'].apply(lambda x: round(x, 2))
        df['twos_tried_avg'] = df['twos_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['twos_perc'] = df['twos_perc'].apply(lambda x: round(float(x), 2))
        df['threes_in_avg'] = df['threes_in_avg'].apply(lambda x: round(x, 2))
        df['threes_tried_avg'] = df['threes_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['threes_perc'] = df['threes_perc']\
            .apply(lambda x: round(float(x), 2))
        df['field_goals_in_avg'] = df['field_goals_in_avg']\
            .apply(lambda x: round(x, 2))
        df['field_goals_tried_avg'] = df['field_goals_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['field_goals_perc'] = df['field_goals_perc']\
            .apply(lambda x: round(float(x), 2))
        df['free_throws_in_avg'] = df['free_throws_in_avg']\
            .apply(lambda x: round(x, 2))
        df['free_throws_tried_avg'] = df['free_throws_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['free_throws_perc'] = df['free_throws_perc']\
            .apply(lambda x: round(float(x), 2))
        df['offensive_rebounds_avg'] = df['offensive_rebounds_avg']\
            .apply(lambda x: round(x, 2))
        df['deffensive_rebounds_avg'] = df['deffensive_rebounds_avg']\
            .apply(lambda x: round(x, 2))
        df['total_rebounds_avg'] = df['total_rebounds_avg']\
            .apply(lambda x: round(x, 2))
        df['assists_avg'] = df['assists_avg'].apply(lambda x: round(x, 2))
        df['turnovers_avg'] = df['turnovers_avg'].apply(lambda x: round(x, 2))
        df['blocks_favor_avg'] = df['blocks_favor_avg']\
            .apply(lambda x: round(x, 2))
        df['blocks_against_avg'] = df['blocks_against_avg']\
            .apply(lambda x: round(x, 2))
        df['dunks_avg'] = df['dunks_avg'].apply(lambda x: round(x, 2))
        df['personal_fouls_avg'] = df['personal_fouls_avg']\
            .apply(lambda x: round(x, 2))
        df['fouls_received_avg'] = df['fouls_received_avg']\
            .apply(lambda x: round(x, 2))
        df['efficiency_avg'] = df['efficiency_avg']\
            .apply(lambda x: round(x, 2))
        return df

    def querying(self):
        """
        Return DataFrame with all the players matching the stats inputted
        """
        self.connect()

        where_clause, league_clause, params = self._create_query()
        df = self._get_query(where_clause, league_clause, params)

        df_processed = self._proccess_df(df)
        
        self.close_connection()
        return df_processed


class SearchPlayer:
    def __init__(self):
        # Variables to access to data
        self.postgres_database = config['postgres_database']
        self.postgres_host = config['postgres_host']
        self.postgres_user = config['postgres_user']
        self.postgres_pass = config['postgres_pass']
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.postgres_database,
            host=self.postgres_host,
            user=self.postgres_user,
            password=self.postgres_pass
        )
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def on_change_season(self, league, season):
        self.connect()
        params = [league, season]
        self.cur.execute("""
                         SELECT DISTINCT team_id,team_name,season
                         FROM public.players_career_path
                         WHERE league = %s AND season = %s
                            """, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['team_id', 'team_name', 'season']
        teams_list = df['team_name'].tolist()
        df.set_index('team_name', inplace=True)
        ids_dict = df.to_dict()
        teams_list.sort()
        self.close_connection()
        return ids_dict, teams_list

    def on_change_team(self, team_id):
        self.connect()
        params = [team_id]
        self.cur.execute("""
                         SELECT DISTINCT players_info.player_id,
                            players_info.player_name
                        FROM public.players_matches_stats AS stats
                        LEFT JOIN players_info
                            ON players_info.player_id = stats.player_id
                        WHERE stats.team_id = %s
                         AND players_info.player_name IS NOT NULL
                            """, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['player_id', 'player_name']
        names_list = df['player_name'].to_list()
        df.set_index('player_name', inplace=True)
        player_ids_dict = df.to_dict()
        self.close_connection()
        return player_ids_dict, names_list


class PlayerStats:
    def __init__(self, player_id):
        # Variables to access to data
        self.conn = None
        self.cur = None
        self.postgres_database = config['postgres_database']
        self.postgres_host = config['postgres_host']
        self.postgres_user = config['postgres_user']
        self.postgres_pass = config['postgres_pass']
        self.minio_host = config['minio_host']
        self.minio_port = config['minio_port']
        self.minio_api_key = config['minio_api_key']
        self.minio_pass_key = config['minio_pass_key']
        self.bucket_name = config['bucket_name']
        # Player id
        self.player_id = player_id
        # Info
        self.player_name = None
        self.position = None
        self.age = None
        self.nationality = None
        # Path 
        self.last_season = None
        self.last_league = None
        # Player image
        self.image_not_found_path = config['image_not_found_path']
        self.player_image_width = None
        self.player_image_height = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.postgres_database,
            host=self.postgres_host,
            user=self.postgres_user,
            password=self.postgres_pass
        )
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def _get_info(self):
        params = [self.player_id]
        self.cur.execute("""
                         SELECT player_id, player_name, position, birthday,
                            nationality
                         FROM public.players_info
                         WHERE player_id = %s
                         """, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['player_id', 'player_name', 'position', 'birthday',
                      'nationality']
        return df

    def info(self):
        self.connect()
        df = self._get_info()
        birthday = df.loc[0].birthday
        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) <
                                            (birthday.month, birthday.day))
    
        player_name = df.loc[0].player_name
        self.player_name = player_name.upper()
        self.position = df.loc[0].position
        self.age = age
        self.nationality = df.loc[0].nationality

        self.close_connection()
        return

    def _get_path(self):
        params = [self.player_id, self.player_id, self.player_id]
        self.cur.execute("""
            SELECT season,league,team_name,n_matches, efficiency_avg, min_avg
            FROM(SELECT ROW_NUMBER()
                    OVER (PARTITION BY season,league,team_name,n_matches,
                         efficiency_avg,min_avg ORDER BY season,team_name)
                         AS r_number,*
                FROM(WITH pathh AS(SELECT
                                    substring(team_name,
                                              position('[' in team_name) + 1,
                                              position(']' in team_name) -
                                              position('[' in team_name) - 1)
                                    AS path_team_name,*
                                FROM players_career_path
                                WHERE player_id = %s)

                    SELECT stats.season AS season, league,
                         pathh.team_name AS team_name, n_matches,
                         efficiency_avg, min_avg
                    FROM(WITH temporal AS (SELECT season, team_name_extended,
                                            CONCAT(TRUNC(weighted,0),':',
                                             ROUND((MOD(weighted,1)
                                                * 60::integer),0))
                                            AS min_avg
                                    FROM(SELECT season, team_name_extended,
                                          SUM(ROUND((
                                               SPLIT_PART(
                                                min_total, ':', 1)::integer +
                                               SPLIT_PART(
                                                min_total, ':', 2)::integer /
                                                60::numeric)
                                               , 2)
                                             ) / SUM(n_matches) AS weighted
                                        FROM public.players_stats_career
                                        WHERE player_id = %s
                                        GROUP BY season,team_name_extended))

                        SELECT players_stats_career.season,
                            players_stats_career.team_name_extended,
                            SUM(n_matches) AS n_matches,
                            ROUND(SUM(efficiency_avg * n_matches)::numeric /
                             SUM(n_matches)::numeric,2) AS efficiency_avg,
                            temporal.min_avg
                        FROM players_stats_career
                        INNER JOIN temporal
                         ON temporal.season = players_stats_career.season AND
                          temporal.team_name_extended = players_stats_career.team_name_extended
                        WHERE player_id = %s
                        GROUP BY players_stats_career.season,
                         players_stats_career.team_name_extended,
                         temporal.min_avg
                        ORDER BY season DESC) AS stats
                    LEFT JOIN pathh
                         ON stats.season = pathh.season AND
                         (stats.team_name_extended = pathh.team_name OR
                           stats.team_name_extended = pathh.path_team_name)
                    )
                )
            WHERE r_number=1
            ORDER BY season DESC;
        """, params)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['season', 'league', 'team_name', 'n_matches',
                      'efficiency', 'min_avg']
        df['n_matches'] = df['n_matches'].apply(lambda x: int(x))
        df['efficiency'] = df['efficiency'].apply(lambda x: round(float(x), 2))
        return df
    
    def path(self):
        self.connect()
        df = self._get_path()

        # Column name displayed on the front
        df.columns = ['SEASON', 'LEAGUE', 'TEAM NAME', 'NUMBER OF MATCHES',
                      'EFFICIENCY', 'MINUTES PER MATCH']
        try:
            self.last_season = df.loc[0].SEASON
            self.last_league = df.loc[0].LEAGUE
        except Exception:
            print('Error in SEASON or LEAGUE')

        self.close_connection()
        return df

    def _get_player_image(self):
        client = Minio(endpoint=f"{self.minio_host}:{self.minio_port}",
                    access_key=self.minio_api_key,
                    secret_key=self.minio_pass_key, secure=False)
        bucket_name = self.bucket_name
        object_name = f'{self.player_id}.png'
        try:
            response = client.get_object(bucket_name, object_name)
            image_data = response.read()
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)
            width, height = image.size
            height_limit = 250
            if height != height_limit:
                prop = round(height/width, 2)
                height = height_limit
                width = round(height/prop, 0)
        except Exception:
            print('IMAGE NOT FOUND')
            with open(self.image_not_found_path, 'rb') as f:
                image_data = f.read()
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)
            width, height = image.size
            width = f"{width}px"
            height = f"{height}px"
        return image_data, width, height 

    def player_image(self):
        """
        Returns a player image.

        If it can't be found, a template image is returned.
        """
        image_data, width, height = self._get_player_image()
        self.player_image_width = width
        self.player_image_height = height
        
        return image_data

    def _get_shooting_query(self):
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

    def _process_in_out_shootings(self,df):
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
                stats[df.loc[row].season][df.loc[row].shoot_from]['in'] = \
                    df.loc[row].total
            else:
                stats[df.loc[row].season][df.loc[row].shoot_from]['out'] = \
                    df.loc[row].total
        return stats

    def _shooting_stats(self):
        df = self._get_shooting_query()
        dict_in_out = self._process_in_out_shootings(df)

        dict_shootings = {}
        for year, values in dict_in_out.items():
            new_values = {}
            for key, value in values.items():
                new_values[key] = {
                    'in': value['in'],
                    'out': value['out'],
                    'tried': value['in'] + value['out']
                }
            dict_shootings[year] = new_values
        keys = list(dict_shootings.keys())
        keys.sort(reverse=True)
        if len(keys) > 0:
            years = [keys[0], keys[0] - 1, keys[0] - 2]
        else:
            years = [datetime.today().year, datetime.today().year - 1,
                     datetime.today().year - 2]
        return dict_shootings, years

    def shootings_images(self):
        dict_shootings, years = self._shooting_stats()
        images = []
        for year in years:
            fig = generate_image(dic_stats=dict_shootings, year=year)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            images.append(buf)
        final_images = []
        for i, image_buffer in enumerate(images):
            final_images.append(image_buffer.getvalue())
            image_buffer.seek(0)
        image_1 = final_images[0]
        image_2 = final_images[1]
        image_3 = final_images[2]

        return image_1, image_2, image_3

    def _get_stats_total_query(self):
        params = [self.player_id]
        self.cur.execute("""
            SELECT season,
                   team_name_extended,
                   stage_name_extended,
                   SUM(n_matches) AS n_matches,
                   MIN(min_total) AS min_total,
                   SUM(points_total) AS points_total ,
                   SUM(twos_in_total) AS twos_in_total,
                   SUM(twos_tried_total) AS twos_tried_total,
                   CASE
                       WHEN SUM(twos_tried_total)=0
                         THEN 0
                       WHEN SUM(twos_tried_total)!=0
                         THEN SUM(twos_in_total) / SUM(twos_tried_total)
                   END AS twos_perc,
                   SUM(threes_in_total) AS threes_in_total,
                   SUM(threes_tried_total) AS threes_tried_total,
                   CASE
                       WHEN SUM(threes_tried_total)=0
                         THEN 0
                       WHEN SUM(threes_tried_total)!=0
                         THEN SUM(threes_in_total) / SUM(threes_tried_total)
                   END AS threes_perc,
                   SUM(field_goals_in_total) AS field_goals_in_total,
                   SUM(field_goals_tried_total) AS field_goals_tried_total,
                   CASE
                       WHEN SUM(field_goals_tried_total)=0
                         THEN 0
                       WHEN SUM(field_goals_tried_total)!=0
                         THEN SUM(field_goals_in_total) /
                            SUM(field_goals_tried_total)
                   END AS field_goals_perc,
                   SUM(free_throws_in_total) AS free_throws_in_total,
                   SUM(free_throws_tried_total) AS free_throws_tried_total,
                   CASE
                       WHEN SUM(free_throws_tried_total)=0
                         THEN 0
                       WHEN SUM(free_throws_tried_total)!=0
                         THEN SUM(free_throws_in_total) /
                            SUM(free_throws_tried_total)
                   END AS free_throws_perc,
                   SUM(offensive_rebounds_total) AS offensive_rebounds_total,
                   SUM(deffensive_rebounds_total)
                         AS deffensive_rebounds_total,
                   SUM(total_rebounds_total) AS total_rebounds_total,
                   SUM(assists_total) AS assists_total,
                   SUM(turnovers_total) AS turnovers_total,
                   SUM(blocks_favor_total) AS blocks_favor_total,
                   SUM(blocks_against_total) AS blocks_against_total,
                   SUM(dunks_total)AS dunks_total,
                   SUM(personal_fouls_total) AS personal_fouls_total,
                   SUM(fouls_received_total) AS fouls_received_total,
                   SUM(efficiency_total) AS efficiency_total
            FROM players_stats_career
            WHERE player_id = %s
            GROUP BY season,team_name_extended,stage_name_extended
            ORDER BY season DESC
        """, params)

        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['season', 'team_name_extended', 'stage_name_extended',
                      'n_matches', 'min_total', 'points_total',
                      'twos_in_total', 'twos_tried_total', 'twos_perc',
                      'threes_in_total', 'threes_tried_total',
                      'threes_perc', 'field_goals_in_total',
                      'field_goals_tried_total', 'field_goals_perc',
                      'free_throws_in_total', 'free_throws_tried_total',
                      'free_throws_perc', 'offensive_rebounds_total',
                      'deffensive_rebounds_total', 'total_rebounds_total',
                      'assists_total', 'turnovers_total',
                      'blocks_favor_total', 'blocks_against_total',
                      'dunks_total', 'personal_fouls_total',
                      'fouls_received_total', 'efficiency_total']

        return df

    def _process_stats_total(self, df):
        df['n_matches'] = df['n_matches'].apply(lambda x: int(x))
        df['points_total'] = df['points_total'].apply(lambda x: int(x))
        df['twos_in_total'] = df['twos_in_total'].apply(lambda x: int(x))
        df['twos_tried_total'] = df['twos_tried_total'] \
            .apply(lambda x: int(x))
        df['twos_perc'] = df['twos_perc']\
            .apply(lambda x: round(float(x), 2))
        df['threes_in_total'] = df['threes_in_total']\
            .apply(lambda x: int(x))
        df['threes_tried_total'] = df['threes_tried_total']\
            .apply(lambda x: int(x))
        df['threes_perc'] = df['threes_perc']\
            .apply(lambda x: round(float(x), 2))
        df['field_goals_in_total'] = df['field_goals_in_total']\
            .apply(lambda x: int(x))
        df['field_goals_tried_total'] = df['field_goals_tried_total']\
            .apply(lambda x: int(x))
        df['field_goals_perc'] = df['field_goals_perc']\
            .apply(lambda x: round(float(x), 2))
        df['free_throws_in_total'] = df['free_throws_in_total']\
            .apply(lambda x: int(x))
        df['free_throws_tried_total'] = df['free_throws_tried_total']\
            .apply(lambda x: int(x))
        df['free_throws_perc'] = df['free_throws_perc']\
            .apply(lambda x: round(float(x), 2))
        df['offensive_rebounds_total'] = df['offensive_rebounds_total']\
            .apply(lambda x: int(x))
        df['deffensive_rebounds_total'] = df['deffensive_rebounds_total']\
            .apply(lambda x: int(x))
        df['total_rebounds_total'] = df['total_rebounds_total']\
            .apply(lambda x: int(x))
        df['assists_total'] = df['assists_total'].apply(lambda x: int(x))\

        df['turnovers_total'] = df['turnovers_total'].apply(lambda x: int(x))
        df['blocks_favor_total'] = df['blocks_favor_total']\
            .apply(lambda x: int(x))
        df['blocks_against_total'] = df['blocks_against_total']\
            .apply(lambda x: int(x))
        df['dunks_total'] = df['dunks_total'].apply(lambda x: int(x))
        df['personal_fouls_total'] = df['personal_fouls_total']\
            .apply(lambda x: int(x))
        df['fouls_received_total'] = df['fouls_received_total']\
            .apply(lambda x: int(x))
        df['efficiency_total'] = df['efficiency_total']\
            .apply(lambda x: int(x))
        
        return df

    def stats_total_table(self):
        self.connect()
        df = self._get_stats_total_query()
        df_processed = self._process_stats_total(df)
        
        df_processed.columns = ['SEASON', 'TEAM_NAME_EXTENDED', 'STAGE_NAME_EXTENDED',
                      'N_MATCHES', 'MIN', 'POINTS', 'TWOS_IN', 'TWOS_TRIED',
                      'TWOS_PERC', 'THREES_IN', 'THREES_TRIED', 'THREES_PERC',
                      'FIELD_GOALS_IN', 'FIELD_GOALS_TRIED',
                      'FIELD_GOALS_PERC', 'FREE_THROWS_IN',
                      'FREE_THROWS_TRIED', 'FREE_THROWS_PERC',
                      'OFFENSIVE_REBOUNDS', 'DEFFENSIVE_REBOUNDS',
                      'TOTAL_REBOUNDS', 'ASSISTS', 'TURNOVERS',
                      'BLOCKS_FAVOR', 'BLOCKS_AGAINST', 'DUNKS',
                      'PERSONAL_FOULS', 'FOULS_RECEIVED', 'EFFICIENCY']
        self.close_connection()

        return df_processed

    def _get_stats_avg_query(self):
        params = [self.player_id]
        self.cur.execute("""
            SELECT season,
                   team_name_extended,
                   stage_name_extended,
                   SUM(n_matches) AS n_matches,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN '00:00'
                       WHEN SUM(n_matches)!=0
                         THEN DATE_TRUNC('second', '00:00:00' +
                                         (SUM(EXTRACT(EPOCH FROM min_avg)
                                                * n_matches) / SUM(n_matches))
                                         * INTERVAL '1 second')
                   END AS min_avg,
                   CASE
                   WHEN SUM(n_matches)=0
                         THEN 0
                   WHEN SUM(n_matches)!=0
                         THEN SUM(points_avg*n_matches)/SUM(n_matches)
                   END AS points_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(twos_in_avg*n_matches)/SUM(n_matches)
                   END AS twos_in_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(twos_tried_avg*n_matches)/SUM(n_matches)
                   END AS twos_tried_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(twos_perc*n_matches)/SUM(n_matches)
                   END AS twos_perc,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(threes_in_avg*n_matches)/SUM(n_matches)
                   END AS threes_in_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(threes_tried_avg*n_matches)/SUM(n_matches)
                   END AS threes_tried_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(threes_perc*n_matches)/SUM(n_matches)
                   END AS threes_perc,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(field_goals_in_avg*n_matches)/SUM(n_matches)
                   END AS field_goals_in_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(field_goals_tried_avg*n_matches) /
                              SUM(n_matches)
                   END AS field_goals_tried_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(field_goals_perc*n_matches)/SUM(n_matches)
                   END AS field_goals_perc,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(free_throws_in_avg*n_matches)/SUM(n_matches)
                   END AS free_throws_in_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(free_throws_tried_avg*n_matches) /
                              SUM(n_matches)
                   END AS free_throws_tried_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(free_throws_perc*n_matches)/SUM(n_matches)
                   END AS free_throws_perc,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(offensive_rebounds_avg*n_matches) /
                              SUM(n_matches)
                   END AS offensive_rebounds_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(deffensive_rebounds_avg*n_matches) /
                              SUM(n_matches)
                   END AS deffensive_rebounds_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                         THEN 0
                       WHEN SUM(n_matches)!=0
                         THEN SUM(total_rebounds_avg*n_matches)/SUM(n_matches)
                   END AS total_rebounds_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(assists_avg*n_matches)/SUM(n_matches)
                   END AS assists_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(turnovers_avg*n_matches)/SUM(n_matches)
                   END AS turnovers_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(blocks_favor_avg*n_matches)/SUM(n_matches)
                   END AS blocks_favor_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(blocks_against_avg*n_matches)/SUM(n_matches)
                   END AS blocks_against_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(dunks_avg*n_matches)/SUM(n_matches)
                   END AS dunks_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(personal_fouls_avg*n_matches)/SUM(n_matches)
                   END AS personal_fouls_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(fouls_received_avg*n_matches)/SUM(n_matches)
                   END AS fouls_received_avg,
                   CASE
                       WHEN SUM(n_matches)=0
                        THEN 0
                       WHEN SUM(n_matches)!=0
                        THEN SUM(efficiency_avg*n_matches)/SUM(n_matches)
                   END AS efficiency_avg
            FROM players_stats_career
            WHERE player_id = %s
            GROUP BY season, team_name_extended, stage_name_extended
            ORDER BY season DESC
            """, params)

        df = pd.DataFrame(self.cur.fetchall())
        df.columns = ['season', 'team_name_extended', 'stage_name_extended',
                      'n_matches', 'min_avg', 'points_avg', 'twos_in_avg',
                      'twos_tried_avg', 'twos_perc', 'threes_in_avg',
                      'threes_tried_avg', 'threes_perc', 'field_goals_in_avg',
                      'field_goals_tried_avg', 'field_goals_perc',
                      'free_throws_in_avg', 'free_throws_tried_avg',
                      'free_throws_perc', 'offensive_rebounds_avg',
                      'deffensive_rebounds_avg', 'total_rebounds_avg',
                      'assists_avg', 'turnovers_avg', 'blocks_favor_avg',
                      'blocks_against_avg', 'dunks_avg', 'personal_fouls_avg',
                      'fouls_received_avg', 'efficiency_avg']
        
        return df

    def _process_stats_avg(self, df):
        df['n_matches'] = df['n_matches'].apply(lambda x: int(x))
        df['min_avg'] = df['min_avg']\
            .apply(lambda x: (datetime(1900, 1, 1) + x).time()
                   .strftime("%M:%S"))
        df['points_avg'] = df['points_avg'].apply(lambda x: round(x, 2))
        df['twos_in_avg'] = df['twos_in_avg'].apply(lambda x: round(x, 2))
        df['twos_tried_avg'] = df['twos_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['twos_perc'] = df['twos_perc'].apply(lambda x: round(float(x), 2))
        df['threes_in_avg'] = df['threes_in_avg'].apply(lambda x: round(x, 2))
        df['threes_tried_avg'] = df['threes_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['threes_perc'] = df['threes_perc']\
            .apply(lambda x: round(float(x), 2))
        df['field_goals_in_avg'] = df['field_goals_in_avg']\
            .apply(lambda x: round(x, 2))
        df['field_goals_tried_avg'] = df['field_goals_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['field_goals_perc'] = df['field_goals_perc']\
            .apply(lambda x: round(float(x), 2))
        df['free_throws_in_avg'] = df['free_throws_in_avg']\
            .apply(lambda x: round(x, 2))
        df['free_throws_tried_avg'] = df['free_throws_tried_avg']\
            .apply(lambda x: round(x, 2))
        df['free_throws_perc'] = df['free_throws_perc']\
            .apply(lambda x: round(float(x), 2))
        df['offensive_rebounds_avg'] = df['offensive_rebounds_avg']\
            .apply(lambda x: round(x, 2))
        df['deffensive_rebounds_avg'] = df['deffensive_rebounds_avg']\
            .apply(lambda x: round(x, 2))
        df['total_rebounds_avg'] = df['total_rebounds_avg']\
            .apply(lambda x: round(x, 2))
        df['assists_avg'] = df['assists_avg'].apply(lambda x: round(x, 2))
        df['turnovers_avg'] = df['turnovers_avg'].apply(lambda x: round(x, 2))
        df['blocks_favor_avg'] = df['blocks_favor_avg']\
            .apply(lambda x: round(x, 2))
        df['blocks_against_avg'] = df['blocks_against_avg']\
            .apply(lambda x: round(x, 2))
        df['dunks_avg'] = df['dunks_avg'].apply(lambda x: round(x, 2))
        df['personal_fouls_avg'] = df['personal_fouls_avg']\
            .apply(lambda x: round(x, 2))
        df['fouls_received_avg'] = df['fouls_received_avg']\
            .apply(lambda x: round(x, 2))
        df['efficiency_avg'] = df['efficiency_avg']\
            .apply(lambda x: round(x, 2))

        return df

    def stats_avg_table(self):
        self.connect()
        df = self._get_stats_avg_query()
        df_processed = self._process_stats_avg(df)
        
        df_processed.columns = ['SEASON', 'TEAM_NAME_EXTENDED', 'STAGE_NAME_EXTENDED',
                      'N_MATCHES', 'MIN', 'POINTS', 'TWOS_IN', 'TWOS_TRIED',
                      'TWOS_PERC', 'THREES_IN', 'THREES_TRIED', 'THREES_PERC',
                      'FIELD_GOALS_IN', 'FIELD_GOALS_TRIED',
                      'FIELD_GOALS_PERC', 'FREE_THROWS_IN',
                      'FREE_THROWS_TRIED', 'FREE_THROWS_PERC',
                      'OFFENSIVE_REBOUNDS', 'DEFFENSIVE_REBOUNDS',
                      'TOTAL_REBOUNDS', 'ASSISTS', 'TURNOVERS',
                      'BLOCKS_FAVOR', 'BLOCKS_AGAINST', 'DUNKS',
                      'PERSONAL_FOULS', 'FOULS_RECEIVED', 'EFFICIENCY']
        self.close_connection()

        return df_processed




