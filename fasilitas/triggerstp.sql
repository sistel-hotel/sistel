CREATE OR REPLACE FUNCTION check_name_input()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.facility_name ~* '^[a-zA-Z]+$' THEN
        RETURN NEW;
    ELSE
        RAISE EXCEPTION 'Pendaftaran fasilitas hotel gagal, nama hanya boleh terdiri dari huruf';
    END IF;
END;
$$ LANGUAGE plpgsql;
=================================================

CREATE TRIGGER check_name_trigger
BEFORE INSERT ON hotel_facilities
FOR EACH ROW
EXECUTE FUNCTION check_name_input();

=================================================

CREATE OR REPLACE FUNCTION update_facility(facility_name_input VARCHAR, hotel_name_input VARCHAR, hotel_branch_input VARCHAR)
RETURNS VOID AS $$
DECLARE
    existing_facility_name VARCHAR;
BEGIN
    SELECT facility_name INTO existing_facility_name
    FROM hotel_facilities
    WHERE hotel_name = hotel_name_input AND hotel_branch = hotel_branch_input;

    IF existing_facility_name = facility_name_input THEN
        RAISE EXCEPTION 'Update fasilitas hotel gagal, nama fasilitas sama dengan sebelumnya';
    ELSE
        UPDATE hotel_facilities
        SET facility_name = facility_name_input
        WHERE hotel_name = hotel_name_input AND hotel_branch = hotel_branch_input;
    END IF;
END;
$$ LANGUAGE plpgsql;