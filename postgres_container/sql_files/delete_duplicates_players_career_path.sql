--DELETE SOME DUPLICATES IN players_career_path
CREATE TEMP TABLE duplicate_rows AS
SELECT ROW_NUMBER() OVER (PARTITION BY player_id, season,league,team_id,team_name,license,date_in,date_out ORDER BY identifier) AS row_num, *
FROM public.players_career_path;

DELETE FROM  players_career_path
USING duplicate_rows 
WHERE players_career_path.identifier = duplicate_rows.identifier AND duplicate_rows.row_num > 1;

DROP TABLE duplicate_rows;
