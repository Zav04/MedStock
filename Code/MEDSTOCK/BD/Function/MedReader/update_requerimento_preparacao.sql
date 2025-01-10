CREATE OR REPLACE FUNCTION update_requerimento_preparacao(
    p_user_id BIGINT,
    p_requerimento_id BIGINT
) 
RETURNS BOOLEAN AS $$
DECLARE
    updated_rows INT;
BEGIN
    SELECT COUNT(*) INTO updated_rows
    FROM Requerimento
    WHERE requerimento_id = p_requerimento_id;

    IF updated_rows = 0 THEN
        RAISE EXCEPTION 'Requerimento com ID % não encontrado.', p_requerimento_id;
    END IF;

    INSERT INTO HistoricoRequerimento (
        requerimento_id,
        status,
        descricao,
        data_modificacao,
        user_id_responsavel
    )
    VALUES (
        p_requerimento_id,
        3,
        'Requerimento em preparação',
        CURRENT_TIMESTAMP(0),
        p_user_id
    );

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
