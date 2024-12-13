CREATE OR REPLACE FUNCTION update_requerimento_finish(
    p_user_id BIGINT,
    p_requerimento_id BIGINT,
    p_comentario TEXT
) 
RETURNS BOOLEAN AS $$
DECLARE
    updated_rows INT;
    descricao_final TEXT;
BEGIN
    SELECT COUNT(*) INTO updated_rows
    FROM Requerimento
    WHERE requerimento_id = p_requerimento_id;

    IF updated_rows = 0 THEN
        RAISE EXCEPTION 'Requerimento com ID % não encontrado.', p_requerimento_id;
    END IF;

    IF p_comentario IS NULL OR TRIM(p_comentario) = '' THEN
        descricao_final := 'Requerimento finalizado.';
    ELSE
        descricao_final := p_comentario || ' Requerimento finalizado.';
    END IF;

    INSERT INTO HistoricoRequerimento (
        requerimento_id, 
        data_modificacao, 
        status, 
        descricao, 
        user_id_responsavel
    )
    VALUES (
        p_requerimento_id, 
        CURRENT_TIMESTAMP(0), 
        4,
        descricao_final, 
        p_user_id
    );

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao finalizar requerimento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
