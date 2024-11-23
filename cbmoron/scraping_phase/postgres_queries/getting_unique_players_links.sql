SELECT *
FROM(
	WITH duppp AS(
		SELECT *
		FROM(
			WITH dupl AS(
				SELECT t1.identifier,t1.match_id,t1.team_id,t1.player_id,t1.player_link,t2.date,t1.player_name
				FROM public.players_matches_stats AS t1
				LEFT JOIN public.results AS t2
				ON t2.match_id=t1.match_id
				ORDER BY player_id,date DESC
				)
			SELECT ROW_NUMBER() OVER(PARTITION BY player_id ORDER BY date DESC) AS row_num,*
			FROM dupl
			)
	WHERE row_num=1 AND (player_name !='- -, - -' AND player_name!='-, -')
				)
	SELECT ROW_NUMBER() OVER(PARTITION BY player_name ORDER BY date DESC) AS row_numm,*
	FROM duppp
	)
WHERE row_numm=1