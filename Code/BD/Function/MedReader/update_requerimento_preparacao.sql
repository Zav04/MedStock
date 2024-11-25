CREATE OR REPLACE FUNCTION update_requerimento_preparacao(
    p_user_id BIGINT,
    p_requerimento_id BIGINT
) 
RETURNS BOOLEAN AS $$
DECLARE
    updated_rows INT;
BEGIN
    UPDATE Requerimento
    SET 
        status = 3,
        user_id_preparacao = p_user_id,
        data_preparacao = CURRENT_TIMESTAMP
    WHERE 
        requerimento_id = p_requerimento_id;
    
    GET DIAGNOSTICS updated_rows = ROW_COUNT;

    IF updated_rows = 0 THEN
        RAISE EXCEPTION 'Requerimento com ID % não encontrado.', p_requerimento_id;
    END IF;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
