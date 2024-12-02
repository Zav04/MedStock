CREATE OR REPLACE FUNCTION update_requerimento_send(
    p_requerimento_id INT,
    p_user_id INT
) RETURNS BOOL AS $$
BEGIN
    UPDATE Requerimento
    SET status = 8,
        user_id_envio = p_user_id,
        data_envio = CURRENT_TIMESTAMP(0)
    WHERE requerimento_id = p_requerimento_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
