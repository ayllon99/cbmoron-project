SELECT CASE
    WHEN LEFT(season, 2)::integer < 90  THEN ('20'|| LEFT(season, 2)) ::integer
    WHEN LEFT(season, 2)::integer >= 90  THEN ('19'|| LEFT(season, 2)) ::integer
    ELSE 1900
END AS years,player_id,season,team_name_extended,

SUM(n_matches) AS n_matches,SUM(min_total_mins) AS total_mins,SUM(min_avg) AS cambiar,SUM(points_total)AS pts_total,ROUND(SUM(points_total)/SUM(n_matches),2)AS pts_avg,SUM(twos_in_total) AS twos_in,SUM(twos_tried_total) AS twos_tried,SUM(twos_perc),SUM(twos_in_avg),SUM(twos_tried_avg),SUM(threes_in_total),SUM(threes_perc),SUM(threes_in_avg),SUM(threes_tried_avg),SUM(field_goals_tried_total),SUM(field_goals_perc),SUM(field_goals_in_avg),SUM(field_goals_tried_avg),SUM(free_throws_tried_total),SUM(free_throws_perc),SUM(free_throws_in_avg),SUM(free_throws_tried_avg),SUM(offensive_rebounds_total),SUM(offensive_rebounds_avg),SUM(deffensive_rebounds_total),SUM(deffensive_rebounds_avg),SUM(total_rebounds_total),SUM(total_rebounds_avg),SUM(assists_total),SUM(assists_avg),SUM(turnovers_total),SUM(turnovers_avg),SUM(blocks_favor_total),SUM(blocks_favor_avg),SUM(blocks_against_total),SUM(blocks_against_avg),SUM(dunks_total),SUM(dunks_avg),SUM(personal_fouls_total),SUM(personal_fouls_avg),SUM(fouls_received_total),SUM(fouls_received_avg),SUM(efficiency_total),SUM(efficiency_avg)

FROM public.players_stats_career_view
WHERE player_id = {}
GROUP BY years,player_id,season,team_name_extended
--ORDER BY season ASC