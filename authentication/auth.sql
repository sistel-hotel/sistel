SET SEARCH_PATH to sistel;
CREATE OR REPLACE FUNCTION check_password_complexity(password_to_check TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    contains_letter BOOLEAN;
    contains_digit BOOLEAN;
BEGIN
    contains_letter := false;
    contains_digit := false;

    FOR i IN 1..length(password_to_check) LOOP
        IF substring(password_to_check, i, 1) ~ '[A-Za-z]' THEN
            contains_letter := true;
        ELSIF substring(password_to_check, i, 1) ~ '[0-9]' THEN
            contains_digit := true;
        END IF;
    END LOOP;

    RETURN contains_letter AND contains_digit;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION prevent_weak_password()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT check_password_complexity(NEW.password) THEN
        RAISE EXCEPTION 'Password must contain both letters and digits';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_weak_password_trigger
BEFORE INSERT ON sistel.user
FOR EACH ROW
EXECUTE FUNCTION prevent_weak_password();

