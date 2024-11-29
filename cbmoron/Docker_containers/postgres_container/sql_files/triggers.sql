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
----------------------------------------------------------------------------------
-- Create the trigger function
CREATE OR REPLACE FUNCTION check_and_insert_away_team_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM teams WHERE team_id = NEW.away_team_id) THEN
        INSERT INTO teams (team_id) VALUES (NEW.away_team_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER check_and_insert_away_team_id_trigger
BEFORE INSERT ON results
FOR EACH ROW
EXECUTE FUNCTION check_and_insert_away_team_id();
----------------------------------------------------------------------------------
-- Create the trigger function
CREATE OR REPLACE FUNCTION check_and_insert_home_team_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM teams WHERE team_id = NEW.home_team_id) THEN
        INSERT INTO teams (team_id) VALUES (NEW.home_team_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER check_and_insert_home_team_id_trigger
BEFORE INSERT ON results
FOR EACH ROW
EXECUTE FUNCTION check_and_insert_home_team_id();
----------------------------------------------------------------------------------
-- Create the trigger function
CREATE OR REPLACE FUNCTION check_and_insert_player_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM players_info WHERE player_id = NEW.player_id) THEN
        INSERT INTO players_info (player_id,player_link) VALUES (NEW.player_id,NEW.player_link);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER check_and_insert_player_id_trigger
BEFORE INSERT ON results
FOR EACH ROW
EXECUTE FUNCTION check_and_insert_player_id();