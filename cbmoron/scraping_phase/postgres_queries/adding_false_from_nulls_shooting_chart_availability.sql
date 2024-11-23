INSERT INTO public.shooting_chart_availability (match_id, availability)
SELECT match_id,availability
FROM (
	SELECT t1.match_id,false AS availability
	FROM public.results AS t1
	LEFT JOIN public.shooting_chart_availability AS t2
	ON t1.match_id=t2.match_id
	WHERE availability IS NULL)