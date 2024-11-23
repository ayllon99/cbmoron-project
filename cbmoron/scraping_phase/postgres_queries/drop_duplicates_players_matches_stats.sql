CREATE TABLE players_matches_stats_2 AS(
	WITH duplicates AS(
		SELECT ROW_NUMBER() OVER (PARTITION BY match_id,player_id ORDER BY identifier) AS number_row,*
		FROM players_matches_stats
	)

	SELECT *
	FROM duplicates
	WHERE number_row=1
	ORDER BY identifier ASC
);

ALTER TABLE players_matches_stats_2 
DROP COLUMN number_row;

DROP TABLE IF EXISTS players_matches_stats CASCADE;

ALTER TABLE IF EXISTS public.players_matches_stats_2
    RENAME TO players_matches_stats;