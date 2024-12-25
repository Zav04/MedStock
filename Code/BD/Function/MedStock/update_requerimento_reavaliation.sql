CREATE OR REPLACE FUNCTION update_requerimento_reavaliation(
    p_user_id BIGINT,
    p_requerimento_id BIGINT,
    p_comentario TEXT,
    consumiveis_rejeitados TEXT
) 
RETURNS BOOLEAN AS $$
DECLARE
    comentario_final TEXT;
    item JSON;
    consumiveis_formatados TEXT DEFAULT '';
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM public.Requerimento WHERE requerimento_id = p_requerimento_id
    ) THEN
        RAISE EXCEPTION 'Requerimento com ID % não encontrado.', p_requerimento_id;
    END IF;

    IF consumiveis_rejeitados IS NOT NULL AND TRIM(consumiveis_rejeitados) <> '' THEN
        FOR item IN SELECT * FROM json_array_elements(consumiveis_rejeitados::JSON) LOOP
            consumiveis_formatados := consumiveis_formatados || 
                'Consumível Nome: ' || COALESCE(item->>'consumivel_nome', 'N/A') || ',' ||
                'Quantidade Pedida: ' || COALESCE(item->>'quantidade_pedida', 'N/A') || ',' ||
                'Quantidade Recebida: ' || COALESCE(item->>'quantidade_recebida', 'N/A');
        END LOOP;
    END IF;

    IF p_comentario IS NULL OR TRIM(p_comentario) = '' THEN
        IF consumiveis_formatados <> '' THEN
            comentario_final := 'Requerimento enviado para reavaliação.' || consumiveis_formatados;
        ELSE
            comentario_final := 'Requerimento enviado para reavaliação.';
        END IF;
    ELSE
        IF consumiveis_formatados <> '' THEN
            comentario_final := p_comentario || '\n\n' || consumiveis_formatados;
        ELSE
            comentario_final := p_comentario;
        END IF;
    END IF;

    INSERT INTO public.HistoricoRequerimento (
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
