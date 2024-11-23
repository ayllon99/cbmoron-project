WITH no_duplicates AS(SELECT ROW_NUMBER() OVER(PARTITION BY player_id,season,team_id ORDER BY date_in ASC)AS number_row,*
FROM public.players_career_path
WHERE player_id = {})

SELECT CASE
    WHEN LEFT(season, 2)::integer < 90  THEN ('20'|| LEFT(season, 2)) ::integer
    WHEN LEFT(season, 2)::integer >= 90  THEN ('19'|| LEFT(season, 2)) ::integer
    ELSE 1900
END AS years,*
FROM no_duplicates
WHERE number_row = 1
ORDER BY years DESC

