UPDATE public.shootings 
SET shoot_time = temporal_new_time_column.time
FROM temporal_new_time_column
WHERE shootings.identifier=temporal_new_time_column.identifier

