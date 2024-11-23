SELECT path_season,path_league,path_team_name,stats_n_matches
FROM(SELECT DISTINCT season AS path_season,league AS path_league,substring(team_name, position('[' in team_name) + 1, position(']' in team_name) - position('[' in team_name) - 1)AS path_team_name,date_in AS path_date_in FROM players_career_path
				WHERE player_id={}
	ORDER BY path_date_in DESC) AS pathh

LEFT JOIN (WITH dup AS(SELECT DISTINCT player_id, season, team_name_extended, stage_abbrev,stage_name_extended,n_matches,min_total,min_avg,points_total FROM public.players_stats_career
				WHERE player_id = {})
		SELECT season AS stats_season, team_name_extended AS stats_team_name , SUM(n_matches) AS stats_n_matches
		FROM dup
		GROUP BY  team_name_extended,season
		ORDER BY stats_season) AS matches

ON matches.stats_season = pathh.path_season AND matches.stats_team_name = pathh.path_team_name
ORDER BY path_season DESC