CREATE OR REPLACE FUNCTION update_requerimento_resume(
    p_requerimento_id INT
) RETURNS BOOL AS $$
BEGIN
    UPDATE Requerimento
    SET status = 1
    WHERE requerimento_id = p_requerimento_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
