CREATE OR REPLACE FUNCTION update_requerimento_reject(
    p_requerimento_id INT,
    p_user_id INT,
    p_motivo VARCHAR
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
        CURRENT_TIMESTAMP,
        5,
        COALESCE(p_motivo, 'Requerimento rejeitado sem motivo especificado.'),
        p_user_id
    );

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao rejeitar requerimento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
