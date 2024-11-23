CREATE TABLE shootings_2 AS(
	WITH duplicates AS(
		SELECT ROW_NUMBER() OVER(PARTITION BY match_id,player_id,quarter,top_top,left_left,shoot_time ORDER BY identifier) AS number_row,*
		FROM public.shootings
	)

	SELECT identifier,player_id,match_id,team_id,home_away,vs_team_id,number,player_name,success,quarter,shoot_time,top_top,left_left,shooting_type
	FROM duplicates
	WHERE number_row=1
	ORDER BY identifier ASC
)

DROP TABLE IF EXISTS shootings CASCADE;

ALTER TABLE IF EXISTS public.shootings_2
    RENAME TO shootings;

DROP TABLE IF EXISTS temporal_new_time_column CASCADE;