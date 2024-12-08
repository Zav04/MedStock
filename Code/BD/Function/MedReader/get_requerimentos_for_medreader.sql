CREATE OR REPLACE FUNCTION get_requerimentos_for_medreader()
RETURNS TABLE(
    requerimento_id BIGINT,
    urgente BOOLEAN,
    itens_pedidos JSON
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        r.requerimento_id,
        r.urgente,
        (
            SELECT JSON_AGG(
                JSON_BUILD_OBJECT(
                    'nome_consumivel', c.nome_consumivel,
                    'codigo', c.codigo,
                    'quantidade', cr.quantidade
                )
            )
            FROM Consumivel_Requerimento cr
            INNER JOIN Consumivel c ON cr.consumivel_id = c.consumivel_id
            WHERE cr.requerimento_id = r.requerimento_id
        ) AS itens_pedidos
    FROM 
        Requerimento r
    WHERE 
        (
            SELECT h.status
            FROM HistoricoRequerimento h
            WHERE h.requerimento_id = r.requerimento_id
            ORDER BY h.data_modificacao DESC
            LIMIT 1
        ) = 2;
END;
$$ LANGUAGE plpgsql;