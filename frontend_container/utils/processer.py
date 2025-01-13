import pandas as pd


def new_col(stat, n_matches):
    return (n_matches * stat).sum() / n_matches.sum()


def proccess_df_avg(df):
    dff = df.groupby('SEASON')\
        .apply(lambda x:
               pd.Series(
                {'N_MATCHES': x['N_MATCHES'].sum(),
                 'POINTS': new_col(x['POINTS'], x['N_MATCHES']),
                 'TWOS_IN': new_col(x['TWOS_IN'],
                                    x['N_MATCHES']),
                 'TWOS_TRIED': new_col(x['TWOS_TRIED'],
                                       x['N_MATCHES']),
                 'TWOS_PERC': new_col(x['TWOS_PERC'],
                                      x['N_MATCHES']),
                 'THREES_IN': new_col(x['THREES_IN'],
                                      x['N_MATCHES']),
                 'THREES_TRIED': new_col(x['THREES_TRIED'],
                                         x['N_MATCHES']),
                 'THREES_PERC': new_col(x['THREES_PERC'],
                                        x['N_MATCHES']),
                 'FIELD_GOALS_IN': new_col(x['FIELD_GOALS_IN'],
                                           x['N_MATCHES']),
                 'FIELD_GOALS_TRIED': new_col(x['FIELD_GOALS_TRIED'],
                                              x['N_MATCHES']),
                 'FIELD_GOALS_PERC': new_col(x['FIELD_GOALS_PERC'],
                                             x['N_MATCHES']),
                 'FREE_THROWS_IN': new_col(x['FREE_THROWS_IN'],
                                           x['N_MATCHES']),
                 'FREE_THROWS_TRIED': new_col(x['FREE_THROWS_TRIED'],
                                              x['N_MATCHES']),
                 'FREE_THROWS_PERC': new_col(x['FREE_THROWS_PERC'],
                                             x['N_MATCHES']),
                 'OFFENSIVE_REBOUNDS': new_col(x['OFFENSIVE_REBOUNDS'],
                                               x['N_MATCHES']),
                 'DEFFENSIVE_REBOUNDS': new_col(x['DEFFENSIVE_REBOUNDS'],
                                                x['N_MATCHES']),
                 'TOTAL_REBOUNDS': new_col(x['TOTAL_REBOUNDS'],
                                           x['N_MATCHES']),
                 'ASSISTS': new_col(x['ASSISTS'],
                                    x['N_MATCHES']),
                 'TURNOVERS': new_col(x['TURNOVERS'],
                                      x['N_MATCHES']),
                 'BLOCKS_FAVOR': new_col(x['BLOCKS_FAVOR'],
                                         x['N_MATCHES']),
                 'BLOCKS_AGAINST': new_col(x['BLOCKS_AGAINST'],
                                           x['N_MATCHES']),
                 'DUNKS': new_col(x['DUNKS'], x['N_MATCHES']),
                 'PERSONAL_FOULS': new_col(x['PERSONAL_FOULS'],
                                           x['N_MATCHES']),
                 'FOULS_RECEIVED': new_col(x['FOULS_RECEIVED'],
                                           x['N_MATCHES']),
                 'EFFICIENCY': new_col(x['EFFICIENCY'],
                                       x['N_MATCHES'])
                 }), include_groups=False)
    return dff


def proccess_df_total(df):
    dff = df.groupby('SEASON')\
        .apply(lambda x:
               pd.Series(
                {'N_MATCHES': x['N_MATCHES'].sum(),
                 'POINTS':  x['POINTS'].sum(),
                 'TWOS_IN': x['TWOS_IN'].sum(),
                 'TWOS_TRIED': x['TWOS_TRIED'].sum(),
                 'TWOS_PERC': new_col(x['TWOS_PERC'],
                                      x['N_MATCHES']),
                 'THREES_IN': x['THREES_IN'].sum(),
                 'THREES_TRIED': x['THREES_TRIED'].sum(),
                 'THREES_PERC': new_col(x['THREES_PERC'],
                                        x['N_MATCHES']),
                 'FIELD_GOALS_IN': x['FIELD_GOALS_IN'].sum(),
                 'FIELD_GOALS_TRIED': x['FIELD_GOALS_TRIED'].sum(),
                 'FIELD_GOALS_PERC': new_col(x['FIELD_GOALS_PERC'],
                                             x['N_MATCHES']),
                 'FREE_THROWS_IN': x['FREE_THROWS_IN'].sum(),
                 'FREE_THROWS_TRIED': x['FREE_THROWS_TRIED'].sum(),
                 'FREE_THROWS_PERC': new_col(x['FREE_THROWS_PERC'],
                                             x['N_MATCHES']),
                 'OFFENSIVE_REBOUNDS': x['OFFENSIVE_REBOUNDS'].sum(),
                 'DEFFENSIVE_REBOUNDS': x['DEFFENSIVE_REBOUNDS'].sum(),
                 'TOTAL_REBOUNDS': x['TOTAL_REBOUNDS'].sum(),
                 'ASSISTS': x['ASSISTS'].sum(),
                 'TURNOVERS': x['TURNOVERS'].sum(),
                 'BLOCKS_FAVOR': x['BLOCKS_FAVOR'].sum(),
                 'BLOCKS_AGAINST': x['BLOCKS_AGAINST'].sum(),
                 'DUNKS': x['DUNKS'].sum(),
                 'PERSONAL_FOULS': x['PERSONAL_FOULS'].sum(),
                 'FOULS_RECEIVED': x['FOULS_RECEIVED'].sum(),
                 'EFFICIENCY': x['EFFICIENCY'].sum(),
                 }), include_groups=False)
    return dff
