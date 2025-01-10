CREATE OR REPLACE FUNCTION create_redistribuicao(
    p_consumivel_id BIGINT,
    p_requerimento_origem BIGINT,
    p_requerimento_destino BIGINT,
    p_quantidade BIGINT
)
RETURNS BOOLEAN AS $$
BEGIN

    IF NOT EXISTS (
        SELECT 1 
        FROM Requerimento 
        WHERE requerimento_id = p_requerimento_origem
    ) THEN
        RAISE EXCEPTION 'Requerimento_origem com ID % não existe.', p_requerimento_origem;
    END IF;

    IF NOT EXISTS (
        SELECT 1 
        FROM Requerimento 
        WHERE requerimento_id = p_requerimento_destino
    ) THEN
        RAISE EXCEPTION 'Requerimento_destino com ID % não existe.', p_requerimento_destino;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM Consumivel_Requerimento
        WHERE consumivel_id = p_consumivel_id
          AND requerimento_id = p_requerimento_origem
          AND quantidade_alocada < p_quantidade
    ) THEN
        RAISE EXCEPTION 'Quantidade alocada insuficiente para redistribuição. 
        Consumível: %, Requerimento_origem: %, Quantidade disponível: %, Quantidade necessária: %.',
        p_consumivel_id, p_requerimento_origem,
        (SELECT quantidade_alocada 
         FROM Consumivel_Requerimento 
         WHERE consumivel_id = p_consumivel_id 
           AND requerimento_id = p_requerimento_origem),
        p_quantidade;
    END IF;

    INSERT INTO Redistribuicao (
        consumivel_id,
        requerimento_origem,
        requerimento_destino,
        quantidade,
        data_redistribuicao
    )
    VALUES (
        p_consumivel_id,
        p_requerimento_origem,
        p_requerimento_destino,
        p_quantidade,
        CURRENT_TIMESTAMP(0)
    );

    UPDATE Consumivel_Requerimento
    SET quantidade_alocada = quantidade_alocada - p_quantidade
    WHERE consumivel_id = p_consumivel_id
      AND requerimento_id = p_requerimento_origem;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Falha ao atualizar quantidade_alocada. Registro não encontrado para Consumível: % e Requerimento: %.',
        p_consumivel_id, p_requerimento_origem;
    END IF;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
