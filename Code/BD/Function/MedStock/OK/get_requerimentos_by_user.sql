CREATE OR REPLACE FUNCTION get_requerimentos_by_user(user_id BIGINT)
RETURNS TABLE(
    requerimento_id BIGINT,
    setor_nome_localizacao VARCHAR,
    nome_utilizador_pedido VARCHAR,
    status INT,
    urgente BOOLEAN,
    itens_pedidos JSON,
    data_pedido TIMESTAMP,
    historico JSON
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        r.requerimento_id,
        CONCAT(s.nome_setor, ' - ', s.localizacao)::VARCHAR AS setor_nome_localizacao,
        u_pedido.nome AS nome_utilizador_pedido,
        (
            SELECT h.status
            FROM HistoricoRequerimento h
            WHERE h.requerimento_id = r.requerimento_id
            ORDER BY h.data_modificacao DESC
            LIMIT 1
        )::INT AS status,
        r.urgente,
        (
            SELECT JSON_AGG(
                JSON_BUILD_OBJECT(
                    'nome_consumivel', c.nome_consumivel,
                    'quantidade', cr.quantidade,
                    'tipo_consumivel', tc.nome_tipo
                )
            )
            FROM Consumivel_Requerimento cr
            INNER JOIN Consumivel c ON cr.consumivel_id = c.consumivel_id
            INNER JOIN Tipo_Consumivel tc ON c.tipo_id = tc.tipo_id
            WHERE cr.requerimento_id = r.requerimento_id
        ) AS itens_pedidos,
        (
            SELECT h.data_modificacao
            FROM HistoricoRequerimento h
            WHERE h.requerimento_id = r.requerimento_id AND h.status = 0
            ORDER BY h.data_modificacao ASC
            LIMIT 1
        ) AS data_pedido,
        (
            SELECT JSON_AGG(sub_historico)
            FROM (
                SELECT 
                    h.status,
                    h.descricao,
                    h.data_modificacao,
                    u_historico.nome AS user_responsavel
                FROM HistoricoRequerimento h
                LEFT JOIN Utilizador u_historico ON h.user_id_responsavel = u_historico.utilizador_id
                WHERE h.requerimento_id = r.requerimento_id
                ORDER BY h.data_modificacao ASC
            ) sub_historico
        ) AS historico
    FROM 
        Requerimento r
    INNER JOIN 
        Setor_Hospital s ON r.setor_id = s.setor_id
    INNER JOIN 
        Utilizador u_pedido ON r.user_id_pedido = u_pedido.utilizador_id
    WHERE 
        r.user_id_pedido = user_id;
END;
$$ LANGUAGE plpgsql;
