CREATE OR REPLACE FUNCTION get_consumiveis_details()
RETURNS TABLE (
    consumivel_id BIGINT,
    nome_consumivel VARCHAR,
    nome_tipo VARCHAR,
    codigo VARCHAR,
    quantidade_total BIGINT,
    quantidade_alocada BIGINT,
    quantidade_minima BIGINT,
    quantidade_pedido BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        i.consumivel_id,
        i.nome_consumivel,
        t.nome_tipo,
        i.codigo,
        i.quantidade_total,
        COALESCE(
            (SELECT SUM(cr.quantidade_alocada)::BIGINT
             FROM Consumivel_Requerimento cr
             WHERE cr.consumivel_id = i.consumivel_id),
            0
        ) AS quantidade_alocada,
        i.quantidade_minima,
        i.quantidade_pedido
    FROM 
        Consumivel i
    INNER JOIN 
        Tipo_Consumivel t ON i.tipo_id = t.tipo_id;
END;
$$ LANGUAGE plpgsql;