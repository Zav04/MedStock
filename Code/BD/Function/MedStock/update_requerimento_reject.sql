CREATE OR REPLACE FUNCTION update_requerimento_reject(
    p_requerimento_id INT,
    p_user_id INT
) RETURNS BOOL AS $$
BEGIN
    UPDATE Requerimento
    SET status = 5,
        user_id_confirmacao = p_user_id,
        data_confirmacao = CURRENT_TIMESTAMP(0)
    WHERE requerimento_id = p_requerimento_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
