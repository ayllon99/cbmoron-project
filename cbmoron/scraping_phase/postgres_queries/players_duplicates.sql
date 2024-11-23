SELECT year_y,COUNT(*)
FROM(
WITH media AS(
	SELECT match_id,player_id,COUNT(player_id)AS counted 
	FROM public.players_matches_stats
	GROUP BY match_id,player_id
	ORDER BY counted DESC)
SELECT player_id,t1.match_id,counted,EXTRACT(YEAR FROM date) AS year_y
FROM media as t1
LEFT JOIN public.results AS t2
ON t1.match_id=t2.match_id
WHERE counted >1
ORDER BY date)
GROUP BY year_y
ORDER BY year_y