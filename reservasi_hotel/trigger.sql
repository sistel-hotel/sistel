CREATE OR REPLACE FUNCTION validate_hotel_reservation_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rsid NOT IN ('P1Q0R2S3T4U5V6', 'X9Y8Z7W6V5U4T3') THEN
        RAISE EXCEPTION 'Pihak Hotel hanya dapat melakukan perubahan status ke ''Ditolak oleh Hotel'' atau ''Terkonfirmasi oleh Hotel''';
    END IF;

    IF OLD.rsid <> 'A7B1D9E4F2C5G3H0' THEN
        RAISE EXCEPTION 'Hotel hanya dapat mengubah reservasi dengan status ''Menunggu Konfirmasi Pihak Hotel''';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER hotel_reservation_status_change_trigger
BEFORE UPDATE ON RESERVATION_STATUS_HISTORY
FOR EACH ROW
EXECUTE FUNCTION validate_hotel_reservation_status_change();


CREATE OR REPLACE FUNCTION validasi_shuttle() RETURNS TRIGGER AS $$
BEGIN
    -- Memeriksa apakah reservasi kamar masih aktif berdasarkan rsv_id yang akan dibuat untuk penjemputan
    IF EXISTS (
        SELECT 1 FROM RESERVATION_ROOM WHERE RESERVATION_ROOM.rsv_id = NEW.rsv_id
         AND RESERVATION_ROOM.isactive = FALSE
    ) THEN
        -- Jika reservasi sudah tidak aktif, maka penjemputan (shuttle) tidak dapat dibuat
        RAISE EXCEPTION 'Reservasi tidak aktif. Shuttle hanya dapat dibuat untuk reservasi yang masih aktif.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Membuat trigger yang memanggil fungsi validasi_shuttle sebelum melakukan INSERT pada RESERVATION_SHUTTLESERVICE
CREATE TRIGGER validasi_shuttle_trigger
BEFORE INSERT ON RESERVATION_SHUTTLESERVICE
FOR EACH ROW
EXECUTE FUNCTION validasi_shuttle();