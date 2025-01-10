CREATE OR REPLACE FUNCTION update_requerimento_cancel(
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
        7,
        'Requerimento cancelado.',
        p_user_id
    );

    UPDATE Consumivel c
    SET quantidade_alocada = 0
    FROM Consumivel_Requerimento cr
    WHERE cr.requerimento_id = p_requerimento_id AND cr.consumivel_id = c.consumivel_id;

    UPDATE Consumivel_Requerimento
    SET quantidade_alocada = 0
    WHERE requerimento_id = p_requerimento_id;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao cancelar requerimento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
