SELECT EXTRACT(YEAR FROM date) AS year,identifier,player_id,results.match_id,success,quarter,shoot_time,top_top,left_left,shooting_type,date FROM public.shootings
LEFT JOIN results ON shootings.match_id=results.match_id
WHERE player_id = {}