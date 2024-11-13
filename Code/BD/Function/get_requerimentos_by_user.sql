CREATE OR REPLACE FUNCTION get_requerimentos_by_user(user_id BIGINT)
RETURNS TABLE(
    requerimento_id BIGINT,
    setor_nome_localizacao VARCHAR,
    nome_utilizador_pedido VARCHAR,
    status INT,
    urgente BOOLEAN,
    itens_pedidos VARCHAR,
    data_pedido TIMESTAMP,
    nome_utilizador_confirmacao VARCHAR,
    data_confirmacao TIMESTAMP,
    nome_utilizador_envio VARCHAR,
    data_envio TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        r.requerimento_id,
        CONCAT(s.nome_setor, ' - ', s.localizacao)::VARCHAR AS setor_nome_localizacao,
        u_pedido.nome AS nome_utilizador_pedido,
        r.status::INT,
        r.urgente,
        (
            SELECT STRING_AGG(CONCAT(i.nome_item, ' (Quantidade: ', ir.quantidade, ')'), ', ')::VARCHAR
            FROM Item_Requerimento ir
            INNER JOIN Item i ON ir.ItemItem_id = i.item_id
            WHERE ir.Requerimentorequerimento_id = r.requerimento_id
        ) AS itens_pedidos,
        r.data_pedido,
        u_confirmacao.nome AS nome_utilizador_confirmacao,
        r.data_confirmacao,
        u_envio.nome AS nome_utilizador_envio,
        r.data_envio
    FROM 
        Requerimento r
    INNER JOIN 
        Setor_Hospital s ON r.setor_id = s.setor_id
    INNER JOIN 
        Utilizador u_pedido ON r.user_id_pedido = u_pedido.utilizador_id
    LEFT JOIN 
        Utilizador u_confirmacao ON r.user_id_confirmacao = u_confirmacao.utilizador_id
    LEFT JOIN 
        Utilizador u_envio ON r.user_id_envio = u_envio.utilizador_id
    WHERE 
        r.user_id_pedido = user_id;
END;
$$ LANGUAGE plpgsql;

