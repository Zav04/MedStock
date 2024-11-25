CREATE OR REPLACE FUNCTION get_all_sectors()
RETURNS TABLE(
    setor_id BIGINT,
    nome_setor VARCHAR,
    localizacao VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.setor_id,
        s.nome_setor,
        s.localizacao
    FROM
        Setor_Hospital s
    ORDER BY
        s.nome_setor;
END;
$$ LANGUAGE plpgsql;
