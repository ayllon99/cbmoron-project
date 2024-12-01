CREATE OR REPLACE FUNCTION shootings_insert_function()
RETURNS TRIGGER AS $$
BEGIN
    NEW.shoot_from := 
    CASE 
        WHEN NEW.shooting_type = 'Zone' THEN 'Zone'
        WHEN NEW.shooting_type = 'Middle' AND NEW.top_top > 10 AND NEW.top_top < 38 AND NEW.left_left < 10 THEN 'Left Corner Middle'
        WHEN NEW.shooting_type = 'Middle' AND NEW.top_top > 62 AND NEW.top_top < 90 AND NEW.left_left < 10 THEN 'Right Corner Middle'
        WHEN NEW.shooting_type = 'Middle' AND NEW.top_top > 38 AND NEW.top_top < 62 THEN 'Front Middle'
        WHEN NEW.shooting_type = 'Middle' AND NEW.top_top < 50 THEN 'Left Side Middle'
        WHEN NEW.shooting_type = 'Middle' AND NEW.top_top > 50 THEN 'Right Side Middle'
        WHEN NEW.shooting_type = 'Three' AND NEW.top_top > 90 AND NEW.left_left < 10 THEN 'Right Corner Three'
        WHEN NEW.shooting_type = 'Three' AND NEW.top_top < 10 AND NEW.left_left > 90 THEN 'Left Corner Three'
        WHEN NEW.shooting_type = 'Three' AND NEW.top_top > 38 AND NEW.top_top < 62 THEN 'Front Three'
        WHEN NEW.shooting_type = 'Three' AND NEW.top_top < 50 THEN 'Left Side Three'
        WHEN NEW.shooting_type = 'Three' AND NEW.top_top > 50 THEN 'Right Side Three'
    END;
    
    NEW.season := 
    CASE 
        WHEN EXTRACT(MONTH FROM NEW.date) < 8 THEN EXTRACT(YEAR FROM NEW.date) - 1
        ELSE EXTRACT(YEAR FROM NEW.date)
    END;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER shootings_insert_trigger
BEFORE INSERT ON shootings
FOR EACH ROW
EXECUTE FUNCTION shootings_insert_function();
