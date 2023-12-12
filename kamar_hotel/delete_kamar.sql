CREATE OR REPLACE FUNCTION delete_kamar()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.checkout >= now() THEN
        RAISE EXCEPTION 'Kamar tidak dapat dihapus karena masih digunakan!';
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_kamar_trigger
BEFORE DELETE ON sistel.room
FOR EACH ROW
EXECUTE FUNCTION delete_kamar();