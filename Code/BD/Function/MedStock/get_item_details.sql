CREATE OR REPLACE FUNCTION get_item_details()
RETURNS TABLE (
    item_id BIGINT,
    nome_item VARCHAR,
    nome_tipo VARCHAR,
    codigo VARCHAR,
    quantidade_disponivel BIGINT,
    quantidade_total BIGINT,
    quantidade_alocada BIGINT,
    quantidade_minima BIGINT,
    quantidade_pedido BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        i.item_id, 
        i.nome_item,
        t.nome_tipo,
        i.codigo,
        i.quantidade_disponivel,
        i.quantidade_total,
        i.quantidade_alocada,
        i.quantidade_minima,
        i.quantidade_pedido
    FROM 
        Consumivel i
    INNER JOIN 
        Tipo_Consumivel t ON i.tipo_id = t.tipo_id;
END;
$$ LANGUAGE plpgsql;
