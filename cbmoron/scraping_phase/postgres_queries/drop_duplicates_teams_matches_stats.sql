CREATE TABLE teams_matches_stats_2 AS(WITH duplicates AS(
	SELECT ROW_NUMBER() OVER(PARTITION BY match_id ORDER BY identifier) AS number_row,*
	FROM public.teams_matches_stats
	)

SELECT *
FROM duplicates
WHERE number_row<3
	ORDER BY identifier ASC
)

	ALTER TABLE teams_macthes_stats_2 
DROP COLUMN number_row;

DROP TABLE IF EXISTS teams_matches_stats CASCADE;

ALTER TABLE IF EXISTS public.teams_matches_stats_2
    RENAME TO teams_matches_stats;