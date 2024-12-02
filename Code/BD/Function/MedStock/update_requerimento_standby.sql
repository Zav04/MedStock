CREATE OR REPLACE FUNCTION update_requerimento_standby(
    p_requerimento_id INT
) RETURNS BOOL AS $$
BEGIN
    UPDATE Requerimento
    SET status = 6
    WHERE requerimento_id = p_requerimento_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
