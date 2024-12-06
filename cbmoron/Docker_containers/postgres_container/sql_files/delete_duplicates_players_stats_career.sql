
CREATE TEMP TABLE duplicate_rows AS
SELECT ROW_NUMBER() OVER (PARTITION BY player_id, season,team_name_extended,stage_abbrev,stage_name_extended,n_matches,min_total,min_avg,points_total,points_avg,twos_in_total ORDER BY season) AS row_num, *
FROM public.players_stats_career;

DELETE FROM  players_stats_career
USING duplicate_rows 
WHERE  players_stats_career.identifier= duplicate_rows.identifier AND duplicate_rows.row_num > 1;

DROP TABLE duplicate_rows;


