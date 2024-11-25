CREATE OR REPLACE FUNCTION get_requerimentos_for_medreader()
RETURNS TABLE(
    requerimento_id BIGINT,
    itens_pedidos JSON
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        r.requerimento_id,
        (
            SELECT JSON_AGG(
                JSON_BUILD_OBJECT(
                    'nome_item', i.nome_item,
                    'codigo', i.codigo,
                    'quantidade', ir.quantidade
                )
            )
            FROM Item_Requerimento ir
            INNER JOIN Item i ON ir.ItemItem_id = i.item_id
            WHERE ir.Requerimentorequerimento_id = r.requerimento_id
        ) AS itens_pedidos
    FROM 
        Requerimento r
    WHERE 
        r.status = 2;
END;
$$ LANGUAGE plpgsql;
