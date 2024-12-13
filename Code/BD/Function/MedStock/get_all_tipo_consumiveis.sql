CREATE OR REPLACE FUNCTION get_all_tipo_consumiveis()
RETURNS TABLE(
    tipo_id BIGINT,
    nome_tipo VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        tc.tipo_id,
        tc.nome_tipo
    FROM 
        Tipo_Consumivel AS tc
    ORDER BY 
        tc.tipo_id ASC;
END;
$$ LANGUAGE plpgsql;