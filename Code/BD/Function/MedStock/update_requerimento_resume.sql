CREATE OR REPLACE FUNCTION update_requerimento_resume(
    p_requerimento_id INT,
    p_user_id INT
) RETURNS BOOL AS $$
BEGIN
    INSERT INTO HistoricoRequerimento (
        requerimento_id,
        data_modificacao,
        status,
        descricao,
        user_id_responsavel
    ) VALUES (
        p_requerimento_id,
        CURRENT_TIMESTAMP(0),
        10,
        'Requerimento retornou a lista de espera.',
        CASE 
            WHEN p_user_id = -1 THEN NULL
            ELSE p_user_id
        END
    );

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao retomar requerimento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
