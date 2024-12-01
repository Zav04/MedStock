CREATE OR REPLACE FUNCTION get_requerimento_avaliation_details(p_requerimento_id BIGINT)
RETURNS TABLE (
    requerimento_id BIGINT,
    email_utilizador_pedido VARCHAR,
    nome_utilizador_confirmacao VARCHAR,
    data_confirmacao TIMESTAMP,
    itens_pedidos JSON,
    status INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.requerimento_id,
        u.email AS email_utilizador_pedido,
        uc.nome AS nome_utilizador_confirmacao,
        r.data_confirmacao,
        (
            SELECT JSON_AGG(
                JSON_BUILD_OBJECT(
                    'nome_item', i.nome_item,
                    'quantidade', ir.quantidade
                )
            )
            FROM Item_Requerimento ir
            JOIN Item i ON ir.ItemItem_id = i.Item_id
            WHERE ir.Requerimentorequerimento_id = r.requerimento_id
        ) AS itens_pedidos,
        r.status
    FROM 
        Requerimento r
    LEFT JOIN 
        Utilizador u ON r.user_id_pedido = u.utilizador_id
    LEFT JOIN 
        Utilizador uc ON r.user_id_confirmacao = uc.utilizador_id
    WHERE 
        r.requerimento_id = p_requerimento_id;
END;
$$ LANGUAGE plpgsql;
