CREATE OR REPLACE FUNCTION insert_kamar()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price < 0 OR NEW.floor < 0 THEN
        RAISE EXCEPTION 'Harga dan Lantai harus diatas 0';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_kamar_trigger
BEFORE INSERT ON sistel.room
FOR EACH ROW
EXECUTE FUNCTION insert_kamar();