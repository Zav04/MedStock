CREATE OR REPLACE FUNCTION get_requerimento_details(p_requerimento_id BIGINT)
RETURNS TABLE(
    requerimento_id BIGINT,
    setor_nome_localizacao VARCHAR,
    nome_utilizador_pedido VARCHAR,
    email_utilizador_pedido VARCHAR,
    nome_gestor_responsavel VARCHAR,
    email_gestor_responsavel VARCHAR,
    status INT,
    urgente BOOLEAN,
    itens_pedidos JSON,
    data_pedido TIMESTAMP,
    nome_utilizador_confirmacao VARCHAR,
    data_confirmacao TIMESTAMP,
    nome_utilizador_envio VARCHAR,
    data_envio TIMESTAMP,
    nome_utilizador_preparacao VARCHAR,
    data_preparacao TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        r.requerimento_id,
        CONCAT(s.nome_setor, ' - ', s.localizacao)::VARCHAR AS setor_nome_localizacao,
        u_pedido.nome AS nome_utilizador_pedido,
        u_pedido.email AS email_utilizador_pedido,
        u_responsavel.nome AS nome_gestor_responsavel,
        u_responsavel.email AS email_gestor_responsavel,
        r.status::INT,
        r.urgente,
        (
            SELECT JSON_AGG(
                JSON_BUILD_OBJECT(
                    'nome_item', i.nome_item,
                    'quantidade', ir.quantidade,
                    'tipo_item', t.nome_tipo
                )
            )
            FROM Item_Requerimento ir
            INNER JOIN Item i ON ir.ItemItem_id = i.item_id
            INNER JOIN Tipo_Item t ON i.tipo_id = t.tipo_id
            WHERE ir.Requerimentorequerimento_id = r.requerimento_id
        ) AS itens_pedidos,
        r.data_pedido,
        u_confirmacao.nome AS nome_utilizador_confirmacao,
        r.data_confirmacao,
        u_envio.nome AS nome_utilizador_envio,
        r.data_envio,
        u_preparacao.nome AS nome_utilizador_preparacao,
        r.data_preparacao
    FROM 
        Requerimento r
    INNER JOIN 
        Setor_Hospital s ON r.setor_id = s.setor_id
    INNER JOIN 
        Utilizador u_pedido ON r.user_id_pedido = u_pedido.utilizador_id
    LEFT JOIN 
        Utilizador u_responsavel ON s.responsavel_id = u_responsavel.utilizador_id
    LEFT JOIN 
        Utilizador u_confirmacao ON r.user_id_confirmacao = u_confirmacao.utilizador_id
    LEFT JOIN 
        Utilizador u_envio ON r.user_id_envio = u_envio.utilizador_id
    LEFT JOIN 
        Utilizador u_preparacao ON r.user_id_preparacao = u_preparacao.utilizador_id
    WHERE 
        r.requerimento_id = p_requerimento_id;
END;
$$ LANGUAGE plpgsql;
