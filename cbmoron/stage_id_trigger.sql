-- Create the trigger function
CREATE OR REPLACE FUNCTION check_and_insert_stage_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM results WHERE stage_id = NEW.stage_id) THEN
        INSERT INTO stages (stage_id) VALUES (NEW.stage_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER check_and_insert_stage_id_trigger
BEFORE INSERT ON results
FOR EACH ROW
EXECUTE FUNCTION check_and_insert_stage_id();