CREATE OR REPLACE FUNCTION update_requerimento_reavaliation(
    p_user_id BIGINT,
    p_requerimento_id BIGINT,
    p_comentario TEXT,
    consumiveis_rejeitados TEXT
) 
RETURNS BOOLEAN AS $$
DECLARE
    updated_rows INT;
    comentario_final TEXT;
BEGIN
    SELECT COUNT(*) INTO updated_rows
    FROM Requerimento
    WHERE requerimento_id = p_requerimento_id;

    IF updated_rows = 0 THEN
        RAISE EXCEPTION 'Requerimento com ID % não encontrado.', p_requerimento_id;
    END IF;

    IF p_comentario IS NULL OR TRIM(p_comentario) = '' THEN
        IF consumiveis_rejeitados IS NOT NULL AND TRIM(consumiveis_rejeitados) <> '' THEN
            comentario_final := 'Requerimento enviado para reavaliação. Consumíveis rejeitados: ' || consumiveis_rejeitados;
        ELSE
            comentario_final := 'Requerimento enviado para reavaliação.';
        END IF;
    ELSE
        IF consumiveis_rejeitados IS NOT NULL AND TRIM(consumiveis_rejeitados) <> '' THEN
            comentario_final := p_comentario || ' Consumíveis rejeitados: ' || consumiveis_rejeitados;
        ELSE
            comentario_final := p_comentario;
        END IF;
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
        9,
        comentario_final, 
        p_user_id
    );

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao enviar requerimento para reavaliação: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
