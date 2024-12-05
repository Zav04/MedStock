CREATE OR REPLACE FUNCTION update_requerimento_cancel(
    p_requerimento_id INT
) RETURNS BOOL AS $$
BEGIN

    UPDATE Requerimento
    SET status = 7
    WHERE requerimento_id = p_requerimento_id;
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
