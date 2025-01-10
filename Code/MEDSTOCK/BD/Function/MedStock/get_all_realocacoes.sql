
CREATE OR REPLACE FUNCTION get_all_realocacoes()
RETURNS TABLE (
    requerimento_origem INT,
    requerimento_destino INT,
    nome_consumivel TEXT,
    quantidade INT,
    data_redistribuicao TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.requerimento_origem,
        r.requerimento_destino,
        c.nome_consumivel,
        r.quantidade,
        r.data_redistribuicao
    FROM redistribuicao r
    JOIN Consumivel c ON r.consumivel_id = c.consumivel_id
    ORDER BY r.data_redistribuicao DESC;
END;
$$ LANGUAGE plpgsql;
