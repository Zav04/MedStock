CREATE OR REPLACE FUNCTION get_item_details()
RETURNS TABLE (
    nome_item VARCHAR,
    nome_tipo VARCHAR,
    codigo VARCHAR,
    quantidade_disponivel BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome_item,
        t.nome_tipo,
        i.codigo,
        i.quantidade_disponivel
    FROM 
        Item i
    INNER JOIN 
        Tipo_Item t ON i.tipo_id = t.tipo_id;
END;
$$ LANGUAGE plpgsql;