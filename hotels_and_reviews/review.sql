CREATE OR REPLACE FUNCTION insert_and_update_rating()
RETURNS TRIGGER AS $$
DECLARE
    total_rating FLOAT;
    count_ratings INTEGER;
BEGIN
    total_rating := 0;
    count_ratings := 0;
    IF NEW.rating < 0 OR NEW.rating > 5 THEN
        RAISE EXCEPTION 'Rating is not valid';
    END IF;
    -- Menghitung total rating yang ada untuk hotel tertentu
    SELECT COALESCE(SUM(rating), 0), COALESCE(COUNT(*), 0) INTO total_rating, count_ratings
    FROM sistel.reviews
    WHERE hotel_name = NEW.hotel_name
    AND hotel_branch = NEW.hotel_branch;

    -- Menambahkan nilai rating yang baru ke total rating
    total_rating := total_rating + NEW.rating;
    count_ratings := count_ratings + 1;

    -- Menghitung rata-rata rating
    UPDATE sistel.hotel
    SET rating = total_rating / count_ratings
    WHERE hotel_name = NEW.hotel_name
    AND hotel_branch = NEW.hotel_branch;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER rating_trigger
BEFORE INSERT ON sistel.reviews
FOR EACH ROW
EXECUTE FUNCTION insert_and_update_rating();
